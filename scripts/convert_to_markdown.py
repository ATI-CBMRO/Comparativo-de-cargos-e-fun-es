import os
from pypdf import PdfReader

# Define paths in the workspace
workspace_dir = r"C:\Users\tiago\OneDrive\Documentos\Comparativo de legislações CBM"
pdf_dir = os.path.join(workspace_dir, "LEGISLAÇÃO CBMS")
output_dir = os.path.join(workspace_dir, "database", "markdown")

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

def clean_text(text):
    if not text:
        return ""
    # Standardize line endings and clean consecutive spaces
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    return text

def convert_pdf_to_markdown(pdf_path, md_path):
    try:
        reader = PdfReader(pdf_path)
        filename = os.path.basename(pdf_path)
        title = filename.replace(".pdf", "")
        
        md_content = f"# {title}\n\n"
        md_content += f"*Documento extraído de: `{filename}`*\n"
        md_content += f"*Total de páginas: {len(reader.pages)}*\n\n---\n\n"
        
        for idx, page in enumerate(reader.pages):
            page_num = idx + 1
            page_text = page.extract_text() or ""
            page_text = clean_text(page_text)
            
            md_content += f"## Página {page_num}\n\n"
            if page_text.strip():
                md_content += page_text + "\n\n"
            else:
                md_content += "*[Página sem texto digital ou escaneada]*\n\n"
            md_content += "---\n\n"
            
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(md_content)
        
        print(f"Successfully converted: {filename} -> {os.path.basename(md_path)}")
        return True
    except Exception as e:
        print(f"Error converting {pdf_path}: {e}")
        return False

def main():
    print(f"Scanning PDF files in: {pdf_dir}")
    if not os.path.exists(pdf_dir):
        print(f"Error: Directory {pdf_dir} does not exist.")
        return
        
    files = [f for f in os.listdir(pdf_dir) if f.endswith(".pdf")]
    print(f"Found {len(files)} PDF files to process.")
    
    success_count = 0
    for filename in files:
        pdf_path = os.path.join(pdf_dir, filename)
        # Keep spaces in the filename, replacing only .pdf with .md
        clean_name = filename.replace(".pdf", ".md")
        md_path = os.path.join(output_dir, clean_name)
        
        if convert_pdf_to_markdown(pdf_path, md_path):
            success_count += 1
            
    print(f"\nProcessing complete: {success_count}/{len(files)} files successfully converted.")

if __name__ == "__main__":
    main()
