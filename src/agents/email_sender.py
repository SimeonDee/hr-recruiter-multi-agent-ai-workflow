from agno.agent.agent import Agent
from agno.models.openai.chat import OpenAIChat
from agno.tools.resend import ResendTools
from textwrap import dedent

email_sender_agent: Agent = Agent(
    description=(
        "You are an expert email sender agent that sends emails to "
        "selected candidates."
    ),
    model=OpenAIChat(id="gpt-4o"),
    instructions=[
        dedent(
            """\
            You are an expert email sender agent that sends emails to
            selected candidates.
            You need to send an email to the candidate using the Resend tool.
            You will be given the email subject and body and you need to send
            it to the candidate.
            """
        )
    ],
    tools=[ResendTools(from_email="email@agno.com")],
)
