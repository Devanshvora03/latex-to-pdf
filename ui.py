import streamlit as st
import subprocess
from pathlib import Path
import shutil
import os

def create_pdf_from_file(file_content, output_filename='output'):
    temp_dir = Path("temp_latex")
    temp_dir.mkdir(exist_ok=True)
    
    tex_file = temp_dir / f"{output_filename}.tex"
    pdf_file = temp_dir / f"{output_filename}.pdf"
    
    tex_file = tex_file.absolute()
    pdf_file = pdf_file.absolute()
    
    with open(tex_file, 'w', encoding='utf-8', newline='\n') as f:
        f.write(file_content)
    
    try:
        # Run pdflatex twice and capture output
        for _ in range(2):
            process = subprocess.run(
                ['pdflatex', '-interaction=nonstopmode', str(tex_file)],
                capture_output=True,
                text=True,
                cwd=temp_dir
            )
            if process.returncode != 0:
                return None, False, f"pdflatex failed with error:\n{process.stderr}"
        
        if pdf_file.exists():
            with open(pdf_file, 'rb') as f:
                pdf_bytes = f.read()
            return pdf_bytes, True, "PDF generated successfully!"
        else:
            return None, False, "PDF generation failed: No PDF file produced. pdflatex output:\n" + process.stderr
    
    except FileNotFoundError:
        return None, False, "Error: pdflatex not found in environment."
    except Exception as e:
        return None, False, f"Error: {str(e)}"

def main():
    st.title("LaTeX to PDF Converter")
    
    uploaded_file = st.file_uploader("Upload LaTeX File", type=['tex', 'txt'])
    output_name = st.text_input("Output Filename", "document")
    
    if uploaded_file is not None:
        file_content = uploaded_file.getvalue().decode("utf-8")
        
        if st.button("Convert to PDF"):
            with st.spinner("Generating PDF..."):
                pdf_bytes, success, message = create_pdf_from_file(file_content, output_name)
                
                st.write(message)
                
                if success and pdf_bytes:
                    st.download_button(
                        label="Download PDF",
                        data=pdf_bytes,
                        file_name=f"{output_name}.pdf",
                        mime="application/pdf"
                    )

if __name__ == "__main__":
    main()