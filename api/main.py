from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import google.generativeai as genai

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust according to your needs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Google Generative AI client
api_key = os.getenv("API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

class PromptRequest(BaseModel):
    prompt: str

@app.post("/api/chat")
async def chat(request: PromptRequest):
    try:
        result = model.generate_content(request.prompt)
        print("Result object:", result)  # Print the result to see its attributes
        # Handle the response properly
        # e.g., if it has multiple outputs, pick the first one
        if hasattr(result, 'text'):
            text = result.text
        elif hasattr(result, 'content'):
            text = result.content
        else:
            raise HTTPException(status_code=500, detail="Unexpected response structure")
        return {"text": text}
    except Exception as e:
        print(f"Error generating response: {e}")
        raise HTTPException(status_code=500, detail="Error generating response")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
