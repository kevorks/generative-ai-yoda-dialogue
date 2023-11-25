import os
import uvicorn
from openai import OpenAI
from fastapi import FastAPI, Body, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI(
    title='Yoda Dialogue Generator',
    description='API for Yoda dialogue generation',
    openapi_tags=[
        {
            'name': 'endpoints'
        }
    ]
)


class TextInput(BaseModel):
    content: str


@app.get("/", tags=['endpoints'])
def read_root():
    return {'message': 'Welcome to OpenAI Yoda Chat API'}


@app.post("/inputtext", tags=['endpoints'])
def get_yoda_dialogue(text_input: TextInput = Body(...)):
    try:
        api_key_file_path = os.getcwd() + "/api_key.txt"
        with open(api_key_file_path, 'r') as file:
            api_key = file.read().strip()

        client = OpenAI(api_key=api_key)

        prompt_message_path = os.getcwd() + "/prompt_message.txt"
        with open(prompt_message_path, 'r') as file:
            prompt_message = file.read().strip()

        message_text = [
            {"role": "system", "content": prompt_message},
            {"role": "user", "content": text_input.content}
        ]

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=message_text,
            temperature=1,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        completed_text = response.choices[0].message.content

        return HTMLResponse(content=completed_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
