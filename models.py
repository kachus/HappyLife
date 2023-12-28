from datetime import datetime
from ChatGPT.gpt_message import GPTMessage, GPTRole
from dataclasses import dataclass, field
from uuid import uuid4

Role = GPTRole

class Message(GPTMessage):
    id: int
    role: Role
    content: str
    timestamp: datetime
    is_final: False

    def __init__(self, id: int, role: Role, content: str, timestamp: datetime | None = None):
        super().__init__(role, content)
        self.id = id
        self.role = role
        self.content = content
        self.timestamp = timestamp or datetime.now()


class SystemMessage(Message):
    def __init__(self, content: str, timestamp: datetime | None = None):
        super().__init__(-1, Role.SYSTEM, content, timestamp or datetime.now())


class AssistantMessage(Message):
    replied_to_id: int

    def __init__(self,
                 id: int,
                 content: str,
                 replied_to_id: int,
                 timestamp: datetime | None = None):
        super().__init__(id, Role.ASSISTANT, content, timestamp)
        self.id = id
        self.replied_to_id = replied_to_id


class UserMessage(Message):
    answer_id: int | None

    def __init__(self, id: int, content: str, timestamp: datetime | None = None):
        super().__init__(id, Role.USER, content, timestamp)
        self.id = id
        self.answer_id = None


@dataclass
class Conversation:
    started_at: datetime
    messages: list[Message]
    chat_system_message: SystemMessage | None = None
    id: str = field(default_factory=lambda: str(uuid4()))

    @property
    def last_message(self):
        if len(self.messages) == 0:
            return None
        return self.messages[-1]
