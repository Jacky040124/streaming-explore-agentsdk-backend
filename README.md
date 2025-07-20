# Streaming Explore AgentSDK Backend

A multi-agent content creation workflow using OpenAI Agents SDK with FastAPI backend.

## Overview

This backend orchestrates multiple AI agents to create comprehensive content including research, image generation, and storytelling. The system uses the OpenAI Agents SDK to coordinate between specialized agents for different tasks.

## Features

- 🔍 **Research Agent**: Web search and information gathering
- 🎨 **Artist Agent**: DALL-E 3 image generation with custom prompts
- ✍️ **Writer Agent**: Creative story generation
- 🧠 **Prompt Generator**: Optimized prompt creation for better results
- 🚀 **FastAPI**: REST API endpoints for workflow execution
- 📝 **Markdown Storage**: Automatic result saving with image handling

## Architecture

### Multi-Agent Workflow
1. **Research Phase**: Gather relevant information about the topic
2. **Prompt Generation**: Create optimized prompts for image and story creation
3. **Content Creation**: Generate image and story in parallel
4. **Result Aggregation**: Combine all outputs into structured format

### API Endpoints
- `POST /workflow/create` - Execute content creation workflow
- `GET /workflow/health` - Health check endpoint
- `GET /health` - Global API health check

## Setup

### Prerequisites
- Python 3.11+
- OpenAI API key
- UV package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Jacky040124/streaming-explore-agentsdk-backend.git
   cd streaming-explore-agentsdk-backend
   ```

2. **Install dependencies**
   ```bash
   uv sync
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

4. **Run the API server**
   ```bash
   uv run run_api.py
   ```

The API will be available at `http://localhost:8000`

## Environment Variables

Create a `.env` file with:

```env
OPENAI_API_KEY=your_openai_api_key_here
DEFAULT_MODEL=gpt-4-turbo-preview
```

## Usage

### API Example

```bash
curl -X POST http://localhost:8000/workflow/create \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "space exploration and Mars missions",
    "save_markdown": true
  }'
```

### Response Format

```json
{
  "research_summary": "...",
  "image_prompt": "...", 
  "story_prompt": "...",
  "generated_image": "https://...",
  "generated_story": "...",
  "metadata": {
    "workflow_id": "...",
    "timestamp": "...",
    "execution_time_seconds": 45.2,
    "status": "completed"
  }
}
```

## Project Structure

```
backend/
├── api/                    # FastAPI application
│   ├── main.py            # FastAPI app instance
│   ├── models/            # Pydantic models
│   └── routes/            # API route definitions
├── workers/               # Agent definitions
│   ├── artist.py          # Image generation agent
│   ├── writer.py          # Story generation agent
│   ├── researcher.py      # Research agent
│   └── prompt_generator.py # Prompt optimization agent
├── workflows/             # Workflow orchestration
│   └── content_creation.py # Main workflow logic
├── tools/                 # Custom agent tools
│   └── generate_image.py  # DALL-E 3 integration
├── utils/                 # Utilities
│   ├── config.py          # Configuration management
│   ├── models.py          # Data models
│   ├── markdown_storage.py # File storage utilities
│   └── image_handler.py   # Image processing
└── main.py               # CLI testing interface
```

## Development

### Testing the Workflow

```bash
# Test the complete workflow
uv run python main.py

# Run API server in development mode
uv run run_api.py
```

### API Documentation

Visit `http://localhost:8000/docs` for interactive API documentation.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License.