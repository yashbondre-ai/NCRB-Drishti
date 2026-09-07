from pathlib import Path

_model = None

def _get_whisper_model():
    global _model
    if _model is None:
        import whisper

        _model = whisper.load_model("tiny")
    return _model


def extract_audio(file_path: Path) -> str:
    model = _get_whisper_model()
    result = model.transcribe(str(file_path), fp16=False)
    text = result["text"].strip()

    return text