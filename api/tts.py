import base64
import tempfile
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import edge_tts
import asyncio

app = FastAPI()

@app.post("/api/tts")
async def tts(request: Request):
    data = await request.json()
    text = data.get("text", "").strip()

    if not text:
        return JSONResponse(content={"error": "Text is required"}, status_code=400)

    voice = "en-GB-LibbyNeural"

    try:
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=True, suffix=".mp3") as temp_file:
            communicate = edge_tts.Communicate(text, voice)
            await communicate.save(temp_file.name)

            # Read audio and encode as base64
            with open(temp_file.name, "rb") as f:
                audio_base64 = base64.b64encode(f.read()).decode("utf-8")

        return {"audio_base64": audio_base64}

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
