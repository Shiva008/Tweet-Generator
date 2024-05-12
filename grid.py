import streamlit as st
import requests
from dotenv import load_dotenv
import google.generativeai as genai
import assemblyai as aai
import os

load_dotenv()  # Load all the environment variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")

def get_space_info(space_id):
    """Fetches information about a Twitter Space using the given ID."""
    bearer_token = "RDNJLWV1TF83cS1RdkVSalE3MDVXbG5seHFVbWxBRmRQYVFNZi03YTlScEhHOjE3MTU1MTIyNDc1MTM6MToxOmF0OjE"  # Replace with your actual bearer token
    headers = {"Authorization": f"Bearer {bearer_token}"}
    url = f"https://api.twitter.com/2/spaces/{space_id}?space.fields=speaker_ids&expansions=speaker_ids&user.fields=id&topic.fields=name"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

# Streamlit app
st.title("Gemini Tweet Generator")

# Create a three-grid layout with full width
col1, col2, col3 = st.columns([1, 1, 1])

# First column for uploading ID and MP3 file
with st.sidebar:
    st.header("Upload Twitter Space ID and MP3 File")
    space_id = st.text_input("Enter the Twitter Space ID:")
    uploaded_file = st.file_uploader("Upload MP3 File", type=['mp3'])
    import tweepy
    import streamlit as st

    # Set up Tweepy credentials
    api_key = "jJeS41eHo34bZTteXKVdKqmQh"
    api_secret = "FbDkSj6oqmTxAiKlWCwyKAUExxZC7zgJNvavBuv176KoYzwogf"
    bearer_token = "AAAAAAAAAAAAAAAAAAAAAPzYtgEAAAAA2oBpWBkwLqVscTYQAvMtfUr1U4Y%3D0osLE0jyPGiMGoXYkK2SHUraXia8KE7sPG7vfNo5z9d4vuvlhb"
    access_token = "1788286387956899840-UODtBVnzsotXMRLkoQEyb1NB0KDX3s"
    access_token_secret = "9kQuz1JxZdaAQM5zJrSgjtrBez74UxZmXTbHFxqONY9dH"

    # Initialize Tweepy Client
    client = tweepy.Client(bearer_token, api_key, api_secret, access_token, access_token_secret)

    # Streamlit UI
    st.title("Tweet with Tweepy")

    # Input box for tweet text
    tweet_text = st.text_area("Enter your tweet:")

    # Tweet button
    if st.button("Tweet"):
        if tweet_text:
            try:                  
                tweet = client.create_tweet(text=tweet_text)
                st.success("Tweet posted successfully!")
            except tweepy.TweepError as e:
                st.error(f"Error posting tweet: {e}")
        else:
            st.warning("Please enter some text for your tweet.")
# Second column for summary and tweet generation

if uploaded_file is not None and space_id:
    with open(uploaded_file.name, "wb") as f:
        f.write(uploaded_file.getbuffer())
    FILE_URL = uploaded_file.name
    space_info = get_space_info(space_id)
    if space_info:
        try:
            usernames = [user['username'] for user in space_info['includes']['users']]
        except:
            st.error("Invalid Space ID")
        config = aai.TranscriptionConfig(speaker_labels=True)
        transcriber = aai.Transcriber()
        try:
            transcript = transcriber.transcribe(FILE_URL, config=config)
            transcript_text = "\n".join([f"Speaker {utterance.speaker}: {utterance.text}" for utterance in transcript.utterances])
            prompt = f"""you are expert conversation summarizer and tweet writer. 
            You will be taking the transcript text and summarizing the entire conversation and providing the important summary 
            and with the help of it write the tweet. tag the usernames from {usernames} in the tweet.
            Also give the tags to trend it. make different tweets for all the speakers on what they said.
            Please provide the tweet here: """
            model = genai.GenerativeModel("gemini-pro")
            response = model.generate_content(prompt + transcript_text)
            gemini_summary = response.text
            st.header("Gemini Summary:")
            st.write(gemini_summary)
        except requests.exceptions.HTTPError as e:
            st.write(f"HTTP Error: {e.response.status_code} - {e.response.data}")
    else:
        st.write("Error fetching Twitter Space information.")
else:
    st.write("Please upload an MP3 file and enter the Twitter Space ID.")

# # Third column (empty)
# with col3:
#     st.write("hjir")
