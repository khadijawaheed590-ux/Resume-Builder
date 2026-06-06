from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from datetime import datetime

class PDFResumeGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
    
    def make_resume(self, your_data, filename="my_resume.pdf"):
        template = your_data.get('template', 'modern')
        
        doc = SimpleDocTemplate(filename, pagesize=letter,
                                rightMargin=72, leftMargin=72,
                                topMargin=72, bottomMargin=72)
        story = []
        info = your_data['personal']
        
        if template == "modern":
            main_color = colors.HexColor('#1a5490')
            name_size = 32
        elif template == "traditional":
            main_color = colors.black
            name_size = 28
        else:
            main_color = colors.HexColor('#0d3b66')
            name_size = 32
        
        style_name = ParagraphStyle('Name', parent=self.styles['Heading1'],
                                      fontSize=name_size, textColor=main_color,
                                      spaceAfter=8, alignment=0, fontName='Helvetica-Bold')
        story.append(Paragraph(info.get('name', 'YOUR NAME'), style_name))
        
        contact = f"{info.get('email', '')}  |  {info.get('phone', '')}  |  {info.get('address', '')}"
        style_contact = ParagraphStyle('Contact', parent=self.styles['Normal'],
                                        fontSize=9, textColor=colors.HexColor('#666666'),
                                        spaceAfter=15, alignment=0)
        story.append(Paragraph(contact, style_contact))
        
        line = Table([[' ']], colWidths=[450])
        line.setStyle(TableStyle([('LINEABOVE', (0,0), (-1,-1), 2, main_color)]))
        story.append(line)
        story.append(Spacer(1, 0.15 * inch))
        
        if your_data.get('summary'):
            story.append(self._section_title("📋 PROFILE SUMMARY", main_color))
            story.append(Paragraph(your_data['summary'], self.styles['Normal']))
            story.append(Spacer(1, 0.12 * inch))
        
        if your_data['skills']:
            story.append(self._section_title("💡 CORE SKILLS", main_color))
            skills_text = "  ◉  ".join([s['name'] for s in your_data['skills']])
            story.append(Paragraph(skills_text, self.styles['Normal']))
            story.append(Spacer(1, 0.12 * inch))
        
        if your_data['experience']:
            story.append(self._section_title("💼 WORK EXPERIENCE", main_color))
            for job in your_data['experience']:
                style_job = ParagraphStyle('Job', parent=self.styles['Normal'],
                                            fontSize=12, textColor=main_color,
                                            spaceAfter=4, fontName='Helvetica-Bold')
                story.append(Paragraph(job['title'], style_job))
                
                style_company = ParagraphStyle('Company', parent=self.styles['Normal'],
                                                fontSize=10, textColor=colors.HexColor('#555555'),
                                                spaceAfter=6, fontName='Helvetica-Oblique')
                story.append(Paragraph(f"{job['company']} | {job['duration']}", style_company))
                
                if isinstance(job['achievements'], str):
                    achievements_list = job['achievements'].split('\n')
                    for achievement in achievements_list:
                        if achievement.strip():
                            story.append(Paragraph(f"  ◉  {achievement.strip()}", self.styles['Normal']))
                elif isinstance(job['achievements'], list):
                    for achievement in job['achievements']:
                        if achievement.strip():
                            story.append(Paragraph(f"  ◉  {achievement.strip()}", self.styles['Normal']))
                else:
                    story.append(Paragraph(f"  ◉  {job['achievements']}", self.styles['Normal']))
                
                story.append(Spacer(1, 0.08 * inch))
        
        if your_data['projects']:
            story.append(self._section_title("🚀 PROJECTS", main_color))
            for project in your_data['projects']:
                style_project = ParagraphStyle('Project', parent=self.styles['Normal'],
                                                fontSize=11, textColor=main_color,
                                                spaceAfter=4, fontName='Helvetica-Bold')
                story.append(Paragraph(project['name'], style_project))
                story.append(Paragraph(project['description'], self.styles['Normal']))
                story.append(Paragraph(f"🔧 {project['technologies']}", self.styles['Italic']))
                story.append(Spacer(1, 0.08 * inch))
        
        if your_data['certifications']:
            story.append(self._section_title("🎖️ CERTIFICATIONS", main_color))
            for cert in your_data['certifications']:
                story.append(Paragraph(f"  ◉  {cert['name']} ({cert['year']})", self.styles['Normal']))
            story.append(Spacer(1, 0.1 * inch))
        
        if your_data['languages']:
            story.append(self._section_title("🗣️ LANGUAGES", main_color))
            for lang in your_data['languages']:
                story.append(Paragraph(f"  ◉  {lang['name']} - {lang['level']}", self.styles['Normal']))
            story.append(Spacer(1, 0.1 * inch))
        
        if your_data['education']:
            story.append(self._section_title("🎓 EDUCATION", main_color))
            for edu in your_data['education']:
                style_degree = ParagraphStyle('Degree', parent=self.styles['Normal'],
                                               fontSize=11, textColor=main_color,
                                               spaceAfter=3, fontName='Helvetica-Bold')
                story.append(Paragraph(edu['degree'], style_degree))
                story.append(Paragraph(f"🏫 {edu['institution']}  •  📅 {edu['year']}", self.styles['Normal']))
                story.append(Spacer(1, 0.08 * inch))
        
        if your_data['hobbies']:
            story.append(self._section_title("🎨 INTERESTS & HOBBIES", main_color))
            hobbies_text = "  ◉  ".join([h['name'] for h in your_data['hobbies']])
            story.append(Paragraph(hobbies_text, self.styles['Normal']))
            story.append(Spacer(1, 0.1 * inch))
        
        story.append(Spacer(1, 0.3 * inch))
        
        footer_text = f"✨ Generated with Resume Builder Pro | {datetime.now().strftime('%B %Y')} ✨"
        style_footer = ParagraphStyle('Footer', parent=self.styles['Normal'],
                                       fontSize=8, textColor=colors.HexColor('#999999'),
                                       alignment=1)
        story.append(Paragraph(footer_text, style_footer))
        
        doc.build(story)
        return filename
    
    def _section_title(self, text, color):
        style = ParagraphStyle(
            f'Title_{text}',
            parent=self.styles['Heading2'],
            fontSize=15,
            textColor=color,
            spaceBefore=12,
            spaceAfter=8,
            fontWeight='bold',
            fontName='Helvetica-Bold'
        )
        return Paragraph(text, style)