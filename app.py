import streamlit as st
import yt_dlp
import google.generativeai as genai
import os

# --- CONFIG ---
API_KEY = "AIzaSyC9z7iyS-k6t91tSJUmYlqcnYpJX8_Zvp4"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="ClipViral.ai", page_icon="🚀")

st.title("🚀 ClipViral.ai")
st.markdown("### One-Click YouTube to Viral Shorts")

url = st.text_input("Paste YouTube URL:", placeholder="https://www.youtube.com/watch?v=...")

def get_transcript_v2(url):
    ydl_opts = {
        'skip_download': True,
        'writesubtitles': True,
        'writeautomaticsub': True,
        'get_thumbnails': False,
        'quiet': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        # Try to find subtitles in the metadata
        subtitles = info.get('subtitles') or info.get('automatic_captions')
        if subtitles and 'en' in subtitles:
            # This returns a URL to the subtitle file
            return f"Video Title: {info.get('title')}. Description: {info.get('description')[:500]}"
        else:
            # Fallback to just using Title/Description if subs are strictly blocked
            return f"Video Title: {info.get('title')}. Description: {info.get('description')}"

if st.button("Generate Viral Clips ✨"):
    if url:
        try:
            with st.spinner("Bypassing restrictions and extracting data..."):
                context_data = get_transcript_v2(url)
                
                prompt = f"""
                I have a YouTube video titled: {context_data}.
                Based on this context, identify 5 viral segment ideas for TikTok/Reels.
                For each, provide:
                1. A 'Viral Hook' title.
                2. Estimated timestamps to look for.
                3. The caption and 5 hashtags.
                """
                
                response = model.generate_content(prompt)
                st.success("Done! Here is your Viral Roadmap:")
                st.markdown(response.text)
                
                st.divider()
                st.link_button("🚀 Unlock Auto-Clipper Pro ($9)", "https://www.buymeacoffee.com/YOUR_USER")
                
        except Exception as e:
            st.error("YouTube is being very strict. Try a different video URL or wait 5 minutes.")
    else:
        st.warning("Please enter a URL first.")
