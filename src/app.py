from flask import Flask, render_template, request, redirect, url_for, jsonify
from processing.document_processor import process_document
from processing.cv_parser import parse_cv
from llm_integration import LLMAnalyzer
from database import create_tables, store_candidate, store_analysis

# Initialize Flask app
app = Flask(__name__)

# Ensure tables exist
create_tables()

# Route to home page
@app.route('/')
def home():
    return render_template('index.html')

# Route to process all CVs
@app.route('/process_all')
def process_all():
    file_paths = [
        r"C:\Users\ashas\cv_analysis_system\data\sample_cvs\File.pdf",
        r"C:\Users\ashas\cv_analysis_system\data\sample_cvs\File (1).pdf",
        r"C:\Users\ashas\cv_analysis_system\data\sample_cvs\File (2).pdf",
        r"C:\Users\ashas\cv_analysis_system\data\sample_cvs\File (3).pdf",
        r"C:\Users\ashas\cv_analysis_system\data\sample_cvs\File (4).pdf",
        r"C:\Users\ashas\cv_analysis_system\data\sample_cvs\File (5).pdf"
    ]

    llm = LLMAnalyzer()  # Initialize LLM

    for file_path in file_paths:
        try:
            # Extract text and parse it into structured data
            text = process_document(file_path)
            structured_data = parse_cv(text)

            # Store extracted data in database
            candidate_id = store_candidate(structured_data, text)

            # Send structured data to LLM
            llm_response = llm.analyze_cv(structured_data)

            # Convert LLM response from JSON string to dictionary
            try:
                analysis_data = json.loads(llm_response)
                store_analysis(candidate_id, analysis_data)  # Store LLM analysis
            except json.JSONDecodeError:
                print("Error: LLM response is not valid JSON.")
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

    return redirect(url_for('home'))

# Route to handle queries
@app.route('/query', methods=['POST'])
def query():
    query_text = request.form['query']
    llm = LLMAnalyzer()

    # Handle user query via LLM (for now, just send structured data to LLM)
    query_result = llm.analyze_cv({'query': query_text})  # Use LLM analysis for queries
    
    # Render result in HTML page
    return render_template('index.html', query_result=query_result)

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
