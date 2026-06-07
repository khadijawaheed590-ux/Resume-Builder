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
        
        if template == "modern":
            main_color = colors.HexColor('#1a5490')
            accent_color = colors.HexColor('#2c3e50')
            sidebar_color = colors.HexColor('#e8f4f8')
            border_color = colors.HexColor('#1a5490')
        elif template == "traditional":
            main_color = colors.black
            accent_color = colors.black
            sidebar_color = colors.HexColor('#f5f5f5')
            border_color = colors.black
        else:
            main_color = colors.HexColor('#0d3b66')
            accent_color = colors.HexColor('#1a5490')
            sidebar_color = colors.HexColor('#e8f0f8')
            border_color = colors.HexColor('#0d3b66')
        
        left_column = []
        right_column = []
        info = your_data['personal']
        
        style_name = ParagraphStyle('Name', parent=self.styles['Heading1'],
                                      fontSize=22, textColor=main_color,
                                      spaceAfter=8, fontName='Helvetica-Bold')
        right_column.append(Paragraph(info.get('name', 'YOUR NAME'), style_name))
        
        contact = f"{info.get('email', '')}   |   {info.get('phone', '')}   |   {info.get('address', '')}"
        style_contact = ParagraphStyle('Contact', parent=self.styles['Normal'],
                                        fontSize=8, textColor=colors.HexColor('#666666'),
                                        spaceAfter=15)
        right_column.append(Paragraph(contact, style_contact))
        
        if your_data.get('summary'):
            right_column.append(self._main_heading("PROFILE SUMMARY", main_color))
            right_column.append(Paragraph(your_data['summary'], self.styles['Normal']))
            right_column.append(Spacer(1, 0.08 * inch))
        
        if your_data['experience']:
            right_column.append(self._main_heading("WORK EXPERIENCE", main_color))
            for job in your_data['experience']:
                right_column.append(self._sub_heading(f"▸ {job['title']}", accent_color))
                right_column.append(Paragraph(f"■ {job['company']}  |  ● {job['duration']}", self.styles['Italic']))
                achievements = job.get('achievements', '')
                if achievements:
                    if isinstance(achievements, str):
                        for line in achievements.split('\n'):
                            if line.strip():
                                right_column.append(Paragraph(f"   • {line.strip()}", self.styles['Normal']))
                right_column.append(Spacer(1, 0.06 * inch))
        
        if your_data['projects']:
            right_column.append(self._main_heading("PROJECTS", main_color))
            for project in your_data['projects']:
                right_column.append(self._sub_heading(f"▸ {project['name']}", accent_color))
                right_column.append(Paragraph(f"■ {project['technologies']}", self.styles['Italic']))
                right_column.append(Spacer(1, 0.06 * inch))
        
        if your_data['education']:
            right_column.append(self._main_heading("EDUCATION", main_color))
            for edu in your_data['education']:
                right_column.append(self._sub_heading(f"▸ {edu['degree']}", accent_color))
                right_column.append(Paragraph(f"■ {edu['institution']}  |  ● {edu['year']}", self.styles['Normal']))
                if edu.get('gpa'):
                    right_column.append(Paragraph(f"   ★ GPA: {edu['gpa']}", self.styles['Italic']))
                right_column.append(Spacer(1, 0.06 * inch))
        
        left_column.append(self._sidebar_heading("CONTACT", main_color))
        left_column.append(Paragraph(f"✉ {info.get('email', '')}", self.styles['Normal']))
        left_column.append(Paragraph(f"☎ {info.get('phone', '')}", self.styles['Normal']))
        left_column.append(Paragraph(f"⌂ {info.get('address', '')}", self.styles['Normal']))
        left_column.append(Spacer(1, 0.1 * inch))
        
        if your_data['skills']:
            left_column.append(self._sidebar_heading("SKILLS", main_color))
            for skill in your_data['skills']:
                left_column.append(Paragraph(f"▸ {skill['name']}", self.styles['Normal']))
            left_column.append(Spacer(1, 0.08 * inch))
        
        if your_data['languages']:
            left_column.append(self._sidebar_heading("LANGUAGES", main_color))
            for lang in your_data['languages']:
                left_column.append(Paragraph(f"▸ {lang['name']}  ★ {lang['level']}", self.styles['Normal']))
            left_column.append(Spacer(1, 0.08 * inch))
        
        if your_data['certifications']:
            left_column.append(self._sidebar_heading("CERTIFICATIONS", main_color))
            for cert in your_data['certifications']:
                left_column.append(Paragraph(f"▸ {cert['name']}  ● {cert['year']}", self.styles['Normal']))
            left_column.append(Spacer(1, 0.08 * inch))
        
        if your_data['hobbies']:
            left_column.append(self._sidebar_heading("INTERESTS", main_color))
            hobbies_text = "  ▸  ".join([h['name'] for h in your_data['hobbies']])
            left_column.append(Paragraph(hobbies_text, self.styles['Normal']))
            left_column.append(Spacer(1, 0.08 * inch))
        
        left_table = Table([[content] for content in left_column], colWidths=[180])
        left_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), sidebar_color),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('BOX', (0, 0), (-1, -1), 0.5, border_color),
        ]))
        
        right_table = Table([[content] for content in right_column], colWidths=[380])
        right_table.setStyle(TableStyle([
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
            ('LEFTPADDING', (0, 0), (-1, -1), 15),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('BOX', (0, 0), (-1, -1), 0.5, border_color),
        ]))
        
        main_table = Table([[left_table, right_table]], colWidths=[200, 400])
        main_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ]))
        
        story = [main_table]
        
        footer_text = f"★ Generated with Resume Builder Pro • {datetime.now().strftime('%B %Y')} ★"
        style_footer = ParagraphStyle('Footer', parent=self.styles['Normal'],
                                       fontSize=8, textColor=colors.HexColor('#999999'),
                                       alignment=1)
        story.append(Spacer(1, 0.2 * inch))
        story.append(Paragraph(footer_text, style_footer))
        
        doc.build(story)
        return filename
    
    def _main_heading(self, text, color):
        style = ParagraphStyle(
            f'Main_{text}',
            parent=self.styles['Heading2'],
            fontSize=13,
            textColor=color,
            spaceBefore=10,
            spaceAfter=5,
            fontWeight='bold',
            fontName='Helvetica-Bold',
            underline=True
        )
        return Paragraph(text, style)
    
    def _sub_heading(self, text, color):
        style = ParagraphStyle(
            f'Sub_{text}',
            parent=self.styles['Heading3'],
            fontSize=11,
            textColor=color,
            spaceBefore=6,
            spaceAfter=3,
            fontWeight='bold',
            fontName='Helvetica-Bold'
        )
        return Paragraph(text, style)
    
    def _sidebar_heading(self, text, color):
        style = ParagraphStyle(
            f'Sidebar_{text}',
            parent=self.styles['Heading2'],
            fontSize=11,
            textColor=color,
            spaceBefore=8,
            spaceAfter=4,
            fontWeight='bold',
            fontName='Helvetica-Bold',
            underline=True
        )
        return Paragraph(text, style)