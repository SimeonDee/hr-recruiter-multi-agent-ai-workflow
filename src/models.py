from pydantic import BaseModel, Field


class ScreeningResult(BaseModel):
    name: str = Field(description="The name of the candidate")
    email: str = Field(description="The email of the candidate")
    score: float = Field(description="The score of the candidate from 0 to 10")
    feedback: str = Field(description="The feedback for the candidate")


class CandidateScheduledCall(BaseModel):
    name: str = Field(description="The name of the candidate")
    email: str = Field(description="The email of the candidate")
    call_time: str = Field(description="The time of the call")
    url: str = Field(description="The url of the call")


class Email(BaseModel):
    subject: str = Field(description="The subject of the email")
    body: str = Field(description="The body of the email")
