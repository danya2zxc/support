from dataclasses import dataclass


@dataclass
class EmailMessage:
    body: str
    subject: str
    recepient: str
    sender: str
