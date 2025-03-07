# CV Analysis System

![Screenshot (150)](https://github.com/user-attachments/assets/84676710-286e-4679-92f3-758301d8d3e9)

## Overview

The CV Analysis System is designed to automate the extraction, analysis, and querying of data from CVs. The system can process multiple CV documents (PDF/Word), extract relevant information using OCR (Optical Character Recognition), and provide a chatbot interface for querying the extracted details. It also integrates with an LLM (Large Language Model) like OpenAI or Cohere for further analysis and provides structured outputs such as a summary, skills, missing details, and more.

This system allows HR professionals or recruiters to quickly assess candidate qualifications by querying the system based on their needs.

## Features

- **Document Processing**: Processes PDF and Word documents, performs OCR on scanned text, and extracts structured data.
- **LLM Integration**: Integrates with OpenAI or Cohere APIs for advanced analysis of CVs (skills, summary, fit for specific job roles).
- **Query System**: A chatbot interface that allows users to query specific candidate information.
- **Database Storage**: All extracted and analyzed data is stored in a relational database (SQLite/PostgreSQL).
- **Web Interface**: A Flask-based frontend to interact with the system via a web browser.

## Requirements

To run the CV Analysis System, you need the following tools and libraries:

- **Python 3.x**
- **Flask** (for web interface)
- **Cohere API Key** for LLM Integration
- **Tesseract** (for OCR processing)
- **SQLite** for database storage
- **.env** file to store sensitive configuration such as API keys

## Setup Instructions

### 1. Clone the Repository

Clone this repository to your local machine:

git clone https://github.com/MohammedAshir/cv_analysis_system.git
cd cv-analysis-system

### 2. Create and Activate a Virtual Environment
On Windows:

python -m venv venv
venv\Scripts\activate

On macOS/Linux:

python3 -m venv venv
source venv/bin/activate

### 3. Install Dependencies

Install the required Python dependencies:

pip install -r requirements.txt

### 4. Set Up the Database

Make sure you have PostgreSQL or SQLite set up. SQLite will automatically create the database.


### 5. Running the Application

python app.py

### 6. Sample CVs

Sample CVs are provided in the data/sample_cvs/ directory. You can add more sample files as needed. The system will process these files and extract data from them.

### 7. Querying the System
Once the server is running, open http://127.0.0.1:5000/ in your browser. Use the form to input a query, such as "What skills does this candidate have?". The system will return a structured analysis of the CV.

