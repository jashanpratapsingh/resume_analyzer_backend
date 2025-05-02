from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class Education(BaseModel):
    institution: str
    degree: str
    field_of_study: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    gpa: Optional[float] = None

class WorkExperience(BaseModel):
    company: str
    title: str
    start_date: str
    end_date: Optional[str] = None
    description: List[str] = Field(default_factory=list)
    location: Optional[str] = None
    is_current: bool = False

class Skill(BaseModel):
    name: str
    category: str  # e.g., "Technical", "Soft", "Language"
    years_of_experience: Optional[float] = None
    proficiency_level: Optional[str] = None  # e.g., "Beginner", "Intermediate", "Expert"
    last_used: Optional[str] = None

class Certification(BaseModel):
    name: str
    issuer: str
    date_obtained: Optional[str] = None
    expiration_date: Optional[str] = None

class ResumeAnalysis(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    summary: Optional[str] = None
    education: List[Education] = Field(default_factory=list)
    work_experience: List[WorkExperience] = Field(default_factory=list)
    skills: List[Skill] = Field(default_factory=list)
    certifications: List[Certification] = Field(default_factory=list)
    languages: List[str] = Field(default_factory=list)
    missing_sections: List[str] = Field(default_factory=list)
    analysis_date: datetime = Field(default_factory=datetime.now) 