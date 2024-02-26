import streamlit as st
# import os
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

# Login Page
def login_page():
    st.header("Login Page")
    with st.form("Login Form", clear_on_submit=True):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        # Login button
        submit_button = st.form_submit_button("Login")

        if submit_button:
            if authenticate(username, password):
                st.success(f"Welcome '{username}', You are successfully logged in!")
                st.session_state['authenticated'] = True
            else:
                st.error("The username or password you have entered is incorrect.")

# Main Page
def main_page():

    st.sidebar.write(f"User: \'{st.session_state['username']}\'")
    if st.sidebar.button("Logout"):
        st.session_state['authenticated'] = False
        st.experimental_rerun()

    

    global query
    query = st.text_area("Enter query here.. 👇🏻", key='question')

    submit = st.button("Get Answer")

    if submit:
        if query:
            # get similar docs
            with st.spinner("Generating Response"):
                response = generate_response_rag(query)
                st.write(response)
            # st.success("How was that?")
        else:
            st.error("Provide the document first")

def main():

    st.title("BimaMitra Chatbot")

    # Use session state to keep track of authentication status
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False
        st.session_state['username'] = None

    if not st.session_state['authenticated']:
        login_page()
    else:
        main_page()

if __name__ == "__main__":
    main()
