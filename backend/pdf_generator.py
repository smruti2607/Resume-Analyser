from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from io import BytesIO
from reportlab.lib.enums import TA_LEFT

def generate_resume_pdf(resume_text: str, filename: str = "optimized_resume.pdf") -> BytesIO:
    """Generate a PDF from resume text."""

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)

    styles = getSampleStyleSheet()
    story = []

    custom_style = ParagraphStyle(
        'CustomStyle',
        parent=styles['Normal'],
        fontSize=10,
        leading=12,
        leftIndent=0.25*inch,
        rightIndent=0.25*inch,
        alignment=TA_LEFT
    )

    resume_lines = resume_text.split('\n')

    for line in resume_lines:
        if line.strip():
            if line.isupper() and len(line) < 50:
                section_style = ParagraphStyle(
                    'SectionStyle',
                    parent=styles['Heading1'],
                    fontSize=12,
                    textColor='#1f3a93',
                    spaceAfter=6,
                    spaceBefore=12,
                    fontName='Helvetica-Bold'
                )
                story.append(Paragraph(line.strip(), section_style))
            else:
                story.append(Paragraph(line.strip(), custom_style))
            story.append(Spacer(1, 0.05*inch))

    doc.build(story)
    buffer.seek(0)
    return buffer
