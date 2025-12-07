"""
Module for analyzing audio content using Google Gemini.
"""
import os
import time
import argparse
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

def upload_to_gemini(path, mime_type=None):
    """Uploads the given file to Gemini.

    See https://ai.google.dev/gemini-api/docs/prompting_with_media
    """
    file = genai.upload_file(path, mime_type=mime_type) # type: ignore
    print(f"Uploaded file '{file.display_name}' as: {file.uri}")
    return file

def wait_for_files_active(files):
    """Waits for the given files to be active.

    Some files uploaded to the Gemini API need to be processed before they can
    be used as prompt inputs. The status can be seen by querying the file's
    "state" field.

    This implementation relies on the file's "name" field to perform the query,
    and if the state is not ACTIVE, it waits 10 seconds and checks again.
    """
    print("Waiting for file processing...")
    for name in (file.name for file in files):
        file = genai.get_file(name) # type: ignore
        while file.state.name == "PROCESSING":
            print(".", end="", flush=True)
            time.sleep(10)
            file = genai.get_file(name) # type: ignore
        if file.state.name != "ACTIVE":
            raise RuntimeError(f"File {file.name} failed to process")
    print("...all files ready")

def analyze_audio_content( # pylint: disable=too-many-arguments, too-many-locals, too-many-positional-arguments
        audio_path,
        prompt,
        json_path=None,
        json_context=None,
        model_name="gemini-3-pro-preview",
        api_key=None,
        system_instruction=None
):
    """
    Analyzes audio content using Google Gemini.

    Args:
        audio_path (str): Path to the audio file.
        prompt (str): Prompt for the model.
        json_path (str, optional): Path to a JSON context file.
        json_context (str, optional): JSON context string.
        model_name (str, optional): Gemini model name.
        api_key (str, optional): Google API key.
        system_instruction (str, optional): System instruction for the model.

    Returns:
        str: The model's response.
    """
    if not api_key:
        raise ValueError("API key is required")

    genai.configure(api_key=api_key) # type: ignore

    files_to_upload = []

    # Upload Audio
    if not os.path.exists(audio_path):
        return f"Error: Audio file not found at {audio_path}"

    print(f"Uploading audio: {audio_path}")
    # Simple mime type detection or default to wav/mp3
    mime_type = "audio/wav"
    if audio_path.lower().endswith(".mp3"):
        mime_type = "audio/mp3"

    audio_file = upload_to_gemini(audio_path, mime_type=mime_type)
    files_to_upload.append(audio_file)

    # Handle JSON
    json_content = ""
    if json_context:
        json_content = json_context
    elif json_path:
        if os.path.exists(json_path):
            print(f"Reading JSON: {json_path}")
            with open(json_path, 'r', encoding='utf-8') as f:
                json_content = f.read()
        else:
            print(f"Warning: JSON file not found at {json_path}")

    # Wait for processing
    wait_for_files_active(files_to_upload)

    # Create the model
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel( # type: ignore
        model_name=model_name,
        generation_config=generation_config, # type: ignore
        system_instruction=system_instruction
    )

    # Construct the prompt parts
    prompt_parts = []
    if json_content:
        prompt_parts.append(f"Context JSON:\n{json_content}\n")

    prompt_parts.append(prompt)
    prompt_parts.append(audio_file)

    # Generate content
    print("Generating content...")
    response = model.generate_content(prompt_parts)

    return response.text

def main():
    """
    Main function for command line usage.
    """
    parser = argparse.ArgumentParser(description="Upload audio/JSON and prompt Gemini.")
    parser.add_argument("--audio", required=True, help="Path to the audio file")
    parser.add_argument("--json", help="Path to the JSON file (optional)")
    parser.add_argument("--prompt", default="Describe this audio.", help="The prompt to send")
    parser.add_argument("--model", default="gemini-3-pro-preview", help="The model to use")

    args = parser.parse_args()

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Error: GOOGLE_API_KEY environment variable not set.")
        return

    try:
        result = analyze_audio_content(
            audio_path=args.audio,
            prompt=args.prompt,
            json_path=args.json,
            json_context=None,
            model_name=args.model,
            api_key=api_key
        )
        print("\nResponse:")
        print(result)
    except Exception as e: # pylint: disable=broad-exception-caught
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
