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
        model = genai.GenerativeModel(model_name="gemini-2.0-flash")
        image_data = request.data.get('image_data')
        if not image_data:
            return Response({"error": "Image data is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Convert base64 string to PIL image
        image_bytes = base64.b64decode(image_data)
        image = Image.open(BytesIO(image_bytes))
        prompt = """
You are an expert in analyzing images. I will provide an image, and your job is to examine it and determine the type of content.  

### **Response Guidelines:**  
1. **If the image contains a math or science problem**, solve it using proper formulas and show step-by-step calculations. If a numerical solution is not possible, provide a well-formed expression.  
2. **If the image depicts a diagram or concept**, analyze its meaning and provide relevant explanations.  
3. **If the image contains text, equations, or symbols**, extract and interpret them accurately.  
4. **If it is a general image with no clear problem**, analyze its contents, describe the details, and infer any meaningful insights.  
5. **If the image is unclear or unidentifiable**, mention that the content is ambiguous and suggest possible interpretations.  

Provide a structured and concise response based on the image's content.
"""
       
        prompt2="""You are an expert in summarization. I will provide a response, and your task is to generate a **clear and relevant title** that best represents the content.  

### **Guidelines:**  
1. The title **must not exceed 3 words**.  
2. It should accurately summarize the response.  
3. Use simple and direct language.  
Provide only the title without any extra explanation.
"""
        prompt3="""You are an expert in **HTML formatting**. I will provide a response, and your job is to format it with **clear structure, proper spacing, and step-by-step clarity**.  

### **Instructions:**  
1. Use **headings** (`<h1>`, `<h2>`, etc.) where needed.  
2. Add **multiple `<br>` tags** for spacing between sections and steps.  
3. Use **separate `<p>` tags** for each line in the solution.  
4. Format **math expressions properly** using `<sup>`, `<sub>`, and `<b>` tags.  
5. **Remove unnecessary `*` and markdown artifacts.**  
 

Provide **only** the formatted HTML inside the `<body>` tag (but do not include the `<body>` tag itself).  
""" 
        solution = model.generate_content([prompt, image])
        title= model.generate_content([prompt2,solution.text])
        formatted_solution=model.generate_content([prompt3,solution.text])
        # Query the LLM
        
      
        return Response({"solution": formatted_solution.text,"title":title.text}, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({"error": f"Could not process the image: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

