import streamlit as st
import pandas as pd
import requests
import json

# Function to send CSV data to an AI model for analysis
def get_data_insights(csv_data):
    url = "http://localhost:11434/api/chat"  # Adjust API endpoint
    payload = {
        "model": "deepseek-r1:8b",
        "messages": [{"role": "user", "content": f"Analyze this CSV data and provide insights: {csv_data}"}]
    }
    
    try:
        response = requests.post(url, json=payload, stream=True)
        response.raise_for_status()
        
        collected_response = ""
        for line in response.iter_lines():
            if line:
                try:
                    data = json.loads(line)
                    if "message" in data and "content" in data["message"]:
                        collected_response += data["message"]["content"] + " "
                except json.JSONDecodeError:
                    continue
        
        return collected_response.strip() if collected_response else "No response received."
    except Exception as e:
        return f"Error: {e}"

st.title("CSV Data Analyzer using DeepSeek-R1:8b on Ollama for AI Insights")

# File uploader for CSV data
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

data = None
if uploaded_file is not None:
    # Read the CSV file into a DataFrame, handling empty values properly
    data = pd.read_csv(uploaded_file).dropna(how='all')  # Remove completely empty rows
    st.write("Preview of Uploaded Data:")
    
    # Display data in a grid format with correct column separation
    if not data.empty:
        st.dataframe(data, height=300)
    else:
        st.warning("The uploaded CSV file contains no valid data.")

# Button to analyze the data using AI
if st.button("Analyze with AI"):
    if data is not None and not data.empty:
        csv_string = data.to_csv(index=False)
        insights = get_data_insights(csv_string)
        st.text_area("AI Insights:", value=insights, height=300)
        
        # Allow user to ask follow-up questions
        follow_up = st.text_input("Ask a follow-up question:")
        if follow_up and st.button("Submit Question"):
            follow_up_prompt = f"Based on the previous insights, answer this follow-up question: {follow_up}"
            follow_up_response = get_data_insights(follow_up_prompt)
            st.text_area("Follow-up Response:", value=follow_up_response, height=200)
    else:
        st.warning("Please upload a CSV file with valid data first.")
