import requests
from dotenv import load_dotenv
import json
import streamlit as st
import os

load_dotenv()

BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "146981a9-5e60-4782-abf5-fe873a2c7846"
FLOW_ID = "65506cf3-a890-4b4b-96d4-275e12ffe09c"
APPLICATION_TOKEN = os.environ.get("APP_TOKEN")
ENDPOINT = "customer" # The endpoint name of the flow


def run_flow(message: str) -> dict:
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{ENDPOINT}"

    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat",
    }
    
    headers = {"Authorization": "Bearer " + APPLICATION_TOKEN, "Content-Type": "application/json"}
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()


def main():
    st.title("Chat Interface")
    
    message = st.text_area("Message", placeholder="Ask Something...")
    
    if st.button("Run Flow"):
        if not message.strip():
            st.error("Please enter a message")
            return
        try:
            with st.spinner("Running Flow..."):
                response = run_flow(message)
            response = response["outputs"][0]["outputs"][0]["results"]["message"]["text"]
            st.markdown(response)
        except Exception as e:
            st.error(str(e))       

if __name__ == "__main__":
    main()