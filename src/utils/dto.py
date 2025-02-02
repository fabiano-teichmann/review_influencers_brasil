from typing import Literal, List

from pydantic import BaseModel, Field


class Message(BaseModel):
    role: Literal["system", "user", "assistant"] = Field(..., description="O papel do participante na conversa")
    content: str = Field(..., description="Texto da mensagem para ser analisada pelo GPT")


class GPTPrompt(BaseModel):
    messages: List[Message] = Field(..., description="Lista de mensagens para a API do GPT")

    class Config:
        json_schema_extra = {
            "example": {
                "messages": [
                    {"role": "system", "content": "You are an AI assistant specialized..."},
                    {"role": "user", "content": "Analyze the table below and classify each entry as instructed..."}
                ]
            }
        }


class ConfigModel(BaseModel):
    model: Literal["gpt-4o-mini", "gpt-3.5-turbo"] = Field("gpt-4o-mini",  description="LLM model")
    temperature: int = 0
