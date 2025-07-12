import io
from datetime import datetime
from typing import List

import requests
from agno.run.response import RunResponse

try:
    from pypdf import PdfReader
except ImportError:
    raise ImportError(
        "pypdf is not installed. Please install it using `pip install pypdf`"
    )
from agno.utils.log import logger
from agno.workflow.workflow import Workflow

from agents.screener import screening_agent
from agents.interview_scheduler import interview_scheduler_agent
from agents.email_sender import email_sender_agent
from agents.email_writer import email_writer_agent

current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class EmployeeRecruitmentWorkflow(Workflow):
    screening_agent = screening_agent
    interview_scheduler_agent = interview_scheduler_agent
    email_sender_agent = email_sender_agent
    email_writer_agent = email_writer_agent

    def extract_text_from_pdf(self, pdf_url: str) -> str:
        """Download PDF from URL and extract text content"""
        try:
            # Download PDF content
            response = requests.get(pdf_url)
            response.raise_for_status()

            # Create PDF reader object
            pdf_file = io.BytesIO(response.content)
            pdf_reader = PdfReader(pdf_file)

            # Extract text from all pages
            text_content = ""
            for page in pdf_reader.pages:
                text_content += page.extract_text()

            return text_content

        except Exception as e:
            print(f"Error processing PDF: {str(e)}")
            return ""

    def run(
        self, candidate_resume_urls: List[str], job_description: str
    ) -> RunResponse:
        selected_candidates = []

        if not candidate_resume_urls:
            raise Exception("candidate_resume_urls cannot be empty")

        for resume_url in candidate_resume_urls:
            # Extract text from PDF resume
            if resume_url in self.session_state:
                resume_content = self.session_state[resume_url]
            else:
                resume_content = self.extract_text_from_pdf(resume_url)
                self.session_state[resume_url] = resume_content
            screening_result = None

            if resume_content:
                # Screen the candidate
                input = (
                    f"Candidate resume: {resume_content}, "
                    f"Job description: {job_description}"
                )  # no-qa
                screening_result = self.screening_agent.run(input)
                logger.info(screening_result)
            else:
                logger.error(
                    f"Could not process resume from URL: {resume_url}"
                )  # no-qa

            if (
                screening_result
                and screening_result.content
                and screening_result.content.score > 7.0
            ):
                selected_candidates.append(screening_result.content)

        for selected_candidate in selected_candidates:
            input = (
                f"Schedule a 1hr call with Candidate name: "
                "{selected_candidate.name}, Candidate email: "
                f"{selected_candidate.email} and the interviewer "
                "would be Manthan Gupts with email manthan@agno.com"
            )  # no-qa
            scheduled_call = self.interview_scheduler_agent.run(input)
            logger.info(scheduled_call.content)

            if (
                scheduled_call.content
                and scheduled_call.content.url
                and scheduled_call.content.call_time
            ):
                input = (
                    "Write an email to Candidate name: "
                    f"{selected_candidate.name}, Candidate email: "
                    f"{selected_candidate.email} for the call scheduled at "
                    f"{scheduled_call.content.call_time} with the url "
                    f"{scheduled_call.content.url} and congratulate them for "
                    "the interview from John Doe designation Senior Software "
                    "Engineer and email john@agno.com"
                )  # no-qa
                email = self.email_writer_agent.run(input)
                logger.info(email.content)

                if email.content:
                    input = (
                        f"Send email to {selected_candidate.email} "
                        f"with subject {email.content.subject} "
                        f"and body {email.content.body}"
                    )  # no-qa
                    self.email_sender_agent.run(input)

        return RunResponse(
            content=(
                f"Selected {len(selected_candidates)} "
                "candidates for the interview."  # no-qa
            ),  # no-qa
        )
