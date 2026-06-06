class ResumeData:
    def __init__(self):
        self.personal_info = {}
        self.education = []
        self.skills = []
        self.experience = []
        self.template_choice = "modern"
        self.color_theme = "professional"
    
    def set_personal_info(self, name, email, phone, address=""):
        self.personal_info = {
            'name': name,
            'email': email,
            'phone': phone,
            'address': address
        }
    
    def add_education(self, degree, institution, year, grade=""):
        self.education.append({
            'degree': degree,
            'institution': institution,
            'year': year,
            'grade': grade
        })
    
    def add_skill(self, skill, level="Expert"):
        self.skills.append({'name': skill, 'level': level})
    
    def add_experience(self, job_title, company, duration, description, achievements=[]):
        self.experience.append({
            'title': job_title,
            'company': company,
            'duration': duration,
            'description': description,
            'achievements': achievements
        })
    
    def set_template(self, template_name):
        self.template_choice = template_name
    
    def get_formatted_data(self):
        return {
            'personal': self.personal_info,
            'education': self.education,
            'skills': self.skills,
            'experience': self.experience,
            'template': self.template_choice,
            'color': self.color_theme
        }
    
    def calculate_completion(self):
        filled = 0
        total = 7
        
        if self.personal_info.get('name'): filled += 1
        if self.personal_info.get('email'): filled += 1
        if self.personal_info.get('phone'): filled += 1
        if len(self.education) > 0: filled += 1
        if len(self.skills) > 0: filled += 1
        if len(self.experience) > 0: filled += 1
        if self.personal_info.get('address'): filled += 1
        
        return int((filled / total) * 100)