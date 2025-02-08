import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# System Prompt for Markdown Generation
MARKDOWN_PROMPT = """You are a professional expert plain text to markdown converter.
Generate a professional, well-structured GitHub README.md file from the given input text, explaining the content clearly and formatting it properly.

---

## **Task:**  
Convert the following text into a professional, **GitHub-optimized** README.md file with:  
✔ **Proper headings** (H1-H6) with relevant **emojis**   
✔ **Formatted lists** (ordered/unordered, checklists, nested, etc.)  
✔ **Bold, italic, and underlined text** for emphasis  
✔ **Syntax-highlighted code blocks** with correct language tags  
✔ **Organized sections** with clear formatting  
✔ **Modern and copy-friendly code snippets**   
✔ **Tables and blockquotes** where applicable  
✔ **Links and images** in proper Markdown format  
✔ **Cloning instructions with Git commands**  

---

## **📌 Input Text:**  
{user_input}

---

## **📜 README Structure Guidelines:**  
## Explain in professional way and generate a comperhensive markdown.
## Also add how to clone/use this project on github.
### 1️⃣ **Project Title & Overview**  
   - `#` Project Title (with an engaging **emoji**)  
   - Short, clear project introduction  
   - Badges (if applicable)  

### 2️⃣ **Features**  
   - **Bullet points** (✔ Feature 1, ✔ Feature 2...)  
   - **Highlight core functionalities**  

### 3️⃣ **Tech Stack**  
   - Use icons if applicable  
   - Clearly list frameworks, programming languages  

### 4️⃣ **Installation Guide**  
   - List **prerequisites**  
   - Provide **step-by-step installation**  
   - Use proper **code blocks** (`sh`, `python`, etc.)  

### 5️⃣ **How to Clone & Use This Project**  
   - Provide **GitHub repository link**  
   - Explain how to **clone the repo** using:  
     ```sh
     git clone <repo_url>
     cd <project_folder>
     ```
   - Steps to install dependencies:  
     ```sh
     pip install -r requirements.txt
     ```
   - Steps to run the project:  
     ```sh
     python main.py
     ```
   - Alternative methods if applicable (e.g., using **Docker, Conda, or virtual environments**)  

### 6️⃣ **Usage Instructions**  
   - Add **sample commands**  
   - Provide **screenshots or GIFs**  

### 7️⃣ **Project Structure (if applicable)**  
   - Explain folder structure  
   - Show example API calls or file hierarchy  

### 8️⃣ **Contributing**  
   - Provide clear **contribution guidelines**  
   - Add roadmap (if available)  

### 9️⃣ **License & Credits**  
   - Specify license type  
   - Give proper acknowledgments  

---

## **🚀 Additional Formatting Guidelines:**  
✔ Use **headings (`#`, `##`)** for sections  
✔ Include **emojis** to improve readability (🚀, 📌, 🔧, etc.)  
✔ Use **tables** for comparisons (if needed)  
✔ Ensure **clear, readable markdown syntax**  
✔ Highlight **important notes** using blockquotes `>`  
✔ Provide proper **code formatting** for shell, Python, etc.  
✔ Use **tabbed code sections** for multiple languages if necessary  

---

**💡 Output Only the Markdown File Without Extra Explanations**  
"""


# Streamlit UI Configuration
st.set_page_config(
    page_title="AI README Generator",
    page_icon="📄",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional look
st.markdown("""
<style>
.stTextInput>div>div>input {border-radius: 8px;}
.stSelectbox>div>div>div {border-radius: 8px;}
.code-block {padding: 15px; background: #f8f9fa; border-radius: 8px;}
</style>
""", unsafe_allow_html=True)

# Main Application Logic
def main():
    st.title("🤖 AI-Powered README Generator")
    st.subheader("Transform Plain Text to Professional Documentation")
    
    user_input = st.text_area(
    "📝 Enter your project description:", 
    height=200, 
    placeholder="""Briefly explain your project to generate a professional README file.
- What your project does and its main purpose.
- Key features and functionalities.
- Installation instructions and prerequisites.
- How to use the project, including example commands or scripts.
- A description of the project structure and important files.
This information will be used to generate a well-structured README for your project."""
)



    if st.button("✨ Generate README", use_container_width=True):
        with st.spinner("🔧 Crafting professional documentation..."):
            try:
                model = genai.GenerativeModel('gemini-pro')
                response = model.generate_content(MARKDOWN_PROMPT.format(user_input=user_input))
                markdown_output = response.text
                
                with st.expander("📄 Generated README Preview", expanded=True):
                    st.markdown(markdown_output)
                    
                st.success("✅ README generated successfully!")
                st.code(markdown_output, language="markdown", line_numbers=True)
                
                st.download_button(
                    label="📥 Download README.md",
                    data=markdown_output,
                    file_name="README.md",
                    mime="text/markdown"
                )
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main()
