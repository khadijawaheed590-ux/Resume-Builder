
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime
import os

class PDFResumeGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_beautiful_styles()
    
    def _setup_beautiful_styles(self):
        # Professional Header Style
        self.styles.add(ParagraphStyle(
            name='BeautifulHeader',
            parent=self.styles['Heading1'],
            fontSize=28,
            textColor=colors.HexColor('#1a5490'),
            spaceAfter=20,
            alignment=0,
            fontName='Helvetica-Bold'
        ))
        
        # Contact Info Style
        self.styles.add(ParagraphStyle(
            name='ContactInfo',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#666666'),
            spaceAfter=15,
            alignment=0
        ))
        
        # Section Title Style (Beautiful Blue)
        self.styles.add(ParagraphStyle(
            name='BeautifulSection',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#1a5490'),
            spaceBefore=20,
            spaceAfter=10,
            fontWeight='bold',
            borderPadding=5,
            fontName='Helvetica-Bold'
        ))
        
        # Job Title Style
        self.styles.add(ParagraphStyle(
            name='JobTitle',
            parent=self.styles['Normal'],
            fontSize=12,
            textColor=colors.HexColor('#333333'),
            spaceAfter=5,
            fontWeight='bold'
        ))
        
        # Company Style
        self.styles.add(ParagraphStyle(
            name='CompanyName',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#1a5490'),
            spaceAfter=3,
            fontName='Helvetica-Oblique'
        ))
        
        # Description Style
        self.styles.add(ParagraphStyle(
            name='Description',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#444444'),
            spaceAfter=8,
            leftIndent=20
        ))
        
        # Skill Badge Style
        self.styles.add(ParagraphStyle(
            name='SkillStyle',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#1a5490'),
            backColor=colors.HexColor('#e8f4f8'),
            spaceAfter=5,
            leftIndent=10
        ))
    
    def generate_resume(self, resume_data, output_filename="professional_resume.pdf", photo_path=None):
        doc = SimpleDocTemplate(
            output_filename,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72,
            title="Professional Resume"
        )
        
        story = []
        
        # Add Header with Name
        personal = resume_data['personal']
        name = personal.get('name', 'YOUR NAME')
        story.append(Paragraph(name.upper(), self.styles['BeautifulHeader']))
        
        # Add Contact Information
        contact_text = self._format_contact(personal)
        story.append(Paragraph(contact_text, self.styles['ContactInfo']))
        story.append(Spacer(1, 0.2 * inch))
        
        # Add Divider Line
        story.append(self._add_divider())
        story.append(Spacer(1, 0.1 * inch))
        
        # Add Profile Summary
        story.append(Paragraph("PROFESSIONAL SUMMARY", self.styles['BeautifulSection']))
        summary = personal.get('summary', 'Dedicated professional with strong skills and passion for excellence.')
        story.append(Paragraph(summary, self.styles['Description']))
        story.append(Spacer(1, 0.1 * inch))
        
        # Add Skills Section (Beautiful Layout)
        if resume_data['skills']:
            story.append(Paragraph("CORE COMPETENCIES", self.styles['BeautifulSection']))
            skills_text = self._format_skills_beautifully(resume_data['skills'])
            story.append(Paragraph(skills_text, self.styles['SkillStyle']))
            story.append(Spacer(1, 0.1 * inch))
        
        # Add Experience Section
        if resume_data['experience']:
            story.append(Paragraph("WORK EXPERIENCE", self.styles['BeautifulSection']))
            for exp in resume_data['experience']:
                story.append(Paragraph(exp['title'], self.styles['JobTitle']))
                story.append(Paragraph(f"{exp['company']} | {exp['duration']}", self.styles['CompanyName']))
                story.append(Paragraph(exp['description'], self.styles['Description']))
                story.append(Spacer(1, 0.05 * inch))
        
        # Add Education Section
        if resume_data['education']:
            story.append(Paragraph("EDUCATION", self.styles['BeautifulSection']))
            for edu in resume_data['education']:
                edu_text = f"<b>{edu['degree']}</b><br/>{edu['institution']} - {edu['year']}"
                if edu.get('grade'):
                    edu_text += f"<br/><i>Grade: {edu['grade']}</i>"
                story.append(Paragraph(edu_text, self.styles['Description']))
                story.append(Spacer(1, 0.05 * inch))
        
        # Add Footer
        story.append(Spacer(1, 0.5 * inch))
        story.append(self._add_footer())
        
        # Build PDF
        doc.build(story)
        return output_filename
    
    def _format_contact(self, personal):
        parts = []
        if personal.get('email'):
            parts.append(f"✉ {personal['email']}")
        if personal.get('phone'):
            parts.append(f"📞 {personal['phone']}")
        if personal.get('address'):
            parts.append(f"📍 {personal['address']}")
        return " | ".join(parts)
    
    def _format_skills_beautifully(self, skills):
        skill_names = [skill['name'] if isinstance(skill, dict) else skill for skill in skills]
        return " • ".join(skill_names)
    
    def _add_divider(self):
        from reportlab.platypus import Table
        divider = Table([[' ']], colWidths=[450])
        divider.setStyle(TableStyle([
            ('LINEABOVE', (0, 0), (-1, -1), 1, colors.HexColor('#1a5490')),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
        ]))
        return divider
    
    def _add_footer(self):
        from reportlab.platypus import Table
        current_date = datetime.now().strftime("%B %Y")
        footer_text = f"Generated with Resume Builder | {current_date}"
        footer = Table([[footer_text]], colWidths=[450])
        footer.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#999999')),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
        ]))
        return footer