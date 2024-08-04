from openai import OpenAI
from openai.types.chat.chat_completion_system_message_param import (
    ChatCompletionSystemMessageParam,
)
from ..core.config import settings
from ..core.utils.timer_tracker import tracktime
from typing import Literal


client = OpenAI(api_key=settings.OPENAI_API_KEY)
model = settings.OPENAI_MODEL


def _get_assistant(instructions: str) -> ChatCompletionSystemMessageParam:
    return ChatCompletionSystemMessageParam(
        role="system",
        content=instructions,
    )


def _get_completion_result(assistant_instructions: str, command: str) -> str | None:
    setup_assistant = _get_assistant(assistant_instructions)

    completion = client.chat.completions.create(
        model=model,
        messages=[
            setup_assistant,
            {
                "role": "user",
                "content": command,
            },
        ],
    )

    return completion.choices[0].message.content


@tracktime
def generate_summary_from_transcription_chunk(transcription_chunk: str, summary_last_tokens: str) -> str | None:
    INSTRUCTIONS = "You are an expert assistant in summarizing technical content about college choices"
    COMMAND = f"""
    You will receive a transcript of a video call between two Portuguese-speaking people about undergraduate courses and you will be asked to generate a summary of this conversation.
    Your response should only contain the summary of the conversation, in Portuguese, and no additional observations or comments.
    Do not include any references to the names of people who may be present in the transcript.
    If you are unable to generate a transcript for any reason, reply: "Unable to generate a summary. Please review the transcript"
    Respond with bullet points separating each topic covered in the conversation

    You are currently writing the summary of a text.
    Here you have the last {settings.OPENAI_SUMMARY_LAST_TOKENS_SIZE // 3} tokens of your summary: {summary_last_tokens}
    Return only the new parts of the summary, you don't need to repeat in your answer what's already summarized
    Summarize this chunk so it can be added to your summary: {transcription_chunk}
    """

    return _get_completion_result(assistant_instructions=INSTRUCTIONS, command=COMMAND)


@tracktime
def generate_summary_final(initial_summary: str) -> str:
    INSTRUCTIONS = "You are an expert assistant in summarizing technical content about college choices. Your responses should be in portuguese"
    COMMAND = f"""
    Summarize this conversation and remove duplicates: {initial_summary}
    """

    return _get_completion_result(assistant_instructions=INSTRUCTIONS, command=COMMAND)


@tracktime
def generate_info_from_summary(summary: str, type: Literal["main_topics", "interest_courses", "main_questions_and_concerns", "insights"]) -> str | None:
    INSTRUCTIONS = "You are an expert assistant in summarizing technical content about college choices"
    COMMAND = f"""
    You will receive a summary of a video call transcription between two Portuguese-speaking people about undergraduate courses and you will be asked to generate a list of {type} for this conversation.
    Your response should only contain the {type}, in Portuguese, and no additional observations or comments.
    Do not include any references to the names of people who may be present in the summary.
    If you are unable to generate a list of {type} for any reason, reply: "Unable to generate {type}. Please review the summary"
    Respond with ";" separating each {type}

    Summary: {summary}
    """

    return _get_completion_result(assistant_instructions=INSTRUCTIONS, command=COMMAND)
