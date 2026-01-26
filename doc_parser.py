import os
import fitz  # PyMuPDF (Assuming this won your evaluation)
from docx import Document

class DocumentParser:
    def __init__(self):
        self.supported_formats = ['.pdf', '.docx']

    def _parse_pdf(self, file_path):
        """Extracts text from PDF using PyMuPDF."""
        text_content = []
        try:
            with fitz.open(file_path) as doc:
                for page in doc:
                    text_content.append(page.get_text())
            return "\n".join(text_content)
        except Exception as e:
            return f"Error reading PDF: {str(e)}"

    def _parse_docx(self, file_path):
        """Extracts text from DOCX using python-docx."""
        try:
            doc = Document(file_path)
            # Joining with newlines to preserve paragraph structure
            return "\n".join([para.text for para in doc.paragraphs])
        except Exception as e:
            return f"Error reading DOCX: {str(e)}"

    def convert_to_text(self, input_path, output_dir="processed_data"):
        """Main function to process input and export to .txt"""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        _, ext = os.path.splitext(input_path)
        filename = os.path.basename(input_path)
        output_filename = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}.txt")

        if ext.lower() == ".pdf":
            extracted_text = self._parse_pdf(input_path)
        elif ext.lower() == ".docx":
            extracted_text = self._parse_docx(input_path)
        else:
            raise ValueError(f"Unsupported format: {ext}")

        # Exporting to .txt as per requirements
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(extracted_text)
        
        return output_filename

if __name__ == "__main__":
    parser = DocumentParser()
    
    # These are the exact names of the 3 files you have in your folder
    files_to_process = [
        "sample1.pdf", 
        "sample2.pdf", 
        "sample3.pdf"
    ]
    
    print("Starting conversion...")
    for filename in files_to_process:
        if os.path.exists(filename):
            output_file = parser.convert_to_text(filename)
            print(f"Successfully converted: {filename} -> {output_file}")
        else:
            print(f"ERROR: Could not find file: {filename}")