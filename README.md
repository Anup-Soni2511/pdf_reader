# PDF Data Extraction Script

This project extracts metadata, text (paragraphs), tables, and images from PDF files in a specified folder. It processes all PDFs and saves the extracted data in both JSON and CSV formats. The CSV file provides a summary report of the extraction results.

## Features
- Extracts metadata (e.g., title, author, number of pages) from PDF files.
- Extracts text (paragraphs) from all pages of the PDF.
- Extracts tables from PDFs and saves them as a list.
- Extracts images from PDF pages and saves them as PNG files.
- Generates a CSV report summarizing the number of tables, paragraphs, and images in each PDF.

## Requirements
The project requires Python 3.x and the following Python libraries:
- `PyMuPDF` (fitz) for reading and extracting data from PDFs.
- `pdfplumber` for extracting tables.
- `pandas` for generating a summary CSV report.
- `glob` and `os` for file handling.

## Installation Instructions

### Step 1: Create a Virtual Environment
To ensure dependencies are isolated, you should create a Python virtual environment. Follow these steps:

1. Open a terminal or command prompt.
2. Navigate to your project directory.
3. Run the following command to create a virtual environment named `evn`:

   ```bash
   python -m venv evn
   ```

4. Activate the virtual environment:
   - **Windows:**

     ```bash
     .\evn\Scripts\activate
     ```

   - **Linux/macOS:**

     ```bash
     source evn/bin/activate
     ```

### Step 2: Install Dependencies
Once the virtual environment is activated, install the required dependencies from the `requirements.txt` file.

1. Create a `requirements.txt` file with the following content:

   ```txt
   PyMuPDF
   pdfplumber
   pandas
   ```

2. Install the dependencies by running:

   ```bash
   pip install -r requirements.txt
   ```

### Step 3: Running the Project
Once the dependencies are installed, you can run the script with the following command:

```bash
python script.py <folder_path> <output_dir> [--filter <keyword>]
```

- **`folder_path`**: Path to the folder containing PDF files.
- **`output_dir`**: Directory where extracted data (JSON files) and the summary CSV report will be saved.
- **`--filter`** (optional): Filter PDF files by a keyword in the filename. If provided, only PDF files containing the keyword in their filename will be processed.

### Example Command:

```bash
python script.py /path/to/pdf_folder /path/to/output_dir --filter keyword
```

This will process all PDFs in `/path/to/pdf_folder`, filter by the keyword (if specified), and save the extracted data and the summary report to `/path/to/output_dir`.

## Output Files
- **JSON Files**: For each PDF, a JSON file will be generated containing extracted metadata, paragraphs, tables, and images.
  - Example: `example_data.json`
  
- **CSV Report**: A summary CSV file `consolidated_report.csv` will be created, containing:
  - **File Name**: Title of the PDF (from metadata).
  - **Number of Tables**: Count of tables extracted.
  - **Number of Paragraphs**: Count of paragraphs extracted.
  - **Number of Images**: Count of images extracted.

## Example Output
For a sample `consolidated_report.csv`, the file might look like this:

| File Name  | Number of Tables | Number of Paragraphs | Number of Images |
|------------|------------------|----------------------|------------------|
| example.pdf| 2                | 10                   | 3                |

