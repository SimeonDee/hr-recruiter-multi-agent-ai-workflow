from agno.agent.agent import Agent
from agno.models.openai.chat import OpenAIChat
from textwrap import dedent

from models import Email


email_writer_agent: Agent = Agent(
    description=(
        "You are an expert email writer agent that writes emails "
        "to selected candidates."
    ),  # no-qa
    model=OpenAIChat(id="gpt-4o"),
    instructions=[
        dedent(
            """\
            You are an expert email writer agent that writes emails to selected
            candidates.
            You need to write an email and send it to the candidates using the
            Resend tool.
            You represent the company and the job position.
            You need to write an email that is concise and to the point.
            You need to write an email that is friendly and professional.
            You need to write an email that is not too long and not too short.
            You need to write an email that is not too formal and not too
            informal.
            """
        )
    ],
    response_model=Email,
)
