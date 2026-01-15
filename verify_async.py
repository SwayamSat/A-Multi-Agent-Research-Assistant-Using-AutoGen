import asyncio
import os
import json
import httpx
from dotenv import load_dotenv

load_dotenv()

async def verify():
    api_key = os.getenv("GEMINI_API_KEY")
    url = "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    payload = {
        "model": "gemini-1.5-flash",
        "messages": [
            {"role": "user", "content": "Hello!"}
        ]
    }
    
    print(f"Testing URL: {url}")
    
    async with httpx.AsyncClient(follow_redirects=True) as client:
        response = await client.post(url, headers=headers, json=payload)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")

if __name__ == "__main__":
    asyncio.run(verify())
