"""
youtube_transcript_server.py
An MCP server that exposes one tool: `get_transcript`.
Given any valid YouTube URL it returns the video_id and a
plain-text transcript (no timestamps) using youtube-transcript-api.
"""

import re
from typing import TypedDict

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from mcp.server.fastmcp import FastMCP

# ----------------------------------------------------------------------
# Initialise the MCP server ----------------------------------------------------
mcp = FastMCP(
    name="YouTube Transcript Server",
    description="Fetches plain-text transcripts for public YouTube videos"
)

# ----------------------------------------------------------------------
# Helper – identical to your Flask version -------------------------------------
YOUTUBE_REGEX = re.compile(
    r"(https?://)?(www\.)?"
    r"(youtube|youtu|youtube-nocookie)\.(com|be)/"
    r"(watch\?v=|embed/|v/|.+\?v=)?(?P<id>[^&=%\?]{11})"
)


def extract_video_id(url: str) -> str | None:
    """Return the 11-character YouTube video ID (or None if invalid)."""
    match = YOUTUBE_REGEX.match(url)
    return match.group("id") if match else None


# ----------------------------------------------------------------------
# The actual MCP tool ----------------------------------------------------
class TranscriptRequest(TypedDict):
    url: str


class TranscriptResponse(TypedDict):
    video_id: str
    transcript: str


@mcp.tool()
def get_transcript(data: TranscriptRequest) -> TranscriptResponse:  # noqa: D401
    """Return the transcript of a YouTube video.

    Parameters
    ----------
    data.url : str
        Any valid YouTube watch / share / short-link URL.

    Returns
    -------
    video_id : str
        The 11-character ID of the video.
    transcript : str
        The plain-text transcript with time-codes removed.

    Raises
    ------
    ValueError
        If the URL is missing or invalid.
    youtube_transcript_api.YouTubeTranscriptApiError
        If the video has no available transcript.
    """
    url = data["url"]
    video_id = extract_video_id(url)
    if not video_id:
        raise ValueError("Invalid YouTube URL")

    transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
    formatter = TextFormatter()
    formatted_text = formatter.format_transcript(transcript_list)

    return {"video_id": video_id, "transcript": formatted_text}


# ----------------------------------------------------------------------
# Kick everything off ----------------------------------------------------
if __name__ == "__main__":
    # Default port is 7000; set MCP_PORT to override.
    mcp.run()