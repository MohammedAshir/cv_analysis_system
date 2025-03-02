import re
import spacy
import phonenumbers

# Load NLP model
nlp = spacy.load("en_core_web_lg")

def extract_email(text):
    """Extract email, fixing common OCR errors (like missing '.' in .com)."""
    match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+", text)
    if match:
        email = match.group(0)
        # Fix common OCR errors (e.g., missing dot before "com")
        email = re.sub(r"(?<=@gmail)(com$)", ".com", email)  # Fix only "gmailcom" issue
        return email
    return "Not Found"


def extract_phone(text):
    for match in phonenumbers.PhoneNumberMatcher(text, "US"):
        return phonenumbers.format_number(match.number, phonenumbers.PhoneNumberFormat.NATIONAL)

    # Fallback regex
    match = re.search(r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}", text)
    return match.group(0) if match else "Not Found"

def extract_name(text):
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    words = text.split()
    return " ".join(words[:2]) if len(words) >= 2 else "Not Found"



def extract_experience(text):
    """Extract work experience details."""
    exp_pattern = r"(?i)([A-Za-z ]+?), ([A-Z][a-zA-Z0-9&, ]+)\n(\w+ \d{4}) - (\w+ \d{4}|Present)"
    matches = re.findall(exp_pattern, text)
    
    experience_list = []
    for role, company, start_date, end_date in matches:
        experience_list.append({
            "role": role.strip(),
            "company": company.strip(),
            "start_date": start_date,
            "end_date": end_date
        })
    
    return experience_list if experience_list else None


def extract_education(text):
    """Extracts degree, university, and duration correctly from different formats."""
    education = []

    # **Step 1: Extract Full Education Section**
    edu_match = re.search(r"(?i)education\n([\s\S]+?)(?:\n(?:SKILLS|WORK EXPERIENCE|PROJECTS|CERTIFICATIONS|SUMMARY)|\Z)", text)
    
    if not edu_match:
        return [{"degree": "Not Found", "university": "Not Found", "duration": "Not Found"}]
    
    edu_text = edu_match.group(1).strip()
    lines = [line.strip() for line in edu_text.split("\n") if line.strip()]

    degree, university, duration = "Not Found", "Not Found", "Not Found"

    # **Step 2: Extract Duration (YYYY-YYYY or Month YYYY - Month YYYY)**
    duration_pattern = r"\b(?:[A-Za-z]{3} \d{4} - [A-Za-z]{3} \d{4}|\d{4} - \d{4})\b"
    duration_match = re.search(duration_pattern, edu_text)
    
    if duration_match:
        duration = duration_match.group(0).strip()

    # **Step 3: Extract Degree (Handling Multi-line Degrees)**
    degree_pattern = r"(Bachelor|Master|B\.S\.|M\.S\.|B\.Tech|M\.Tech|Ph\.D)[^\n]*"
    degree_match = re.search(degree_pattern, edu_text, re.IGNORECASE)
    
    if degree_match:
        degree_index = edu_text.index(degree_match.group(0))  # Find index to handle multi-line degrees
        degree = edu_text[degree_index:].split("\n")[0].strip()  # Start from this line
        next_lines = edu_text.split("\n")[degree_index + 1:]  # Check next lines

        for line in next_lines:
            if not re.search(duration_pattern, line) and "University" not in line:
                degree += " " + line.strip()  # Append next lines until we hit a date or university
            else:
                break
        degree = degree.strip()

    # **Step 4: Extract University**
    doc = nlp(edu_text)
    universities = [ent.text.strip() for ent in doc.ents if ent.label_ == "ORG"]

    if universities:
        university = universities[0]
    
    # **Step 5: Handle case where degree, duration, and university are on the same line**
    for line in lines:
        if degree in line and duration in line:
            possible_university = line.replace(degree, "").replace(duration, "").strip()
            if possible_university and possible_university != degree:
                university = possible_university

    # **Step 6: Fallback for university detection**
    if university == "Not Found":
        for line in lines:
            if "University" in line or "Institute" in line or "College" in line:
                university = line.strip()
                break

    return [{
        "degree": degree,
        "university": university,
        "duration": duration
    }]

def extract_skills_and_tools(text):
    skills = set()
    tools = set()

    # Define known tools
    tool_keywords = {"JIRA", "GitHub", "HPALM", "TestRail", "Selenium"}  # Extendable

    # Extract SKILLS section
    skills_section = re.search(
        r"SKILLS\n([\s\S]+?)\n(?:WORK EXPERIENCE|EDUCATION|PROJECTS|CERTIFICATIONS|SUMMARY)",
        text, re.IGNORECASE
    )

    if skills_section:
        raw_skills = skills_section.group(1).split("\n")
        for skill in raw_skills:
            clean_skill = re.sub(r"[-–•]", "", skill).strip()  # Remove bullet points
            clean_skill = re.sub(r"\s*\b(Expert|Intermediate|Beginner|Advanced)\b", "", clean_skill, flags=re.IGNORECASE)  # Remove proficiency levels
            clean_skill = re.sub(r"\s+", " ", clean_skill).strip()  # Normalize spaces
            
            # Separate tools from skills
            if clean_skill and len(clean_skill) > 2 and not any(char.isdigit() for char in clean_skill):
                if clean_skill in tool_keywords:
                    tools.add(clean_skill)
                else:
                    skills.add(clean_skill)

    return list(skills) if skills else ["Not Found"], list(tools) if tools else ["Not Found"]



def extract_certifications(text):
    certifications = []
    cert_pattern = r"([\w\s]+)\s(\d{4}-\d{2}-\d{2})\n([\w\s]+)"

    matches = re.findall(cert_pattern, text)
    for match in matches:
        cert_name, cert_date, cert_issuer = match
        certifications.append({
            "name": cert_name.strip(),
            "date": cert_date.strip(),
            "issuer": cert_issuer.strip()
        })
    
    return certifications if certifications else "Not Found"


def extract_projects(text):
    projects = []
    lines = text.split("\n")
    project_name = None
    github_pattern = r"https?://github\.com[^\s]+"

    for i, line in enumerate(lines):
        if "projects" in line.lower():  # Find "Projects" section
            j = i + 1
            while j < len(lines) and "certification" not in lines[j].lower():  # Stop at "Certifications"
                github_match = re.search(github_pattern, lines[j])
                if github_match:
                    if project_name:  # Ensure project name exists before appending
                        projects.append({
                            "name": project_name.strip(),
                            "url": github_match.group().strip()
                        })
                    project_name = None  # Reset for next project
                else:
                    project_name = lines[j]  # Assign project name
                j += 1

    return projects if projects else "Not Found"


def parse_cv(text):
    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "education": extract_education(text),
        "experience": extract_experience(text),
        "skills": extract_skills_and_tools(text),
        "projects": extract_projects(text),
        "certifications": extract_certifications(text)
    }
