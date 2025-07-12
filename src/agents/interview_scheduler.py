from agno.agent.agent import Agent
from agno.models.openai.chat import OpenAIChat
from agno.tools.zoom import ZoomTools

from textwrap import dedent
import os

from models import CandidateScheduledCall

interview_scheduler_agent: Agent = Agent(
    description=(
        "You are an interview scheduler agent that schedules "
        "interviews for candidates."
    ),  # no-qa
    model=OpenAIChat(id="gpt-4o"),
    instructions=[
        dedent(
            """\
            You are an interview scheduler agent that schedules interviews
            for candidates.
            You need to schedule interviews for the candidates using the
            Zoom tool.
            You need to schedule the interview for the candidate at the
            earliest possible time between 10am and 6pm.
            Check if the candidate and interviewer are available at the
            time and if the time is free in the calendar.
            You are in GMT+1 timezone and the current time is {current_time}.
            So schedule the call in future time with reference to current time.
            """
        )
    ],
    tools=[
        ZoomTools(
            account_id=os.getenv("ZOOM_ACCOUNT_ID"),
            client_id=os.getenv("ZOOM_CLIENT_ID"),
            client_secret=os.getenv("ZOOM_CLIENT_SECRET"),
        )
    ],
    response_model=CandidateScheduledCall,
)
