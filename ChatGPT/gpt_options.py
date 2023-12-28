from dataclasses import dataclass, field


@dataclass
class GPTOptions:
    api_key: str = field(repr=False)
    model_name: str = "gpt-3.5-turbo"
    model_3_16: str = "gpt-3.5-turbo-16k-0613"
    model_4: str = "gpt-4"
    max_message_count: int | None = None
    max_token_count: int = 4096
