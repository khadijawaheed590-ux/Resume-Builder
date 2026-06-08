import tkinter as tk
from tkinter import messagebox
from database import Database

class LoginWindow:
    def __init__(self, root, on_login_success):
        self.root = root
        self.on_login_success = on_login_success
        self.db = Database()
        
        self.root.title("Login - Resume Builder")
        self.root.geometry("400x420")
        self.root.configure(bg='#1a5490')
        
        self.setup_ui()
    
    def setup_ui(self):
        main_frame = tk.Frame(self.root, bg='white', padx=30, pady=30)
        main_frame.place(relx=0.5, rely=0.5, anchor='center', width=350, height=350)
        
        tk.Label(main_frame, text="RESUME BUILDER", 
                font=('Arial', 18, 'bold'), fg='#1a5490', bg='white').pack(pady=10)
        
        tk.Label(main_frame, text="Login to your account", 
                font=('Arial', 10), fg='gray', bg='white').pack(pady=(0, 20))
        
        tk.Label(main_frame, text="Username:", font=('Arial', 10), bg='white').pack(anchor='w')
        self.username_entry = tk.Entry(main_frame, font=('Arial', 11), width=30, relief='solid', bd=1)
        self.username_entry.pack(pady=(0, 10))
        
        tk.Label(main_frame, text="Password:", font=('Arial', 10), bg='white').pack(anchor='w')
        self.password_entry = tk.Entry(main_frame, font=('Arial', 11), width=30, relief='solid', bd=1, show="*")
        self.password_entry.pack(pady=(0, 20))
        
        tk.Button(main_frame, text="LOGIN", command=self.do_login,
                 bg='#1a5490', fg='white', font=('Arial', 11, 'bold'),
                 padx=20, pady=5, cursor='hand2').pack(fill='x', pady=5)
        
        tk.Button(main_frame, text="SIGN UP", command=self.show_signup,
                 bg='#28a745', fg='white', font=('Arial', 11, 'bold'),
                 padx=20, pady=5, cursor='hand2').pack(fill='x', pady=5)
    
    def do_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter username and password!")
            return
        
        success, result = self.db.login(username, password)
        if success:
            messagebox.showinfo("Welcome", f"Welcome back, {username}!")
            self.root.destroy()
            self.on_login_success(result)
        else:
            messagebox.showerror("Error", result)
    
    def show_signup(self):
        self.signup_window = tk.Toplevel(self.root)
        self.signup_window.title("Sign Up")
        self.signup_window.geometry("400x480")
        self.signup_window.configure(bg='white')
        
        main_frame = tk.Frame(self.signup_window, bg='white', padx=30, pady=30)
        main_frame.pack(fill='both', expand=True)
        
        tk.Label(main_frame, text="CREATE ACCOUNT", 
                font=('Arial', 16, 'bold'), fg='#1a5490', bg='white').pack(pady=10)
        
        tk.Label(main_frame, text="Username:", font=('Arial', 10), bg='white').pack(anchor='w')
        self.signup_username = tk.Entry(main_frame, font=('Arial', 11), width=30, relief='solid', bd=1)
        self.signup_username.pack(pady=(0, 10))
        
        tk.Label(main_frame, text="Email:", font=('Arial', 10), bg='white').pack(anchor='w')
        self.signup_email = tk.Entry(main_frame, font=('Arial', 11), width=30, relief='solid', bd=1)
        self.signup_email.pack(pady=(0, 10))
        
        tk.Label(main_frame, text="Password:", font=('Arial', 10), bg='white').pack(anchor='w')
        self.signup_password = tk.Entry(main_frame, font=('Arial', 11), width=30, relief='solid', bd=1, show="*")
        self.signup_password.pack(pady=(0, 10))
        
        tk.Label(main_frame, text="Confirm Password:", font=('Arial', 10), bg='white').pack(anchor='w')
        self.signup_confirm = tk.Entry(main_frame, font=('Arial', 11), width=30, relief='solid', bd=1, show="*")
        self.signup_confirm.pack(pady=(0, 20))
        
        tk.Button(main_frame, text="REGISTER", command=self.do_register,
                 bg='#28a745', fg='white', font=('Arial', 11, 'bold'),
                 padx=20, pady=5, cursor='hand2').pack(fill='x', pady=5)
    
    def do_register(self):
        username = self.signup_username.get()
        email = self.signup_email.get()
        password = self.signup_password.get()
        confirm = self.signup_confirm.get()
        
        if not username or not email or not password:
            messagebox.showerror("Error", "All fields are required!")
            return
        
        if password != confirm:
            messagebox.showerror("Error", "Passwords don't match!")
            return
        
        if '@' not in email or '.' not in email:
            messagebox.showerror("Error", "Invalid email address!")
            return
        
        success, msg = self.db.register(username, password, email)
        if success:
            messagebox.showinfo("Success", msg)
            self.signup_window.destroy()
        else:
            messagebox.showerror("Error", msg)