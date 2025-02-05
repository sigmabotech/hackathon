import os
import google.generativeai as genai

def configure_gemini():
    """Configure Gemini API with environment variable."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set")
    genai.configure(api_key=api_key)

def upload_to_gemini(path, mime_type="image/png"):
    """Uploads the given file to Gemini."""
    file = genai.upload_file(path, mime_type=mime_type)
    print(f"Uploaded file '{file.display_name}' as: {file.uri}")
    return file

def get_model():
    """Create and configure the Gemini model."""
    generation_config = {
        "temperature": 1.0,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "application/json",
    }
    
    system_instruction = """You are an AI trained to process construction-related documents.
            Extract the following information from the text below into a structured JSON format:
            - Vorderansicht:
                - Bauteil:
                    - Länge "Gesamt"
                    - Höhe "Gesamt"
                - Ausklinkung links:
                    - Länge (left of the image, the first dimension above the original/full Länge)
                    - Höhe (The way to this value is: left of the image, the first and lower dimension to the right of the original/full Höhe)
                - Ausklinkung rechts:
                    - Länge (right of the image, the first dimension above the original/full Länge)
                    - Höhe (The way to this value is: right of the image, the first and lower dimension to the left of the original/full Höhe)
            
            Return only the JSON object, structured like this:
            {
                "Vorderansicht": {
                    "Bauteil": {
                        "Länge_Gesamt": 0.0,
                        "Höhe_Gesamt": 0.0
                    },
                    "Ausklinkung_links": {
                        "Länge": 0.0,
                        "Höhe": 0.0
                    },
                    "Ausklinkung_rechts": {
                        "Länge": 0.0,
                        "Höhe": 0.0
                    }
                }
            }"""
    
    return genai.GenerativeModel(
        model_name="gemini-2.0-flash-exp",
        generation_config=generation_config,
        system_instruction=system_instruction,
    )

def process_vorderansicht_image(image_path):
    """
    Process a front view (Vorderansicht) image using Gemini API and return structured JSON data.
    
    Args:
        image_path (str): Path to the front view image file
        
    Returns:
        str: JSON response from Gemini containing front view measurements
    """
    try:
        # Configure Gemini
        configure_gemini()
        
        # Upload the image
        image_file = upload_to_gemini(image_path)
        
        # Get the model
        model = get_model()
        
        # Initialize chat with historical context
        chat_session = model.start_chat(
            history=[
                {
                    "role": "user",
                    "parts": [image_file],
                }
            ]
        )
        
        # Get response
        response = chat_session.send_message("Please extract the measurements from this front view drawing.")
        
        return response.text
        
    except Exception as e:
        print(f"Error processing front view image: {str(e)}")
        raise

def main():
    """Main function for testing."""
    try:
        # Example usage
        image_path = r"plancir\cropped_sections\Vorderansicht.png"
        result = process_vorderansicht_image(image_path)
        print("Processed Result:")
        print(result)
        
    except Exception as e:
        print(f"Error in main: {str(e)}")

if __name__ == "__main__":
    main()