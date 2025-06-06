import base64 
import requests 
import io 
from PIL import Image 
from dotenv import load_dotenv 
import os
import logging 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



load_dotenv()
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


def process_image(image_path, query):
    """
    Process an image using the Groq API with the provided query.
    
    Args:
        image_path (str): Path to the image file
        query (str): The query text to send with the image
        
    Returns:
        dict: A dictionary containing either the answer or an error message
    """
    if not GROQ_API_KEY:
        logger.warning("GROQ API KEY is not set in the environment variables")
        return {"error": "API key not configured. Please contact the administrator."}
   
    try:
        with open(image_path, "rb") as image_file:
            image_content = image_file.read()
            encoded_image = base64.b64encode(image_content).decode("utf-8")
        
       
        try:  
            img = Image.open(io.BytesIO(image_content))
            img.verify()
        except Exception as e:
            logger.error(f"Invalid image format: {str(e)}")
            return {"error": f"Invalid image format: {str(e)}"} 
        
        
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": query},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}}
                ]
            }
        ]
        
        
        model = "meta-llama/llama-4-scout-17b-16e-instruct"
        try:
            response = requests.post(
                GROQ_API_URL,
                json={
                    "model": model,
                    "messages": messages,
                    "max_tokens": 1000
                },
                headers={
                    "Authorization": f"Bearer {GROQ_API_KEY}", 
                    "Content-Type": "application/json"
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                answer = result["choices"][0]["message"]["content"]
                logger.info(f"Processed response from API")
                return {"answer": answer}
            else:
                error_msg = f"Error from API: {response.status_code} - {response.text}"
                logger.error(error_msg)
                return {"error": error_msg}
                
        except Exception as e:
            logger.error(f"API request failed: {str(e)}")
            return {"error": f"API request failed: {str(e)}"}
                
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
        return {"error": f"An unexpected error occurred: {str(e)}"}
