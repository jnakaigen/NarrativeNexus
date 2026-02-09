#task3 -Docling-based Document Parser
import os
from docling.document_converter import DocumentConverter
class DocumentParser:
    def __init__(self):
        # Expanded list of formats supported by Docling
        self.supported_formats = [
            '.pdf', '.docx', '.pptx', '.html', '.xhtml', '.xml', 
            '.jpg', '.jpeg', '.png', '.bmp'
        ]
        self.converter = DocumentConverter()

    def convert_to_text(self, input_path, output_dir="processed_data"):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        _, ext = os.path.splitext(input_path)
        
        # simple validation to ensure we only try to parse supported files
        if ext.lower() not in self.supported_formats:
            print(f"Skipping {input_path}: Unsupported format {ext}")
            return None

        filename = os.path.basename(input_path)
        output_filename = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}.md")

        try:
            print(f"Processing: {filename}...")
            
            # The 'convert' method automatically detects the format (PDF, PPTX, HTML, etc.)
            result = self.converter.convert(input_path)
            
            # export_to_markdown preserves layout (tables/headers) better than raw text
            extracted_text = result.document.export_to_markdown()

            with open(output_filename, "w", encoding="utf-8") as f:
                f.write(extracted_text)
            
            return output_filename

        except Exception as e:
            print(f"Error converting {filename}: {str(e)}")
            return None

if __name__ == "__main__":
    parser = DocumentParser()
    
    # Define your input folder
    input_folder = "assets"
    

    if os.path.exists(input_folder):
        files_to_process = os.listdir(input_folder)
        
        print(f"Found {len(files_to_process)} files in '{input_folder}'...")
        
        for filename in files_to_process:

            file_path = os.path.join(input_folder, filename)

            if os.path.isfile(file_path):
                output_file = parser.convert_to_text(file_path)
                if output_file:
                    print(f"  -> Saved to: {output_file}")
    else:
        print(f"ERROR: The folder '{input_folder}' does not exist.")

  