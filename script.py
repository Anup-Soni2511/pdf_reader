
import os
import json
import fitz
import pdfplumber
import pandas as pd
from glob import glob

def extract_metadata(pdf_path):
    doc = fitz.open(pdf_path)
    metadata = doc.metadata
    metadata['page_count'] = doc.page_count
    return metadata

def extract_paragraphs(pdf_path):
    doc = fitz.open(pdf_path)
    paragraphs = []
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        text = page.get_text("text")
        paragraphs.append(text)
    return paragraphs

def extract_tables(pdf_path):
    tables = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables_on_page = page.extract_tables()
            for table in tables_on_page:
                tables.append(table)
    return tables

def extract_images(pdf_path, output_dir):
    doc = fitz.open(pdf_path)
    images = []
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        image_list = page.get_images(full=True)
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_filename = os.path.join(output_dir, f"{os.path.basename(pdf_path)}_img{page_num+1}_{img_index+1}.png")
            images.append(image_filename)
            with open(image_filename, "wb") as img_file:
                img_file.write(image_bytes)
    return images

def process_pdf(pdf_path, output_dir):
    pdf_data = {}

    pdf_data['metadata'] = extract_metadata(pdf_path)

    pdf_data['paragraphs'] = extract_paragraphs(pdf_path)

    pdf_data['tables'] = extract_tables(pdf_path)

    pdf_data['images'] = extract_images(pdf_path, output_dir)

    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
    json_filename = os.path.join(output_dir, f"{pdf_name}_data.json")
    with open(json_filename, "w") as json_file:
        json.dump(pdf_data, json_file, indent=4)

    return pdf_data

def generate_csv_report(pdf_files_data, report_file):
    report_data = []
    for data in pdf_files_data:
        report_data.append({
            'File Name': data['metadata']['title'],
            'Number of Tables': len(data['tables']),
            'Number of Paragraphs': len(data['paragraphs']),
            'Number of Images': len(data['images'])
        })
    df = pd.DataFrame(report_data)
    df.to_csv(report_file, index=False)

def process_pdfs_in_folder(folder_path, output_dir, keyword_filter=None):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    pdf_files = glob(os.path.join(folder_path, "*.pdf"))
    filtered_files = [f for f in pdf_files if keyword_filter is None or keyword_filter.lower() in os.path.basename(f).lower()]

    all_pdf_data = []

    for pdf_path in filtered_files:
        pdf_data = process_pdf(pdf_path, output_dir)
        all_pdf_data.append(pdf_data)

    report_file = os.path.join(output_dir, "consolidated_report.csv")
    generate_csv_report(all_pdf_data, report_file)
    print(f"Process completed. Report saved at {report_file}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Extract and process data from PDFs.")
    parser.add_argument("folder_path", help="Path to the folder containing PDFs")
    parser.add_argument("output_dir", help="Path to save the extracted data and report")
    parser.add_argument("--filter", help="Filter PDFs by a keyword in the filename", default=None)

    args = parser.parse_args()

    process_pdfs_in_folder(args.folder_path, args.output_dir, args.filter)

