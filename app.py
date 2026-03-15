import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai
import re

# Page Config
st.set_page_config(page_title="ClipViral.ai", page_icon="🚀")

# --- CUSTOMIZE THIS ---
# Paste your API Key here inside the quotes
API_KEY = "AIzaSyC9z7iyS-k6t91tSJUmYlqcnYpJX8_Zvp4"
# ----------------------

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def get_video_id(url):
    pattern = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
    match = re.search(pattern, url)
    return match.group(1) if match else None

st.title("🚀 ClipViral.ai")
st.subheader("Turn YouTube Links into 5 Viral Shorts (Ideas & Captions)")
st.write("Stop wasting hours re-watching your videos. Let AI find the gold.")

url = st.text_input("Paste YouTube URL here:", placeholder="https://www.youtube.com/watch?v=...")

if st.button("Generate Viral Clips ✨"):
    if url:
        try:
            with st.spinner("Analyzing video transcript..."):
                video_id = get_video_id(url)
                transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
                transcript_text = " ".join([i['text'] for i in transcript_list])

                prompt = f"""
                Analyze this YouTube transcript and identify 5 high-impact segments that would make great TikToks/Reels.
                For each segment, provide:
                1. A catchy 'Viral Hook' for the caption.
                2. Approximate timestamps (e.g., 02:15 - 03:00).
                3. A brief explanation of why this part is 'clip-worthy'.
                4. 5 trending hashtags.
                
                Transcript: {transcript_text[:10000]} 
                """
                
                response = model.generate_content(prompt)
                
                st.success("Analysis Complete!")
                st.markdown(response.text)
                
                st.divider()
                st.info("💡 Want auto-generated video clips? Upgrade to Pro for $9/mo.")
                if st.button("Join Pro Waitlist"):
                    st.balloons()
                    st.write("Thanks! We'll notify you when the auto-editor is ready.")
        
        except Exception as e:
            st.error(f"Error: {e}. Make sure the video has Captions/Subtitles enabled!")
    else:
        st.warning("Please enter a valid URL.")

st.sidebar.markdown("### How it works")
st.sidebar.write("1. Paste a Link\n2. Get 5 Viral Ideas\n3. Record/Clip & Post!")
