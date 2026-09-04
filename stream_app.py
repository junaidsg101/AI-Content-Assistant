# app.py
import streamlit as st
from openai import OpenAI
import os

st.set_page_config(page_title="AI Content Assistant",
                   page_icon="✍️", layout="centered")

st.title("✍️ AI Content Assistant")
st.write("Generate tailored posts, captions, and hashtags .")

st.sidebar.header("Configuration")
api_key = st.secrets.get("API_KEY") or os.getenv("API_KEY")
base_url = st.secrets.get("BASE_URL") or os.getenv(
            "BASE_URL", "https://api.groq.com/openai/v1")
model = st.secrets.get("MODEL") or os.getenv(
            "MODEL", "llama-3.3-70b-versatile")
st.sidebar.markdown("[Get a free Groq API key](https://console.groq.com)")

with st.form("content_form"):
    col1, col2 = st.columns(2)
    with col1:
        content_type = st.selectbox("Content Type", [
                                    "Social Media Post", "Blog Post Intro", "Newsletter Snippet", "Ad Copy"])
        platform = st.selectbox(
            "Platform", ["LinkedIn", "Twitter / X", "Instagram", "Facebook"])
    with col2:
        tone = st.selectbox("Tone", ["Professional", "Casual & Friendly",
                            "Witty & Humorous", "Inspirational", "Authoritative"])
        target_audience = st.text_input(
            "Target Audience", placeholder="e.g., Tech founders, Marketers")

    topic = st.text_area(
        "Topic / Main Idea", placeholder="e.g., The benefits of using AI for daily productivity")

    submitted = st.form_submit_button("Generate Content")

if submitted:
    if not api_key:
        st.error("Please enter your  API Key in the sidebar.")
    elif not topic:
        st.error("Please enter a topic.")
    else:
        with st.spinner("Generating your content..."):
            try:
                client = OpenAI(api_key=api_key, base_url=base_url)
                prompt = f"""
                You are an expert content creator and copywriter. Generate a {content_type} for {platform} about the following topic.
                
                Topic: {topic}
                Target Audience: {target_audience if target_audience else 'General audience'}
                Tone: {tone}
                
                Requirements:
                - Engaging hook
                - Clear, concise body matching the tone and platform style
                - Relevant hashtags at the end
                """

                response = client.chat.completions.create(
                                        model=model,
                                        messages=[
                                            {"role": "system",
                                                "content": "You are an expert content creator."},
                                            {"role": "user", "content": prompt}
                                        ],
                                        temperature=0.7,
                                        max_tokens=1000
                                    )

                content = response.choices[0].message.content
                st.success("Content generated successfully!")
                st.markdown("### Generated Output")
                st.markdown(content)

            except Exception as e:
                st.error(f"An error occurred: {e}")
