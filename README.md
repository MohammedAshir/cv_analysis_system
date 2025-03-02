 
# CV Analysis System

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
```bash
git clone https://github.com/MohammedAshir/cv_analysis_system.git/
cd cv-analysis-system

