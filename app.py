import gradio as gr
import pandas as pd
import os
import atexit
from fastrtc import WebRTC, ReplyOnPause, get_stt_model, get_tts_model
from settings import Settings
from pydantic_ai.messages import (
    ModelMessage,
    ModelRequest,
    ModelResponse,
    UserPromptPart,
    TextPart
)
from agents import form_agent, response_agent

# Config and Globals
settings = Settings()
stt_model = get_stt_model()
tts_model = get_tts_model()
messages: list[ModelMessage] = []

DATA_PATH = "data.csv"
df = pd.read_csv(DATA_PATH) if os.path.exists(DATA_PATH) else pd.DataFrame(columns=["customer_name", "request_type", "issue", "emotion"])

def save_data_on_exit():
    df.to_csv(DATA_PATH, index=False)

atexit.register(save_data_on_exit)

def df_update():
    global df
    try:
        form_response = form_agent.run_sync(user_prompt="Do your thing", message_history=messages)
        new_row = {
            "customer_name": form_response.data.customername,
            "request_type": form_response.data.requesttype,
            "issue": form_response.data.issue,
            "emotion": form_response.data.emotion
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(DATA_PATH, index=False)
        return "✅ DataFrame updated successfully!"
    except Exception as e:
        return f"❌ Update failed: {str(e)}"

def update_table():
    global df
    if os.path.exists(DATA_PATH):
        df = pd.read_csv(DATA_PATH)
    else:
        df = pd.DataFrame(columns=["customer_name", "request_type", "issue", "emotion"])
    return df

def reset_memory():
    global messages
    messages = []
    return "🧠 Memory reset successfully."

async def handle_audio(audio):
    prompt = stt_model.stt(audio)
    response_text = await response_agent.run(user_prompt=prompt, message_history=messages)
    messages.append(ModelRequest(parts=[UserPromptPart(content=prompt)]))
    messages.append(ModelResponse(parts=[TextPart(content=response_text.data)]))
    for chunk in tts_model.stream_tts(response_text.data):
        yield chunk

async def handle_text_chat(user_text, history):
    response = await response_agent.run(user_prompt=user_text, message_history=messages)
    messages.append(ModelRequest(parts=[UserPromptPart(content=user_text)]))
    messages.append(ModelResponse(parts=[TextPart(content=response.data)]))
    history = history + [[user_text, response.data]]
    return "", history

# Gradio UI
with gr.Blocks(css="""
.toolbox { display: flex; gap: 0.5rem; margin-top: 0.5rem; }
.footer-note { text-align: center; font-size: 0.85rem; color: #666; margin-top: 1rem; }
""") as demo:
    gr.Markdown("<h2 style='text-align: center;'>💬 Customer Support Assistant</h2>")

    debug_box = gr.Textbox(visible=False)

    with gr.Tabs():
        with gr.Tab("Chat"):
            with gr.Row():
                with gr.Column(scale=3):
                    chatbot = gr.Chatbot(label="Chat Interface")
                    user_input = gr.Textbox(placeholder="Type your message...", show_label=False)
                    user_input.submit(fn=handle_text_chat, inputs=[user_input, chatbot], outputs=[user_input, chatbot])

                with gr.Column(scale=1):
                    mic_button = WebRTC(mode="send-receive", modality="audio")
                    mic_button.stream(fn=ReplyOnPause(handle_audio), inputs=[mic_button], outputs=[mic_button], time_limit=60)

        with gr.Tab("Customer Data"):
            gr.Markdown("### Customer Information Table")
            data_frame = gr.Dataframe(
                headers=["customer_name", "request_type", "issue", "emotion"],
                interactive=False,
                wrap=True
            )
            with gr.Row(elem_classes="toolbox"):
                update_button = gr.Button("📤 Update DataFrame")
                refresh_button = gr.Button("🔄 Refresh Table")
                reset_button = gr.Button("🪹 Reset Memory")

            update_button.click(fn=df_update, outputs=[debug_box])
            refresh_button.click(fn=update_table, outputs=[data_frame])
            reset_button.click(fn=reset_memory, outputs=[debug_box])

    # Toast feedback
    def show_toast(msg: str):
        if msg:
            gr.Info(msg)

    debug_box.change(fn=show_toast, inputs=[debug_box])

    # Footer
    gr.Markdown("<div class='footer-note'>🚀 Made with ❤️ by Rikhil</div>")

    demo.load(fn=update_table, outputs=[data_frame])


if __name__ == "__main__":
    demo.launch()
