import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from resume_logic import ResumeData
from pdf_generator import PDFResumeGenerator

class ResumeBuilderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Professional Resume Builder")
        self.root.geometry("750x650")
        self.root.configure(bg='#f0f0f0')
        
        self.my_resume = ResumeData()
        
        self._make_title_bar()
        self._make_tabs()
        self._make_progress_bar()
        self._make_generate_button()
    
    def _make_title_bar(self):
        title_frame = tk.Frame(self.root, bg='#1a5490', height=60)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        tk.Label(title_frame, text="RESUME BUILDER PRO", 
                font=('Arial', 18, 'bold'), fg='white', bg='#1a5490').pack(pady=15)
    
    def _make_tabs(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=5)
        self._tab_personal_info(notebook)
        self._tab_education(notebook)
        self._tab_skills(notebook)
        self._tab_experience(notebook)
        self._tab_template(notebook)
    
    def _make_progress_bar(self):
        progress_frame = tk.Frame(self.root, bg='#f0f0f0')
        progress_frame.pack(fill='x', padx=10, pady=5)
        self.progress_label = tk.Label(progress_frame, text="Completion: 0%", 
                                       font=('Arial', 10), bg='#f0f0f0')
        self.progress_label.pack()
        self.progress_bar = ttk.Progressbar(progress_frame, length=400, mode='determinate')
        self.progress_bar.pack(pady=2)
    
    def _make_generate_button(self):
        btn_frame = tk.Frame(self.root, bg='#f0f0f0')
        btn_frame.pack(fill='x', padx=10, pady=10)
        tk.Button(btn_frame, text="GENERATE RESUME PDF", command=self._create_pdf,
                 bg='#28a745', fg='white', font=('Arial', 12, 'bold'),
                 padx=20, pady=8, cursor='hand2').pack()
    
    def _tab_personal_info(self, notebook):
        tab = tk.Frame(notebook, bg='#f0f0f0')
        notebook.add(tab, text="Personal Info")
        main_frame = tk.Frame(tab, bg='#f0f0f0')
        main_frame.pack(pady=20)
        
        fields = [('Full Name:', 'name'), ('Email:', 'email'), ('Phone:', 'phone'), ('Address:', 'address')]
        self.personal_entries = {}
        
        for i, (label, key) in enumerate(fields):
            tk.Label(main_frame, text=label, font=('Arial', 10, 'bold'), 
                    bg='#f0f0f0').grid(row=i, column=0, sticky='w', pady=5)
            entry = tk.Entry(main_frame, width=35, font=('Arial', 10), relief='solid', bd=1)
            entry.grid(row=i, column=1, padx=10)
            self.personal_entries[key] = entry
        
        tk.Button(main_frame, text="Save Personal Info", command=self._save_personal,
                 bg='#007bff', fg='white', font=('Arial', 10, 'bold'),
                 padx=15, pady=3).grid(row=4, column=0, columnspan=2, pady=15)
    
    def _tab_education(self, notebook):
        tab = tk.Frame(notebook, bg='#f0f0f0')
        notebook.add(tab, text="Education")
        main_frame = tk.Frame(tab, bg='#f0f0f0')
        main_frame.pack(pady=15)
        input_frame = tk.Frame(main_frame, bg='#f0f0f0')
        input_frame.pack()
        
        self.edu_degree = tk.Entry(input_frame, width=25, font=('Arial', 10))
        self.edu_school = tk.Entry(input_frame, width=25, font=('Arial', 10))
        self.edu_year = tk.Entry(input_frame, width=12, font=('Arial', 10))
        
        tk.Label(input_frame, text="Degree:", bg='#f0f0f0', font=('Arial', 9)).grid(row=0, column=0, pady=3)
        self.edu_degree.grid(row=0, column=1, padx=5)
        tk.Label(input_frame, text="Institution:", bg='#f0f0f0', font=('Arial', 9)).grid(row=1, column=0, pady=3)
        self.edu_school.grid(row=1, column=1, padx=5)
        tk.Label(input_frame, text="Year:", bg='#f0f0f0', font=('Arial', 9)).grid(row=2, column=0, pady=3)
        self.edu_year.grid(row=2, column=1, padx=5)
        
        tk.Button(input_frame, text="Add Education", command=self._add_education,
                 bg='#28a745', fg='white', font=('Arial', 9)).grid(row=3, column=0, columnspan=2, pady=10)
        
        self.edu_listbox = tk.Listbox(main_frame, height=4, width=55, font=('Arial', 9))
        self.edu_listbox.pack(pady=8)
    
    def _tab_skills(self, notebook):
        tab = tk.Frame(notebook, bg='#f0f0f0')
        notebook.add(tab, text="Skills")
        main_frame = tk.Frame(tab, bg='#f0f0f0')
        main_frame.pack(pady=25)
        
        tk.Label(main_frame, text="Enter a skill:", font=('Arial', 10), bg='#f0f0f0').pack()
        self.skill_entry = tk.Entry(main_frame, width=30, font=('Arial', 10), relief='solid', bd=1)
        self.skill_entry.pack(pady=5)
        tk.Button(main_frame, text="Add Skill", command=self._add_skill,
                 bg='#28a745', fg='white', font=('Arial', 9)).pack()
        
        self.skills_listbox = tk.Listbox(main_frame, height=5, width=40, font=('Arial', 9))
        self.skills_listbox.pack(pady=10)
        tk.Button(main_frame, text="Remove Selected", command=self._remove_skill,
                 bg='#dc3545', fg='white', font=('Arial', 8)).pack()
    
    def _tab_experience(self, notebook):
        tab = tk.Frame(notebook, bg='#f0f0f0')
        notebook.add(tab, text="Experience")
        main_frame = tk.Frame(tab, bg='#f0f0f0')
        main_frame.pack(pady=15)
        
        self.exp_title = tk.Entry(main_frame, width=35, font=('Arial', 10))
        self.exp_company = tk.Entry(main_frame, width=35, font=('Arial', 10))
        self.exp_duration = tk.Entry(main_frame, width=25, font=('Arial', 10))
        
        tk.Label(main_frame, text="Job Title:", bg='#f0f0f0', font=('Arial', 9)).pack()
        self.exp_title.pack(pady=2)
        tk.Label(main_frame, text="Company:", bg='#f0f0f0', font=('Arial', 9)).pack()
        self.exp_company.pack(pady=2)
        tk.Label(main_frame, text="Duration:", bg='#f0f0f0', font=('Arial', 9)).pack()
        self.exp_duration.pack(pady=2)
        tk.Label(main_frame, text="Description:", bg='#f0f0f0', font=('Arial', 9)).pack()
        self.exp_description = scrolledtext.ScrolledText(main_frame, height=3, width=40)
        self.exp_description.pack(pady=2)
        
        tk.Button(main_frame, text="Add Experience", command=self._add_experience,
                 bg='#28a745', fg='white', font=('Arial', 9)).pack(pady=5)
        
        self.exp_listbox = tk.Listbox(main_frame, height=3, width=60, font=('Arial', 9))
        self.exp_listbox.pack(pady=5)
    
    def _tab_template(self, notebook):
        tab = tk.Frame(notebook, bg='#f0f0f0')
        notebook.add(tab, text="Template")
        main_frame = tk.Frame(tab, bg='#f0f0f0')
        main_frame.pack(pady=30)
        
        tk.Label(main_frame, text="Select Resume Style:", 
                 font=('Arial', 12, 'bold'), bg='#f0f0f0').pack(pady=10)
        
        self.template_choice = tk.StringVar(value="modern")
        
        def save_template():
            self.my_resume.choose_template(self.template_choice.get())
        
        styles = [
            ("Modern (Blue Theme)", "modern"),
            ("Traditional (Classic B&W)", "traditional"),
            ("Professional (Executive Style)", "professional")
        ]
        
        for text, value in styles:
            tk.Radiobutton(main_frame, text=text, variable=self.template_choice,
                          value=value, bg='#f0f0f0', font=('Arial', 10),
                          padx=15, pady=5, command=save_template).pack(anchor='w')
    
    def _save_personal(self):
        name = self.personal_entries['name'].get()
        email = self.personal_entries['email'].get()
        phone = self.personal_entries['phone'].get()
        address = self.personal_entries['address'].get()
        
        if not name:
            messagebox.showwarning("Warning", "Please enter your name!")
            return
        
        self.my_resume.save_personal_info(name, email, phone, address)
        messagebox.showinfo("Success", "Personal info saved!")
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
            messagebox.showinfo("Success", "Education added!")
    
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
        description = self.exp_description.get("1.0", tk.END).strip()
        
        if title and company and duration and description:
            self.my_resume.add_experience(title, company, duration, description)
            self.exp_listbox.insert(tk.END, f"{title} at {company} ({duration})")
            self.exp_title.delete(0, tk.END)
            self.exp_company.delete(0, tk.END)
            self.exp_duration.delete(0, tk.END)
            self.exp_description.delete("1.0", tk.END)
            self._update_progress()
            messagebox.showinfo("Success", "Experience added!")
    
    def _update_progress(self):
        percent = self.my_resume.show_completion_percentage()
        self.progress_bar['value'] = percent
        self.progress_label.config(text=f"Completion: {percent}%")
    
    def _create_pdf(self):
        try:
            name = self.my_resume.personal_info.get('name', 'Resume')
            filename = f"{name}_Resume.pdf"
            
            pdf_maker = PDFResumeGenerator()
            pdf_maker.make_resume(self.my_resume.get_all_data(), filename)
            messagebox.showinfo("Success!", f"Resume saved as: {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed: {str(e)}\n\nRun: pip install reportlab")

if __name__ == "__main__":
    window = tk.Tk()
    app = ResumeBuilderApp(window)
    window.mainloop()