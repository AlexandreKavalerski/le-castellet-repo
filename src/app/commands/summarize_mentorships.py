import typer
from typing import Sequence

from ..core.config import settings
from ..core.db.database import local_session
from ..services.openai import generate_summary_from_transcription_chunk, generate_summary_final
from ..models.mentorship import Mentorship


from ..core.utils import typer_async
from ..core.logger import logger


app = typer.Typer(
    no_args_is_help=True,
    rich_markup_mode="rich",
    pretty_exceptions_enable=True,
    pretty_exceptions_show_locals=True,
    pretty_exceptions_short=True,
)


def summarize_transcription(transcription: str) -> str:
    CHUNK_SIZE = settings.OPENAI_TEXT_CHUNK_SIZE
    SUMMARY_LAST_TOKENS_SIZE = settings.OPENAI_SUMMARY_LAST_TOKENS_SIZE
    summary = ""

    text_chunks = [
        transcription[i: i + CHUNK_SIZE]
        for i in range(0, len(transcription), CHUNK_SIZE)
    ]
    for chunk in text_chunks:
        summary += generate_summary_from_transcription_chunk(
            transcription_chunk=chunk,
            summary_last_tokens=summary[-SUMMARY_LAST_TOKENS_SIZE:],
        )
    return generate_summary_final(summary)


@app.command()
@typer_async
async def summarize() -> None:
    async with local_session() as db_session:
        mentorships: Sequence[Mentorship] = await Mentorship.get_all_missing_summary(
            session=db_session
        )

        for mentorship in mentorships:
            logger.info(
                f"Generating summary for mentorship id={mentorship.id}; transcription_length={len(mentorship.transcription)}"
            )
            summary: str = summarize_transcription(mentorship.transcription)
            mentorship.summary = summary
            logger.info(
                f"Updated summary for mentorship id={mentorship.id}; summary_length={len(summary)}"
            )
        await db_session.commit()

    logger.info(f"Finished update summaries for {len(mentorships)} mentorships")
    typer.echo("Summaries updated successfully.")


if __name__ == "__main__":
    logger.debug("Starting summarize mentorships script")
    app()
