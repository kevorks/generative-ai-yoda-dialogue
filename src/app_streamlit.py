import streamlit as st
import requests
from pydantic import BaseModel


class TextInput(BaseModel):
    content: str


backend_url = "http://0.0.0.0:8000"

st.title("Yoda Dialogue Generator")

# Input for user's text
user_input = st.text_area("Enter your text:")

# Button to generate Yoda dialogue
if st.button("Generate Yoda Dialogue"):
    # Request to the FastAPI backend
    input_data = TextInput(content=user_input)
    response = requests.post(
        f"{backend_url}/inputtext", json=input_data.dict()
    )

    if response.status_code == 200:
        yoda_dialogue = response.text
        st.success("Yoda Dialogue:")
        st.write(yoda_dialogue)
    else:
        st.error(f"Error from FastAPI backend: {response.text}")
