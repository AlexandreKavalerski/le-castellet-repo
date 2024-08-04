import typer
from typing import Sequence

from ..core.db.database import local_session
from ..services.openai import generate_info_from_summary
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


@app.command()
@typer_async
async def more_details() -> None:
    async with local_session() as db_session:
        mentorships: Sequence[Mentorship] = await Mentorship.get_all_missing_details(
            session=db_session
        )

        for mentorship in mentorships:
            logger.info(
                f"Generating details (insights, questions, main topics, courses) for mentorship id={mentorship.id}; summary_length={len(mentorship.summary)}"
            )

            details = {
                "main_topics": "main topics",
                "interest_courses": "course(s) of interest",
                "main_questions_and_concerns": "main questions and concerns",
                "insights": "insights",
            }
            for key, value in details.items():
                new_info = generate_info_from_summary(mentorship.summary, type=value)
                setattr(mentorship, key, new_info)

            await db_session.commit()
            logger.info(
                f"Updated details for mentorship id={mentorship.id}; summary_length={len(mentorship.summary)}"
            )

    logger.info(f"Finished update details for {len(mentorships)} mentorships")
    typer.echo("Details updated successfully.")


if __name__ == "__main__":
    logger.debug("Starting add detail infos for mentorships script")
    app()
