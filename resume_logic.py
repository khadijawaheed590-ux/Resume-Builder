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
    
    def add_education(self, degree, school, year):
        self.education.append({
            'degree': degree,
            'institution': school,
            'year': year
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
    
    def add_project(self, project_name, description, technologies):
        self.projects.append({
            'name': project_name,
            'description': description,
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
    
    def show_completion_percentage(self):
        filled = 0
        total = 10
        
        if self.personal_info.get('name'): filled += 1
        if self.personal_info.get('email'): filled += 1
        if self.summary: filled += 1
        if len(self.education) > 0: filled += 1
        if len(self.skills) > 0: filled += 1
        if len(self.experience) > 0: filled += 1
        if len(self.certifications) > 0: filled += 1
        if len(self.languages) > 0: filled += 1
        if len(self.projects) > 0: filled += 1
        if len(self.hobbies) > 0: filled += 1
        
        return int((filled / total) * 100)