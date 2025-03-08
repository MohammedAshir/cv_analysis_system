import json
from processing.document_processor import process_document
from processing.cv_parser import parse_cv
from llm_integration import LLMAnalyzer
from database import create_tables, store_candidate, store_analysis

# Ensure tables exist
create_tables()

def process_all_cvs(file_paths):
    llm = LLMAnalyzer()  # Initialize LLM

    for file_path in file_paths:
        try:
            # Extract text and parse it into structured data
            text = process_document(file_path)
            structured_data = parse_cv(text)
            # print(text)
            print(json.dumps(structured_data, indent=4))  

        except Exception as e:
            print(f"Error processing {file_path}: {e}")

# List of CVs to process
file_paths = [
    r"C:\Users\ashas\cv_analysis_system\data\sample_cvs\File.pdf",
    r"C:\Users\ashas\cv_analysis_system\data\sample_cvs\File (1).pdf",
    r"C:\Users\ashas\cv_analysis_system\data\sample_cvs\File (2).pdf",
    r"C:\Users\ashas\cv_analysis_system\data\sample_cvs\File (3).pdf",
    r"C:\Users\ashas\cv_analysis_system\data\sample_cvs\File (4).pdf",
    r"C:\Users\ashas\cv_analysis_system\data\sample_cvs\File (5).pdf"
]

process_all_cvs(file_paths)