import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from resume_logic import ResumeData
from pdf_generator import PDFResumeGenerator

class ResumeBuilderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Professional Resume Builder")
        self.root.geometry("850x750")
        self.root.configure(bg='#f0f0f0')
        
        self.my_resume = ResumeData()
        
        self._make_title_bar()
        self._make_tabs()
        self._make_progress_bar()
        self._make_generate_button()
    
    def _make_title_bar(self):
        title_frame = tk.Frame(self.root, bg='#1a5490', height=70)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        tk.Label(title_frame, text="📄 RESUME BUILDER PRO 📄", 
                font=('Arial', 20, 'bold'), fg='white', bg='#1a5490').pack(pady=18)
    
    def _make_tabs(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=5)
        self._tab_personal(notebook)
        self._tab_summary(notebook)
        self._tab_education(notebook)
        self._tab_skills(notebook)
        self._tab_experience(notebook)
        self._tab_projects(notebook)
        self._tab_certifications(notebook)
        self._tab_languages(notebook)
        self._tab_hobbies(notebook)
        self._tab_template(notebook)
    
    def _make_progress_bar(self):
        progress_frame = tk.Frame(self.root, bg='#f0f0f0')
        progress_frame.pack(fill='x', padx=10, pady=5)
        self.progress_label = tk.Label(progress_frame, text="📊 Completion: 0%", 
                                       font=('Arial', 10), bg='#f0f0f0')
        self.progress_label.pack()
        self.progress_bar = ttk.Progressbar(progress_frame, length=500, mode='determinate')
        self.progress_bar.pack(pady=3)
    
    def _make_generate_button(self):
        btn_frame = tk.Frame(self.root, bg='#f0f0f0')
        btn_frame.pack(fill='x', padx=10, pady=10)
        tk.Button(btn_frame, text="🚀 GENERATE RESUME PDF 🚀", command=self._create_pdf,
                 bg='#28a745', fg='white', font=('Arial', 13, 'bold'),
                 padx=30, pady=10, cursor='hand2').pack()
    
    def _tab_personal(self, notebook):
        tab = tk.Frame(notebook, bg='#f0f0f0')
        notebook.add(tab, text="👤 Personal Info")
        main_frame = tk.Frame(tab, bg='#f0f0f0')
        main_frame.pack(pady=25)
        
        fields = [('Full Name:', 'name'), ('Email:', 'email'), ('Phone:', 'phone'), ('Address:', 'address')]
        self.personal_entries = {}
        
        for i, (label, key) in enumerate(fields):
            tk.Label(main_frame, text=label, font=('Arial', 11, 'bold'), 
                    bg='#f0f0f0').grid(row=i, column=0, sticky='w', pady=8)
            entry = tk.Entry(main_frame, width=40, font=('Arial', 11), relief='solid', bd=1)
            entry.grid(row=i, column=1, padx=15)
            self.personal_entries[key] = entry
        
        tk.Button(main_frame, text="💾 Save Personal Info", command=self._save_personal,
                 bg='#007bff', fg='white', font=('Arial', 11, 'bold'),
                 padx=20, pady=5).grid(row=4, column=0, columnspan=2, pady=20)
    
    def _tab_summary(self, notebook):
        tab = tk.Frame(notebook, bg='#f0f0f0')
        notebook.add(tab, text="📝 Summary")
        main_frame = tk.Frame(tab, bg='#f0f0f0')
        main_frame.pack(pady=30)
        
        tk.Label(main_frame, text="📋 Professional Summary:", font=('Arial', 12, 'bold'),
                bg='#f0f0f0').pack()
        tk.Label(main_frame, text="(Write 2-3 sentences about yourself)", 
                font=('Arial', 9), fg='gray', bg='#f0f0f0').pack()
        
        self.summary_text = scrolledtext.ScrolledText(main_frame, height=8, width=60, font=('Arial', 11))
        self.summary_text.pack(pady=10)
        
        tk.Button(main_frame, text="💾 Save Summary", command=self._save_summary,
                 bg='#007bff', fg='white', font=('Arial', 11)).pack(pady=10)
    
    def _tab_education(self, notebook):
        tab = tk.Frame(notebook, bg='#f0f0f0')
        notebook.add(tab, text="🎓 Education")
        main_frame = tk.Frame(tab, bg='#f0f0f0')
        main_frame.pack(pady=20)
        
        input_frame = tk.Frame(main_frame, bg='#f0f0f0')
        input_frame.pack()
        
        self.edu_degree = tk.Entry(input_frame, width=30, font=('Arial', 11))
        self.edu_school = tk.Entry(input_frame, width=30, font=('Arial', 11))
        self.edu_year = tk.Entry(input_frame, width=15, font=('Arial', 11))
        
        tk.Label(input_frame, text="🎓 Degree:", bg='#f0f0f0', font=('Arial', 10)).grid(row=0, column=0, pady=5)
        self.edu_degree.grid(row=0, column=1, padx=10)
        tk.Label(input_frame, text="🏫 Institution:", bg='#f0f0f0', font=('Arial', 10)).grid(row=1, column=0, pady=5)
        self.edu_school.grid(row=1, column=1, padx=10)
        tk.Label(input_frame, text="📅 Year:", bg='#f0f0f0', font=('Arial', 10)).grid(row=2, column=0, pady=5)
        self.edu_year.grid(row=2, column=1, padx=10)
        
        tk.Button(input_frame, text="➕ Add Education", command=self._add_education,
                 bg='#28a745', fg='white', font=('Arial', 10)).grid(row=3, column=0, columnspan=2, pady=15)
        
        self.edu_listbox = tk.Listbox(main_frame, height=5, width=65, font=('Arial', 10))
        self.edu_listbox.pack(pady=10)
    
    def _tab_skills(self, notebook):
        tab = tk.Frame(notebook, bg='#f0f0f0')
        notebook.add(tab, text="💡 Skills")
        main_frame = tk.Frame(tab, bg='#f0f0f0')
        main_frame.pack(pady=30)
        
        tk.Label(main_frame, text="💪 Enter a skill:", font=('Arial', 11), bg='#f0f0f0').pack()
        self.skill_entry = tk.Entry(main_frame, width=40, font=('Arial', 11), relief='solid', bd=1)
        self.skill_entry.pack(pady=8)
        tk.Button(main_frame, text="➕ Add Skill", command=self._add_skill,
                 bg='#28a745', fg='white', font=('Arial', 10)).pack()
        
        self.skills_listbox = tk.Listbox(main_frame, height=6, width=45, font=('Arial', 10))
        self.skills_listbox.pack(pady=15)
        tk.Button(main_frame, text="❌ Remove Selected", command=self._remove_skill,
                 bg='#dc3545', fg='white', font=('Arial', 9)).pack()
    
    def _tab_experience(self, notebook):
        tab = tk.Frame(notebook, bg='#f0f0f0')
        notebook.add(tab, text="💼 Experience")
        main_frame = tk.Frame(tab, bg='#f0f0f0')
        main_frame.pack(pady=15)
        
        self.exp_title = tk.Entry(main_frame, width=40, font=('Arial', 11))
        self.exp_company = tk.Entry(main_frame, width=40, font=('Arial', 11))
        self.exp_duration = tk.Entry(main_frame, width=30, font=('Arial', 11))
        
        tk.Label(main_frame, text="🎯 Job Title:", bg='#f0f0f0', font=('Arial', 10)).pack()
        self.exp_title.pack(pady=3)
        tk.Label(main_frame, text="🏢 Company:", bg='#f0f0f0', font=('Arial', 10)).pack()
        self.exp_company.pack(pady=3)
        tk.Label(main_frame, text="📅 Duration:", bg='#f0f0f0', font=('Arial', 10)).pack()
        self.exp_duration.pack(pady=3)
        tk.Label(main_frame, text="🏆 Achievements (one per line):", bg='#f0f0f0', font=('Arial', 10)).pack()
        self.exp_achievements = scrolledtext.ScrolledText(main_frame, height=5, width=45, font=('Arial', 11))
        self.exp_achievements.pack(pady=5)
        
        tk.Button(main_frame, text="➕ Add Experience", command=self._add_experience,
                 bg='#28a745', fg='white', font=('Arial', 10)).pack(pady=10)
        
        self.exp_listbox = tk.Listbox(main_frame, height=4, width=70, font=('Arial', 10))
        self.exp_listbox.pack(pady=8)
    
    def _tab_projects(self, notebook):
        tab = tk.Frame(notebook, bg='#f0f0f0')
        notebook.add(tab, text="🚀 Projects")
        main_frame = tk.Frame(tab, bg='#f0f0f0')
        main_frame.pack(pady=15)
        
        self.proj_name = tk.Entry(main_frame, width=40, font=('Arial', 11))
        self.proj_tech = tk.Entry(main_frame, width=40, font=('Arial', 11))
        
        tk.Label(main_frame, text="📁 Project Name:", bg='#f0f0f0', font=('Arial', 10)).pack()
        self.proj_name.pack(pady=3)
        tk.Label(main_frame, text="🔧 Technologies Used:", bg='#f0f0f0', font=('Arial', 10)).pack()
        self.proj_tech.pack(pady=3)
        
        tk.Button(main_frame, text="➕ Add Project", command=self._add_project,
                 bg='#28a745', fg='white', font=('Arial', 10)).pack(pady=10)
        
        self.proj_listbox = tk.Listbox(main_frame, height=4, width=70, font=('Arial', 10))
        self.proj_listbox.pack(pady=8)
    
    def _tab_certifications(self, notebook):
        tab = tk.Frame(notebook, bg='#f0f0f0')
        notebook.add(tab, text="🎖️ Certifications")
        main_frame = tk.Frame(tab, bg='#f0f0f0')
        main_frame.pack(pady=25)
        
        self.cert_name = tk.Entry(main_frame, width=40, font=('Arial', 11))
        self.cert_year = tk.Entry(main_frame, width=15, font=('Arial', 11))
        
        tk.Label(main_frame, text="📜 Certification Name:", bg='#f0f0f0', font=('Arial', 10)).pack()
        self.cert_name.pack(pady=3)
        tk.Label(main_frame, text="📅 Year:", bg='#f0f0f0', font=('Arial', 10)).pack()
        self.cert_year.pack(pady=3)
        
        tk.Button(main_frame, text="➕ Add Certification", command=self._add_certification,
                 bg='#28a745', fg='white', font=('Arial', 10)).pack(pady=15)
        
        self.cert_listbox = tk.Listbox(main_frame, height=5, width=55, font=('Arial', 10))
        self.cert_listbox.pack(pady=10)
    
    def _tab_languages(self, notebook):
        tab = tk.Frame(notebook, bg='#f0f0f0')
        notebook.add(tab, text="🗣️ Languages")
        main_frame = tk.Frame(tab, bg='#f0f0f0')
        main_frame.pack(pady=25)
        
        self.lang_name = tk.Entry(main_frame, width=30, font=('Arial', 11))
        self.lang_level = tk.Entry(main_frame, width=20, font=('Arial', 11))
        
        tk.Label(main_frame, text="🌍 Language:", bg='#f0f0f0', font=('Arial', 10)).pack()
        self.lang_name.pack(pady=3)
        tk.Label(main_frame, text="⭐ Level:", bg='#f0f0f0', font=('Arial', 10)).pack()
        self.lang_level.pack(pady=3)
        
        tk.Button(main_frame, text="➕ Add Language", command=self._add_language,
                 bg='#28a745', fg='white', font=('Arial', 10)).pack(pady=15)
        
        self.lang_listbox = tk.Listbox(main_frame, height=5, width=50, font=('Arial', 10))
        self.lang_listbox.pack(pady=10)
    
    def _tab_hobbies(self, notebook):
        tab = tk.Frame(notebook, bg='#f0f0f0')
        notebook.add(tab, text="🎨 Hobbies")
        main_frame = tk.Frame(tab, bg='#f0f0f0')
        main_frame.pack(pady=30)
        
        tk.Label(main_frame, text="🎯 Enter a hobby:", font=('Arial', 11), bg='#f0f0f0').pack()
        self.hobby_entry = tk.Entry(main_frame, width=40, font=('Arial', 11), relief='solid', bd=1)
        self.hobby_entry.pack(pady=8)
        tk.Button(main_frame, text="➕ Add Hobby", command=self._add_hobby,
                 bg='#28a745', fg='white', font=('Arial', 10)).pack()
        
        self.hobby_listbox = tk.Listbox(main_frame, height=5, width=45, font=('Arial', 10))
        self.hobby_listbox.pack(pady=15)
        tk.Button(main_frame, text="❌ Remove Selected", command=self._remove_hobby,
                 bg='#dc3545', fg='white', font=('Arial', 9)).pack()
    
    def _tab_template(self, notebook):
        tab = tk.Frame(notebook, bg='#f0f0f0')
        notebook.add(tab, text="🎨 Template")
        main_frame = tk.Frame(tab, bg='#f0f0f0')
        main_frame.pack(pady=40)
        
        tk.Label(main_frame, text="🎨 Select Your Resume Style:", 
                 font=('Arial', 14, 'bold'), bg='#f0f0f0').pack(pady=15)
        
        self.template_choice = tk.StringVar(value="modern")
        
        def save_template():
            self.my_resume.choose_template(self.template_choice.get())
        
        styles = [
            ("✨ Modern - Blue Theme", "modern"),
            ("📜 Traditional - Classic Black & White", "traditional"),
            ("💼 Professional - Executive Dark Blue", "professional")
        ]
        
        for text, value in styles:
            tk.Radiobutton(main_frame, text=text, variable=self.template_choice,
                          value=value, bg='#f0f0f0', font=('Arial', 11),
                          padx=20, pady=8, command=save_template).pack(anchor='w')
    
    def _save_personal(self):
        name = self.personal_entries['name'].get()
        email = self.personal_entries['email'].get()
        phone = self.personal_entries['phone'].get()
        address = self.personal_entries['address'].get()
        
        if not name:
            messagebox.showwarning("⚠️ Warning", "Please enter your name!")
            return
        
        self.my_resume.save_personal_info(name, email, phone, address)
        messagebox.showinfo("✅ Success", "Personal info saved!")
        self._update_progress()
    
    def _save_summary(self):
        summary = self.summary_text.get("1.0", tk.END).strip()
        self.my_resume.add_summary(summary)
        messagebox.showinfo("✅ Success", "Summary saved!")
        self._update_progress()
    
    def _add_education(self):
        degree = self.edu_degree.get()
        school = self.edu_school.get()
        year = self.edu_year.get()
        
        if degree and school and year:
            self.my_resume.add_education(degree, school, year)
            self.edu_listbox.insert(tk.END, f"{degree} - {school} ({year})")
            self.edu_degree.delete(0, tk.END)
            self.edu_school.delete(0, tk.END)
            self.edu_year.delete(0, tk.END)
            self._update_progress()
            messagebox.showinfo("✅ Success", "Education added!")
    
    def _add_skill(self):
        skill = self.skill_entry.get()
        if skill:
            self.my_resume.add_skill(skill)
            self.skills_listbox.insert(tk.END, skill)
            self.skill_entry.delete(0, tk.END)
            self._update_progress()
    
    def _remove_skill(self):
        selected = self.skills_listbox.curselection()
        if selected:
            index = selected[0]
            self.skills_listbox.delete(index)
            self.my_resume.skills = []
            for i in range(self.skills_listbox.size()):
                self.my_resume.add_skill(self.skills_listbox.get(i))
            self._update_progress()
    
    def _add_experience(self):
        title = self.exp_title.get()
        company = self.exp_company.get()
        duration = self.exp_duration.get()
        achievements = self.exp_achievements.get("1.0", tk.END).strip()
        
        if title and company and duration and achievements:
            self.my_resume.add_experience(title, company, duration, achievements)
            self.exp_listbox.insert(tk.END, f"{title} at {company} ({duration})")
            self.exp_title.delete(0, tk.END)
            self.exp_company.delete(0, tk.END)
            self.exp_duration.delete(0, tk.END)
            self.exp_achievements.delete("1.0", tk.END)
            self._update_progress()
            messagebox.showinfo("✅ Success", "Experience added!")
        else:
            messagebox.showwarning("⚠️ Warning", "Please fill all fields including achievements!")
    
    def _add_project(self):
        name = self.proj_name.get()
        tech = self.proj_tech.get()
        
        if name and tech:
            self.my_resume.add_project(name, tech)
            self.proj_listbox.insert(tk.END, f"{name} ({tech})")
            self.proj_name.delete(0, tk.END)
            self.proj_tech.delete(0, tk.END)
            self._update_progress()
            messagebox.showinfo("✅ Success", "Project added!")
    
    def _add_certification(self):
        name = self.cert_name.get()
        year = self.cert_year.get()
        
        if name and year:
            self.my_resume.add_certification(name, year)
            self.cert_listbox.insert(tk.END, f"{name} ({year})")
            self.cert_name.delete(0, tk.END)
            self.cert_year.delete(0, tk.END)
            self._update_progress()
            messagebox.showinfo("✅ Success", "Certification added!")
    
    def _add_language(self):
        name = self.lang_name.get()
        level = self.lang_level.get()
        
        if name and level:
            self.my_resume.add_language(name, level)
            self.lang_listbox.insert(tk.END, f"{name} - {level}")
            self.lang_name.delete(0, tk.END)
            self.lang_level.delete(0, tk.END)
            self._update_progress()
            messagebox.showinfo("✅ Success", "Language added!")
    
    def _add_hobby(self):
        hobby = self.hobby_entry.get()
        if hobby:
            self.my_resume.add_hobby(hobby)
            self.hobby_listbox.insert(tk.END, hobby)
            self.hobby_entry.delete(0, tk.END)
            self._update_progress()
    
    def _remove_hobby(self):
        selected = self.hobby_listbox.curselection()
        if selected:
            index = selected[0]
            self.hobby_listbox.delete(index)
            self.my_resume.hobbies = []
            for i in range(self.hobby_listbox.size()):
                self.my_resume.add_hobby(self.hobby_listbox.get(i))
            self._update_progress()
    
    def _update_progress(self):
        percent = self.my_resume.show_completion_percentage()
        self.progress_bar['value'] = percent
        self.progress_label.config(text=f"📊 Completion: {percent}%")
    
    def _create_pdf(self):
        try:
            name = self.my_resume.personal_info.get('name', 'Resume')
            filename = f"{name}_Resume.pdf"
            
            pdf_maker = PDFResumeGenerator()
            pdf_maker.make_resume(self.my_resume.get_all_data(), filename)
            messagebox.showinfo("🎉 Success!", f"✅ Resume saved as: {filename}")
        except Exception as e:
            messagebox.showerror("❌ Error", f"Failed: {str(e)}\n\nRun: pip install reportlab")

if __name__ == "__main__":
    window = tk.Tk()
    app = ResumeBuilderApp(window)
    window.mainloop()