import streamlit as st
import os
from utils import *

# Function to simulate user authentication using environment variable
def authenticate(username, password):
    # Fetch the user list from the environment variable, handling spaces and newlines
    user_list_env = os.getenv("USER_LIST", "")  # Default to empty string if not set
    users = [u.strip().split(":") for u in user_list_env.split(",") if u.strip()]

    # Check if the provided credentials match any user in the list
    for user, pwd in users:
        if username == user.strip() and password == pwd.strip():
            st.session_state['username']=username
            return True
    return False

# Main app
def main():
    # Use session state to keep track of authentication status
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False
        st.session_state['username']=False

    # Sidebar for login/logout
    with st.sidebar:
        if not st.session_state['authenticated']:
            st.title("Login Page")

            with st.form("Login Form", clear_on_submit=True):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                
                # Login button
                submit_button = st.form_submit_button("Login")

                if submit_button:
                    st.session_state['authenticated'] = authenticate(username, password)
                    if st.session_state['authenticated']:
                        st.success(f"Welcome \'{username}\', You are successfully logged in!")
                    else:
                        st.error("The username or password you have entered is incorrect.")

        if st.session_state['authenticated']:
            st.write(f"User: {st.session_state['username']}")
            if st.button("Logout"):
                st.session_state['authenticated'] = False
                st.experimental_rerun()

    # Content to show after login
    if st.session_state['authenticated']:
        # st.title("Welcome to the app!")
        st.title("BimaMitra Chatbot")    

        global query
        query = st.text_area("Enter query here.. 👇🏻", key='question')

        submit = st.button("Get Answer")

        if submit:
            if query:
                
                # get similar docs
                with st.spinner("Generating Response"):
                    response = generate_response_rag(query)
                    st.write(response)
                st.success("How was that?")
                
            
            else:
                st.error("You gotta be kidding me.. I really wish I could read your mind")
        elif submit:
            st.error("Provide the document first")

if __name__ == "__main__":
    main()
