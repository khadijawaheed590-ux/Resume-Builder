import json
import os

class ResumeData:
    def __init__(self):
        self.personal_info = {}
        self.summary = ""
        self.education = []
        self.skills = []
        self.experience = []
        self.certifications = []
        self.languages = []
        self.projects = []
        self.hobbies = []
        self.template_choice = "modern"
    
    def save_personal_info(self, name, email, phone, address=""):
        self.personal_info = {
            'name': name,
            'email': email,
            'phone': phone,
            'address': address
        }
    
    def add_summary(self, summary_text):
        self.summary = summary_text
    
    def add_education(self, degree, school, year, gpa=""):
        self.education.append({
            'degree': degree,
            'institution': school,
            'year': year,
            'gpa': gpa
        })
    
    def add_skill(self, skill_name):
        self.skills.append({'name': skill_name})
    
    def add_experience(self, job_title, company, duration, achievements):
        self.experience.append({
            'title': job_title,
            'company': company,
            'duration': duration,
            'achievements': achievements
        })
    
    def add_certification(self, cert_name, year):
        self.certifications.append({
            'name': cert_name,
            'year': year
        })
    
    def add_language(self, language, level):
        self.languages.append({
            'name': language,
            'level': level
        })
    
    def add_project(self, project_name, technologies):
        self.projects.append({
            'name': project_name,
            'technologies': technologies
        })
    
    def add_hobby(self, hobby_name):
        self.hobbies.append({'name': hobby_name})
    
    def choose_template(self, template_name):
        self.template_choice = template_name
    
    def get_all_data(self):
        return {
            'personal': self.personal_info,
            'summary': self.summary,
            'education': self.education,
            'skills': self.skills,
            'experience': self.experience,
            'certifications': self.certifications,
            'languages': self.languages,
            'projects': self.projects,
            'hobbies': self.hobbies,
            'template': self.template_choice
        }
    
    def save_to_file(self, filename):
        data = self.get_all_data()
        with open(filename, 'w') as f:
            json.dump(data, f)
        return True
    
    def load_from_file(self, filename):
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                data = json.load(f)
                self.personal_info = data.get('personal', {})
                self.summary = data.get('summary', '')
                self.education = data.get('education', [])
                self.skills = data.get('skills', [])
                self.experience = data.get('experience', [])
                self.certifications = data.get('certifications', [])
                self.languages = data.get('languages', [])
                self.projects = data.get('projects', [])
                self.hobbies = data.get('hobbies', [])
                self.template_choice = data.get('template', 'modern')
            return True
        return False
    
    def show_completion_percentage(self):
        filled = 0
        total = 9
        
        if self.personal_info.get('name'): filled += 1
        if self.personal_info.get('email'): filled += 1
        if self.summary: filled += 1
        if len(self.education) > 0: filled += 1
        if len(self.skills) > 0: filled += 1
        if len(self.experience) > 0: filled += 1
        if len(self.certifications) > 0: filled += 1
        if len(self.languages) > 0: filled += 1
        if len(self.projects) > 0: filled += 1
        
        return int((filled / total) * 100)