"""
MCP Server for Gemini Audio analysis.
"""
import os
import sys
from typing import Optional
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP # type: ignore

try:
    from analyze_audio import analyze_audio_content
except ImportError:
    # Fallback for when running from root or as a package
    from gemini_audio.analyze_audio import analyze_audio_content

load_dotenv()

mcp = FastMCP("GeminiAudio")

@mcp.tool()
def analyze_audio( # pylint: disable=too-many-arguments, too-many-positional-arguments
        audio_path: str,
        prompt: str = "Describe this audio.",
        json_path: Optional[str] = None,
        json_context: Optional[str] = None,
        instruction_file: Optional[str] = None,
        model: str = "gemini-3-pro-preview"
) -> str:
    """
    Analyze an audio file using Google Gemini.

    Args:
        audio_path: Path to the audio file (wav, mp3, etc.)
        prompt: The prompt to send to Gemini.
        json_path: Optional path to a JSON file to provide as context.
        json_context: Optional JSON string to provide as context (overrides json_path if provided).
        instruction_file: Optional path to a text file containing system instructions.
        model: The Gemini model to use.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return "Error: GOOGLE_API_KEY not set."

    system_instruction = None
    if instruction_file:
        if os.path.exists(instruction_file):
            try:
                with open(instruction_file, 'r', encoding='utf-8') as f:
                    system_instruction = f.read()
            except Exception as e: # pylint: disable=broad-exception-caught
                return f"Error reading instruction file: {str(e)}"
        else:
            return f"Error: Instruction file not found at {instruction_file}"

    try:
        return analyze_audio_content(
            audio_path,
            prompt,
            json_path,
            json_context,
            model,
            api_key,
            system_instruction
        )
    except Exception as e: # pylint: disable=broad-exception-caught
        return f"Error analyzing audio: {str(e)}"

if __name__ == "__main__":
    if "--help" in sys.argv:
        print("GeminiAudio MCP Server")
        print("Run this server using an MCP client (e.g. Claude Desktop, VS Code MCP extension).")
        print("\nTools:")
        print("  - analyze_audio: Analyze an audio file using Google Gemini.")
        sys.exit(0)
    mcp.run()
