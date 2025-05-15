"""
Main entry point for the podcast-mcp application.
A simple MCP server example.
"""

import re
import sys
from typing import TypedDict

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from mcp.server.fastmcp import FastMCP

# Initialize the MCP server
mcp = FastMCP(
    name="YouTube Transcript Server",
    description="Fetches plain-text transcripts for public YouTube videos"
)

# YouTube URL regex pattern
YOUTUBE_REGEX = re.compile(
    r"(https?://)?(www\.)?"
    r"(youtube|youtu|youtube-nocookie)\.(com|be)/"
    r"(watch\?v=|embed/|v/|.+\?v=)?(?P<id>[^&=%\?]{11})"
)


def extract_video_id(url: str) -> str | None:
    """Return the 11-character YouTube video ID (or None if invalid)."""
    match = YOUTUBE_REGEX.match(url)
    return match.group("id") if match else None


class TranscriptRequest(TypedDict):
    url: str


@mcp.tool()
def get_transcript(url: str):
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
    if not url:
        raise ValueError("URL is required")
    
    video_id = extract_video_id(url)
    if not video_id:
        raise ValueError("Invalid YouTube URL")

    transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
    transcript_text = ""
    for item in transcript_list:
        transcript_text += item["text"] + " "

    return {
        "video_id": video_id,
        "transcript": transcript_text
    }


if __name__ == "__main__":
    print("🔧 Starting YouTube Transcript MCP server...", file=sys.stderr)
    mcp.run(transport="stdio")
