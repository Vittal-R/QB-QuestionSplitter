import os
from pypdf import PdfReader
import re


def parse_pdfs_in_folder(sets):
    # Ensure the folder exists
    if not os.path.exists(sets):
        print(f"Folder '{sets}' does not exist.")
        return

    # Iterate through all files in the folder
    for file_name in os.listdir(sets):
        if file_name.endswith(".pdf"):
            pdf_path = os.path.join(sets, file_name)
            print(f"Parsing: {file_name}")
            pdfText = ""
            try:
                # Open and read the PDF
                reader = PdfReader(pdf_path)
                for page_num, page in enumerate(reader.pages):
                    text = page.extract_text()
                    pdfText = pdfText + (text + "\n")
            except Exception as e:
                return(f"Error reading {file_name}: {e}")
            return pdfText

if __name__ == "__main__":
    # Define the path to the 'sets' folder
    txtName = "2020-2021 History Bowl Set.txt"
    sets_folder = os.path.join(os.path.dirname(__file__), "sets")

    # Process the PDFs
    parse_pdfs_in_folder(sets_folder)
    output_file_path = os.path.join(os.path.dirname(__file__), "output", txtName)
    with open(output_file_path, "w", encoding="utf-8") as out_file:
        for parsed_text in parse_pdfs_in_folder(sets_folder):
            out_file.write(parsed_text)
    print(f"Parsing complete. Output written to {output_file_path}")