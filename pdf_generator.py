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
        
        if template == "modern":
            return self._modern(your_data, filename)
        elif template == "traditional":
            return self._traditional(your_data, filename)
        elif template == "professional":
            return self._professional(your_data, filename)
        else:
            return self._modern(your_data, filename)
    
    def _modern(self, data, filename):
        doc = SimpleDocTemplate(filename, pagesize=letter)
        story = []
        info = data['personal']
        
        self.styles.add(ParagraphStyle(
            'H1', parent=self.styles['Heading1'], fontSize=28,
            textColor=colors.HexColor('#1a5490'), spaceAfter=10
        ))
        story.append(Paragraph(info.get('name', 'YOUR NAME'), self.styles['H1']))
        
        contact = f"{info.get('email', '')} | {info.get('phone', '')} | {info.get('address', '')}"
        self.styles.add(ParagraphStyle('C', parent=self.styles['Normal'], fontSize=10,
                    textColor=colors.HexColor('#666666'), spaceAfter=20))
        story.append(Paragraph(contact, self.styles['C']))
        
        line = Table([[' ']], colWidths=[450])
        line.setStyle(TableStyle([('LINEABOVE', (0,0), (-1,-1), 1, colors.HexColor('#1a5490'))]))
        story.append(line)
        
        if data['skills']:
            self.styles.add(ParagraphStyle('S', parent=self.styles['Heading2'], fontSize=14,
                        textColor=colors.HexColor('#1a5490'), spaceBefore=12, fontWeight='bold'))
            story.append(Paragraph("SKILLS", self.styles['S']))
            skills_text = " • ".join([s['name'] for s in data['skills']])
            story.append(Paragraph(skills_text, self.styles['Normal']))
            story.append(Spacer(1, 0.1*inch))
        
        if data['experience']:
            story.append(Paragraph("WORK EXPERIENCE", self.styles['S']))
            for job in data['experience']:
                story.append(Paragraph(f"<b>{job['title']}</b>", self.styles['Normal']))
                story.append(Paragraph(f"{job['company']} | {job['duration']}", self.styles['Italic']))
                story.append(Paragraph(job['description'], self.styles['Normal']))
                story.append(Spacer(1, 0.1*inch))
        
        if data['education']:
            story.append(Paragraph("EDUCATION", self.styles['S']))
            for edu in data['education']:
                story.append(Paragraph(f"<b>{edu['degree']}</b>", self.styles['Normal']))
                story.append(Paragraph(f"{edu['institution']} - {edu['year']}", self.styles['Normal']))
        
        doc.build(story)
        return filename
    
    def _traditional(self, data, filename):
        doc = SimpleDocTemplate(filename, pagesize=letter)
        story = []
        info = data['personal']
        
        self.styles.add(ParagraphStyle(
            'H1', parent=self.styles['Heading1'], fontSize=24,
            textColor=colors.black, alignment=1, spaceAfter=5
        ))
        story.append(Paragraph(info.get('name', 'YOUR NAME'), self.styles['H1']))
        
        contact = f"{info.get('email', '')}  •  {info.get('phone', '')}  •  {info.get('address', '')}"
        story.append(Paragraph(contact, self.styles['Normal']))
        story.append(Spacer(1, 0.1*inch))
        
        line = Table([[' ']], colWidths=[450])
        line.setStyle(TableStyle([('LINEABOVE', (0,0), (-1,-1), 1, colors.black)]))
        story.append(line)
        
        self.styles.add(ParagraphStyle('S', parent=self.styles['Heading2'], fontSize=14,
                    textColor=colors.black, spaceBefore=12, fontWeight='bold'))
        
        if data['experience']:
            story.append(Paragraph("WORK EXPERIENCE", self.styles['S']))
            for job in data['experience']:
                story.append(Paragraph(f"<b>{job['title']}</b>", self.styles['Normal']))
                story.append(Paragraph(f"{job['company']}, {job['duration']}", self.styles['Italic']))
                story.append(Paragraph(f"  • {job['description']}", self.styles['Normal']))
                story.append(Spacer(1, 0.1*inch))
        
        if data['education']:
            story.append(Paragraph("EDUCATION", self.styles['S']))
            for edu in data['education']:
                story.append(Paragraph(f"<b>{edu['degree']}</b>", self.styles['Normal']))
                story.append(Paragraph(f"{edu['institution']}, {edu['year']}", self.styles['Normal']))
        
        if data['skills']:
            story.append(Paragraph("SKILLS", self.styles['S']))
            skills_text = ", ".join([s['name'] for s in data['skills']])
            story.append(Paragraph(skills_text, self.styles['Normal']))
        
        doc.build(story)
        return filename
    
    def _professional(self, data, filename):
        doc = SimpleDocTemplate(filename, pagesize=letter)
        story = []
        info = data['personal']
        
        self.styles.add(ParagraphStyle(
            'H1', parent=self.styles['Heading1'], fontSize=26,
            textColor=colors.HexColor('#0d3b66'), spaceAfter=5
        ))
        story.append(Paragraph(info.get('name', 'YOUR NAME'), self.styles['H1']))
        story.append(Paragraph("Professional Resume", self.styles['Normal']))
        story.append(Spacer(1, 0.1*inch))
        
        self.styles.add(ParagraphStyle('S', parent=self.styles['Heading2'], fontSize=14,
                    textColor=colors.HexColor('#0d3b66'), spaceBefore=12, fontWeight='bold'))
        
        if data['skills']:
            story.append(Paragraph("KEY SKILLS", self.styles['S']))
            skills = [s['name'] for s in data['skills']]
            half = len(skills)//2 + len(skills)%2
            col1 = skills[:half]
            col2 = skills[half:]
            table_data = []
            for i in range(max(len(col1), len(col2))):
                row = [col1[i] if i < len(col1) else "", col2[i] if i < len(col2) else ""]
                table_data.append(row)
            skill_table = Table(table_data, colWidths=[200, 200])
            skill_table.setStyle(TableStyle([('FONTSIZE', (0,0), (-1,-1), 10)]))
            story.append(skill_table)
            story.append(Spacer(1, 0.1*inch))
        
        if data['experience']:
            story.append(Paragraph("CAREER HIGHLIGHTS", self.styles['S']))
            for job in data['experience']:
                text = f"<b>{job['title']}</b><br/><font color='#0d3b66'>{job['company']}</font> | {job['duration']}<br/>{job['description']}"
                story.append(Paragraph(text, self.styles['Normal']))
                story.append(Spacer(1, 0.1*inch))
        
        if data['education']:
            story.append(Paragraph("EDUCATION", self.styles['S']))
            for edu in data['education']:
                story.append(Paragraph(f"<b>{edu['degree']}</b>", self.styles['Normal']))
                story.append(Paragraph(f"{edu['institution']} • {edu['year']}", self.styles['Normal']))
        
        doc.build(story)
        return filename