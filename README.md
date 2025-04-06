# 💬 Customer Support Assistant

An AI-powered voice + text chatbot built with [`pydantic_ai`](https://github.com/roboflow/pydantic-ai), powered by Llama 3.3 70B via Cerebras/Groq. It processes customer issues, detects emotional tone, and records support requests into a structured data table. Deployable on Gradio Spaces and usable locally with both text and audio input.

---

## ⚡ Features

- 🔥 **LLM-powered form extraction** using `Agent` abstraction from `pydantic_ai`
- 🎙️ **Voice chat** with real-time streaming via [`fastrtc`](https://github.com/Rikhil-Rai/fastrtc)
- 🧠 **Memory-aware responses** using `message_history`
- 📊 **Live DataFrame updates** for structured customer requests
- 💾 **Persistent CSV logging**
- 🛠️ One-click Gradio UI with tabs for Chat + Customer Data

---

## 🚀 Getting Started

### 1. Clone the Repo

```bash
git clone https://github.com/your-username/customer-support-assistant
cd customer-support-assistant
```

### 2. Install Dependencies

> ⚠️ Make sure you use `uv` to ensure proper dependency resolution (especially for `pydantic_ai`).

```bash
uv pip install -r requirements.txt
```

> Or use `uv` directly:

```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

---

### 3. Setup `.env` File

Create a `.env` file in the root directory.

Refer to `settings.py` for required fields. At a minimum, you will need:

```env
CEREBRAS_API_KEY=your_api_key
CEREBRAS_BASE_URL=https://api.groq.com/openai/v1
```

You can optionally set environment variables for your own STT/TTS models as required by `fastrtc`.

---

### 4. Run the App Locally

```bash
python app.py
```

---

## 🌐 Deploy on Gradio Spaces

1. Add your `CEREBRAS_API_KEY` and `CEREBRAS_BASE_URL` as secrets in the Gradio Space.
2. Make sure `fastrtc` audio support is configured in the hardware tab.
3. Gradio Spaces will auto-launch the app via `app.py`.

---

## 🧪 Debug Tips

To simulate extraction alone:

```bash
python agents.py
```

Then type messages in the CLI to test how well the form is filled.

---

## 📁 File Structure

```plaintext
├── app.py                 # Main Gradio UI
├── agents.py              # Agent config + LLM interaction logic
├── settings.py            # Handles env/config
├── form_prompt.txt        # System prompt for form extraction
├── response_prompt.txt    # System prompt for response generation
├── data.csv               # Auto-generated CSV storage
├── requirements.txt
├── README.md
```

---

## 🧠 What the AI Extracts

The form agent will pull out:

- `customername`: Extracted from input or marked as `"unknown"`
- `requesttype`: e.g., `"billing"`, `"technical support"`
- `issue`: 50-line description of the issue
- `emotion`: `"angry"`, `"happy"`, etc.

---

## 🛑 Known Limitations

- Longform audio may require silence-based segmentation tuning.
- This project assumes inputs are customer support related. General queries may misfire.
- Error handling is basic — add guards if scaling for production use.

---

## 🙏 Credits

- Built using [pydantic_ai](https://github.com/roboflow/pydantic-ai)
- Voice support via [fastrtc](https://github.com/Rikhil-Rai/fastrtc)
- LLM backend: Llama 3.3 70B via [Groq](https://groq.com/)
- UI powered by [Gradio](https://gradio.app/)

---

## ❤️ Made with care by Rikhil
