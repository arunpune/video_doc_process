import streamlit as st
import os
from dotenv import load_dotenv
import time
from doc_processing import process_video  # Import the processing function
hide_github_icon = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.css-1v3fvcr {visibility: hidden;}
</style>
"""

# Inject custom CSS
st.markdown(hide_github_icon, unsafe_allow_html=True)
load_dotenv()

def save_uploaded_file(uploaded_file, save_path):
    """Save uploaded file to disk."""
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return save_path

def main():
    st.title("Video to Word and DrawIO Converter")

    uploaded_file = st.file_uploader("Upload a video file", type=["mp4", "avi", "mov", "mkv"])

    if "word_file" not in st.session_state:
        st.session_state.word_file = None
    if "drawio_file" not in st.session_state:
        st.session_state.drawio_file = None

    if uploaded_file is not None:
        save_path = os.path.join("temp_videos", uploaded_file.name)
        os.makedirs("temp_videos", exist_ok=True)

        if st.button("Upload and Process"):
            st.info("Processing... Please wait.")
            save_uploaded_file(uploaded_file, save_path)

            try:
                word_file, drawio_file = process_video(save_path)
                time.sleep(2)  # Wait to ensure files are fully written

                if word_file and os.path.exists(word_file) and drawio_file and os.path.exists(drawio_file):
                    st.success("Processing completed successfully!")

                    # Store file paths in session state
                    st.session_state.word_file = word_file
                    st.session_state.drawio_file = drawio_file

            except Exception as e:
                st.error(f"Error: {str(e)}")

    # Show download buttons only if files exist in session state
    if st.session_state.word_file:
        st.subheader("Word File")
        with open(st.session_state.word_file, "rb") as wf:
            st.download_button("Download Word File", data=wf, file_name=os.path.basename(st.session_state.word_file))

    if st.session_state.drawio_file:
        st.subheader("DrawIO File")
        with open(st.session_state.drawio_file, "rb") as df:
            st.download_button("Download DrawIO File", data=df, file_name=os.path.basename(st.session_state.drawio_file))

if __name__ == "__main__":
    main()
