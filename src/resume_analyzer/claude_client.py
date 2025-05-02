import os
from typing import Dict, Any
import anthropic
from dotenv import load_dotenv

load_dotenv()

class ClaudeClient:
    def __init__(self):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
        
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = "claude-3-opus-20240229"  # Using the latest Claude model

    def analyze_resume(self, resume_text: str) -> Dict[str, Any]:
        """
        Analyze resume text using Claude API.
        
        Args:
            resume_text: Cleaned text from the resume
            
        Returns:
            Dictionary containing the analysis results
        """
        prompt = self._create_prompt(resume_text)
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4000,
                temperature=0.1,  # Low temperature for more consistent results
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            return self._parse_response(response.content[0].text)
        except Exception as e:
            raise Exception(f"Error calling Claude API: {str(e)}")

    def _create_prompt(self, resume_text: str) -> str:
        """Create a structured prompt for Claude."""
        return f"""Please analyze the following resume text and extract the following information in JSON format:

1. Personal Information:
   - Name
   - Email
   - Phone
   - Location

2. Education:
   - Institution
   - Degree
   - Field of Study
   - Start and End Dates
   - GPA (if available)

3. Work Experience:
   - Company Name
   - Job Title
   - Start and End Dates
   - Location
   - Key Responsibilities and Achievements
   - Current Position (yes/no)

4. Skills:
   - Technical Skills
   - Soft Skills
   - Languages
   - Years of Experience for each skill
   - Proficiency Level (Beginner/Intermediate/Expert)

5. Certifications:
   - Name
   - Issuer
   - Date Obtained
   - Expiration Date (if applicable)

6. Missing Information:
   - List any important sections that are missing

Resume Text:
{resume_text}

Please provide the analysis in a structured JSON format that matches the following schema:
{{
    "name": "string",
    "email": "string",
    "phone": "string",
    "location": "string",
    "education": [
        {{
            "institution": "string",
            "degree": "string",
            "field_of_study": "string",
            "start_date": "string",
            "end_date": "string",
            "gpa": "float"
        }}
    ],
    "work_experience": [
        {{
            "company": "string",
            "title": "string",
            "start_date": "string",
            "end_date": "string",
            "description": ["string"],
            "location": "string",
            "is_current": "boolean"
        }}
    ],
    "skills": [
        {{
            "name": "string",
            "category": "string",
            "years_of_experience": "float",
            "proficiency_level": "string",
            "last_used": "string"
        }}
    ],
    "certifications": [
        {{
            "name": "string",
            "issuer": "string",
            "date_obtained": "string",
            "expiration_date": "string"
        }}
    ],
    "languages": ["string"],
    "missing_sections": ["string"]
}}"""

    def _parse_response(self, response_text: str) -> Dict[str, Any]:
        """Parse Claude's response into a structured format."""
        # Extract JSON from the response
        try:
            # Find the JSON part in the response
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            if start_idx == -1 or end_idx == 0:
                raise ValueError("No JSON found in response")
            
            json_str = response_text[start_idx:end_idx]
            import json
            return json.loads(json_str)
        except Exception as e:
            raise Exception(f"Error parsing Claude response: {str(e)}") 