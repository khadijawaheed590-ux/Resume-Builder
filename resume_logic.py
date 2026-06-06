class ResumeData:
    def __init__(self):
        self.personal_info = {}
        self.education = []
        self.skills = []
        self.experience = []
        self.template_choice = "modern"
    
    def save_personal_info(self, name, email, phone, address=""):
        self.personal_info = {
            'name': name,
            'email': email,
            'phone': phone,
            'address': address
        }
    
    def add_education(self, degree, school, year):
        self.education.append({
            'degree': degree,
            'institution': school,
            'year': year
        })
    
    def add_skill(self, skill_name):
        self.skills.append({'name': skill_name})
    
    def add_experience(self, job_title, company, duration, description):
        self.experience.append({
            'title': job_title,
            'company': company,
            'duration': duration,
            'description': description
        })
    
    def choose_template(self, template_name):
        self.template_choice = template_name
    
    def get_all_data(self):
        return {
            'personal': self.personal_info,
            'education': self.education,
            'skills': self.skills,
            'experience': self.experience,
            'template': self.template_choice
        }
    
    def show_completion_percentage(self):
        filled = 0
        total = 7
        
        if self.personal_info.get('name'):
            filled += 1
        if self.personal_info.get('email'):
            filled += 1
        if self.personal_info.get('phone'):
            filled += 1
        if len(self.education) > 0:
            filled += 1
        if len(self.skills) > 0:
            filled += 1
        if len(self.experience) > 0:
            filled += 1
        if self.personal_info.get('address'):
            filled += 1
        
        return int((filled / total) * 100)