import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai
import re

st.set_page_config(page_title="ClipViral.ai", page_icon="🚀")

# --- SETTINGS ---
# Use your same API Key here
API_KEY = "PASTE_YOUR_GOOGLE_API_KEY_HERE"

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("🚀 ClipViral.ai")
st.write("Turn any video content into 5 viral-ready Shorts/Reels.")

# Two ways to get content
tab1, tab2 = st.tabs(["YouTube Link", "Paste Transcript/Text"])

with tab1:
    url = st.text_input("YouTube URL:")
    if st.button("Generate from Link"):
        try:
            video_id = url.split("v=")[1].split("&")[0]
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            text = " ".join([i['text'] for i in transcript])
            
            with st.spinner("Finding viral moments..."):
                response = model.generate_content(f"Analyze this transcript and give me 5 viral short-form clip ideas with timestamps, hooks, and hashtags: {text[:10000]}")
                st.markdown(response.text)
        except Exception as e:
            st.error("YouTube blocked the automatic script. Use 'Tab 2' to paste the transcript manually!")

with tab2:
    manual_text = st.text_area("Paste the transcript or video text here:", height=300)
    if st.button("Generate from Text"):
        if manual_text:
            with st.spinner("Analyzing text..."):
                response = model.generate_content(f"Analyze this text and give me 5 viral short-form clip ideas, hooks, and hashtags: {manual_text[:10000]}")
                st.markdown(response.text)
                st.success("Done! Copy these to your notes.")
        else:
            st.warning("Please paste some text first.")

st.sidebar.info("Tip: To get a transcript from YouTube, click the '...' under a video > Show Transcript > Copy/Paste it here!")
