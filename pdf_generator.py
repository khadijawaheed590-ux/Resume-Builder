from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
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
        elif template == "traditional":
            main_color = colors.black
        else:
            main_color = colors.HexColor('#0d3b66')
        
        style_name = ParagraphStyle('Name', parent=self.styles['Heading1'],
                                      fontSize=28, textColor=main_color,
                                      spaceAfter=8, alignment=0, fontName='Helvetica-Bold')
        story.append(Paragraph(f"✨ {info.get('name', 'YOUR NAME')} ✨", style_name))
        
        contact = f"📧 {info.get('email', '')}   📞 {info.get('phone', '')}   📍 {info.get('address', '')}"
        style_contact = ParagraphStyle('Contact', parent=self.styles['Normal'],
                                        fontSize=9, textColor=colors.HexColor('#666666'),
                                        spaceAfter=15, alignment=0)
        story.append(Paragraph(contact, style_contact))
        
        story.append(Spacer(1, 0.05 * inch))
        
        if your_data.get('summary'):
            story.append(self._main_heading("📋 PROFILE SUMMARY", main_color))
            story.append(Paragraph(f"💬 {your_data['summary']}", self.styles['Normal']))
            story.append(Spacer(1, 0.1 * inch))
        
        if your_data['skills']:
            story.append(self._main_heading("💡 TECHNICAL SKILLS", main_color))
            skills_text = "  •  ".join([s['name'] for s in your_data['skills']])
            story.append(Paragraph(f"⚡ {skills_text}", self.styles['Normal']))
            story.append(Spacer(1, 0.1 * inch))
        
        if your_data['experience']:
            story.append(self._main_heading("💼 WORK EXPERIENCE", main_color))
            for job in your_data['experience']:
                story.append(self._sub_heading(f"🎯 {job['title']}", main_color))
                story.append(Paragraph(f"🏢 {job['company']}  |  📅 {job['duration']}", self.styles['Italic']))
                achievements = job.get('achievements', '')
                if achievements:
                    if isinstance(achievements, str):
                        for line in achievements.split('\n'):
                            if line.strip():
                                story.append(Paragraph(f"   • {line.strip()}", self.styles['Normal']))
                    elif isinstance(achievements, list):
                        for item in achievements:
                            if item.strip():
                                story.append(Paragraph(f"   • {item.strip()}", self.styles['Normal']))
                story.append(Spacer(1, 0.08 * inch))
        
        if your_data['projects']:
            story.append(self._main_heading("🚀 PROJECTS", main_color))
            for project in your_data['projects']:
                story.append(self._sub_heading(f"📁 {project['name']}", main_color))
                story.append(Paragraph(f"🔧 {project['technologies']}", self.styles['Italic']))
                story.append(Spacer(1, 0.08 * inch))
        
        if your_data['certifications']:
            story.append(self._main_heading("🎖️ CERTIFICATIONS", main_color))
            for cert in your_data['certifications']:
                story.append(Paragraph(f"   • {cert['name']}  📅 {cert['year']}", self.styles['Normal']))
            story.append(Spacer(1, 0.08 * inch))
        
        if your_data['languages']:
            story.append(self._main_heading("🗣️ LANGUAGES", main_color))
            for lang in your_data['languages']:
                story.append(Paragraph(f"   • {lang['name']}  🌟 {lang['level']}", self.styles['Normal']))
            story.append(Spacer(1, 0.08 * inch))
        
        if your_data['education']:
            story.append(self._main_heading("🎓 EDUCATION", main_color))
            for edu in your_data['education']:
                story.append(self._sub_heading(f"📖 {edu['degree']}", main_color))
                story.append(Paragraph(f"🏫 {edu['institution']}  •  📅 {edu['year']}", self.styles['Normal']))
                story.append(Spacer(1, 0.08 * inch))
        
        if your_data['hobbies']:
            story.append(self._main_heading("🎨 INTERESTS", main_color))
            hobbies_text = "  •  ".join([h['name'] for h in your_data['hobbies']])
            story.append(Paragraph(f"✨ {hobbies_text}", self.styles['Normal']))
            story.append(Spacer(1, 0.08 * inch))
        
        story.append(Spacer(1, 0.3 * inch))
        
        footer_text = f"✨ Generated with Resume Builder Pro • {datetime.now().strftime('%B %Y')} ✨"
        style_footer = ParagraphStyle('Footer', parent=self.styles['Normal'],
                                       fontSize=8, textColor=colors.HexColor('#999999'),
                                       alignment=1)
        story.append(Paragraph(footer_text, style_footer))
        
        doc.build(story)
        return filename
    
    def _main_heading(self, text, color):
        style = ParagraphStyle(
            f'MainHeading_{text}',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=color,
            spaceBefore=12,
            spaceAfter=6,
            fontWeight='bold',
            fontName='Helvetica-Bold',
            underline=True
        )
        return Paragraph(text, style)
    
    def _sub_heading(self, text, color):
        style = ParagraphStyle(
            f'SubHeading_{text}',
            parent=self.styles['Heading3'],
            fontSize=12,
            textColor=color,
            spaceBefore=8,
            spaceAfter=4,
            fontWeight='bold',
            fontName='Helvetica-Bold'
        )
        return Paragraph(text, style)