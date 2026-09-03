import os
import json
import streamlit as st
from groq import Groq

# ----------------------------
# Page setup
# ----------------------------
st.set_page_config(page_title="AI Content Assistant", page_icon="✨", layout="centered")
st.title("✨ AI Content Assistant")
st.caption("Generate a ready-to-post caption + hashtags in seconds.")

# ----------------------------
# Groq API key handling
# Priority: Streamlit secrets -> environment variable -> manual sidebar input
# ----------------------------
api_key = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY", ""))

with st.sidebar:
    st.header("Settings")
    if not api_key:
        api_key = st.text_input("Groq API Key", type="password",
                                 help="Get a free key at console.groq.com")
    st.markdown("[Get a free Groq API key](https://console.groq.com/keys)")
    model = st.selectbox(
        "Model",
        ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"],
        help="Free Groq models. Check console.groq.com/docs/models for the latest list."
    )

# ----------------------------
# Content form
# ----------------------------
content_type = st.selectbox(
    "Content Type",
    ["Social Media Post", "Product Description", "Blog Intro", "Ad Copy", "Email Newsletter"]
)
platform = st.selectbox(
    "Platform",
    ["Instagram", "Twitter / X", "LinkedIn", "Facebook", "TikTok", "YouTube", "General / Website"]
)
topic = st.text_input("Topic", placeholder="e.g. Launching our new eco-friendly water bottle")
target_audience = st.text_input("Target Audience", placeholder="e.g. Young professionals who care about sustainability")
tone = st.selectbox(
    "Tone",
    ["Professional", "Casual", "Funny", "Inspirational", "Persuasive", "Informative"]
)

generate = st.button("Generate Content", type="primary", use_container_width=True)

# ----------------------------
# Generation logic
# ----------------------------
def build_prompt():
    return f"""You are a social media copywriter. Create content with these details:

- Content type: {content_type}
- Platform: {platform}
- Topic: {topic}
- Target audience: {target_audience}
- Tone: {tone}

Respond ONLY with valid JSON in this exact format, no extra text:
{{
  "caption": "the full post caption/copy, written for the platform above",
  "hashtags": ["#tag1", "#tag2", "#tag3"]
}}
Include 8-12 relevant, specific hashtags."""


def generate_content():
    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": build_prompt()}],
        temperature=0.8,
    )
    raw = response.choices[0].message.content.strip()
    # Models sometimes wrap JSON in code fences - strip those if present
    raw = raw.replace("```json", "").replace("```", "").strip()
    return json.loads(raw)


if generate:
    if not api_key:
        st.error("Please add your Groq API key in the sidebar first.")
    elif not topic:
        st.error("Please enter a topic.")
    else:
        with st.spinner("Generating your content..."):
            try:
                result = generate_content()
                st.subheader("📝 Caption")
                st.text_area("Caption", value=result["caption"], height=180, label_visibility="collapsed")

                st.subheader("🏷️ Hashtags")
                hashtags_str = " ".join(result["hashtags"])
                st.text_area("Hashtags", value=hashtags_str, height=100, label_visibility="collapsed")

                st.success("Done! Copy the text above from the boxes.")
            except json.JSONDecodeError:
                st.error("The model returned an unexpected format. Please try again.")
            except Exception as e:
                st.error(f"Something went wrong: {e}")
