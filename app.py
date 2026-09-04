import streamlit as st
from openai import OpenAI
import os

# --- Page setup ---
st.set_page_config(page_title="AI Content Assistant", page_icon="✍️")
st.title("✍️ AI Content Assistant")
st.markdown("Generate tailored posts for any platform, audience, and tone.")

# --- Sidebar: User inputs ---
with st.sidebar:
    st.header("Content Parameters")
    content_type = st.selectbox(
        "Content Type",
        ["Blog Post", "Social Media Post", "Article", "Email", "Ad Copy"]
    )
    platform = st.selectbox(
        "Platform",
        ["LinkedIn", "Twitter", "Instagram", "Facebook", "Blog"]
    )
    topic = st.text_input("Topic", placeholder="e.g., AI in healthcare")
    target_audience = st.text_input(
        "Target Audience", placeholder="e.g., healthcare professionals"
    )
    tone = st.selectbox(
        "Tone",
        ["Professional", "Casual", "Humorous", "Inspirational", "Formal"]
    )
    generate_button = st.button("🚀 Generate Content")

# --- Main area ---
if generate_button:
    if not topic:
        st.warning("Please enter a topic.")
    else:
        # --- Read all configuration from secrets / environment ---
        api_key = st.secrets.get("API_KEY") or os.getenv("API_KEY")
        base_url = st.secrets.get("BASE_URL") or os.getenv(
            "BASE_URL", "https://api.groq.com/openai/v1")
        model = st.secrets.get("MODEL") or os.getenv(
            "MODEL", "llama-3.3-70b-versatile")

        if not api_key:
            st.error(
                "API key not found. "
                "Please set it in Streamlit secrets or as an environment variable."
            )
        else:
            with st.spinner("Crafting your content..."):
                try:
                    # --- Initialize the client (works with DeepSeek, Groq, OpenAI, etc.) ---
                    client = OpenAI(api_key=api_key, base_url=base_url)

                    # --- Build the prompt ---
                    prompt = f"""
Generate a {content_type} for {platform} on the topic: "{topic}".
Target audience: {target_audience}.
Tone: {tone}.

Provide the full content with:
- A compelling caption/headline
- The main body
- A set of relevant hashtags

Format the output clearly with these sections.
"""

                    # --- Call the API ---
                    response = client.chat.completions.create(
                        model=model,
                        messages=[
                            {"role": "system",
                                "content": "You are an expert content creator."},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.7,
                        max_tokens=800
                    )

                    content = response.choices[0].message.content
                    st.markdown("### ✨ Generated Content")
                    st.write(content)

                except Exception as e:
                    st.error(f"An error occurred: {e}")
