from pydantic_ai import Agent, RunContext
import openai
from pydantic_ai.models.openai import OpenAIModelSettings, OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic import BaseModel, Field
from settings import Settings
import asyncio
from dataclasses import dataclass

settings = Settings()

groq_settings = OpenAIModelSettings(
    temperature=0.7,
    top_p=0.95,
    frequency_penalty=0,
)

model_name = "llama-3.3-70b"

client = openai.AsyncOpenAI(api_key=settings.cerebras_api_key, base_url=settings.cerebras_base_url)

model = OpenAIModel(
    model_name=model_name,
    provider=OpenAIProvider(openai_client=client),
)

@dataclass
class Deps:
    pass

class Form(BaseModel):
    customername: str = Field(description="The name of the customer making the request if given, else 'unknown'")
    requesttype: str = Field(description="The type of request being made. example: 'technical support', 'billing', etc.")
    issue: str = Field(description="Detailed description of 50 lines of the issue being reported by the customer")
    emotion: str = Field(description="The emotion of the customer to be given in one word. example: 'angry', 'happy', 'sad', etc.")

with open("form_prompt.txt", "r") as file:
    form_prompt = file.read()

with open("response_prompt.txt", "r") as file:
    response_prompt = file.read()

form_agent = Agent(
    model=model,
    model_settings=groq_settings,
    system_prompt=form_prompt,
    retries=3,
    result_type=Form,
)

response_agent = Agent(
    model=model,
    model_settings=groq_settings,
    system_prompt=response_prompt,
    retries=3,
)

# Code below is only for debugging please ignore

async def chat():
    while True:
        user_message = input("You: ")

        if user_message == "exit":
            break

        result = await form_agent.run(user_prompt=user_message)
        response = result.data if result else "Sorry, I failed to process that."

        print("Bot:", response)

# asyncio.run(chat())