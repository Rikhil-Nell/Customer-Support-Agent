from typing import List
from fastrtc import (ReplyOnPause, Stream, get_stt_model, get_tts_model)
from agent import agent
from pydantic_ai.messages import ModelMessage, ModelRequest, ModelResponse, UserPromptPart, TextPart
from settings import Settings

settings = Settings()
hf_token = settings.hf_token
stt_model = get_stt_model()
tts_model = get_tts_model()

messages: List[ModelMessage] = []

def echo(audio):
    prompt = stt_model.stt(audio)
    
    response = agent.run_sync(user_prompt=prompt, message_history=messages)

    messages.append(ModelRequest(parts=[UserPromptPart(content=prompt)]))
    messages.append(ModelResponse(parts=[TextPart(content=response.data)]))

    for audio_chunk in tts_model.stream_tts_sync(response.data):
        yield audio_chunk

stream = Stream(
    handler=ReplyOnPause(echo),
    modality="audio", 
    mode="send-receive")

stream.ui.launch()