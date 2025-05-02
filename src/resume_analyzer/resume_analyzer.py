from typing import Optional
from pathlib import Path
from .pdf_processor import PDFProcessor
from .claude_client import ClaudeClient
from .models import ResumeAnalysis

class ResumeAnalyzer:
    def __init__(self):
        self.pdf_processor = PDFProcessor()
        self.claude_client = ClaudeClient()

    def analyze_resume(self, file_path: str) -> ResumeAnalysis:
        """
        Analyze a resume PDF file and return structured information.
        
        Args:
            file_path: Path to the PDF resume file
            
        Returns:
            ResumeAnalysis object containing the extracted information
        """
        # Validate file path
        if not Path(file_path).exists():
            raise FileNotFoundError(f"Resume file not found: {file_path}")

        # Extract and clean text from PDF
        raw_text = self.pdf_processor.extract_text(file_path)
        cleaned_text = self.pdf_processor.clean_text(raw_text)

        # Analyze text using Claude
        analysis_result = self.claude_client.analyze_resume(cleaned_text)

        # Convert to Pydantic model
        return ResumeAnalysis(**analysis_result)

    def match_skills(self, resume_analysis: ResumeAnalysis, desired_skills: list[str]) -> dict:
        """
        Match skills from the resume against a list of desired skills.
        
        Args:
            resume_analysis: ResumeAnalysis object
            desired_skills: List of desired skills to match against
            
        Returns:
            Dictionary containing matched skills and their details
        """
        matched_skills = []
        missing_skills = []
        
        # Convert desired skills to lowercase for case-insensitive matching
        desired_skills_lower = [skill.lower() for skill in desired_skills]
        
        for skill in resume_analysis.skills:
            if skill.name.lower() in desired_skills_lower:
                matched_skills.append({
                    "name": skill.name,
                    "category": skill.category,
                    "years_of_experience": skill.years_of_experience,
                    "proficiency_level": skill.proficiency_level
                })
        
        # Find missing skills
        for desired_skill in desired_skills:
            if not any(skill.name.lower() == desired_skill.lower() 
                      for skill in resume_analysis.skills):
                missing_skills.append(desired_skill)
        
        return {
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "match_percentage": len(matched_skills) / len(desired_skills) * 100
        }

    def validate_resume(self, resume_analysis: ResumeAnalysis) -> dict:
        """
        Validate the resume for completeness and common issues.
        
        Args:
            resume_analysis: ResumeAnalysis object
            
        Returns:
            Dictionary containing validation results
        """
        validation_results = {
            "missing_sections": [],
            "potential_issues": [],
            "completeness_score": 0
        }
        
        # Check for missing sections
        if not resume_analysis.name:
            validation_results["missing_sections"].append("Name")
        if not resume_analysis.email:
            validation_results["missing_sections"].append("Email")
        if not resume_analysis.phone:
            validation_results["missing_sections"].append("Phone")
        if not resume_analysis.education:
            validation_results["missing_sections"].append("Education")
        if not resume_analysis.work_experience:
            validation_results["missing_sections"].append("Work Experience")
        if not resume_analysis.skills:
            validation_results["missing_sections"].append("Skills")
        
        # Check for potential issues
        if len(resume_analysis.work_experience) < 2:
            validation_results["potential_issues"].append("Limited work experience")
        if not any(exp.is_current for exp in resume_analysis.work_experience):
            validation_results["potential_issues"].append("No current position listed")
        if not any(skill.years_of_experience for skill in resume_analysis.skills):
            validation_results["potential_issues"].append("Missing years of experience for skills")
        
        # Calculate completeness score
        total_sections = 7  # name, email, phone, education, work_experience, skills, certifications
        missing_sections = len(validation_results["missing_sections"])
        validation_results["completeness_score"] = ((total_sections - missing_sections) / total_sections) * 100
        
        return validation_results 