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

            print(f"\nExtracted Data from: {file_path}")
            print(json.dumps(structured_data, indent=4))  

            # Store extracted data in database
            candidate_id = store_candidate(structured_data, text)

            # Send structured data to LLM
            llm_response = llm.analyze_cv(structured_data)
            print("\n🔹 LLM Analysis Result:")
            print(llm_response)

            # Convert LLM response from JSON string to dictionary
            try:
                analysis_data = json.loads(llm_response)
                store_analysis(candidate_id, analysis_data)  # Store LLM analysis
            except json.JSONDecodeError:
                print("Error: LLM response is not valid JSON.")

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
