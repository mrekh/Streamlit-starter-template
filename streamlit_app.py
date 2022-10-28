"""A Streamlit app for getting the Google autocomplete queries
"""
import json

import requests
import streamlit as st
import streamlit_authenticator as stauth
import yaml


def google_autocomplete(keyword: str) -> list[str]:
    """Get Google autocomplete queries for a seed keyword

    Args:
        keyword (str): The seed keyword

    Returns:
        list[str]: A list of the autocomplete queries
    """
    google_autocomplete_api: str = "https://www.google.com/complete/search"
    google_autocomplete_params: dict = {
        "q": keyword,
        "cp": 8,
        "client": "gws-wiz",
        "xssi": "t",
        "hl": "en-US"
    }

    response = requests.get(google_autocomplete_api,
                            params=google_autocomplete_params)

    list_google_autocomplete_uncleaned: list[list] = json.loads(
        response.content.decode("UTF-8")[5:])[0]
    list_google_autocomplete_cleaned: list[str] = [
        element[0].replace("<b>", "").replace("</b>", "")
        for element in list_google_autocomplete_uncleaned
    ]

    return list_google_autocomplete_cleaned


# The Streamlit app
st.set_page_config(
    page_title="Oh My App!",
    page_icon="😎",
    layout="wide"
)

# The Streamlit app authentication section
with open("./config.yaml") as file:
    config = yaml.load(file, Loader=yaml.SafeLoader)

authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"],
    config["preauthorized"]
)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status:
    authenticator.logout('Logout', 'main')

    # The Streamlit app main section
    st.title("This is a next level SEO app")
    st.write("Make your ideas real.")

    input_google_autocomplete_keyword: str = st.text_input(
        "What is your seed keyword?")

    if input_google_autocomplete_keyword:
        output_list_google_autocomplete: list[str] = google_autocomplete(
            input_google_autocomplete_keyword)

        if output_list_google_autocomplete:
            st.download_button("Download the output",
                               "\n".join(output_list_google_autocomplete))

elif not authentication_status:
    st.error('Username/password is incorrect')
elif authentication_status is None:
    st.warning('Please enter your username and password')
