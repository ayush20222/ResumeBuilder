import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django.contrib.auth.models import User
from .models import UserProfile
import requests
from django.conf import settings

def preprocess_text(text):
    text = text.lower().strip()
    return text

def extract_skills(text):
    skills = set(skill.strip() for skill in text.lower().split(','))
    return skills

def load_job_profiles(file_path):
    df = pd.read_excel(file_path)
    job_profiles = df[['Job Profile', 'Skills']].dropna()
    return job_profiles

def get_job_recommendations(resume_content, job_profiles):
    resume_skills = extract_skills(preprocess_text(resume_content))
    recommendations = []
    
    for _, row in job_profiles.iterrows():
        job_title = row['Job Profile']
        job_skills = set(skill.strip().lower() for skill in row['Skills'].split(','))
        matching_skills = resume_skills.intersection(job_skills)
        
        if len(matching_skills) >= 2:
            recommendations.append((job_title, matching_skills, job_skills))
    recommendations = sorted(recommendations, key=lambda x: x[1], reverse=True)
    
    return recommendations

