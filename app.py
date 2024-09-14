import os
import streamlit as st
from dotenv import load_dotenv
load_dotenv() ##load all the environment variables
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
prompt = """Youtube video summarizer. Summarize the entire video and provide the important summary in points within 250 words. Please generate the summary"""

#Functionality
def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = ""
        for i in transcript_text:
            transcript+=" "+i["text"]
        return transcript
    except Exception as e:
        raise e


def generate_gemini_content(transcript,prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt+transcript_text)
    return response.text


#UI(Streamlit)
st.title("YouTube Transcript Summarizer")
youtube_link = st.text_input("Enter YouTube video Link:")

if youtube_link:
    video_id = youtube_link.split("=")[1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width = True)

if(st.button("Summarize")):
    transcript_text = extract_transcript_details(youtube_link)
    if(transcript_text):
        summary = generate_gemini_content(transcript_text,prompt)
        st.markdown('Summary: ')
        st.write(summary)