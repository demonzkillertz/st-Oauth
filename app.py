import streamlit as st
from streamlit_oauth import OAuth2Component
import json
import os

# OAuth configuration for Google
CLIENT_ID = st.secrets["google"]["client_id"]
CLIENT_SECRET = st.secrets["google"]["client_secret"]
REDIRECT_URI = os.getenv("REDIRECT_URI", "https://your-app-name.streamlit.app")
AUTHORIZE_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"
SCOPE = "openid email profile"

# Initialize OAuth2Component
oauth2 = OAuth2Component(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    authorize_endpoint=AUTHORIZE_URL,
    token_endpoint=TOKEN_URL,
    userinfo_endpoint=USERINFO_URL,
    redirect_uri=REDIRECT_URI
)

def main():
    st.title("Google OAuth Sign-In App")

    # Check if user is already authenticated
    if "token" not in st.session_state:
        # Display sign-in button
        result = oauth2.authorize_button(
            name="Sign in with Google",
            icon="https://www.google.com/favicon.ico",
            scope=SCOPE,
            button_type="standard",
            button_css={"width": "200px", "padding": "10px"}
        )

        if result:
            # Store token in session state
            st.session_state["token"] = result["token"]
            st.rerun()

    # If user is authenticated, display user info
    if "token" in st.session_state:
        token = st.session_state["token"]
        # Fetch user info
        headers = {"Authorization": f"Bearer {token['access_token']}"}
        user_info = oauth2.get_userinfo(headers=headers)
        
        st.subheader("Signed In Account")
        st.write(f"**Name**: {user_info.get('name', 'N/A')}")
        st.write(f"**Email**: {user_info.get('email', 'N/A')}")
        
        # Display user avatar if available
        if user_info.get("picture"):
            st.image(user_info["picture"], width=100)
        
        # Sign out button
        if st.button("Sign Out"):
            del st.session_state["token"]
            st.rerun()

if __name__ == "__main__":
    main()