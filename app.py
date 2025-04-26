import streamlit as st
import ollama
from PIL import Image
import io
import base64

# Set the page configuration
st.set_page_config(
    page_title="OCR Program using Gemma3",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Set the title and description of the app
st.title("OCR Program using Gemma3")

# Add clear button to top right
col1, col2 = st.columns([6, 1])
with col2:
    if st.button("Clear"):
        if 'ocr_result' in st.session_state:
            del st.session_state['ocr_result']
        st._rerun()

st.markdown('Extract structured data from images using Gemma3.')
st.markdown("------")

# Move upload controls to sidebar
with st.sidebar:
    st.header("Upload Image")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        # Read the image file and display it
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image', use_column_width=True)
        
        if st.button("Extract Text", type="primary"):
            with st.spinner("Processing..."):
                try:
                    # Convert image to base64
                    buffered = io.BytesIO()
                    image.save(buffered, format="PNG")
                    img_str = base64.b64encode(buffered.getvalue()).decode()
                    
                    # Make the API call
                    response = ollama.chat(
                        model="gemma3:12b",
                        messages=[{
                            "role": "user",
                            "content": """Analyze the text in the provided image. Extract all readable content
                                        and present it in a structured Markdown format that is clear, concise, 
                                        and well-organized. Ensure proper formatting (e.g., headings, lists, or
                                        code blocks) as necessary to represent the content effectively.""",
                            "images": [img_str]
                        }]
                    )
                    
                    if response and hasattr(response, 'message'):
                        st.session_state['ocr_result'] = response.message.content
                    else:
                        st.error("No response received from the model")
                        
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
                    st.info("Make sure Ollama is running and the gemma3:12b model is installed.")

# Main content for result
if 'ocr_result' in st.session_state:
    st.markdown(st.session_state['ocr_result'])
else:
    st.info("Upload an image to extract text and click 'Extract Text' to see the results.")

# Footer
st.markdown("---")
st.markdown("### Instructions")
st.markdown("""
1. Make sure Ollama is installed and running on your system
2. Install the gemma3:12b model using: `ollama pull gemma3:12b`
3. Upload an image containing text
4. Click 'Extract Text' to process the image
""")