from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

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
            title_color = colors.HexColor('#1a5490')
            title_size = 28
        elif template == "traditional":
            title_color = colors.black
            title_size = 24
        else:
            title_color = colors.HexColor('#0d3b66')
            title_size = 26
        
        style_title = ParagraphStyle('Title', parent=self.styles['Heading1'],
                                      fontSize=title_size, textColor=title_color,
                                      spaceAfter=10, alignment=0)
        story.append(Paragraph(info.get('name', 'YOUR NAME'), style_title))
        
        contact = f"{info.get('email', '')} | {info.get('phone', '')} | {info.get('address', '')}"
        style_contact = ParagraphStyle('Contact', parent=self.styles['Normal'],
                                        fontSize=10, textColor=colors.HexColor('#666666'),
                                        spaceAfter=20, alignment=0)
        story.append(Paragraph(contact, style_contact))
        
        story.append(Spacer(1, 0.1 * inch))
        
        line = Table([[' ']], colWidths=[450])
        line.setStyle(TableStyle([('LINEABOVE', (0,0), (-1,-1), 1, title_color)]))
        story.append(line)
        story.append(Spacer(1, 0.2 * inch))
        
        if template == "modern":
            story = self._add_modern_sections(story, your_data, title_color)
        elif template == "traditional":
            story = self._add_traditional_sections(story, your_data, title_color)
        else:
            story = self._add_professional_sections(story, your_data, title_color)
        
        doc.build(story)
        return filename
    
    def _add_modern_sections(self, story, data, color):
        if data['skills']:
            story.append(self._underlined_title("PROFESSIONAL SKILLS", color))
            skills_text = " • ".join([s['name'] for s in data['skills']])
            story.append(Paragraph(skills_text, self.styles['Normal']))
            story.append(Spacer(1, 0.15 * inch))
        
        if data['experience']:
            story.append(self._underlined_title("WORK EXPERIENCE", color))
            for job in data['experience']:
                story.append(Paragraph(f"<b>{job['title']}</b>", self.styles['Normal']))
                story.append(Paragraph(f"{job['company']} | {job['duration']}", self.styles['Italic']))
                story.append(Paragraph(f"• {job['description']}", self.styles['Normal']))
                story.append(Spacer(1, 0.1 * inch))
        
        if data['education']:
            story.append(self._underlined_title("EDUCATION", color))
            for edu in data['education']:
                edu_text = f"<b>Degree:</b> {edu['degree']}<br/>"
                edu_text += f"<b>Institution:</b> {edu['institution']}<br/>"
                edu_text += f"<b>Year:</b> {edu['year']}"
                story.append(Paragraph(edu_text, self.styles['Normal']))
                story.append(Spacer(1, 0.08 * inch))
        
        return story
    
    def _add_traditional_sections(self, story, data, color):
        if data['experience']:
            story.append(self._underlined_title("WORK EXPERIENCE", color))
            for job in data['experience']:
                story.append(Paragraph(f"<b>{job['title']}</b>", self.styles['Normal']))
                story.append(Paragraph(f"{job['company']}, {job['duration']}", self.styles['Italic']))
                story.append(Paragraph(f"• {job['description']}", self.styles['Normal']))
                story.append(Spacer(1, 0.1 * inch))
        
        if data['education']:
            story.append(self._underlined_title("EDUCATION", color))
            for edu in data['education']:
                edu_text = f"<b>Degree:</b> {edu['degree']}<br/>"
                edu_text += f"<b>Institution:</b> {edu['institution']}<br/>"
                edu_text += f"<b>Year:</b> {edu['year']}"
                story.append(Paragraph(edu_text, self.styles['Normal']))
                story.append(Spacer(1, 0.08 * inch))
        
        if data['skills']:
            story.append(self._underlined_title("SKILLS", color))
            skills_text = ", ".join([s['name'] for s in data['skills']])
            story.append(Paragraph(skills_text, self.styles['Normal']))
        
        return story
    
    def _add_professional_sections(self, story, data, color):
        if data['skills']:
            story.append(self._underlined_title("CORE COMPETENCIES", color))
            skills = [s['name'] for s in data['skills']]
            half = len(skills)//2 + len(skills)%2
            col1 = skills[:half]
            col2 = skills[half:]
            table_data = []
            for i in range(max(len(col1), len(col2))):
                row = [col1[i] if i < len(col1) else "", col2[i] if i < len(col2) else ""]
                table_data.append(row)
            skill_table = Table(table_data, colWidths=[200, 200])
            skill_table.setStyle(TableStyle([
                ('FONTSIZE', (0,0), (-1,-1), 10),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('TOPPADDING', (0,0), (-1,-1), 6),
                ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ]))
            story.append(skill_table)
            story.append(Spacer(1, 0.15 * inch))
        
        if data['experience']:
            story.append(self._underlined_title("CAREER HIGHLIGHTS", color))
            for job in data['experience']:
                text = f"<b>{job['title']}</b><br/><font color='#0d3b66'>{job['company']}</font> | {job['duration']}<br/>{job['description']}"
                story.append(Paragraph(text, self.styles['Normal']))
                story.append(Spacer(1, 0.12 * inch))
        
        if data['education']:
            story.append(self._underlined_title("ACADEMIC BACKGROUND", color))
            for edu in data['education']:
                edu_text = f"<b>Degree:</b> {edu['degree']}<br/>"
                edu_text += f"<b>Institution:</b> {edu['institution']}<br/>"
                edu_text += f"<b>Year:</b> {edu['year']}"
                story.append(Paragraph(edu_text, self.styles['Normal']))
                story.append(Spacer(1, 0.08 * inch))
        
        return story
    
    def _underlined_title(self, text, color):
        style = ParagraphStyle(
            f'Underlined_{text}',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=color,
            spaceBefore=12,
            spaceAfter=6,
            fontWeight='bold',
            underline=True
        )
        return Paragraph(text, style)