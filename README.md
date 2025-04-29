# YouTube Transcript MCP Server

A simple server that extracts and returns transcripts from YouTube videos.

## Setup

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the server:
   ```
   python main.py
   ```

The server will start on port 5000.

## API Usage

### Get Transcript

**Endpoint:** `/transcript`
**Method:** POST
**Content-Type:** application/json

**Request Body:**
```json
{
  "url": "https://www.youtube.com/watch?v=VIDEO_ID"
}
```

**Response:**
```json
{
  "video_id": "VIDEO_ID",
  "transcript": "Full video transcript text..."
}
```

### Health Check

**Endpoint:** `/health`
**Method:** GET

**Response:**
```json
{
  "status": "ok"
}
```

## Error Handling

The API returns appropriate error messages with HTTP status codes when:
- The YouTube URL is missing or invalid
- The transcript cannot be retrieved 