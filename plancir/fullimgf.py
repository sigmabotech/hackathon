import google.generativeai as genai

def upload_to_gemini(path, mime_type="image/png"):
    """Uploads the given file to Gemini."""
    file = genai.upload_file(path, mime_type=mime_type)
    print(f"Uploaded file '{file.display_name}' as: {file.uri}")
    return file

def read_prompt_file(file_path):
    """Reads the contents of a prompt file."""
    with open(file_path, "r") as f:
        prompt = f.read().strip()
    return prompt

def extract_structured_data(image_file):
    """Extract structured data from the image using the Gemini API."""
    # Configure Gemini API
    genai.configure(api_key="AIzaSyA_TXvuJYCkKHBEO4hzuffe6RB09P7PdpA")
    
    # Upload file
    gemini_file = upload_to_gemini(image_file)

    # Configure the generation model
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "application/json",
    }

    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash-exp",
        generation_config=generation_config,
    )

    # Start a chat session
    prompt_text = read_prompt_file("prompt.txt")
    history = [
        {
            "role": "user",
            "parts": [
                gemini_file,
                prompt_text,
            ],
        }
    ]
    chat_session = model.start_chat(history=history)

    # Send a message to get a response
    response = chat_session.send_message("Please process the uploaded image.")
    print("Extracted Data:\n", response.text)
    return response.text