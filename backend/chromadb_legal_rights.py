import fitz  # PyMuPDF

# Load the PDF
doc = fitz.open("data/pdfs/constitution_of_india.pdf")

# Prepare text file for saving
output_path = "data/pdfs/legal_rights.txt"
with open(output_path, "w", encoding="utf-8") as f:
    for page in doc:
        text = page.get_text()
        f.write(text + "\n")

print("✅ Constitution text extracted to legal_rights.txt")
