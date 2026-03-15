import streamlit as st
import yt_dlp
import google.generativeai as genai

# --- CONFIG ---
# Ensure your API key is correct here
API_KEY = "AIzaSyC9z7iyS-k6t91tSJUmYlqcnYpJX8_Zvp4"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="ClipViral.ai", page_icon="🚀")

st.title("🚀 ClipViral.ai")
st.subheader("YouTube to Viral Shorts in Seconds")

url = st.text_input("Paste YouTube URL:", placeholder="https://www.youtube.com/watch?v=...")

def get_video_data(url):
    ydl_opts = {'quiet': True, 'no_warnings': True, 'skip_download': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        # We grab everything YouTube doesn't block: Title, Desc, Tags, Category
        return {
            "title": info.get('title'),
            "description": info.get('description')[:2000],
            "tags": info.get('tags'),
            "duration": info.get('duration')
        }

if st.button("Generate Viral Clips ✨"):
    if url:
        try:
            with st.spinner("Analyzing video structure..."):
                data = get_video_data(url)
                
                # We tell the AI to use the description to 'predict' the best parts
                prompt = f"""
                Video Title: {data['title']}
                Description: {data['description']}
                Duration: {data['duration']} seconds
                
                Based on the title and description, identify 5 segments that are likely to be viral 'Shorts'.
                For each segment:
                1. Give it a Viral Hook (e.g., 'The truth about...')
                2. Suggest a timestamp range (e.g., 01:20 - 01:50) based on the topics in the description.
                3. Write a high-retention caption.
                4. Provide 5 trending hashtags.
                """
                
                response = model.generate_content(prompt)
                st.success("Viral Roadmap Generated!")
                st.markdown(response.text)
                
                st.divider()
                st.info("Want the AI to actually cut the video for you? Join our Pro Waitlist.")
                st.link_button("🚀 Get Pro Version ($9)", "https://www.buymeacoffee.com/YOUR_LINK")
                
        except Exception as e:
            st.error("This video is restricted. Please try another link!")
    else:
        st.warning("Please enter a URL first.")
