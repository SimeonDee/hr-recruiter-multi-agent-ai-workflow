from agno.agent.agent import Agent
from agno.models.openai.chat import OpenAIChat
from textwrap import dedent

from models import ScreeningResult


screening_agent: Agent = Agent(
    description=(
        "You are an HR agent that screens candidates for a job interview."
    ),  # no-qa
    model=OpenAIChat(id="gpt-4o"),
    instructions=[
        dedent(
            """\
            You will receive a candidate's name, email, and a score
            from 0 to 10.
            You are an expert HR agent that screens candidates for a
            job interview.
            You are given a candidate's name and resume and job description.
            You need to screen the candidate and determine if they are a good
            fit for the job.
            You need to provide a score for the candidate from 0 to 10.
            You need to provide a feedback for the candidate on why they
            are a good fit or not.
            """
        )
    ],
    response_model=ScreeningResult,
)
