import os
import subprocess

def create_pdf_from_file(file_path, output_filename='output'):
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' does not exist.")
        return

    base_name, ext = os.path.splitext(file_path)
    tex_file = f"{base_name}.tex" if ext.lower() != '.tex' else file_path

    if file_path != tex_file:
        with open(file_path, 'r', encoding='utf-8') as input_file:
            latex_code = input_file.read()
        with open(tex_file, 'w', encoding='utf-8') as output_file:
            output_file.write(latex_code)
        print(f"Created temporary .tex file: {tex_file}")
    else:
        tex_file = file_path

    try:
        result = subprocess.run(
            ['pdflatex', '-interaction=nonstopmode', tex_file],
            check=True,
            capture_output=True,
            text=True
        )
        print(f"PDF generated: {output_filename}.pdf")
        print("Compilation output:")
        print(result.stdout)
        
        for ext in ['.aux', '.log']:
            aux_file = f"{base_name}{ext}"
            if os.path.exists(aux_file):
                os.remove(aux_file)
                print(f"Removed auxiliary file: {aux_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error during PDF generation: {e}")
        print("pdflatex error output:")
        print(e.output)
    except FileNotFoundError:
        print("Error: pdflatex not found. Ensure MiKTeX or another LaTeX distribution is installed and added to PATH.")

if __name__ == "__main__":
    latex_file_path = 'latex.txt'
    output_name = 'Devansh_Vora_Resume'
    
    create_pdf_from_file(latex_file_path, output_name)