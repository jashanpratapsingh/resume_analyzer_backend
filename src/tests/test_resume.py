from src.resume_analyzer.resume_analyzer import ResumeAnalyzer
import os

def test_resume_analyzer():
    # Initialize the analyzer
    analyzer = ResumeAnalyzer()
    
    # Check if API key is set
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY not found in environment variables")
        print("Please create a .env file with your API key")
        return
    
    # Path to your test resume
    resume_path = input("Enter the path to your resume PDF: ")
    
    if not os.path.exists(resume_path):
        print(f"Error: File not found at {resume_path}")
        return
    
    try:
        # Analyze the resume
        print("\nAnalyzing resume...")
        analysis = analyzer.analyze_resume(resume_path)
        
        # Print basic information
        print("\n=== Resume Analysis ===")
        print(f"Name: {analysis.name}")
        print(f"Email: {analysis.email}")
        print(f"Phone: {analysis.phone}")
        print(f"Location: {analysis.location}")
        
        # Print education
        print("\n=== Education ===")
        for edu in analysis.education:
            print(f"{edu.degree} at {edu.institution}")
            print(f"Field: {edu.field_of_study}")
            print(f"Dates: {edu.start_date} - {edu.end_date}")
            if edu.gpa:
                print(f"GPA: {edu.gpa}")
            print()
        
        # Print work experience
        print("\n=== Work Experience ===")
        for exp in analysis.work_experience:
            print(f"{exp.title} at {exp.company}")
            print(f"Location: {exp.location}")
            print(f"Dates: {exp.start_date} - {exp.end_date or 'Present'}")
            print("Responsibilities:")
            for desc in exp.description:
                print(f"- {desc}")
            print()
        
        # Print skills
        print("\n=== Skills ===")
        for skill in analysis.skills:
            print(f"{skill.name} ({skill.category})")
            if skill.years_of_experience:
                print(f"Years of Experience: {skill.years_of_experience}")
            if skill.proficiency_level:
                print(f"Proficiency: {skill.proficiency_level}")
            print()
        
        # Example skill matching
        desired_skills = [
            "Python",
            "Machine Learning",
            "Data Analysis",
            "Project Management"
        ]
        
        skill_match = analyzer.match_skills(analysis, desired_skills)
        print("\n=== Skill Matching ===")
        print(f"Match Percentage: {skill_match['match_percentage']:.1f}%")
        print("\nMatched Skills:")
        for skill in skill_match['matched_skills']:
            print(f"- {skill['name']} ({skill['years_of_experience']} years)")
        print("\nMissing Skills:")
        for skill in skill_match['missing_skills']:
            print(f"- {skill}")
        
        # Validate resume
        validation = analyzer.validate_resume(analysis)
        print("\n=== Resume Validation ===")
        print(f"Completeness Score: {validation['completeness_score']:.1f}%")
        if validation['missing_sections']:
            print("\nMissing Sections:")
            for section in validation['missing_sections']:
                print(f"- {section}")
        if validation['potential_issues']:
            print("\nPotential Issues:")
            for issue in validation['potential_issues']:
                print(f"- {issue}")
        
    except Exception as e:
        print(f"Error analyzing resume: {str(e)}")

if __name__ == "__main__":
    test_resume_analyzer() 