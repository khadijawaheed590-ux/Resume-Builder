
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from resume_logic import ResumeData
from pdf_generator import PDFResumeGenerator

class ResumeBuilderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Professional Resume Builder")
        self.root.geometry("900x700")
        self.root.configure(bg='#f0f0f0')
        
        self.resume_data = ResumeData()
        
        # Set modern style
        self.setup_styles()
        self.create_widgets()
    
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook.Tab', padding=[20, 5], font=('Arial', 10, 'bold'))
        style.configure('TButton', padding=[10, 5], font=('Arial', 10))
        style.configure('TLabel', font=('Arial', 10), background='#f0f0f0')
        
    def create_widgets(self):
        # Title Frame
        title_frame = tk.Frame(self.root, bg='#1a5490', height=80)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="🎯 PROFESSIONAL RESUME BUILDER", 
                               font=('Arial', 20, 'bold'), 
                               fg='white', bg='#1a5490')
        title_label.pack(pady=20)
        
        # Main Notebook
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Create Tabs
        self.create_personal_tab(notebook)
        self.create_education_tab(notebook)
        self.create_skills_tab(notebook)
        self.create_experience_tab(notebook)
        
        # Progress Bar Frame
        progress_frame = tk.Frame(self.root, bg='#f0f0f0', height=60)
        progress_frame.pack(fill='x', padx=20, pady=10)
        progress_frame.pack_propagate(False)
        
        self.progress_label = tk.Label(progress_frame, text="Resume Completion: 0%", 
                                       font=('Arial', 10), bg='#f0f0f0')
        self.progress_label.pack()
        
        self.progress_bar = ttk.Progressbar(progress_frame, length=400, mode='determinate')
        self.progress_bar.pack(pady=5)
        
        # Generate Button
        generate_frame = tk.Frame(self.root, bg='#f0f0f0')
        generate_frame.pack(pady=20)
        
        generate_btn = tk.Button(generate_frame, text="✨ GENERATE PROFESSIONAL RESUME ✨", 
                                 command=self.generate_resume,
                                 bg='#1a5490', fg='white', 
                                 font=('Arial', 12, 'bold'),
                                 padx=30, pady=10,
                                 cursor='hand2')
        generate_btn.pack()
        
        self.update_progress()
    
    def create_personal_tab(self, notebook):
        tab = tk.Frame(notebook, bg='#f0f0f0')
        notebook.add(tab, text="📋 Personal Info")
        
        # Create main frame
        main_frame = tk.Frame(tab, bg='#f0f0f0')
        main_frame.pack(pady=30, padx=50)
        
        fields = [
            ('Full Name:', 'name', 0),
            ('Email Address:', 'email', 1),
            ('Phone Number:', 'phone', 2),
            ('Address:', 'address', 3),
            ('Professional Summary:', 'summary', 4)
        ]
        
        self.personal_entries = {}
        
        for label, key, row in fields:
            tk.Label(main_frame, text=label, font=('Arial', 11, 'bold'), 
                    bg='#f0f0f0').grid(row=row, column=0, sticky='w', pady=10)
            
            if key == 'summary':
                entry = scrolledtext.ScrolledText(main_frame, height=5, width=40, font=('Arial', 10))
                entry.grid(row=row, column=1, padx=20, pady=5)
            else:
                entry = tk.Entry(main_frame, width=40, font=('Arial', 10), 
                                relief='solid', bd=1)
                entry.grid(row=row, column=1, padx=20, pady=5)
            
            self.personal_entries[key] = entry
        
        save_btn = tk.Button(main_frame, text="Save Personal Information", 
                            command=self.save_personal_info,
                            bg='#28a745', fg='white',
                            font=('Arial', 10, 'bold'),
                            padx=20, pady=5,
                            cursor='hand2')
        save_btn.grid(row=5, column=0, columnspan=2, pady=20)
    
    def create_education_tab(self, notebook):
        tab = tk.Frame(notebook, bg='#f0f0f0')
        notebook.add(tab, text="🎓 Education")
        
        main_frame = tk.Frame(tab, bg='#f0f0f0')
        main_frame.pack(pady=20, padx=50)
        
        # Input Frame
        input_frame = tk.Frame(main_frame, bg='#f0f0f0')
        input_frame.pack()
        
        labels = ['Degree:', 'Institution:', 'Year:', 'Grade (Optional):']
        self.edu_entries = {}
        
        for i, label in enumerate(labels):
            tk.Label(input_frame, text=label, font=('Arial', 10, 'bold'), 
                    bg='#f0f0f0').grid(row=i, column=0, sticky='w', pady=5)
            entry = tk.Entry(input_frame, width=35, font=('Arial', 10),
                           relief='solid', bd=1)
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.edu_entries[label] = entry
        
        add_btn = tk.Button(input_frame, text="➕ Add Education", 
                           command=self.add_education,
                           bg='#007bff', fg='white',
                           font=('Arial', 10, 'bold'),
                           cursor='hand2')
        add_btn.grid(row=len(labels), column=0, columnspan=2, pady=15)
        
        # Listbox Frame
        listbox_frame = tk.Frame(main_frame, bg='#f0f0f0')
        listbox_frame.pack(pady=10)
        
        tk.Label(listbox_frame, text="Saved Education:", font=('Arial', 10, 'bold'),
                bg='#f0f0f0').pack()
        
        self.edu_listbox = tk.Listbox(listbox_frame, height=6, width=60, 
                                      font=('Arial', 10))
        self.edu_listbox.pack(pady=5)
    
    def create_skills_tab(self, notebook):
        tab = tk.Frame(notebook, bg='#f0f0f0')
        notebook.add(tab, text="💡 Skills")
        
        main_frame = tk.Frame(tab, bg='#f0f0f0')
        main_frame.pack(pady=40, padx=50)
        
        input_frame = tk.Frame(main_frame, bg='#f0f0f0')
        input_frame.pack()
        
        tk.Label(input_frame, text="Skill Name:", font=('Arial', 11, 'bold'),
                bg='#f0f0f0').grid(row=0, column=0, pady=10)
        
        self.skill_entry = tk.Entry(input_frame, width=35, font=('Arial', 10),
                                   relief='solid', bd=1)
        self.skill_entry.grid(row=0, column=1, padx=10, pady=10)
        
        add_btn = tk.Button(input_frame, text="➕ Add Skill", 
                           command=self.add_skill,
                           bg='#007bff', fg='white',
                           font=('Arial', 10, 'bold'),
                           cursor='hand2')
        add_btn.grid(row=1, column=0, columnspan=2, pady=10)
        
        listbox_frame = tk.Frame(main_frame, bg='#f0f0f0')
        listbox_frame.pack(pady=20)
        
        tk.Label(listbox_frame, text="Your Skills:", font=('Arial', 11, 'bold'),
                bg='#f0f0f0').pack()
        
        self.skills_listbox = tk.Listbox(listbox_frame, height=8, width=50,
                                        font=('Arial', 10))
        self.skills_listbox.pack(pady=5)
        
        remove_btn = tk.Button(listbox_frame, text="❌ Remove Selected Skill",
                              command=self.remove_skill,
                              bg='#dc3545', fg='white',
                              font=('Arial', 9), cursor='hand2')
        remove_btn.pack(pady=5)
    
    def create_experience_tab(self, notebook):
        tab = tk.Frame(notebook, bg='#f0f0f0')
        notebook.add(tab, text="💼 Experience")
        
        main_frame = tk.Frame(tab, bg='#f0f0f0')
        main_frame.pack(pady=20, padx=50)
        
        input_frame = tk.Frame(main_frame, bg='#f0f0f0')
        input_frame.pack()
        
        exp_fields = [
            ('Job Title:', 'title'),
            ('Company:', 'company'),
            ('Duration (e.g., 2022-2024):', 'duration'),
            ('Description:', 'description')
        ]
        
        self.exp_entries = {}
        
        for i, (label, key) in enumerate(exp_fields):
            tk.Label(input_frame, text=label, font=('Arial', 10, 'bold'),
                    bg='#f0f0f0').grid(row=i, column=0, sticky='w', pady=5)
            
            if key == 'description':
                entry = scrolledtext.ScrolledText(input_frame, height=4, width=40,
                                                 font=('Arial', 10))
                entry.grid(row=i, column=1, padx=10, pady=5)
            else:
                entry = tk.Entry(input_frame, width=40, font=('Arial', 10),
                               relief='solid', bd=1)
                entry.grid(row=i, column=1, padx=10, pady=5)
            
            self.exp_entries[key] = entry
        
        add_btn = tk.Button(input_frame, text="➕ Add Experience", 
                           command=self.add_experience,
                           bg='#007bff', fg='white',
                           font=('Arial', 10, 'bold'),
                           cursor='hand2')
        add_btn.grid(row=len(exp_fields), column=0, columnspan=2, pady=15)
        
        listbox_frame = tk.Frame(main_frame, bg='#f0f0f0')
        listbox_frame.pack(pady=10)
        
        tk.Label(listbox_frame, text="Work Experience:", font=('Arial', 11, 'bold'),
                bg='#f0f0f0').pack()
        
        self.exp_listbox = tk.Listbox(listbox_frame, height=6, width=70,
                                     font=('Arial', 10))
        self.exp_listbox.pack(pady=5)
    
    def save_personal_info(self):
        name = self.personal_entries['name'].get()
        email = self.personal_entries['email'].get()
        phone = self.personal_entries['phone'].get()
        address = self.personal_entries['address'].get()
        summary = self.personal_entries['summary'].get("1.0", tk.END).strip()
        
        if not name:
            messagebox.showwarning("Warning", "Name is required!")
            return
        
        self.resume_data.set_personal_info(name, email, phone, address)
        self.resume_data.personal_info['summary'] = summary
        
        messagebox.showinfo("Success", "Personal information saved!")
        self.update_progress()
    
    def add_education(self):
        degree = self.edu_entries['Degree:'].get()
        institution = self.edu_entries['Institution:'].get()
        year = self.edu_entries['Year:'].get()
        grade = self.edu_entries['Grade (Optional):'].get()
        
        if degree and institution and year:
            self.resume_data.add_education(degree, institution, year, grade)
            self.edu_listbox.insert(tk.END, f"{degree} - {institution} ({year})")
            
            # Clear entries
            for entry in self.edu_entries.values():
                entry.delete(0, tk.END)
            
            self.update_progress()
            messagebox.showinfo("Success", "Education added!")
        else:
            messagebox.showwarning("Warning", "Please fill Degree, Institution, and Year!")
    
    def add_skill(self):
        skill = self.skill_entry.get()
        if skill:
            self.resume_data.add_skill(skill)
            self.skills_listbox.insert(tk.END, skill)
            self.skill_entry.delete(0, tk.END)
            self.update_progress()
    
    def remove_skill(self):
        selection = self.skills_listbox.curselection()
        if selection:
            index = selection[0]
            self.skills_listbox.delete(index)
            # Rebuild skills list
            self.resume_data.skills = []
            for i in range(self.skills_listbox.size()):
                self.resume_data.add_skill(self.skills_listbox.get(i))
            self.update_progress()
    
    def add_experience(self):
        title = self.exp_entries['title'].get()
        company = self.exp_entries['company'].get()
        duration = self.exp_entries['duration'].get()
        description = self.exp_entries['description'].get("1.0", tk.END).strip()
        
        if title and company and duration and description:
            self.resume_data.add_experience(title, company, duration, description)
            self.exp_listbox.insert(tk.END, f"{title} at {company} ({duration})")
            
            # Clear entries
            self.exp_entries['title'].delete(0, tk.END)
            self.exp_entries['company'].delete(0, tk.END)
            self.exp_entries['duration'].delete(0, tk.END)
            self.exp_entries['description'].delete("1.0", tk.END)
            
            self.update_progress()
            messagebox.showinfo("Success", "Experience added!")
        else:
            messagebox.showwarning("Warning", "Please fill all experience fields!")
    
    def update_progress(self):
        completion = self.resume_data.calculate_completion()
        self.progress_bar['value'] = completion
        self.progress_label.config(text=f"Resume Completion: {completion}%")
        
        if completion == 100:
            self.progress_label.config(fg='green')
        elif completion >= 50:
            self.progress_label.config(fg='orange')
        else:
            self.progress_label.config(fg='red')
    
    def generate_resume(self):
        try:
            generator = PDFResumeGenerator()
            filename = generator.generate_resume(
                self.resume_data.get_formatted_data(),
                "Professional_Resume.pdf"
            )
            messagebox.showinfo("Success!", f"✅ Resume generated successfully!\n\nSaved as: {filename}\n\nCheck your project folder!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate PDF: {str(e)}\n\nMake sure you have installed: pip install reportlab")

if __name__ == "__main__":
    root = tk.Tk()
    app = ResumeBuilderApp(root)
    root.mainloop()