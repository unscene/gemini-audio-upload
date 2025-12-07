# Gemini Multimodal Audio Upload

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

2.  Create and activate a virtual environment (recommended):
    ```bash
    python -m venv .venv
    # Windows
    .venv\Scripts\activate
    # macOS/Linux
    source .venv/bin/activate
    ```

3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    pip install mcp # Required for the MCP server
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

You can run the MCP server directly using Python:

```bash
python gemini_audio/mcp_server.py
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

## License

[MIT](LICENSE)
