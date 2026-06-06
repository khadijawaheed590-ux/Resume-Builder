from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

class PDFResumeGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
    
    def make_resume(self, your_data, filename="my_resume.pdf", style="modern"):
        if style == "modern":
            return self._make_modern_resume(your_data, filename)
        elif style == "traditional":
            return self._make_traditional_resume(your_data, filename)
        elif style == "professional":
            return self._make_professional_resume(your_data, filename)
        else:
            return self._make_modern_resume(your_data, filename)
    
    def _make_modern_resume(self, data, filename):
        doc = SimpleDocTemplate(filename, pagesize=letter)
        story = []
        info = data['personal']
        
        self.styles.add(ParagraphStyle(
            name='BigBlueName',
            parent=self.styles['Heading1'],
            fontSize=28,
            textColor=colors.HexColor('#1a5490'),
            alignment=0
        ))
        story.append(Paragraph(info.get('name', 'YOUR NAME'), self.styles['BigBlueName']))
        
        contact = f"{info.get('email', '')}  |  {info.get('phone', '')}  |  {info.get('address', '')}"
        self.styles.add(ParagraphStyle(
            name='GrayContact',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#666666'),
            spaceAfter=20
        ))
        story.append(Paragraph(contact, self.styles['GrayContact']))
        
        blue_line = Table([[' ']], colWidths=[450])
        blue_line.setStyle(TableStyle([('LINEABOVE', (0, 0), (-1, -1), 1, colors.HexColor('#1a5490'))]))
        story.append(blue_line)
        
        if data['skills']:
            story.append(self._make_section_title("CORE SKILLS", '#1a5490'))
            skills_text = " • ".join([s['name'] for s in data['skills']])
            story.append(Paragraph(skills_text, self.styles['Normal']))
            story.append(Spacer(1, 0.1 * inch))
        
        if data['experience']:
            story.append(self._make_section_title("WORK EXPERIENCE", '#1a5490'))
            for job in data['experience']:
                story.append(Paragraph(f"<b>{job['title']}</b>", self.styles['Normal']))
                story.append(Paragraph(f"{job['company']} | {job['duration']}", self.styles['Italic']))
                story.append(Paragraph(job['description'], self.styles['Normal']))
                story.append(Spacer(1, 0.1 * inch))
        
        if data['education']:
            story.append(self._make_section_title("EDUCATION", '#1a5490'))
            for edu in data['education']:
                story.append(Paragraph(f"<b>{edu['degree']}</b>", self.styles['Normal']))
                story.append(Paragraph(f"{edu['institution']} - {edu['year']}", self.styles['Normal']))
                story.append(Spacer(1, 0.05 * inch))
        
        doc.build(story)
        return filename
    
    def _make_traditional_resume(self, data, filename):
        doc = SimpleDocTemplate(filename, pagesize=letter)
        story = []
        info = data['personal']
        
        self.styles.add(ParagraphStyle(
            name='CenterName',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.black,
            alignment=1
        ))
        story.append(Paragraph(info.get('name', 'YOUR NAME'), self.styles['CenterName']))
        
        contact = f"{info.get('email', '')}  •  {info.get('phone', '')}  •  {info.get('address', '')}"
        story.append(Paragraph(contact, self.styles['Normal']))
        story.append(Spacer(1, 0.1 * inch))
        
        black_line = Table([[' ']], colWidths=[450])
        black_line.setStyle(TableStyle([('LINEABOVE', (0, 0), (-1, -1), 1, colors.black)]))
        story.append(black_line)
        
        if data['experience']:
            story.append(self._make_section_title("WORK HISTORY", colors.black))
            for job in data['experience']:
                story.append(Paragraph(f"<b>{job['title']}</b>", self.styles['Normal']))
                story.append(Paragraph(f"{job['company']}, {job['duration']}", self.styles['Italic']))
                story.append(Paragraph(f"  • {job['description']}", self.styles['Normal']))
                story.append(Spacer(1, 0.1 * inch))
        
        if data['education']:
            story.append(self._make_section_title("EDUCATION", colors.black))
            for edu in data['education']:
                story.append(Paragraph(f"<b>{edu['degree']}</b>", self.styles['Normal']))
                story.append(Paragraph(f"{edu['institution']}, {edu['year']}", self.styles['Normal']))
        
        if data['skills']:
            story.append(self._make_section_title("SKILLS", colors.black))
            skills_text = ", ".join([s['name'] for s in data['skills']])
            story.append(Paragraph(skills_text, self.styles['Normal']))
        
        doc.build(story)
        return filename
    
    def _make_professional_resume(self, data, filename):
        doc = SimpleDocTemplate(filename, pagesize=letter)
        story = []
        info = data['personal']
        
        self.styles.add(ParagraphStyle(
            name='ExecutiveName',
            parent=self.styles['Heading1'],
            fontSize=26,
            textColor=colors.HexColor('#0d3b66'),
            alignment=0
        ))
        story.append(Paragraph(info.get('name', 'YOUR NAME'), self.styles['ExecutiveName']))
        story.append(Paragraph("Professional Resume", self.styles['Normal']))
        story.append(Spacer(1, 0.1 * inch))
        
        if data['skills']:
            story.append(self._make_section_title("KEY SKILLS", '#0d3b66'))
            skills = [s['name'] for s in data['skills']]
            half = len(skills)//2 + len(skills)%2
            col1 = skills[:half]
            col2 = skills[half:]
            
            table_data = []
            for i in range(max(len(col1), len(col2))):
                row = []
                row.append(col1[i] if i < len(col1) else "")
                row.append(col2[i] if i < len(col2) else "")
                table_data.append(row)
            
            skill_table = Table(table_data, colWidths=[200, 200])
            skill_table.setStyle(TableStyle([
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))
            story.append(skill_table)
            story.append(Spacer(1, 0.1 * inch))
        
        if data['experience']:
            story.append(self._make_section_title("CAREER HIGHLIGHTS", '#0d3b66'))
            for job in data['experience']:
                exp_text = f"<b>{job['title']}</b><br/>"
                exp_text += f"<font color='#0d3b66'>{job['company']}</font> | {job['duration']}<br/>"
                exp_text += f"{job['description']}"
                story.append(Paragraph(exp_text, self.styles['Normal']))
                story.append(Spacer(1, 0.1 * inch))
        
        if data['education']:
            story.append(self._make_section_title("EDUCATION", '#0d3b66'))
            for edu in data['education']:
                story.append(Paragraph(f"<b>{edu['degree']}</b>", self.styles['Normal']))
                story.append(Paragraph(f"{edu['institution']} • {edu['year']}", self.styles['Normal']))
        
        doc.build(story)
        return filename
    
    def _make_section_title(self, title_text, color_code):
        self.styles.add(ParagraphStyle(
            name=f'Title_{title_text}',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=color_code,
            spaceBefore=12,
            spaceAfter=6,
            fontWeight='bold'
        ))
        return Paragraph(title_text, self.styles[f'Title_{title_text}'])