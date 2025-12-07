# Gemini Multimodal Audio Upload

![CodeRabbit Pull Request Reviews](https://img.shields.io/coderabbit/prs/github/unscene/gemini-audio-upload?utm_source=oss&utm_medium=github&utm_campaign=unscene%2Fgemini-audio-upload&labelColor=171717&color=FF570A&link=https%3A%2F%2Fcoderabbit.ai&label=CodeRabbit+Reviews)

This project provides a Model Context Protocol (MCP) server that enables audio analysis using Google's Gemini models. It allows you to upload audio files, provide optional context (JSON), and receive detailed analysis based on your prompts.

## Features

- **Audio Analysis**: Upload and analyze audio files (WAV, MP3, etc.) using Google Gemini.
- **Multimodal Context**: Support for providing additional context via JSON files or strings.
- **System Instructions**: Ability to provide system instructions (e.g., "Gem" definitions) to guide the model's behavior.
- **MCP Server**: Exposes functionality as an MCP tool, making it compatible with MCP clients like Claude Desktop or VS Code extensions.

## Prerequisites

- Python 3.10 or higher
- A Google Cloud Project with the Gemini API enabled.
- An API key for the Gemini API.

## Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/unscene/gemini-audio-upload.git
    cd gemini-audio-upload
    ```

2.  Install dependencies with uv:
    ```bash
    uv sync
    ```

## Configuration

1.  Create a `.env` file in the root directory:
    ```bash
    cp .env.example .env # If .env.example exists, otherwise create new
    ```

2.  Add your Google API key to the `.env` file:
    ```env
    GOOGLE_API_KEY=your_api_key_here
    ```

## Usage

### Running the MCP Server

You can run the MCP server directly using `uv`:

```bash
uv run gemini_audio/mcp_server.py
```

However, it is typically run by an MCP client.

### MCP Tool: `analyze_audio`

The server exposes a single tool: `analyze_audio`.

**Arguments:**

- `audio_path` (string, required): The absolute path to the audio file you want to analyze.
- `prompt` (string, optional): The prompt to guide the analysis. Default: "Describe this audio."
- `json_path` (string, optional): Path to a JSON file containing context data.
- `json_context` (string, optional): A JSON string containing context data (overrides `json_path`).
- `instruction_file` (string, optional): Path to a text file containing system instructions.
- `model` (string, optional): The Gemini model to use. Default: "gemini-1.5-pro".

### Example Usage (Conceptual)

If you are using an MCP client, you might ask:

> "Analyze the audio file at `C:\path\to\recording.wav` and tell me if the speaker sounds happy."

The client would call the `analyze_audio` tool with:
- `audio_path`: `C:\path\to\recording.wav`
- `prompt`: "Tell me if the speaker sounds happy."

## Client Configuration

### Claude Desktop App

To use this server with the Claude Desktop App, add the following configuration to your `claude_desktop_config.json` file.

**Windows Location:** `%APPDATA%\Claude\claude_desktop_config.json`
**macOS Location:** `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "gemini-audio": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/gemini-audio-upload",
        "run",
        "gemini_audio/mcp_server.py"
      ],
      "env": {
        "GOOGLE_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

*Note: Replace `/absolute/path/to/gemini-audio-upload` with the actual path to where you cloned this repository. You can also set the `GOOGLE_API_KEY` in the `.env` file in the project directory instead of the config JSON, provided `uv` picks it up correctly or you use the python executable directly.*

### VS Code (MCP Extension)

If you are using an MCP extension in VS Code (like the official "Model Context Protocol" extension), you can typically configure it in your VS Code `settings.json`:

```json
"mcp.servers": {
    "gemini-audio": {
        "command": "uv",
        "args": [
            "--directory",
            "C:\\absolute\\path\\to\\gemini-audio-upload",
            "run",
            "gemini_audio/mcp_server.py"
        ],
        "env": {
            "GOOGLE_API_KEY": "your_api_key_here"
        }
    }
}
```

## License

[MIT](LICENSE)
