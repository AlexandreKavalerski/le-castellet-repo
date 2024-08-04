import typer
from typing import Sequence

from ..core.db.database import local_session
from ..services.whisper import transcribe_file_content
from ..models.mentorship import Mentorship


from ..core.utils import typer_async
from ..core.logger import logger
from ..core.config import settings


app = typer.Typer(
    no_args_is_help=True,
    rich_markup_mode="rich",
    pretty_exceptions_enable=True,
    pretty_exceptions_show_locals=True,
    pretty_exceptions_short=True,
)


@app.command()
@typer_async
async def transcribe() -> None:
    async with local_session() as db_session:
        mentorships: Sequence[Mentorship] = await Mentorship.get_all_missing_transcription(
            session=db_session
        )

        for mentorship in mentorships:
            logger.info(f"Generating transcription for mentorship id={mentorship.id}; whisper_model={settings.WHISPER_MODEL}")
            transcription = transcribe_file_content(mentorship.recording_location)
            mentorship.transcription = transcription
            await db_session.commit()
            logger.info(
                f"Updated transcription for mentorship id={mentorship.id}; transcription_length={len(transcription)}; whisper_model={settings.WHISPER_MODEL}"
            )

    logger.info(f"Finished update transcriptions for {len(mentorships)} mentorships; whisper_model={settings.WHISPER_MODEL}")
    typer.echo("Transcriptions updated successfully.")


if __name__ == "__main__":
    logger.debug("Starting transcribe mentorships script")
    app()
