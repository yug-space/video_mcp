# YouTube Transcript MCP Server

This is a Model Control Protocol (MCP) server that provides a tool to fetch transcripts from YouTube videos.

## Features

- Extracts video ID from any valid YouTube URL
- Returns plain-text transcripts (without timestamps)
- Uses the `youtube-transcript-api` library

## Installation

```bash
# Install dependencies
pip install youtube-transcript-api "mcp[fastmcp]"
```

## Usage

Run the server:

```bash
python main.py
```

The server exposes a single tool:

- `get_transcript`: Takes a YouTube URL and returns the video ID and transcript

## Example

Using the MCP client:

```python
from mcp.client import Client

client = Client(transport="stdio")
response = client.call("get_transcript", {"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"})
print(f"Video ID: {response['video_id']}")
print(f"Transcript: {response['transcript'][:100]}...")  # First 100 chars
```

## Error Handling

The server handles these error cases:
- Invalid YouTube URLs
- Videos without available transcripts
