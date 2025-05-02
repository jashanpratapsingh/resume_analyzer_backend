import os
from anthropic import Anthropic
import PyPDF2
from typing import Dict, Any
from dotenv import load_dotenv
import json
from datetime import datetime

class ResumeAnalyzer:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
        self.client = Anthropic(api_key=api_key)

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ''
                for page in pdf_reader.pages:
                    text += page.extract_text()
                return text
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")

    def analyze_resume(self, pdf_path: str) -> Dict[str, Any]:
        try:
            # Extract text from PDF
            resume_text = self.extract_text_from_pdf(pdf_path)
            
            # Prepare the prompt for Claude
            prompt = f"""Analyze this resume text and extract the following information in a structured format. Return ONLY a valid JSON object with these fields:

Resume text:
{resume_text}

Required fields in the JSON response:
- name (string)
- email (string)
- phone (string)
- location (string)
- education (array of objects with: institution, degree, field_of_study, start_date, end_date)
- work_experience (array of objects with: company, title, start_date, end_date, description array, location)
- skills (array of objects with: name, category)
- certifications (array of objects with: name, issuer, date_obtained)
- languages (array of strings)

Format all dates as YYYY-MM strings. Ensure the JSON is properly formatted and valid."""

            # Get analysis from Claude
            response = self.client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=4000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            # Parse Claude's response as JSON
            try:
                analysis = json.loads(response.content[0].text)
            except json.JSONDecodeError:
                # If JSON parsing fails, extract JSON from the response
                text = response.content[0].text
                start = text.find('{')
                end = text.rfind('}') + 1
                if start >= 0 and end > start:
                    analysis = json.loads(text[start:end])
                else:
                    raise Exception("Could not parse Claude's response as JSON")

            # Add analysis date
            analysis['analysis_date'] = datetime.now().strftime('%Y-%m-%d')
            
            # Ensure all required fields exist
            required_fields = ['name', 'email', 'phone', 'location', 'education', 
                             'work_experience', 'skills', 'certifications', 'languages']
            for field in required_fields:
                if field not in analysis:
                    analysis[field] = [] if field in ['education', 'work_experience', 'skills', 
                                                    'certifications', 'languages'] else ""

            return analysis

        except Exception as e:
            raise Exception(f"Error analyzing resume: {str(e)}") 