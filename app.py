import streamlit as st
import os
from dotenv import load_dotenv
import time
load_dotenv()
from doc_processing import process_video  # Import the processing function

def save_uploaded_file(uploaded_file, save_path):
    """Save uploaded file to disk."""
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return save_path

st.markdown(
        """
        <style>
         /* Background image */
        .stApp {
            background-image: url('https://wallpaperaccess.com/full/1398314.jpg'); /* Replace with your background image URL */
            background-size: cover;
            background-attachment: fixed;
            background-position: center;
            color: white;
        }
        /* Informational section styling */
        .info-section {
            background-color: rgba(0, 0, 0, 0.7);
            color: white;
            padding: 15px;
            border-radius: 10px;
            margin-top: 20px;
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.5);
        }

        .info-section h3 {
            color: #ffcc00;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def main():
    st.title("Video to Word and DrawIO Converter")

    uploaded_file = st.file_uploader("Upload a video file", type=["mp4", "avi", "mov", "mkv"])

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
                    
                    # Download Word file
                    st.subheader("Word File")
                    with open(word_file, "rb") as wf:
                        st.download_button("Download Word File", data=wf, file_name=os.path.basename(word_file))
                    
                    # Download DrawIO file
                    st.subheader("DrawIO File")
                    with open(drawio_file, "rb") as df:
                        st.download_button("Download DrawIO File", data=df, file_name=os.path.basename(drawio_file))
                else:
                    st.error("Failed to generate files. One or more files do not exist.")
            except Exception as e:
                st.error(f"Error: {str(e)}")
                
# Informational section
    st.markdown(
        """
        <br>
        <div class="info-section">
            <h3>What is Video Processor Tool?</h3>
            <p>The Video Processor is an advanced tool designed to extract and structure visual data from videos into Word and Draw.io formats. By leveraging artificial intelligence and machine learning, this system enables users to analyze video content efficiently and generate structured representations of the extracted information.</p>
            <p>The Video Processor provides an intuitive and automated approach to handling visual data, making it an essential tool for content analysis, documentation, and knowledge extraction from video sources.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

if __name__ == "__main__":
    main()
