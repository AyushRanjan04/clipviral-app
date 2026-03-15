import streamlit as st
import google.generativeai as genai

# --- CONFIG ---
API_KEY = "AIzaSyC9z7iyS-k6t91tSJUmYlqcnYpJX8_Zvp4"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="ClipViral.ai", page_icon="🚀")

st.title("🚀 ClipViral.ai")
st.markdown("### The Instant Viral Script Generator")

# Instructions for the user (The 'Manual' part that makes it professional)
with st.expander("👉 How to get your transcript (Free & Fast)"):
    st.write("1. Open your video on YouTube.")
    st.write("2. Click '... More' under the video and select 'Show Transcript'.")
    st.write("3. Copy the text and paste it below!")

# The Input Box
transcript_input = st.text_area("Paste your Video Transcript here:", height=300, placeholder="Paste the text here...")

if st.button("Generate 5 Viral Clips ✨"):
    if transcript_input:
        with st.spinner("Analyzing for viral potential..."):
            prompt = f"""
            Act as a Viral Content Strategist. Analyze this transcript and give me 5 specific segments for TikTok/Reels:
            1. A 'Scroll-Stopping' Hook.
            2. The exact text/topic from the transcript for the clip.
            3. A caption with 5 trending hashtags.
            
            Transcript: {transcript_input[:15000]}
            """
            response = model.generate_content(prompt)
            st.success("Your Viral Roadmap is Ready!")
            st.markdown(response.text)
            
            st.divider()
            # YOUR REVENUE LINK
            st.link_button("☕ Support the Tool & Get Pro ($9)", "https://www.buymeacoffee.com/YOUR_LINK")
    else:
        st.warning("Please paste a transcript first!")

st.sidebar.write("Built for Creators by ClipViral.ai")
