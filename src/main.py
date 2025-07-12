from workflow import EmployeeRecruitmentWorkflow

from textwrap import dedent

import os
from dotenv import load_dotenv

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


def main():
    workflow = EmployeeRecruitmentWorkflow()
    result = workflow.run(
        candidate_resume_urls=[
            # Add resume URLs here
            "https://yunlongjiao.github.io/resume/resume.pdf"
        ],
        job_description=dedent(
            """
            We are hiring for backend and systems engineers!
            Join our team building the future of agentic software

            Apply if:
            🧠 You know your way around Python, typescript, docker, and AWS.
            ⚙️ Love to build in public and contribute to open source.
            🚀 Are ok dealing with the pressure of an early-stage startup.
            🏆 Want to be a part of the biggest technological shift since the
            internet.
            🌟 Bonus: experience with infrastructure as code.
            """
        ),
    )
    print(result.content)


if __name__ == "__main__":
    main()
