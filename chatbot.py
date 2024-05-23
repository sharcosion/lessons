import streamlit as st
from amadeus import Client, ResponseError
import openai

# Initialize Amadeus API
amadeus = Client(
    client_id='YOUR_AMADEUS_API_KEY',
    client_secret='YOUR_AMADEUS_API_SECRET'
)

# Initialize OpenAI API
openai.api_key = 'YOUR_OPENAI_API_KEY'

# Function to interact with Amadeus API
def check_amadeus_api(request_data):
    try:
        response = amadeus.get(request_data['endpoint'], **request_data['params'])
        return response.data
    except ResponseError as error:
        return str(error)

# Function to check vector store
def check_vector_store(request_data, response_data):
    prompt = f"Check the following API request and response for issues:\n\nRequest:\n{request_data}\n\nResponse:\n{response_data}"
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

# Streamlit UI
st.title('Amadeus API Chatbot')

# Session state to hold the conversation
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Input form
with st.form(key='chat_form', clear_on_submit=True):
    user_input = st.text_input('You: ', '')
    submit_button = st.form_submit_button(label='Send')

# Process the user input
if submit_button and user_input:
    st.session_state.messages.append({'role': 'user', 'content': user_input})

    # Simulate chatbot response
    if user_input.lower().startswith('check request'):
        # Extract request details from the user input
        request_data = {
            'endpoint': '/v1/reference-data/locations/airports',  # Example endpoint
            'params': {'subType': 'CITY', 'keyword': 'LON'}  # Example parameters
        }
        response_data = check_amadeus_api(request_data)
        st.session_state.messages.append({'role': 'system', 'content': f'Request: {request_data}\nResponse: {response_data}'})
    elif user_input.lower().startswith('check issues'):
        # Extract request and response details from the conversation
        request_data = "Sample request data"
        response_data = "Sample response data"
        issues = check_vector_store(request_data, response_data)
        st.session_state.messages.append({'role': 'system', 'content': f'Issues found: {issues}'})
    else:
        st.session_state.messages.append({'role': 'system', 'content': "I'm sorry, I didn't understand that. Try 'check request' or 'check issues'."})

# Display the conversation
for message in st.session_state.messages:
    if message['role'] == 'user':
        st.write(f"**You**: {message['content']}")
    else:
        st.write(f"**Bot**: {message['content']}")