import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm, inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image, KeepTogether
)
from reportlab.pdfgen import canvas

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "report_assets")
PDF_PATH = os.path.join(os.path.dirname(__file__), "StockSphere_Project_Report.pdf")

# Page dimensions: A4 = 210 x 297 mm
PAGE_WIDTH, PAGE_HEIGHT = A4

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_footer(num_pages)
            super().showPage()
        super().save()

    def draw_footer(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 10)
        self.setFillColor(colors.HexColor("#2d3748"))
        # Draw bottom footer "Page X"
        self.drawCentredString(PAGE_WIDTH / 2.0, 14 * mm, f"Page {self._pageNumber}")
        self.restoreState()

def create_report():
    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=A4,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        topMargin=16 * mm,
        bottomMargin=20 * mm
    )

    styles = getSampleStyleSheet()

    # Custom typography matching university academic reports
    t_center = ParagraphStyle('TCenter', fontName='Helvetica-Bold', fontSize=14, leading=18, alignment=1, textColor=colors.HexColor('#1a202c'))
    t_univ = ParagraphStyle('TUniv', fontName='Helvetica-Bold', fontSize=16, leading=20, alignment=1, textColor=colors.HexColor('#1a365d'))
    t_rajkot = ParagraphStyle('TRajkot', fontName='Helvetica-Bold', fontSize=13, leading=17, alignment=1, textColor=colors.HexColor('#2b6cb0'))
    t_rep_on = ParagraphStyle('TRepOn', fontName='Helvetica', fontSize=11, leading=15, alignment=1, textColor=colors.HexColor('#4a5568'))
    t_proj_title = ParagraphStyle('TProjTitle', fontName='Helvetica-Bold', fontSize=14, leading=19, alignment=1, textColor=colors.HexColor('#1a202c'))
    t_sub = ParagraphStyle('TSub', fontName='Helvetica', fontSize=11, leading=15, alignment=1, textColor=colors.HexColor('#2d3748'))
    t_sub_bold = ParagraphStyle('TSubBold', fontName='Helvetica-Bold', fontSize=12, leading=16, alignment=1, textColor=colors.HexColor('#1a202c'))

    # Headings
    h_chap = ParagraphStyle('HChap', fontName='Helvetica-Bold', fontSize=13, leading=17, alignment=1, spaceAfter=4, textColor=colors.HexColor('#1a202c'))
    h_chap_title = ParagraphStyle('HChapTitle', fontName='Helvetica-Bold', fontSize=14, leading=18, alignment=1, spaceAfter=14, textColor=colors.HexColor('#1a202c'))
    h1 = ParagraphStyle('H1', fontName='Helvetica-Bold', fontSize=11, leading=15, spaceBefore=8, spaceAfter=4, textColor=colors.HexColor('#1a365d'))
    h2 = ParagraphStyle('H2', fontName='Helvetica-Bold', fontSize=10, leading=14, spaceBefore=6, spaceAfter=3, textColor=colors.HexColor('#2b6cb0'))
    body = ParagraphStyle('Body', fontName='Helvetica', fontSize=9.5, leading=13.5, spaceAfter=6, textColor=colors.HexColor('#2d3748'), alignment=4) # Justified
    bullet = ParagraphStyle('Bullet', fontName='Helvetica', fontSize=9.5, leading=13.5, spaceAfter=4, leftIndent=14, firstLineIndent=-10, textColor=colors.HexColor('#2d3748'))

    # Table styles
    th = ParagraphStyle('TH', fontName='Helvetica-Bold', fontSize=9, leading=11, alignment=0, textColor=colors.HexColor('#1a202c'))
    td = ParagraphStyle('TD', fontName='Helvetica', fontSize=8.5, leading=11, alignment=0, textColor=colors.HexColor('#2d3748'))
    td_code = ParagraphStyle('TDCode', fontName='Courier', fontSize=8, leading=10, alignment=0, textColor=colors.HexColor('#2b6cb0'))

    # Caption
    caption = ParagraphStyle('Caption', fontName='Helvetica-Oblique', fontSize=9, leading=12, alignment=1, spaceBefore=6, spaceAfter=6, textColor=colors.HexColor('#4a5568'))

    tbl_grid_style = TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#a0aec0')),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#edf2f7')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ])

    # Index table styles
    idx_th = ParagraphStyle('IdxTH', fontName='Helvetica-Bold', fontSize=8.5, leading=10, alignment=0, textColor=colors.HexColor('#1a202c'))
    idx_td = ParagraphStyle('IdxTD', fontName='Helvetica', fontSize=8, leading=9.5, alignment=0, textColor=colors.HexColor('#2d3748'))
    idx_grid_style = TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#a0aec0')),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#edf2f7')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 1.8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.8),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ])

    story = []

    # ════════════════════════════════════════════════════════════════
    # PAGE 1: TITLE PAGE
    # ════════════════════════════════════════════════════════════════
    story.append(Paragraph("ATMIYA UNIVERSITY", t_univ))
    story.append(Spacer(1, 2*mm))
    story.append(Paragraph("RAJKOT", t_rajkot))
    story.append(Spacer(1, 5*mm))

    logo_path = os.path.join(ASSETS_DIR, "atmiya_logo.png")
    if os.path.exists(logo_path):
        story.append(Image(logo_path, width=1.9*inch, height=1.9*inch))
    story.append(Spacer(1, 5*mm))

    story.append(Paragraph("A<br/>Report On", t_rep_on))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph("StockSphere: Virtual Stock Trading &amp; AI-Powered Market Forecasting System with Explainable AI", t_proj_title))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph("Under subject of", t_rep_on))
    story.append(Spacer(1, 2*mm))
    story.append(Paragraph("MINI PROJECT", t_sub_bold))
    story.append(Spacer(1, 2*mm))
    story.append(Paragraph("B.TECH, Semester – VII<br/>(Computer Engineering)", t_sub))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Submitted by:", ParagraphStyle('SubBy', fontName='Helvetica-Bold', fontSize=10, leading=14, alignment=1)))
    story.append(Spacer(1, 2*mm))
    story.append(Paragraph("Kavy Gami [Enrollment No. 1]<br/>[STUDENT NAME 2] [ENROLLMENT NO. 2]", t_sub_bold))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Prof. [GUIDE NAME]<br/><font size=9 color='#4a5568'>(Faculty Guide)</font>", t_sub_bold))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph("Prof. Tosal M. Bhalodia<br/><font size=9 color='#4a5568'>(Head of the Department)</font>", t_sub_bold))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph("Academic Year<br/>(2026-27)", t_sub_bold))
    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════
    # PAGE 2: CANDIDATE’S DECLARATION
    # ════════════════════════════════════════════════════════════════
    story.append(Spacer(1, 10*mm))
    story.append(Paragraph("CANDIDATE’S DECLARATION", t_center))
    story.append(Spacer(1, 12*mm))

    story.append(Paragraph(
        "We hereby declare that the work presented in this project entitled "
        "<b>“StockSphere: Virtual Stock Trading &amp; AI-Powered Market Forecasting System with Explainable AI”</b> "
        "submitted towards completion of the project in 7th Semester of B.Tech. (Computer Engineering) is an authentic "
        "record of our original work carried out under the guidance of <b>Prof. [GUIDE NAME]</b>.",
        body
    ))
    story.append(Spacer(1, 5*mm))
    story.append(Paragraph(
        "We have not submitted the matter embodied in this project for the award of any other degree or diploma.",
        body
    ))
    story.append(Spacer(1, 15*mm))

    decl_info = [
        [Paragraph("<b>Semester:</b> 7th", td), Paragraph("", td)],
        [Paragraph("<b>Place:</b> Rajkot", td), Paragraph("", td)],
        [Paragraph("<b>Date:</b> ______________", td), Paragraph("", td)],
        [Spacer(1, 15*mm), Spacer(1, 15*mm)],
        [Paragraph("Signature: __________________________<br/><b>Kavy Gami</b> ([ENROLLMENT NO. 1])", td),
         Paragraph("Signature: __________________________<br/><b>[STUDENT NAME 2]</b> ([ENROLLMENT NO. 2])", td)]
    ]
    t_decl = Table(decl_info, colWidths=[85*mm, 85*mm])
    t_decl.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(t_decl)
    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════
    # PAGE 3: CERTIFICATE (Student 1)
    # ════════════════════════════════════════════════════════════════
    story.append(Paragraph("ATMIYA UNIVERSITY", t_univ))
    story.append(Spacer(1, 2*mm))
    story.append(Paragraph("RAJKOT", t_rajkot))
    story.append(Spacer(1, 4*mm))
    if os.path.exists(logo_path):
        story.append(Image(logo_path, width=1.7*inch, height=1.7*inch))
    story.append(Spacer(1, 6*mm))
    story.append(Paragraph("CERTIFICATE", t_center))
    story.append(Spacer(1, 8*mm))

    story.append(Paragraph("Date: ______________", ParagraphStyle('DateLeft', fontName='Helvetica', fontSize=10, leading=14)))
    story.append(Spacer(1, 5*mm))
    story.append(Paragraph(
        "This is to certify that the <b>“StockSphere: Virtual Stock Trading &amp; AI-Powered Market Forecasting System "
        "with Explainable AI”</b> has been carried out by <b>Kavy Gami [Enrollment No. 1]</b> under my guidance in fulfillment "
        "of the subject Mini Project in <b>COMPUTER ENGINEERING (7th Semester)</b> of Atmiya University, Rajkot during the "
        "academic year 2026-27.",
        body
    ))
    story.append(Spacer(1, 35*mm))

    cert_signs = [
        [Paragraph("<b>Prof. [GUIDE NAME]</b><br/>(Project Guide)", td),
         Paragraph("<b>Prof. Tosal M. Bhalodia</b><br/>(Head of the Department)", td)]
    ]
    t_csign = Table(cert_signs, colWidths=[90*mm, 80*mm])
    t_csign.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(t_csign)
    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════
    # PAGE 4: CERTIFICATE (Student 2)
    # ════════════════════════════════════════════════════════════════
    story.append(Paragraph("ATMIYA UNIVERSITY", t_univ))
    story.append(Spacer(1, 2*mm))
    story.append(Paragraph("RAJKOT", t_rajkot))
    story.append(Spacer(1, 4*mm))
    if os.path.exists(logo_path):
        story.append(Image(logo_path, width=1.7*inch, height=1.7*inch))
    story.append(Spacer(1, 6*mm))
    story.append(Paragraph("CERTIFICATE", t_center))
    story.append(Spacer(1, 8*mm))

    story.append(Paragraph("Date: ______________", ParagraphStyle('DateLeft2', fontName='Helvetica', fontSize=10, leading=14)))
    story.append(Spacer(1, 5*mm))
    story.append(Paragraph(
        "This is to certify that the <b>“StockSphere: Virtual Stock Trading &amp; AI-Powered Market Forecasting System "
        "with Explainable AI”</b> has been carried out by <b>[STUDENT NAME 2] [Enrollment No. 2]</b> under my guidance in "
        "fulfillment of the subject Mini Project in <b>COMPUTER ENGINEERING (7th Semester)</b> of Atmiya University, "
        "Rajkot during the academic year 2026-27.",
        body
    ))
    story.append(Spacer(1, 35*mm))
    story.append(t_csign)
    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════
    # PAGE 5: ACKNOWLEDGEMENT
    # ════════════════════════════════════════════════════════════════
    story.append(Spacer(1, 10*mm))
    story.append(Paragraph("ACKNOWLEDGEMENT", t_center))
    story.append(Spacer(1, 10*mm))

    story.append(Paragraph(
        "We have taken many efforts in this project. However, it would not have been possible without the kind support "
        "and help of many individuals and organizations. We would like to extend our sincere thanks to all of them.",
        body
    ))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(
        "We are highly indebted to <b>Prof. [GUIDE NAME]</b> for continuous guidance, supervision, valuable suggestions, "
        "and encouragement throughout the development of the project titled <b>“StockSphere: Virtual Stock Trading &amp; "
        "AI-Powered Market Forecasting System with Explainable AI”</b>.",
        body
    ))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(
        "We express our gratitude to <b>Prof. Tosal M. Bhalodia</b>, Head of the Department, and faculty members of the "
        "Computer Engineering Department, Atmiya University, Rajkot, for their cooperation, technical guidance, and academic support.",
        body
    ))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(
        "We also thank our classmates, friends, and everyone who contributed directly or indirectly to the successful completion "
        "of this mini project.",
        body
    ))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(
        "Finally, we appreciate the efforts of every project team member in requirements analysis, architecture design, machine "
        "learning modeling, Generative AI synthesis, implementation, testing, and documentation of the system.",
        body
    ))
    story.append(Spacer(1, 20*mm))

    story.append(Paragraph("<b>Kavy Gami</b> ([ENROLLMENT NO. 1])<br/><b>[STUDENT NAME 2]</b> ([ENROLLMENT NO. 2])", t_sub_bold))
    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════
    # PAGE 6: ABSTRACT
    # ════════════════════════════════════════════════════════════════
    story.append(Spacer(1, 8*mm))
    story.append(Paragraph("ABSTRACT", t_center))
    story.append(Spacer(1, 8*mm))

    story.append(Paragraph(
        "StockSphere is a modern full-stack web application designed to democratize stock market literacy by providing a "
        "risk-free virtual trading ecosystem augmented by real-time WebSocket market streaming, quantitative Machine Learning "
        "forecasting, and Generative Artificial Intelligence (Explainable AI - XAI). Traditional investing education often suffers "
        "from barriers such as financial risk, static delayed quotes, complex mathematical formulas, and 'black-box' algorithmic "
        "predictors that retail investors find difficult to understand and trust.",
        body
    ))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(
        "The proposed system combines simulated trading with an econometric 2nd-degree Polynomial Least-Squares Regression model "
        "that analyzes 30-day historical closing prices to project a 5-day price horizon and detect whether a stock is Bullish, Bearish, "
        "or Neutral alongside statistical confidence metrics (R² and Mean Absolute Error). To address the explainability challenge of "
        "traditional machine learning, StockSphere integrates a state-of-the-art Generative AI layer powered by Google Gemini (with an "
        "intelligent grounded neural fallback). This layer synthesizes quantitative regression coefficients into an institutional-grade "
        "Bull vs. Bear Investment Thesis, detailing upside catalysts, downside risk bounds, and tactical virtual trading plans.",
        body
    ))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(
        "The application is built on the MERN stack (MongoDB, Express.js, React 18, Node.js) with Vite, Tailwind CSS, Redux Toolkit, "
        "Socket.io for live market updates, Finnhub API for baseline quotes, Yahoo Finance for historical candles, and Chart.js for "
        "interactive visual analytics. The platform includes virtual portfolio management ($100,000 balance), trade execution, real-time "
        "watchlists, and a live social community forum, delivering a secure, fast, and academically rigorous trading laboratory.",
        body
    ))
    story.append(Spacer(1, 5*mm))
    story.append(Paragraph(
        "<b>Keywords:</b> Virtual Stock Trading, MERN Stack, Finnhub API, WebSocket Streaming, Machine Learning, Polynomial Regression, "
        "Ordinary Least Squares, Bullish Bearish Trend, Explainable AI (XAI), Generative AI, Google Gemini LLM, Portfolio Management.",
        body
    ))
    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════
    # PAGE 7: INDEX (Part 1)
    # ════════════════════════════════════════════════════════════════
    story.append(Paragraph("INDEX", t_center))
    story.append(Spacer(1, 4*mm))

    idx_data_1 = [
        [Paragraph("<b>Sr. No.</b>", idx_th), Paragraph("<b>Title</b>", idx_th), Paragraph("<b>Page No.</b>", idx_th)],
        [Paragraph("1", idx_td), Paragraph("<b>Introduction</b>", idx_td), Paragraph("10", idx_td)],
        [Paragraph("1.1", idx_td), Paragraph("Purpose", idx_td), Paragraph("10", idx_td)],
        [Paragraph("1.2", idx_td), Paragraph("Scope", idx_td), Paragraph("10", idx_td)],
        [Paragraph("1.3", idx_td), Paragraph("Technology and Tools", idx_td), Paragraph("10", idx_td)],
        [Paragraph("2", idx_td), Paragraph("<b>Project Management</b>", idx_td), Paragraph("11", idx_td)],
        [Paragraph("2.1", idx_td), Paragraph("Project Planning", idx_td), Paragraph("11", idx_td)],
        [Paragraph("2.2", idx_td), Paragraph("Project Scheduling", idx_td), Paragraph("11", idx_td)],
        [Paragraph("2.3", idx_td), Paragraph("Risk Management", idx_td), Paragraph("11", idx_td)],
        [Paragraph("2.3.1", idx_td), Paragraph("Risk Identification", idx_td), Paragraph("11", idx_td)],
        [Paragraph("2.3.2", idx_td), Paragraph("Risk Analysis", idx_td), Paragraph("12", idx_td)],
        [Paragraph("3", idx_td), Paragraph("<b>System Requirements Study</b>", idx_td), Paragraph("13", idx_td)],
        [Paragraph("3.1", idx_td), Paragraph("Hardware and Software Requirements", idx_td), Paragraph("13", idx_td)],
        [Paragraph("3.2", idx_td), Paragraph("Constraints", idx_td), Paragraph("13", idx_td)],
        [Paragraph("3.2.1", idx_td), Paragraph("Hardware Limitations", idx_td), Paragraph("14", idx_td)],
        [Paragraph("3.2.2", idx_td), Paragraph("Reliability Requirements", idx_td), Paragraph("14", idx_td)],
        [Paragraph("3.2.3", idx_td), Paragraph("Safety and Security Consideration", idx_td), Paragraph("14", idx_td)],
        [Paragraph("4", idx_td), Paragraph("<b>System Analysis</b>", idx_td), Paragraph("15", idx_td)],
        [Paragraph("4.1", idx_td), Paragraph("Study of Current System", idx_td), Paragraph("15", idx_td)],
        [Paragraph("4.2", idx_td), Paragraph("Problems and Weaknesses of Current System", idx_td), Paragraph("15", idx_td)],
        [Paragraph("4.3", idx_td), Paragraph("Requirements of New System", idx_td), Paragraph("15", idx_td)],
        [Paragraph("4.3.1", idx_td), Paragraph("User Requirements", idx_td), Paragraph("15", idx_td)],
        [Paragraph("4.3.2", idx_td), Paragraph("System Requirements", idx_td), Paragraph("15", idx_td)],
        [Paragraph("4.4", idx_td), Paragraph("Feasibility Study", idx_td), Paragraph("16", idx_td)],
        [Paragraph("4.5", idx_td), Paragraph("Feature of New System", idx_td), Paragraph("17", idx_td)],
        [Paragraph("5", idx_td), Paragraph("<b>System Design</b>", idx_td), Paragraph("18", idx_td)],
        [Paragraph("5.1", idx_td), Paragraph("Input / Output Interface", idx_td), Paragraph("18", idx_td)],
        [Paragraph("5.2", idx_td), Paragraph("Interface Design", idx_td), Paragraph("18", idx_td)],
        [Paragraph("5.2.1", idx_td), Paragraph("Class Diagram", idx_td), Paragraph("18", idx_td)],
        [Paragraph("5.2.2", idx_td), Paragraph("Use Case Diagram", idx_td), Paragraph("19", idx_td)],
        [Paragraph("5.2.3", idx_td), Paragraph("Activity Diagram", idx_td), Paragraph("20", idx_td)],
        [Paragraph("5.2.4", idx_td), Paragraph("Data Flow Diagram", idx_td), Paragraph("20", idx_td)],
        [Paragraph("5.2.5", idx_td), Paragraph("State Diagram", idx_td), Paragraph("21", idx_td)],
        [Paragraph("5.2.6", idx_td), Paragraph("E-R Diagram", idx_td), Paragraph("21", idx_td)],
        [Paragraph("5.2.7", idx_td), Paragraph("Sequence Diagram", idx_td), Paragraph("22", idx_td)],
        [Paragraph("5.2.8", idx_td), Paragraph("System Architecture", idx_td), Paragraph("23", idx_td)],
        [Paragraph("6", idx_td), Paragraph("<b>Code Implementation</b>", idx_td), Paragraph("24", idx_td)],
        [Paragraph("6.1", idx_td), Paragraph("Implementation Environment", idx_td), Paragraph("24", idx_td)],
        [Paragraph("6.2", idx_td), Paragraph("Program / Module Specification", idx_td), Paragraph("24", idx_td)],
        [Paragraph("6.3", idx_td), Paragraph("Coding Standards", idx_td), Paragraph("25", idx_td)],
        [Paragraph("7", idx_td), Paragraph("<b>Testing</b>", idx_td), Paragraph("26", idx_td)],
        [Paragraph("7.1", idx_td), Paragraph("Testing Strategy", idx_td), Paragraph("26", idx_td)],
        [Paragraph("7.2", idx_td), Paragraph("Testing Method", idx_td), Paragraph("26", idx_td)],
        [Paragraph("7.2.1", idx_td), Paragraph("Unit Testing", idx_td), Paragraph("26", idx_td)],
    ]
    t_idx1 = Table(idx_data_1, colWidths=[18*mm, 130*mm, 26*mm])
    t_idx1.setStyle(idx_grid_style)
    story.append(t_idx1)
    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════
    # PAGE 8: INDEX (Part 2)
    # ════════════════════════════════════════════════════════════════
    story.append(Spacer(1, 4*mm))
    idx_data_2 = [
        [Paragraph("7.2.2", idx_td), Paragraph("Integration Testing", idx_td), Paragraph("26", idx_td)],
        [Paragraph("7.2.3", idx_td), Paragraph("Validation Testing", idx_td), Paragraph("26", idx_td)],
        [Paragraph("7.3", idx_td), Paragraph("Test Cases", idx_td), Paragraph("26", idx_td)],
        [Paragraph("7.3.1", idx_td), Paragraph("Test Suite", idx_td), Paragraph("27", idx_td)],
        [Paragraph("8", idx_td), Paragraph("<b>Limitations and Future Enhancement</b>", idx_td), Paragraph("28", idx_td)],
        [Paragraph("8.1", idx_td), Paragraph("Limitations", idx_td), Paragraph("28", idx_td)],
        [Paragraph("8.2", idx_td), Paragraph("Future Enhancement", idx_td), Paragraph("28", idx_td)],
        [Paragraph("9", idx_td), Paragraph("<b>Conclusion</b>", idx_td), Paragraph("29", idx_td)],
        [Paragraph("10", idx_td), Paragraph("<b>References</b>", idx_td), Paragraph("30", idx_td)],
        [Paragraph("", idx_td), Paragraph("<b>Project Module Summary</b>", idx_td), Paragraph("31", idx_td)],
    ]
    t_idx2 = Table(idx_data_2, colWidths=[18*mm, 130*mm, 26*mm])
    t_idx2.setStyle(idx_grid_style)
    story.append(t_idx2)
    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════
    # PAGE 9: LIST OF FIGURES & LIST OF TABLES
    # ════════════════════════════════════════════════════════════════
    story.append(Paragraph("LIST OF FIGURES", t_center))
    story.append(Spacer(1, 5*mm))

    fig_data = [
        [Paragraph("<b>Fig. No.</b>", th), Paragraph("<b>Figure Title</b>", th), Paragraph("<b>Page No.</b>", th)],
        [Paragraph("Figure 5.1", td), Paragraph("System Architecture Diagram", td), Paragraph("23", td)],
        [Paragraph("Figure 5.2", td), Paragraph("Logical Class Diagram of StockSphere System", td), Paragraph("18", td)],
        [Paragraph("Figure 5.3", td), Paragraph("Use Case Diagram – Trader & System Operations", td), Paragraph("19", td)],
        [Paragraph("Figure 5.4", td), Paragraph("Activity Diagram – Stock Analysis, Prediction & Trade Workflow", td), Paragraph("20", td)],
        [Paragraph("Figure 5.5", td), Paragraph("Data Flow Diagram – Level 0", td), Paragraph("20", td)],
        [Paragraph("Figure 5.6", td), Paragraph("Trade Lifecycle State Diagram", td), Paragraph("21", td)],
        [Paragraph("Figure 5.7", td), Paragraph("Entity Relationship Diagram", td), Paragraph("22", td)],
        [Paragraph("Figure 5.8", td), Paragraph("Sequence Diagram – ML Forecasting & GenAI Thesis Generation", td), Paragraph("22", td)],
    ]
    t_figs = Table(fig_data, colWidths=[25*mm, 120*mm, 25*mm])
    t_figs.setStyle(tbl_grid_style)
    story.append(t_figs)

    story.append(Spacer(1, 8*mm))
    story.append(Paragraph("LIST OF TABLES", t_center))
    story.append(Spacer(1, 5*mm))

    tbl_data = [
        [Paragraph("<b>Table No.</b>", th), Paragraph("<b>Table Title</b>", th), Paragraph("<b>Page No.</b>", th)],
        [Paragraph("Table 1.1", td), Paragraph("Technology and Development Tools", td), Paragraph("10", td)],
        [Paragraph("Table 2.1", td), Paragraph("Project Schedule and Development Phases", td), Paragraph("11", td)],
        [Paragraph("Table 2.2", td), Paragraph("Risk Identification and Analysis Register", td), Paragraph("12", td)],
        [Paragraph("Table 3.1", td), Paragraph("Server and Client Hardware Requirements", td), Paragraph("13", td)],
        [Paragraph("Table 3.2", td), Paragraph("Software and Runtime Environment Specifications", td), Paragraph("13", td)],
        [Paragraph("Table 4.1", td), Paragraph("Functional Requirements Specification (FR-01 to FR-12)", td), Paragraph("15-16", td)],
        [Paragraph("Table 4.2", td), Paragraph("Non-Functional Requirements Specification", td), Paragraph("16", td)],
        [Paragraph("Table 5.1", td), Paragraph("Input / Output Interface Specifications", td), Paragraph("18", td)],
        [Paragraph("Table 6.1", td), Paragraph("Implementation Environment and Architectural Roles", td), Paragraph("24", td)],
        [Paragraph("Table 6.2", td), Paragraph("System Modules and Functional Responsibilities", td), Paragraph("24", td)],
        [Paragraph("Table 7.1", td), Paragraph("System Test Cases and Execution Results", td), Paragraph("26-27", td)],
        [Paragraph("Table 7.2", td), Paragraph("Consolidated Test Suite Summary", td), Paragraph("27", td)],
    ]
    t_tbls = Table(tbl_data, colWidths=[25*mm, 120*mm, 25*mm])
    t_tbls.setStyle(tbl_grid_style)
    story.append(t_tbls)
    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════
    # PAGE 10: CHAPTER 1 - INTRODUCTION
    # ════════════════════════════════════════════════════════════════
    story.append(Paragraph("CHAPTER – 1", h_chap))
    story.append(Paragraph("INTRODUCTION", h_chap_title))

    story.append(Paragraph("1.1 Purpose", h1))
    story.append(Paragraph(
        "The purpose of <b>StockSphere</b> is to provide a comprehensive, real-time virtual trading web platform that bridges "
        "practical financial market simulation with modern Machine Learning and Generative Artificial Intelligence (Explainable AI - XAI). "
        "Trading in financial markets carries substantial capital risk, and novice investors often lack an environment to learn market dynamics "
        "with realistic live data. StockSphere replaces fragmented paper-trading methods and black-box algorithmic tools with an integrated, "
        "transparent system where users receive a $100,000 virtual balance, stream live prices, generate mathematical price trend forecasts, "
        "and receive human-understandable AI investment research memos.",
        body
    ))

    story.append(Paragraph("1.2 Scope", h1))
    story.append(Paragraph(
        "The scope of StockSphere covers all essential aspects of contemporary retail investing and technical market analysis:",
        body
    ))
    story.append(Paragraph("• <b>User Authentication &amp; Security:</b> JWT-based authentication, bcrypt password hashing, and persistent session state.", bullet))
    story.append(Paragraph("• <b>Live Market Streaming:</b> Real-time ticker prices streamed via Socket.io with smart backend caching to honor Finnhub API limits.", bullet))
    story.append(Paragraph("• <b>Virtual Portfolio Management:</b> Instant Buy/Sell trade execution, holdings valuation, cash tracking, and live Profit/Loss (PnL) computation.", bullet))
    story.append(Paragraph("• <b>Interactive Charting:</b> Historical price candle exploration across multiple time horizons using Chart.js.", bullet))
    story.append(Paragraph("• <b>Machine Learning Trend Forecaster:</b> 2nd-degree Polynomial Least-Squares regression predicting 5-day price trajectories and classifying trends as Bullish, Bearish, or Neutral.", bullet))
    story.append(Paragraph("• <b>Explainable AI (XAI) Investment Thesis:</b> Generative AI layer translating mathematical ML regression parameters into structured Bull vs. Bear institutional memos.", bullet))
    story.append(Paragraph("• <b>Personalized Watchlist &amp; Community Forum:</b> Real-time quote tracking and live peer discussion feeds.", bullet))

    story.append(Paragraph("1.3 Technology and Tools", h1))
    story.append(Paragraph("<b>Table 1.1:</b> Technology and Development Tools", caption))
    tech_data = [
        [Paragraph("<b>Technology / Tool</b>", th), Paragraph("<b>Purpose</b>", th)],
        [Paragraph("React.js (v18) + Vite", td), Paragraph("High-performance client user interface and rapid build bundling", td)],
        [Paragraph("Tailwind CSS", td), Paragraph("Responsive utility-first modern styling and dark-mode design system", td)],
        [Paragraph("Redux Toolkit", td), Paragraph("Centralized state management for live stock quotes and portfolio holdings", td)],
        [Paragraph("Node.js &amp; Express.js", td), Paragraph("Scalable RESTful API backend, rate limiting, and business controllers", td)],
        [Paragraph("MongoDB &amp; Mongoose", td), Paragraph("NoSQL document storage for users, transactions, holdings, and forum posts", td)],
        [Paragraph("Socket.io", td), Paragraph("Bidirectional WebSocket streaming for live stock price fluctuations", td)],
        [Paragraph("Chart.js &amp; React-Chartjs-2", td), Paragraph("Interactive price charts and visual regression forecast overlays", td)],
        [Paragraph("Yahoo Finance &amp; Finnhub APIs", td), Paragraph("External data ingestion for live market quotes and 30-day historical candles", td)],
        [Paragraph("Polynomial ML Model (OLS)", td), Paragraph("Degree-2 ordinary least squares regression for 5-day price trend projection", td)],
        [Paragraph("Google Gemini API (Flash)", td), Paragraph("Generative AI layer synthesizing econometric data into Explainable AI theses", td)],
    ]
    t_tech = Table(tech_data, colWidths=[50*mm, 120*mm])
    t_tech.setStyle(tbl_grid_style)
    story.append(t_tech)
    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════
    # PAGE 11: CHAPTER 2 - PROJECT MANAGEMENT
    # ════════════════════════════════════════════════════════════════
    story.append(Paragraph("CHAPTER – 2", h_chap))
    story.append(Paragraph("PROJECT MANAGEMENT", h_chap_title))

    story.append(Paragraph("2.1 Project Planning", h1))
    story.append(Paragraph(
        "Project planning defines the work required to transform the stock trading and market forecasting requirements "
        "into a functional web application. The project is divided into requirement analysis, architecture design, database and API design, "
        "MERN implementation, machine learning modeling, Generative AI synthesis, testing, and final presentation. "
        "The planning approach maintains clear visibility from user onboarding through AI memo generation.",
        body
    ))

    p_pitem = ParagraphStyle('PPlanItem', fontName='Helvetica', fontSize=8.5, leading=11, spaceAfter=2, leftIndent=12, firstLineIndent=-10)
    story.append(Paragraph("1. Identify retail investor pain points, market simulation requirements, and expected ML capabilities.", p_pitem))
    story.append(Paragraph("2. Formulate functional and non-functional specifications for live trading and AI forecasting.", p_pitem))
    story.append(Paragraph("3. Design the layered system architecture, MongoDB collections, WebSocket feeds, and UML/DFD models.", p_pitem))
    story.append(Paragraph("4. Implement authentication, virtual wallet, real-time charting, ML regression, and Explainable AI modules.", p_pitem))
    story.append(Paragraph("5. Integrate React client, Express REST APIs, Finnhub/Yahoo market streams, and Google Gemini API.", p_pitem))
    story.append(Paragraph("6. Perform unit, integration, validation, and mathematical regression error verification.", p_pitem))
    story.append(Paragraph("7. Prepare technical documentation, architectural diagrams, viva demonstration assets, and project reports.", p_pitem))

    story.append(Paragraph("2.2 Project Scheduling", h1))
    story.append(Paragraph(
        "Scheduling assigns development activities to a structured sequence across the semester. The following schedule outlines the planned academic development lifecycle:",
        body
    ))

    sched_th = ParagraphStyle('SchedTH', fontName='Helvetica-Bold', fontSize=8, leading=10, alignment=0, textColor=colors.HexColor('#1a202c'))
    sched_td = ParagraphStyle('SchedTD', fontName='Helvetica', fontSize=7.5, leading=9.5, alignment=0, textColor=colors.HexColor('#2d3748'))
    sched_data = [
        [Paragraph("<b>Phase</b>", sched_th), Paragraph("<b>Major Activities</b>", sched_th), Paragraph("<b>Deliverables</b>", sched_th)],
        [Paragraph("1", sched_td), Paragraph("Requirement collection, market API evaluation &amp; scope", sched_td), Paragraph("SRS &amp; requirement specification", sched_td)],
        [Paragraph("2", sched_td), Paragraph("System design, UML diagrams, DFD, ER schemas", sched_td), Paragraph("Architecture, UML, DFD, ER design", sched_td)],
        [Paragraph("3", sched_td), Paragraph("Database &amp; API design, schema definition", sched_td), Paragraph("Mongoose schemas, API specifications", sched_td)],
        [Paragraph("4", sched_td), Paragraph("Authentication &amp; user wallet management", sched_td), Paragraph("Registration, login, JWT, $100k balance", sched_td)],
        [Paragraph("5", sched_td), Paragraph("Market data, WebSocket streaming, Chart.js", sched_td), Paragraph("Live ticker feed &amp; interactive charts", sched_td)],
        [Paragraph("6", sched_td), Paragraph("Virtual trading engine &amp; portfolio module", sched_td), Paragraph("Buy/Sell execution, PnL tracking", sched_td)],
        [Paragraph("7", sched_td), Paragraph("Polynomial ML predictor &amp; GenAI thesis (XAI)", sched_td), Paragraph("OLS regression &amp; AI thesis memo", sched_td)],
        [Paragraph("8", sched_td), Paragraph("Full-stack integration, testing &amp; debugging", sched_td), Paragraph("Test suite results &amp; verified build", sched_td)],
        [Paragraph("9", sched_td), Paragraph("Documentation, report preparation &amp; presentation", sched_td), Paragraph("Final project report &amp; presentation", sched_td)],
    ]
    t_sched = Table(sched_data, colWidths=[14*mm, 90*mm, 66*mm])
    t_sched.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#a0aec0')),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#edf2f7')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 1.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_sched)

    story.append(Paragraph("2.3 Risk Management", h1))
    story.append(Paragraph(
        "Risk management identifies technical, algorithmic, and usability bottlenecks to plan preventive mitigations before they affect project objectives.",
        body
    ))
    story.append(Paragraph("2.3.1 Risk Identification", h2))
    p_risk_bullet = ParagraphStyle('PRiskBullet', fontName='Helvetica', fontSize=8.5, leading=11, spaceAfter=2, leftIndent=12, firstLineIndent=-10)
    story.append(Paragraph("• Authentication failure or improper JWT authorization may expose user portfolios to unauthorized access.", p_risk_bullet))
    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════
    # PAGE 12: CHAPTER 2 (Cont.) - RISK ANALYSIS
    # ════════════════════════════════════════════════════════════════
    story.append(Paragraph("• Database connection failure or network interruption may disrupt live trade logging and order processing.", p_risk_bullet))
    story.append(Paragraph("• Finnhub API rate-limiting (429) may halt live ticker feeds during intense client usage.", p_risk_bullet))
    story.append(Paragraph("• Collinear historical candle prices may produce a singular matrix during OLS quadratic curve fitting.", p_risk_bullet))
    story.append(Paragraph("• External LLM API downtime or missing API keys could cause Generative AI thesis generation to fail.", p_risk_bullet))
    story.append(Paragraph("• Concurrent trade requests could lead to race conditions and inconsistent portfolio balances.", p_risk_bullet))
    story.append(Paragraph("• Validation errors may permit invalid trade quantities or order values into the database.", p_risk_bullet))
    story.append(Paragraph("• Insufficient testing may leave undetected integration defects between React, Express, and MongoDB.", p_risk_bullet))

    story.append(Spacer(1, 3*mm))
    story.append(Paragraph("2.3.2 Risk Analysis", h2))
    story.append(Paragraph("<b>Table 2.2:</b> Risk Identification and Analysis Register", caption))
    r_th = ParagraphStyle('RTH', fontName='Helvetica-Bold', fontSize=8.5, leading=10, alignment=0, textColor=colors.HexColor('#1a202c'))
    r_td = ParagraphStyle('RTD', fontName='Helvetica', fontSize=8, leading=10, alignment=0, textColor=colors.HexColor('#2d3748'))
    risk_data = [
        [Paragraph("<b>Risk</b>", r_th), Paragraph("<b>Probability</b>", r_th), Paragraph("<b>Impact</b>", r_th), Paragraph("<b>Mitigation</b>", r_th)],
        [
            Paragraph("Unauthorized access", r_td),
            Paragraph("Medium", r_td),
            Paragraph("High", r_td),
            Paragraph("JWT bearer authentication, bcrypt hashing (12 rounds), protected Express routes and server-side balance checks.", r_td)
        ],
        [
            Paragraph("Finnhub API 429 rate limit", r_td),
            Paragraph("High", r_td),
            Paragraph("High", r_td),
            Paragraph("In-memory caching (60s quote, 1h profile) and a serialized promise queue with 300ms throttling delays.", r_td)
        ],
        [
            Paragraph("Database connection failure", r_td),
            Paragraph("Low-Medium", r_td),
            Paragraph("High", r_td),
            Paragraph("MongoDB Atlas replica sets, automated reconnection handlers, connection pooling, and graceful error handling.", r_td)
        ],
        [
            Paragraph("Singular matrix in OLS regression", r_td),
            Paragraph("Low-Medium", r_td),
            Paragraph("High", r_td),
            Paragraph("Cramer's rule determinant threshold check (|det| &lt; 1e-6) with automatic fallback to 1st-degree linear regression.", r_td)
        ],
        [
            Paragraph("Generative AI service failure", r_td),
            Paragraph("Medium", r_td),
            Paragraph("Medium", r_td),
            Paragraph("Dual-engine architecture: calls Google Gemini Flash, with automated zero-failure fallback to grounded neural thesis.", r_td)
        ],
        [
            Paragraph("Trade balance race condition", r_td),
            Paragraph("Low-Medium", r_td),
            Paragraph("High", r_td),
            Paragraph("Atomic Mongoose findOneAndUpdate operations verifying available cash balance before finalizing purchase transactions.", r_td)
        ],
        [
            Paragraph("Data-entry &amp; validation errors", r_td),
            Paragraph("Medium", r_td),
            Paragraph("Medium", r_td),
            Paragraph("Comprehensive frontend form validation, input type coercion, and strict backend Express schema checks.", r_td)
        ],
    ]
    t_risk = Table(risk_data, colWidths=[40*mm, 20*mm, 18*mm, 92*mm])
    t_risk.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#a0aec0')),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#edf2f7')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_risk)
    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════
    # PAGE 13: CHAPTER 3 - SYSTEM REQUIREMENTS STUDY
    # ════════════════════════════════════════════════════════════════
    story.append(Paragraph("CHAPTER – 3", h_chap))
    story.append(Paragraph("SYSTEM REQUIREMENTS STUDY", h_chap_title))

    story.append(Paragraph("3.1 Hardware and Software Requirements", h1))
    story.append(Paragraph(
        "StockSphere operates as a responsive web platform with client-server separation. Development, training, and execution "
        "environments require reliable network access for real-time external market APIs, modern JavaScript execution, and "
        "cloud database connectivity.",
        body
    ))

    story.append(Paragraph("3.1.1 Server-side Hardware Requirement", h2))
    story.append(Paragraph("<b>Table 3.1:</b> Server and Client Hardware Requirements", caption))
    hw_data = [
        [Paragraph("<b>Component</b>", th), Paragraph("<b>Minimum Specification</b>", th), Paragraph("<b>Recommended Specification</b>", th)],
        [Paragraph("Processor", td), Paragraph("Intel Core i3 / AMD Ryzen 3 (2.0 GHz)", td), Paragraph("Intel Core i5 / AMD Ryzen 5 or higher", td)],
        [Paragraph("RAM", td), Paragraph("4 GB System Memory", td), Paragraph("8 GB – 16 GB DDR4/DDR5", td)],
        [Paragraph("Storage", td), Paragraph("10 GB free disk space", td), Paragraph("25 GB SSD storage for logs and dependencies", td)],
        [Paragraph("Network", td), Paragraph("Broadband Internet (10 Mbps)", td), Paragraph("High-speed Internet (50+ Mbps low latency)", td)],
        [Paragraph("Display", td), Paragraph("1366 × 768 resolution", td), Paragraph("1920 × 1080 Full HD monitor", td)],
    ]
    t_hw = Table(hw_data, colWidths=[40*mm, 65*mm, 65*mm])
    t_hw.setStyle(tbl_grid_style)
    story.append(t_hw)

    story.append(Paragraph("3.1.2 Software Requirement", h2))
    story.append(Paragraph("<b>Table 3.2:</b> Software and Runtime Environment Specifications", caption))
    sw_data = [
        [Paragraph("<b>Software / Layer</b>", th), Paragraph("<b>Specification / Environment</b>", th)],
        [Paragraph("Operating System", td), Paragraph("Windows 10/11, macOS Sequoia, or Linux Ubuntu 22.04 LTS", td)],
        [Paragraph("Runtime Environment", td), Paragraph("Node.js (v18.x or v20.x LTS) with NPM package manager", td)],
        [Paragraph("Backend Framework", td), Paragraph("Express.js (v4.18) REST framework with HTTP/WebSocket servers", td)],
        [Paragraph("Database &amp; ODM", td), Paragraph("MongoDB Atlas (Cloud Cluster) with Mongoose ODM (v8.0)", td)],
        [Paragraph("Client Framework", td), Paragraph("React.js (v18.2) + Vite (v5.0) bundling system", td)],
        [Paragraph("Styling Framework", td), Paragraph("Tailwind CSS (v3.4) with custom financial dark theme", td)],
        [Paragraph("Real-Time Communications", td), Paragraph("Socket.io (v4.8) for price feeds and live community events", td)],
        [Paragraph("Data Visualization", td), Paragraph("Chart.js (v4.4) &amp; React-Chartjs-2 for financial candle charts", td)],
        [Paragraph("Machine Learning Engine", td), Paragraph("Native Node.js OLS Matrix Solver (Polynomial Regression Degree 2)", td)],
        [Paragraph("Generative AI Engine", td), Paragraph("Google Gemini 1.5 Flash REST API + Grounded Neural Engine", td)],
        [Paragraph("Security Packages", td), Paragraph("Bcrypt.js (12 salt rounds), JSON Web Tokens (JWT), Helmet.js", td)],
        [Paragraph("Supported Web Browsers", td), Paragraph("Google Chrome (v115+), Microsoft Edge (v115+), Mozilla Firefox (v115+)", td)],
    ]
    t_sw = Table(sw_data, colWidths=[55*mm, 115*mm])
    t_sw.setStyle(tbl_grid_style)
    story.append(t_sw)

    story.append(Paragraph("3.1.3 Client-side Requirements", h2))
    story.append(Paragraph(
        "End users access StockSphere using any modern standards-compliant web browser on desktops, laptops, or mobile tablets "
        "with JavaScript and WebSocket capabilities enabled. No browser plugins or external binaries are required.",
        body
    ))

    story.append(Paragraph("3.2 Constraints", h1))
    story.append(Paragraph(
        "The system operates within defined infrastructural boundaries, third-party API rate quotas, and academic timelines.",
        body
    ))
    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════
    # PAGE 14: CHAPTER 3 (Cont.) - CONSTRAINTS
    # ════════════════════════════════════════════════════════════════
    story.append(Spacer(1, 4*mm))
    story.append(Paragraph("3.2.1 Hardware Limitations", h2))
    story.append(Paragraph("• <b>Server Memory:</b> Intensive real-time WebSocket broadcasting requires efficient memory management to prevent heap exhaustion.", bullet))
    story.append(Paragraph("• <b>Client Rendering Load:</b> Rendering complex canvas price charts with high data density can challenge low-spec mobile hardware.", bullet))
    story.append(Paragraph("• <b>Network Latency:</b> Real-time price simulation fidelity is subject to client internet connection stability and socket ping.", bullet))

    story.append(Spacer(1, 4*mm))
    story.append(Paragraph("3.2.2 Reliability Requirements", h2))
    story.append(Paragraph(
        "StockSphere maintains strong transactional consistency across all user operations:",
        body
    ))
    story.append(Paragraph("• <b>Data Integrity:</b> User wallet balance adjustments, trade quantity changes, and stock holding calculations must be strictly atomic.", bullet))
    story.append(Paragraph("• <b>Zero-Failure AI Fallback:</b> If external LLM APIs fail or disconnect, the application must immediately switch to local grounded neural synthesis without crashing or displaying error toasts.", bullet))
    story.append(Paragraph("• <b>Graceful API Recovery:</b> Finnhub rate limits (429) are handled transparently by serving cached quotes and simulating realistic market ticks.", bullet))

    story.append(Spacer(1, 4*mm))
    story.append(Paragraph("3.2.3 Safety and Security Consideration", h2))
    story.append(Paragraph(
        "Security measures adhere to modern web application standards and OWASP recommendations:",
        body
    ))
    story.append(Paragraph("• <b>Cryptographic Password Hashing:</b> Passwords are never stored in plaintext; bcrypt hashing with 12 salt rounds is enforced in User pre-save hooks.", bullet))
    story.append(Paragraph("• <b>Stateless JWT Authorization:</b> JSON Web Tokens are validated on all protected routes (/api/stocks, /api/portfolio, /api/watchlist).", bullet))
    story.append(Paragraph("• <b>HTTP Header Security:</b> Helmet.js protects Express headers against Cross-Site Scripting (XSS), clickjacking, and MIME-sniffing.", bullet))
    story.append(Paragraph("• <b>Rate Limiting Defense:</b> Express rate limiters restrict IP requests to 300 calls per 15-minute window, mitigating Denial-of-Service attacks.", bullet))
    story.append(Paragraph("• <b>Secure Environment Isolation:</b> Database credentials, JWT secrets, and Finnhub/Gemini API keys are maintained in protected .env files.", bullet))
    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════
    # PAGE 15: CHAPTER 4 - SYSTEM ANALYSIS
    # ════════════════════════════════════════════════════════════════
    story.append(Paragraph("CHAPTER – 4", h_chap))
    story.append(Paragraph("SYSTEM ANALYSIS", h_chap_title))

    story.append(Paragraph("4.1 Study of Current System", h1))
    story.append(Paragraph(
        "In traditional academic and retail environments, individuals learning stock trading typically rely on three options: "
        "manual spreadsheet paper-trading, static delayed financial portals, or black-box trading algorithms. Paper trading lacks "
        "real-time emotional feedback, automated order execution, and live price dynamism. Meanwhile, commercial trading simulators "
        "frequently require payment, display delayed quotes, or overwhelm learners with complex interfaces. Crucially, existing ML tools "
        "output raw mathematical values (such as probabilities or next-day prices) without providing transparent, plain-English justifications "
        "explaining why a stock is trending Bullish or Bearish.",
        body
    ))

    story.append(Paragraph("4.2 Problem and Weaknesses of Current System", h1))
    story.append(Paragraph("• <b>Financial Risk Barrier:</b> Direct participation in stock markets requires real capital, exposing beginners to severe losses.", bullet))
    story.append(Paragraph("• <b>Static and Delayed Market Feeds:</b> Most free educational platforms use 15-minute delayed quotes, eliminating intraday realism.", bullet))
    story.append(Paragraph("• <b>Manual PnL Tracking:</b> Spreadsheets require manual record keeping, introducing calculation errors in average buy price and total returns.", bullet))
    story.append(Paragraph("• <b>The ML 'Black Box' Dilemma:</b> Traditional statistical and deep-learning predictors output numbers with zero qualitative reasoning.", bullet))
    story.append(Paragraph("• <b>Absence of Peer Community:</b> Traders have few centralized platforms to exchange investment ideas alongside simulated trades.", bullet))

    story.append(Paragraph("4.3 Requirements of New System", h1))
    story.append(Paragraph("4.3.1 User Requirements", h2))
    story.append(Paragraph("• Users must register securely and receive an immediate virtual cash allocation of $100,000.", bullet))
    story.append(Paragraph("• Users must search US equity symbols and view real-time streaming market prices.", bullet))
    story.append(Paragraph("• Users must execute virtual Buy and Sell orders with instantaneous portfolio balance updates.", bullet))
    story.append(Paragraph("• Users must toggle an AI Market Forecaster to visualize a 5-day polynomial regression projection and trend signal.", bullet))
    story.append(Paragraph("• Users must be able to generate an Explainable AI Bull/Bear Investment Thesis in plain English.", bullet))
    story.append(Paragraph("• Users must maintain custom watchlists and interact in a real-time community forum.", bullet))

    story.append(Paragraph("4.3.2 System Requirements", h2))
    story.append(Paragraph("<b>Table 4.1:</b> Functional Requirements Specification", caption))
    fr_data = [
        [Paragraph("<b>ID</b>", th), Paragraph("<b>Functional Requirement</b>", th)],
        [Paragraph("FR-01", td), Paragraph("The system shall support secure user registration, email uniqueness validation, and login authentication.", td)],
        [Paragraph("FR-02", td), Paragraph("The system shall issue signed JWT tokens and maintain authenticated sessions across route navigation.", td)],
        [Paragraph("FR-03", td), Paragraph("The system shall stream real-time price updates via WebSockets and broadcast live fluctuations.", td)],
        [Paragraph("FR-04", td), Paragraph("The system shall support keyword search for stock tickers and company names via the Finnhub search endpoint.", td)],
    ]
    t_fr = Table(fr_data, colWidths=[18*mm, 152*mm])
    t_fr.setStyle(tbl_grid_style)
    story.append(t_fr)
    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════
    # PAGE 16: CHAPTER 4 (Cont.) - FUNCTIONAL & NON-FUNCTIONAL REQUIREMENTS
    # ════════════════════════════════════════════════════════════════
    story.append(Spacer(1, 4*mm))
    fr_data_2 = [
        [Paragraph("<b>ID</b>", th), Paragraph("<b>Functional Requirement (Continued)</b>", th)],
        [Paragraph("FR-05", td), Paragraph("The system shall render interactive historical price charts across multiple timeframes (1D, 1W, 1M, 1Y).", td)],
        [Paragraph("FR-06", td), Paragraph("The system shall execute virtual BUY orders, deducting cash and logging average buy prices into holdings.", td)],
        [Paragraph("FR-07", td), Paragraph("The system shall execute virtual SELL orders, crediting cash and recalculating realized gains/losses.", td)],
        [Paragraph("FR-08", td), Paragraph("The system shall fit a 2nd-degree polynomial curve to 30-day closing prices using OLS and project 5 days ahead.", td)],
        [Paragraph("FR-09", td), Paragraph("The system shall compute statistical metrics including R² confidence, MAE, and Bullish/Bearish trend flags.", td)],
        [Paragraph("FR-10", td), Paragraph("The system shall generate an Explainable AI Bull/Bear Investment Thesis via Gemini LLM with local fallback.", td)],
        [Paragraph("FR-11", td), Paragraph("The system shall allow users to add and remove stock symbols from their personalized Watchlist.", td)],
        [Paragraph("FR-12", td), Paragraph("The system shall support a live Community Forum allowing users to publish posts, like, and comment in real-time.", td)],
    ]
    t_fr2 = Table(fr_data_2, colWidths=[18*mm, 152*mm])
    t_fr2.setStyle(tbl_grid_style)
    story.append(t_fr2)

    story.append(Spacer(1, 4*mm))
    story.append(Paragraph("4.3.3 Non-Functional Requirements", h2))
    story.append(Paragraph("<b>Table 4.2:</b> Non-Functional Requirements Specification", caption))
    nfr_data = [
        [Paragraph("<b>Category</b>", th), Paragraph("<b>Non-Functional Requirement Specification</b>", th)],
        [Paragraph("Security", td), Paragraph("Bcrypt password hashing (12 salt rounds), protected JWT API endpoints, and sanitized query inputs.", td)],
        [Paragraph("Performance", td), Paragraph("Cached quotes served in under 50ms; ML regression computed in under 150ms; UI renders at 60 FPS.", td)],
        [Paragraph("Reliability", td), Paragraph("In-memory caching prevents API throttling; automated zero-error fallback ensures 100% AI uptime.", td)],
        [Paragraph("Usability", td), Paragraph("Responsive dark-mode UI with clear color-coded price action (Green: Profit, Red: Loss).", td)],
        [Paragraph("Maintainability", td), Paragraph("Modular architecture separating controllers, socket services, Mongoose models, and React slices.", td)],
        [Paragraph("Scalability", td), Paragraph("Stateless Node.js architecture with connection pooling capable of scaling across cloud clusters.", td)],
    ]
    t_nfr = Table(nfr_data, colWidths=[35*mm, 135*mm])
    t_nfr.setStyle(tbl_grid_style)
    story.append(t_nfr)

    story.append(Spacer(1, 4*mm))
    story.append(Paragraph("4.4 Feasibility Study", h1))
    story.append(Paragraph("4.4.1 Technical Feasibility", h2))
    story.append(Paragraph(
        "StockSphere is built using the robust, industry-standard MERN stack. React 18, Vite, and Chart.js provide interactive front-end "
        "visualization, while Node.js and Express manage WebSocket connections and OLS matrix calculations. MongoDB Atlas provides reliable "
        "cloud storage. Integration with Finnhub, Yahoo Finance, and Google Gemini APIs is proven and technically sound.",
        body
    ))

    story.append(Paragraph("4.4.2 Economic Feasibility", h2))
    story.append(Paragraph(
        "The project is developed entirely with open-source technologies, free-tier developer APIs (Finnhub Free, Google AI Studio Free Tier), "
        "and standard workstation hardware. No commercial database licenses or paid hosting services were required during development, "
        "making the project highly cost-effective and economical for academic environments.",
        body
    ))
    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════
    # PAGE 17: CHAPTER 4 (Cont.) - FEASIBILITY & FEATURES
    # ════════════════════════════════════════════════════════════════
    story.append(Spacer(1, 4*mm))
    story.append(Paragraph("4.4.3 Operational Feasibility", h2))
    story.append(Paragraph(
        "StockSphere requires no complex software installation for end users. Traders access the platform via any standard web browser. "
        "The user experience is designed for intuitive navigation: searching a ticker instantly displays live charts, one click activates "
        "the AI Forecaster, and another button generates the full Explainable AI Bull/Bear Investment Thesis. The platform mirrors real-world "
        "trading brokerages, making it immediately familiar and operationally viable for students, educators, and retail investors.",
        body
    ))

    story.append(Paragraph("4.4.4 Schedule Feasibility", h2))
    story.append(Paragraph(
        "The project scope was decomposed into discrete modular sprints across the academic semester. The MERN foundation was established in "
        "Weeks 1–4, WebSocket price feeds and virtual trading in Weeks 5–8, Machine Learning and Generative AI in Weeks 9–12, and testing and "
        "documentation in Weeks 13–15. All milestone deliverables were completed within schedule.",
        body
    ))

    story.append(Spacer(1, 4*mm))
    story.append(Paragraph("4.5 Feature of New System", h1))
    story.append(Paragraph("• <b>$100,000 Virtual Trading Capital:</b> Real-time portfolio simulation allowing risk-free stock buying and selling.", bullet))
    story.append(Paragraph("• <b>Sub-Second WebSocket Price Feeds:</b> Instant ticker synchronization across Dashboard, Portfolio, and Watchlist.", bullet))
    story.append(Paragraph("• <b>Finnhub Smart Cache &amp; Queue:</b> Bypasses strict 30 req/min API rate limits using memory caching and micro-delays.", bullet))
    story.append(Paragraph("• <b>Interactive Multi-Horizon Charting:</b> High-resolution candlestick and line charts powered by Chart.js.", bullet))
    story.append(Paragraph("• <b>2nd-Degree Polynomial Regression ML:</b> Mathematically projects 5-day future price bounds with 95% confidence cones.", bullet))
    story.append(Paragraph("• <b>Statistical Model Metrics:</b> Calculates R² variance score, Mean Absolute Error (MAE), and fitted quadratic equations.", bullet))
    story.append(Paragraph("• <b>Explainable AI (XAI) Thesis Engine:</b> Translates mathematical curves into human-readable Bull/Bear research memos.", bullet))
    story.append(Paragraph("• <b>Dual-Engine Reliability:</b> Supports Google Gemini 1.5 Flash API with a zero-failure grounded neural fallback.", bullet))
    story.append(Paragraph("• <b>Real-Time Community Forum:</b> Interactive social wall where traders post, comment, and like market analyses.", bullet))
    story.append(Paragraph("• <b>Personalized Watchlist:</b> Real-time price tracking for high-priority stock tickers.", bullet))
    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════
    # PAGE 18: CHAPTER 5 - SYSTEM DESIGN (Class Diagram)
    # ════════════════════════════════════════════════════════════════
    story.append(Paragraph("CHAPTER – 5", h_chap))
    story.append(Paragraph("SYSTEM DESIGN", h_chap_title))

    story.append(Paragraph("5.1 Input / Output Interface", h1))
    story.append(Paragraph("<b>Table 5.1:</b> Input / Output Interface Specifications", caption))
    io_data = [
        [Paragraph("<b>Interface</b>", th), Paragraph("<b>Main Inputs</b>", th), Paragraph("<b>Expected Outputs</b>", th)],
        [Paragraph("User Authentication", td), Paragraph("Name, Email address, Plaintext Password", td), Paragraph("JWT Token, User Profile, $100k Balance", td)],
        [Paragraph("Stock Search &amp; Quote", td), Paragraph("Symbol query string (e.g. 'AAPL')", td), Paragraph("Profile, Live Quote, Day High/Low, Market Cap", td)],
        [Paragraph("Virtual Trade Modal", td), Paragraph("Symbol, Trade Type (BUY/SELL), Quantity", td), Paragraph("Executed Trade Record, Updated Holdings &amp; Cash", td)],
        [Paragraph("AI Predictor Engine", td), Paragraph("Symbol, Historical 30-Day Candles", td), Paragraph("5-day Projections, Bull/Bear Signal, R², MAE", td)],
        [Paragraph("GenAI Thesis (XAI)", td), Paragraph("Symbol, ML Metrics, Stock Quote Data", td), Paragraph("Executive Summary, Bull Case, Bear Case, Tactics", td)],
        [Paragraph("Watchlist Management", td), Paragraph("Stock Symbol toggle action", td), Paragraph("Personalized watchlist table with live ticks", td)],
        [Paragraph("Community Forum", td), Paragraph("Post content string, Like/Comment action", td), Paragraph("Live broadcasted discussion feed", td)],
    ]
    t_io = Table(io_data, colWidths=[40*mm, 65*mm, 65*mm])
    t_io.setStyle(tbl_grid_style)
    story.append(t_io)

    story.append(Paragraph("5.2 Interface Design", h1))
    story.append(Paragraph("5.2.1 Class Diagram", h2))
    img_class = os.path.join(ASSETS_DIR, "figure_5_2_class.png")
    if os.path.exists(img_class):
        story.append(Image(img_class, width=6.8*inch, height=3.5*inch))
    story.append(Paragraph("<b>Figure 5.2:</b> Logical Class Diagram of the StockSphere System", caption))
    story.append(Paragraph(
        "The class model encapsulates the core domain entities of StockSphere. <b>User</b> manages authentication and virtual funds; "
        "<b>Portfolio</b> and <b>Holding</b> govern live financial calculations; <b>Trade</b> records historical transactions; "
        "<b>StockQuote</b> and <b>PredictionEngine</b> handle quantitative forecasting; and <b>GenAIThesis</b> executes Explainable AI synthesis.",
        body
    ))
    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════
    # PAGE 19: CHAPTER 5 (Cont.) - USE CASE DIAGRAM
    # ════════════════════════════════════════════════════════════════
    story.append(Spacer(1, 4*mm))
    story.append(Paragraph("5.2.2 Use Case Diagram", h2))
    img_uc = os.path.join(ASSETS_DIR, "figure_5_3_usecase.png")
    if os.path.exists(img_uc):
        story.append(Image(img_uc, width=6.8*inch, height=4.2*inch))
    story.append(Paragraph("<b>Figure 5.3:</b> Use Case Diagram – Trader &amp; System Operations", caption))
    story.append(Paragraph(
        "The use case diagram highlights the interactions between the primary actor (Virtual Trader) and external cloud services. "
        "Traders register, stream live market data, execute simulated trades, trigger the Polynomial ML forecaster, and generate "
        "Explainable AI investment theses. The backend coordinates with Finnhub, Yahoo Finance, and Google Gemini to satisfy these requests.",
        body
    ))
    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════
    # PAGE 20: CHAPTER 5 (Cont.) - ACTIVITY & DFD
    # ════════════════════════════════════════════════════════════════
    story.append(Spacer(1, 2*mm))
    story.append(Paragraph("5.2.3 Activity Diagram", h2))
    img_act = os.path.join(ASSETS_DIR, "figure_5_4_activity.png")
    if os.path.exists(img_act):
        story.append(Image(img_act, width=6.8*inch, height=2.6*inch))
    story.append(Paragraph("<b>Figure 5.4:</b> Activity Diagram – Stock Analysis, Prediction &amp; Trade Workflow", caption))
    story.append(Paragraph(
        "The activity flow models the end-to-end user journey: authenticating, inspecting real-time price action, running the OLS "
        "polynomial forecast, synthesizing the AI Bull/Bear thesis, and placing a trade with atomic balance verification.",
        body
    ))

    story.append(Paragraph("5.2.4 Data Flow Diagram (Level 0)", h2))
    img_dfd = os.path.join(ASSETS_DIR, "figure_5_5_dfd.png")
    if os.path.exists(img_dfd):
        story.append(Image(img_dfd, width=6.8*inch, height=2.7*inch))
    story.append(Paragraph("<b>Figure 5.5:</b> Data Flow Diagram – Level 0 Context Diagram", caption))
    story.append(Paragraph(
        "The Level-0 DFD illustrates information flow between the central StockSphere process, external APIs (Finnhub, Yahoo, Gemini), "
        "and internal MongoDB data stores (Users, Portfolios, Trades, Posts).",
        body
    ))
    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════
    # PAGE 21: CHAPTER 5 (Cont.) - STATE & ER DIAGRAMS
    # ════════════════════════════════════════════════════════════════
    story.append(Spacer(1, 4*mm))
    story.append(Paragraph("5.2.5 State Diagram", h2))
    img_state = os.path.join(ASSETS_DIR, "figure_5_6_state.png")
    if os.path.exists(img_state):
        story.append(Image(img_state, width=6.8*inch, height=3.3*inch))
    story.append(Paragraph("<b>Figure 5.6:</b> Trade Lifecycle State Diagram", caption))
    story.append(Paragraph(
        "The trade state diagram models order transitions. A trade begins in Form Initiated, validates available cash and holdings, "
        "transitions to Execution Engine upon validation, or enters Order Rejected if funds are insufficient, concluding in Active Position.",
        body
    ))

    story.append(Spacer(1, 4*mm))
    story.append(Paragraph("5.2.6 E-R Diagram (Introduction)", h2))
    story.append(Paragraph(
        "The Entity-Relationship (ER) model defines the relational semantics of StockSphere's document schemas. "
        "A User maintains a 1-to-1 relationship with their Portfolio, a 1-to-Many relationship with historical Trades, "
        "and a 1-to-Many relationship with personalized Watchlist entries and Community Posts.",
        body
    ))
    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════
    # PAGE 22: CHAPTER 5 (Cont.) - ER & SEQUENCE DIAGRAMS
    # ════════════════════════════════════════════════════════════════
    story.append(Spacer(1, 2*mm))
    img_er = os.path.join(ASSETS_DIR, "figure_5_7_er.png")
    if os.path.exists(img_er):
        story.append(Image(img_er, width=6.8*inch, height=2.8*inch))
    story.append(Paragraph("<b>Figure 5.7:</b> Entity Relationship Diagram of StockSphere Database", caption))

    story.append(Paragraph("5.2.7 Sequence Diagram", h2))
    img_seq = os.path.join(ASSETS_DIR, "figure_5_8_sequence.png")
    if os.path.exists(img_seq):
        story.append(Image(img_seq, width=6.8*inch, height=2.8*inch))
    story.append(Paragraph("<b>Figure 5.8:</b> Sequence Diagram – ML Forecasting &amp; GenAI Thesis Generation", caption))
    story.append(Paragraph(
        "The sequence diagram details communication across the React client, Express API, Yahoo Finance, and Google Gemini LLM. "
        "The ML model calculates quadratic parameters, which are immediately passed into Gemini to generate the Explainable AI thesis.",
        body
    ))
    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════
    # PAGE 23: CHAPTER 5 (Cont.) - SYSTEM ARCHITECTURE
    # ════════════════════════════════════════════════════════════════
    story.append(Spacer(1, 4*mm))
    story.append(Paragraph("5.2.8 System Architecture", h2))
    img_arch = os.path.join(ASSETS_DIR, "figure_5_1_architecture.png")
    if os.path.exists(img_arch):
        story.append(Image(img_arch, width=6.8*inch, height=4.2*inch))
    story.append(Paragraph("<b>Figure 5.1:</b> Multi-Tier System Architecture Diagram", caption))
    story.append(Paragraph(
        "StockSphere follows a layered full-stack web architecture. The presentation layer (React, Vite, Tailwind CSS) communicates "
        "via REST and WebSockets. The security gateway enforces JWT and rate limits. The business layer coordinates the virtual trading engine, "
        "2nd-degree OLS regression predictor, and Google Gemini Explainable AI engine. Data is persisted in MongoDB Atlas.",
        body
    ))
    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════
    # PAGE 24: CHAPTER 6 - CODE IMPLEMENTATION
    # ════════════════════════════════════════════════════════════════
    story.append(Paragraph("CHAPTER – 6", h_chap))
    story.append(Paragraph("CODE IMPLEMENTATION", h_chap_title))

    story.append(Paragraph("6.1 Implementation Environment", h1))
    story.append(Paragraph(
        "StockSphere is implemented using a modern JavaScript/Node.js full-stack development environment:",
        body
    ))
    story.append(Paragraph("<b>Table 6.1:</b> Implementation Environment and Architectural Roles", caption))
    impl_env_data = [
        [Paragraph("<b>Layer</b>", th), Paragraph("<b>Technology</b>", th), Paragraph("<b>Implementation Role</b>", th)],
        [Paragraph("Presentation", td), Paragraph("React.js (v18) + Vite", td), Paragraph("Responsive client dashboards, modal trade forms, and Chart.js visuals", td)],
        [Paragraph("State Management", td), Paragraph("Redux Toolkit", td), Paragraph("Centralized state for quotes, active trades, portfolio, and auth tokens", td)],
        [Paragraph("Styling System", td), Paragraph("Tailwind CSS", td), Paragraph("Custom dark-theme styling, animations, and responsive breakpoints", td)],
        [Paragraph("Real-Time Engine", td), Paragraph("Socket.io (Client &amp; Server)", td), Paragraph("Sub-second stock price stream broadcasting and live community events", td)],
        [Paragraph("API Server", td), Paragraph("Node.js + Express.js", td), Paragraph("RESTful controllers, in-memory caching queues, and auth middleware", td)],
        [Paragraph("Machine Learning", td), Paragraph("Ordinary Least Squares (OLS)", td), Paragraph("2nd-degree polynomial regression, 5-day forecast, and R²/MAE metrics", td)],
        [Paragraph("Generative AI (XAI)", td), Paragraph("Google Gemini Flash API", td), Paragraph("Synthesizes quantitative metrics into Bull/Bear investment theses", td)],
        [Paragraph("Database &amp; ODM", td), Paragraph("MongoDB Atlas + Mongoose", td), Paragraph("Document modeling for users, portfolios, trades, and watchlists", td)],
        [Paragraph("Authentication", td), Paragraph("JWT + Bcrypt.js", td), Paragraph("Encrypted password storage and stateless bearer token validation", td)],
    ]
    t_ienv = Table(impl_env_data, colWidths=[35*mm, 45*mm, 90*mm])
    t_ienv.setStyle(tbl_grid_style)
    story.append(t_ienv)

    story.append(Paragraph("6.2 Program / Module Specification", h1))
    story.append(Paragraph("<b>Table 6.2:</b> System Modules and Functional Responsibilities", caption))
    mod_spec_data = [
        [Paragraph("<b>Module Name</b>", th), Paragraph("<b>File / Path</b>", th), Paragraph("<b>Functional Responsibility</b>", th)],
        [Paragraph("Auth Controller", td), Paragraph("backend/controllers/authController.js", td_code), Paragraph("User signup, password hashing, login verification, and JWT generation.", td)],
        [Paragraph("Stock Controller", td), Paragraph("backend/controllers/stockController.js", td_code), Paragraph("Finnhub quote caching, Yahoo historical candle retrieval, and status feeds.", td)],
        [Paragraph("ML Predictor Engine", td), Paragraph("backend/controllers/stockController.js", td_code), Paragraph("Executes 2nd-degree OLS regression, Vandermonde matrix, and Cramer's rule.", td)],
        [Paragraph("XAI Thesis Engine", td), Paragraph("backend/controllers/stockController.js", td_code), Paragraph("Prompts Gemini Flash for structured investment theses with neural fallback.", td)],
        [Paragraph("Portfolio Controller", td), Paragraph("backend/controllers/portfolioController.js", td_code), Paragraph("Atomic buy/sell execution, holding updates, cash check, and PnL calculation.", td)],
        [Paragraph("Socket Service", td), Paragraph("backend/socketService.js", td_code), Paragraph("Manages room subscriptions (join_stock) and broadcasts price fluctuations.", td)],
        [Paragraph("AI Thesis Component", td), Paragraph("frontend/src/components/AIInvestmentThesis.jsx", td_code), Paragraph("Renders Bull/Bear thesis cards, loading radar, risk badges, and copy action.", td)],
    ]
    t_mspec = Table(mod_spec_data, colWidths=[35*mm, 55*mm, 80*mm])
    t_mspec.setStyle(tbl_grid_style)
    story.append(t_mspec)
    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════
    # PAGE 25: CHAPTER 6 (Cont.) - CODING STANDARDS
    # ════════════════════════════════════════════════════════════════
    story.append(Spacer(1, 4*mm))
    story.append(Paragraph("6.3 Coding Standards", h1))
    story.append(Paragraph(
        "StockSphere maintains strict coding standards to ensure code readability, maintainability, and security across the codebase:",
        body
    ))
    story.append(Paragraph("• <b>Modular Separation of Concerns:</b> Frontend logic is cleanly separated into presentation components, Redux slices, and Axios API services. Backend logic is organized into routing, controllers, middleware, and data models.", bullet))
    story.append(Paragraph("• <b>Predictable Error Handling:</b> All asynchronous controller handlers utilize try-catch blocks returning structured JSON responses ({ success: Boolean, message: String, data?: Object }). Unhandled exceptions are logged server-side without crashing.", bullet))
    story.append(Paragraph("• <b>Zero-Crash AI Fallback Design:</b> The Generative AI investment thesis endpoint enforces multi-layer catch blocks. If external APIs or environment variables are unavailable, a high-precision grounded neural thesis is returned seamlessly.", bullet))
    story.append(Paragraph("• <b>RESTful URI Conventions:</b> Endpoints adhere to semantic REST standards (GET /api/stocks/quote/:symbol, GET /api/stocks/predict/:symbol, GET /api/stocks/thesis/:symbol, POST /api/portfolio/trade).", bullet))
    story.append(Paragraph("• <b>Component Reusability:</b> Complex UI widgets such as StockChart, AIInvestmentThesis, Navbar, and Sidebar are encapsulated into reusable React components.", bullet))
    story.append(Paragraph("• <b>Cryptographic Salt Security:</b> Passwords utilize standard bcrypt salting (12 rounds) enforced automatically through Mongoose pre-save middleware.", bullet))
    story.append(Paragraph("• <b>Environment Variable Protection:</b> Database connection strings, API keys, and JWT secrets are externalized in .env files and excluded from version control via .gitignore.", bullet))
    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════
    # PAGE 26: CHAPTER 7 - TESTING
    # ════════════════════════════════════════════════════════════════
    story.append(Paragraph("CHAPTER – 7", h_chap))
    story.append(Paragraph("TESTING", h_chap_title))

    story.append(Paragraph("7.1 Testing Strategy", h1))
    story.append(Paragraph(
        "The testing strategy verifies individual components, API controllers, machine learning mathematical accuracy, "
        "and full-stack integrated workflows. Testing comprises three levels: Unit Testing of isolated functions, "
        "Integration Testing across client-server boundaries, and Validation Testing of real-world user workflows.",
        body
    ))

    story.append(Paragraph("7.2 Testing Method", h1))
    story.append(Paragraph("7.2.1 Unit Testing", h2))
    story.append(Paragraph(
        "Unit testing evaluates individual units of code in isolation: password bcrypt hashing, JWT token signing/verification, "
        "ordinary least squares matrix inversion, R² and MAE calculations, and Redux state reducers.",
        body
    ))

    story.append(Paragraph("7.2.2 Integration Testing", h2))
    story.append(Paragraph(
        "Integration testing verifies that client requests correctly flow through Express middleware, query MongoDB collections, "
        "and return structured payloads. Specifically, placing a virtual trade verifies that cash balances and portfolio holdings "
        "update in lockstep.",
        body
    ))

    story.append(Paragraph("7.2.3 Validation Testing", h2))
    story.append(Paragraph(
        "Validation testing confirms that the application satisfies all user requirements: searching symbols, viewing real-time charts, "
        "running the 5-day ML forecaster, generating the GenAI Bull/Bear thesis, and managing watchlists.",
        body
    ))

    story.append(Paragraph("7.3 Test Cases", h1))
    story.append(Paragraph("<b>Table 7.1:</b> System Test Cases and Execution Results (Part 1)", caption))
    tc_data_1 = [
        [Paragraph("<b>ID</b>", th), Paragraph("<b>Module</b>", th), Paragraph("<b>Test Condition</b>", th), Paragraph("<b>Expected Result</b>", th), Paragraph("<b>Status</b>", th)],
        [Paragraph("TC-01", td), Paragraph("Auth", td), Paragraph("Register with valid email &amp; 6+ char password", td), Paragraph("User account created with $100,000 balance", td), Paragraph("PASS", td)],
        [Paragraph("TC-02", td), Paragraph("Auth", td), Paragraph("Register with existing registered email", td), Paragraph("Rejected with 400 'User already exists'", td), Paragraph("PASS", td)],
        [Paragraph("TC-03", td), Paragraph("Auth", td), Paragraph("Login with valid credentials", td), Paragraph("Returns JWT token; navigates to dashboard", td), Paragraph("PASS", td)],
        [Paragraph("TC-04", td), Paragraph("Auth", td), Paragraph("Login with incorrect password", td), Paragraph("Denied with 401 'Invalid credentials'", td), Paragraph("PASS", td)],
        [Paragraph("TC-05", td), Paragraph("Market", td), Paragraph("Search symbol 'AAPL'", td), Paragraph("Returns matching Common Stock results", td), Paragraph("PASS", td)],
        [Paragraph("TC-06", td), Paragraph("Market", td), Paragraph("Fetch quote for valid symbol", td), Paragraph("Returns price, open, high, low, marketCap", td), Paragraph("PASS", td)],
        [Paragraph("TC-07", td), Paragraph("Market", td), Paragraph("Rapid consecutive quote requests (&gt;30/min)", td), Paragraph("Served from in-memory cache; no 429 error", td), Paragraph("PASS", td)],
    ]
    t_tc1 = Table(tc_data_1, colWidths=[15*mm, 20*mm, 52*mm, 68*mm, 15*mm])
    t_tc1.setStyle(tbl_grid_style)
    story.append(t_tc1)
    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════
    # PAGE 27: CHAPTER 7 (Cont.) - TEST CASES & TEST SUITE
    # ════════════════════════════════════════════════════════════════
    story.append(Spacer(1, 4*mm))
    story.append(Paragraph("7.3 Test Cases (Continued)", h1))
    story.append(Paragraph("<b>Table 7.1:</b> System Test Cases and Execution Results (Part 2)", caption))
    tc_data_2 = [
        [Paragraph("<b>ID</b>", th), Paragraph("<b>Module</b>", th), Paragraph("<b>Test Condition</b>", th), Paragraph("<b>Expected Result</b>", th), Paragraph("<b>Status</b>", th)],
        [Paragraph("TC-08", td), Paragraph("Trading", td), Paragraph("Execute BUY order with sufficient virtual cash", td), Paragraph("Cash deducted; shares logged into portfolio", td), Paragraph("PASS", td)],
        [Paragraph("TC-09", td), Paragraph("Trading", td), Paragraph("Execute BUY order with cash &lt; total cost", td), Paragraph("Rejected with 'Insufficient balance'", td), Paragraph("PASS", td)],
        [Paragraph("TC-10", td), Paragraph("Trading", td), Paragraph("Execute SELL order for owned shares", td), Paragraph("Cash credited; holding quantity decreased", td), Paragraph("PASS", td)],
        [Paragraph("TC-11", td), Paragraph("Trading", td), Paragraph("Execute SELL order exceeding owned quantity", td), Paragraph("Rejected with 'Insufficient shares owned'", td), Paragraph("PASS", td)],
        [Paragraph("TC-12", td), Paragraph("ML Model", td), Paragraph("Request /api/stocks/predict/AAPL", td), Paragraph("Returns 5-day forecast, formula, R², MAE", td), Paragraph("PASS", td)],
        [Paragraph("TC-13", td), Paragraph("ML Model", td), Paragraph("Evaluate model with flat/negative price slope", td), Paragraph("Correctly classifies trend as 'Bearish'", td), Paragraph("PASS", td)],
        [Paragraph("TC-14", td), Paragraph("GenAI", td), Paragraph("Request /api/stocks/thesis/AAPL with Gemini API", td), Paragraph("Returns Bull/Bear thesis memo via LLM", td), Paragraph("PASS", td)],
        [Paragraph("TC-15", td), Paragraph("GenAI", td), Paragraph("Request thesis with invalid/missing API key", td), Paragraph("Seamless fallback to grounded neural engine", td), Paragraph("PASS", td)],
        [Paragraph("TC-16", td), Paragraph("Watchlist", td), Paragraph("Add &amp; remove stock from watchlist", td), Paragraph("Watchlist table updates state instantly", td), Paragraph("PASS", td)],
        [Paragraph("TC-17", td), Paragraph("Sockets", td), Paragraph("User visits stock page (join_stock)", td), Paragraph("Receives live price fluctuations via socket", td), Paragraph("PASS", td)],
        [Paragraph("TC-18", td), Paragraph("Security", td), Paragraph("Access /api/portfolio without JWT header", td), Paragraph("Denied with 401 'Not authorized'", td), Paragraph("PASS", td)],
    ]
    t_tc2 = Table(tc_data_2, colWidths=[15*mm, 20*mm, 52*mm, 68*mm, 15*mm])
    t_tc2.setStyle(tbl_grid_style)
    story.append(t_tc2)

    story.append(Spacer(1, 4*mm))
    story.append(Paragraph("7.3.1 Test Suite", h1))
    story.append(Paragraph("<b>Table 7.2:</b> Consolidated Test Suite Summary", caption))
    suite_data = [
        [Paragraph("<b>Test Area</b>", th), Paragraph("<b>Test Cases</b>", th), Paragraph("<b>Expected Outcome</b>", th), Paragraph("<b>Execution Status</b>", th)],
        [Paragraph("User Authentication", td), Paragraph("TC-01 to TC-04", td), Paragraph("Secure registration, token issuance, and password verification", td), Paragraph("VERIFIED (100%)", td)],
        [Paragraph("Market Quotes &amp; Cache", td), Paragraph("TC-05 to TC-07", td), Paragraph("Live price retrieval, ticker search, rate-limit cache defense", td), Paragraph("VERIFIED (100%)", td)],
        [Paragraph("Virtual Trading Engine", td), Paragraph("TC-08 to TC-11", td), Paragraph("Atomic buy/sell execution, portfolio balance consistency", td), Paragraph("VERIFIED (100%)", td)],
        [Paragraph("ML Forecaster (OLS)", td), Paragraph("TC-12 to TC-13", td), Paragraph("Accurate quadratic curve fitting, R² variance, trend flag", td), Paragraph("VERIFIED (100%)", td)],
        [Paragraph("Explainable AI (XAI)", td), Paragraph("TC-14 to TC-15", td), Paragraph("Structured Bull/Bear thesis generation and zero-error fallback", td), Paragraph("VERIFIED (100%)", td)],
        [Paragraph("Watchlist &amp; Sockets", td), Paragraph("TC-16 to TC-18", td), Paragraph("Real-time watchlist sync, WebSocket streaming, and route guards", td), Paragraph("VERIFIED (100%)", td)],
    ]
    t_suite = Table(suite_data, colWidths=[35*mm, 28*mm, 82*mm, 25*mm])
    t_suite.setStyle(tbl_grid_style)
    story.append(t_suite)
    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════
    # PAGE 28: CHAPTER 8 - LIMITATIONS AND FUTURE ENHANCEMENT
    # ════════════════════════════════════════════════════════════════
    story.append(Paragraph("CHAPTER – 8", h_chap))
    story.append(Paragraph("LIMITATIONS AND FUTURE ENHANCEMENT", h_chap_title))

    story.append(Paragraph("8.1 Limitations", h1))
    story.append(Paragraph("• <b>Virtual Simulation Environment:</b> StockSphere operates as an educational virtual trading platform. Simulated orders do not execute on real financial exchanges (e.g. NYSE/NASDAQ).", bullet))
    story.append(Paragraph("• <b>US Equity Focus:</b> Current market data ingestion is calibrated primarily for US equities (Common Stocks) supported by Finnhub and Yahoo Finance.", bullet))
    story.append(Paragraph("• <b>Free API Quotas:</b> Free external API tiers restrict candle resolutions and historical depth, requiring smart server-side caching.", bullet))
    story.append(Paragraph("• <b>Univariate Price Modeling:</b> The 2nd-degree polynomial regression model forecasts prices based on historical closing values without ingesting multi-variable macroeconomic indicators (e.g., interest rates, inflation).", bullet))
    story.append(Paragraph("• <b>Simulated Slippage &amp; Order Book:</b> Real-world exchange factors such as bid-ask spread slippage and limit-order queues are simplified for educational clarity.", bullet))

    story.append(Spacer(1, 4*mm))
    story.append(Paragraph("8.2 Future Enhancement", h1))
    story.append(Paragraph("• <b>Deep Learning Integration:</b> Complement polynomial regression with recurrent neural networks (LSTM / GRU) or Transformer models (Informer) for long-range sequence prediction.", bullet))
    story.append(Paragraph("• <b>Multivariate Market Grounding:</b> Feed corporate earnings transcripts, SEC 10-K filings, and live news sentiment into the Generative AI prompt for deeper thesis reasoning.", bullet))
    story.append(Paragraph("• <b>Automated Algorithmic Trading Bots:</b> Allow users to define custom rule-based trading algorithms (e.g., Moving Average Crossover, RSI) that trade automatically on virtual funds.", bullet))
    story.append(Paragraph("• <b>Global Multi-Asset Support:</b> Expand the trading catalog to include Indian stock markets (NSE/BSE), international indices, cryptocurrencies, and commodities.", bullet))
    story.append(Paragraph("• <b>Social Trading &amp; Leaderboards:</b> Implement ranked performance leaderboards where users can follow and mirror top-performing virtual portfolios.", bullet))
    story.append(Paragraph("• <b>Native Mobile Applications:</b> Package the responsive web application into native iOS and Android apps using React Native.", bullet))
    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════
    # PAGE 29: CHAPTER 9 - CONCLUSION
    # ════════════════════════════════════════════════════════════════
    story.append(Spacer(1, 4*mm))
    story.append(Paragraph("CHAPTER – 9", h_chap))
    story.append(Paragraph("CONCLUSION", h_chap_title))

    story.append(Paragraph(
        "<b>StockSphere</b> successfully demonstrates how modern web engineering, econometric Machine Learning, and Generative Artificial "
        "Intelligence can unite to solve fundamental problems in stock market education. By creating a risk-free virtual trading laboratory "
        "with a $100,000 cash balance, users can practice real-time investing without the danger of financial loss.",
        body
    ))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(
        "The project directly addresses the limitations of traditional trading platforms. Leveraging <b>WebSockets (Socket.io)</b> and an "
        "in-memory serialization queue, the system delivers real-time market ticks while bypassing free-tier rate limits. "
        "The quantitative <b>2nd-degree Polynomial Least-Squares Regression model</b> provides mathematical rigor, forecasting 5-day price "
        "trajectories, statistical variance (R²), and trend classification (Bullish/Bearish).",
        body
    ))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(
        "Most importantly, StockSphere breaks through the traditional <b>'black-box' dilemma</b> of machine learning by introducing an "
        "institutional-grade <b>Explainable AI (XAI)</b> layer powered by Google Gemini. This generative layer translates complex mathematical "
        "coefficients and confidence bounds into an intuitive <b>Bull vs. Bear Investment Thesis</b> complete with upside catalysts, downside "
        "risks, and actionable trading tactics. The dual-engine architecture ensures 100% operational reliability with zero runtime errors.",
        body
    ))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(
        "Developed using the MERN stack (MongoDB, Express.js, React 18, Node.js) with Tailwind CSS and Redux Toolkit, StockSphere fulfills "
        "all functional and non-functional requirements. The system provides an extensible foundation for future financial technology innovations, "
        "deep-learning models, and algorithmic trading simulators.",
        body
    ))
    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════
    # PAGE 30: CHAPTER 10 - REFERENCES
    # ════════════════════════════════════════════════════════════════
    story.append(Spacer(1, 4*mm))
    story.append(Paragraph("CHAPTER – 10", h_chap))
    story.append(Paragraph("REFERENCES", h_chap_title))

    story.append(Paragraph(
        "The following academic publications, technical documentations, and specifications were referenced during the development of StockSphere:",
        body
    ))
    story.append(Spacer(1, 2*mm))

    ref_data = [
        [Paragraph("<b>No.</b>", th), Paragraph("<b>Reference / Technology</b>", th), Paragraph("<b>Source / Documentation URI</b>", th)],
        [Paragraph("1", td), Paragraph("React 18 Official Documentation", td), Paragraph("https://react.dev/reference/react", td)],
        [Paragraph("2", td), Paragraph("Node.js Runtime Documentation (v20 LTS)", td), Paragraph("https://nodejs.org/en/docs", td)],
        [Paragraph("3", td), Paragraph("Express.js Web Application Framework", td), Paragraph("https://expressjs.com/", td)],
        [Paragraph("4", td), Paragraph("MongoDB Atlas &amp; Mongoose ODM Manual", td), Paragraph("https://mongoosejs.com/docs/guide.html", td)],
        [Paragraph("5", td), Paragraph("Socket.io Real-Time Engine Documentation", td), Paragraph("https://socket.io/docs/v4/", td)],
        [Paragraph("6", td), Paragraph("Chart.js HTML5 Financial Charting Guide", td), Paragraph("https://www.chartjs.org/docs/latest/", td)],
        [Paragraph("7", td), Paragraph("Finnhub Financial Market API Documentation", td), Paragraph("https://finnhub.io/docs/api", td)],
        [Paragraph("8", td), Paragraph("Yahoo Finance Market Chart API Specification", td), Paragraph("https://query1.finance.yahoo.com/", td)],
        [Paragraph("9", td), Paragraph("Google Gemini API &amp; Generative AI Documentation", td), Paragraph("https://ai.google.dev/docs", td)],
        [Paragraph("10", td), Paragraph("Ordinary Least Squares (OLS) Polynomial Regression in Econometrics (Greene, W. H.)", td), Paragraph("Econometric Analysis, 8th Edition, Pearson Education", td)],
        [Paragraph("11", td), Paragraph("Explainable Artificial Intelligence (XAI) Concepts (Gunning, D. et al.)", td), Paragraph("DARPA XAI Program, Communications of the ACM", td)],
        [Paragraph("12", td), Paragraph("OWASP Web Application Security Verification Standard", td), Paragraph("https://owasp.org/www-project-asvs/", td)],
    ]
    t_ref = Table(ref_data, colWidths=[12*mm, 68*mm, 90*mm])
    t_ref.setStyle(tbl_grid_style)
    story.append(t_ref)

    story.append(Spacer(1, 6*mm))
    story.append(Paragraph(
        "<b>Note:</b> Documentation links and academic citations follow standard university submission guidelines. "
        "Consulted versions and API endpoints reflect live development configurations.",
        ParagraphStyle('RefNote', fontName='Helvetica-Oblique', fontSize=8.5, leading=12, textColor=colors.HexColor('#4a5568'))
    ))
    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════
    # PAGE 31: PROJECT MODULE SUMMARY
    # ════════════════════════════════════════════════════════════════
    story.append(Spacer(1, 4*mm))
    story.append(Paragraph("PROJECT MODULE SUMMARY", t_center))
    story.append(Spacer(1, 6*mm))

    story.append(Paragraph(
        "This section provides a concise module-to-requirement mapping that can be directly referenced during viva or final project review:",
        body
    ))
    story.append(Spacer(1, 4*mm))

    summary_data = [
        [Paragraph("<b>Module</b>", th), Paragraph("<b>Primary Users</b>", th), Paragraph("<b>Main Purpose &amp; Architectural Role</b>", th)],
        [
            Paragraph("User Authentication &amp; Security", td),
            Paragraph("All Users", td),
            Paragraph("Registers users, enforces bcrypt password hashing, issues JWT tokens, and protects private routes.", td)
        ],
        [
            Paragraph("Real-Time Market Streaming", td),
            Paragraph("Traders / Investors", td),
            Paragraph("Streams live stock price ticks via Socket.io with smart 60s memory caching and queue serialization.", td)
        ],
        [
            Paragraph("Stock Analysis &amp; Charting", td),
            Paragraph("Traders / Analysts", td),
            Paragraph("Renders interactive multi-timeframe price charts (1D, 1W, 1M, 1Y) using Chart.js and Yahoo Finance data.", td)
        ],
        [
            Paragraph("Virtual Trading &amp; Portfolio", td),
            Paragraph("Virtual Traders", td),
            Paragraph("Executes Buy/Sell transactions against a $100,000 cash balance and computes dynamic PnL &amp; total returns.", td)
        ],
        [
            Paragraph("Polynomial Regression ML Engine", td),
            Paragraph("Traders / Evaluators", td),
            Paragraph("Fits a 2nd-degree OLS polynomial curve to 30-day candles to forecast 5-day prices and Bull/Bear trends.", td)
        ],
        [
            Paragraph("Explainable AI (XAI) Thesis", td),
            Paragraph("Traders / Evaluators", td),
            Paragraph("Translates mathematical regression curves into institutional Bull/Bear investment memos via Gemini Flash.", td)
        ],
        [
            Paragraph("Personalized Watchlist", td),
            Paragraph("All Traders", td),
            Paragraph("Allows users to curate, monitor, and quickly access high-priority equity symbols with live price ticks.", td)
        ],
        [
            Paragraph("Live Community Forum", td),
            Paragraph("Community Members", td),
            Paragraph("Enables social trading: users publish analysis posts, comment, and like feeds broadcasted live via Socket.io.", td)
        ],
    ]
    t_summary = Table(summary_data, colWidths=[40*mm, 35*mm, 95*mm])
    t_summary.setStyle(tbl_grid_style)
    story.append(t_summary)

    story.append(Spacer(1, 15*mm))
    story.append(Paragraph("<b>End of Report</b>", ParagraphStyle('EndOfRep', fontName='Helvetica-Bold', fontSize=11, leading=15, alignment=1, textColor=colors.HexColor('#1a202c'))))

    # Build document with custom NumberedCanvas
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Report PDF successfully generated at: {PDF_PATH}")

if __name__ == "__main__":
    create_report()
