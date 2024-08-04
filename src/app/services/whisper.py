import whisper
from ..core.config import settings
from ..core.utils.timer_tracker import tracktime
from ..core.logger import logger



@tracktime
def transcribe_file_content(file_path: str) -> str:
    model = settings.WHISPER_MODEL
    logger.debug(f"[WHISPER] loading model {model}...")
    model = whisper.load_model(model)

    logger.debug(f"[WHISPER] generating transcription for file {file_path}")
    result = model.transcribe(
        file_path,
        fp16=settings.WHISPER_FP16_ENABLED,
        language=settings.WHISPER_LANGUAGE,
    )
    transcription = result.get("text")
    logger.debug(f"[WHISPER] transcription finished for file {file_path}; initial content='{transcription[:10]}...'")
    return transcription
