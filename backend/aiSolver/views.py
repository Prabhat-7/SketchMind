from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from dotenv import load_dotenv

from PIL import Image
from io import BytesIO

import base64
import google.generativeai as genai

import os
# Load environment variables
load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
# Initialize LLM

@api_view(['POST'])
def process_image(request):
    """
    Process an uploaded image, extract text using Tesseract, and query an LLM with the extracted text.
    """
    try:
        # Validate and preprocess the image
        model = genai.GenerativeModel(model_name="gemini-1.5-flash")
        image_data = request.data.get('image_data')
        if not image_data:
            return Response({"error": "Image data is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Convert base64 string to PIL image
        image_bytes = base64.b64decode(image_data)
        image = Image.open(BytesIO(image_bytes))
        prompt=("I will provide u an image so analyse it . And find the problem and solve it . Finally return the solution")
        # Extract text from image
        response = model.generate_content([prompt, image])

        # Query the LLM
        
      
        return Response({"response": response.text}, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({"error": f"Could not process the image: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

