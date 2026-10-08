import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

DOCX_PATH = os.path.join(os.path.dirname(__file__), "StockSphere_Project_Report.docx")
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "report_assets")

def set_cell_background(cell, hex_color="F2F2F2"):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        print(node)
        tcMar.append(node)
    tcPr.append(tcMar)

def set_table_borders(table, color="D3D3D3", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'  <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:left w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:right w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:insideV w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def add_header_cell(row, col_idx, text, width=None):
    cell = row.cells[col_idx]
    if width:
        cell.width = width
    set_cell_background(cell, "EAEAEA")
    set_cell_margins(cell, top=120, bottom=120, left=150, right=150)
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    run = p.add_run(text)
    run.bold = True
    run.font.name = "Calibri"
    run.font.size = Pt(10)
    run.font.color.rgb = RGBColor(0, 0, 0)
    return cell

def add_data_cell(row, col_idx, text, width=None, bold=False, italic=False):
    cell = row.cells[col_idx]
    if width:
        cell.width = width
    set_cell_margins(cell, top=100, bottom=100, left=150, right=150)
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    run = p.add_run(text)
    run.bold = bold
    run.italic = italic
    run.font.name = "Calibri"
    run.font.size = Pt(9.5)
    run.font.color.rgb = RGBColor(30, 30, 30)
    return cell

def add_para(doc, text="", bold_prefix=None, space_after=6, space_before=0, align=WD_ALIGN_PARAGRAPH.JUSTIFY, size=11, font_name="Calibri"):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.bold = True
        r_pre.font.name = font_name
        r_pre.font.size = Pt(size)
        r_pre.font.color.rgb = RGBColor(0, 0, 0)
    if text:
        r = p.add_run(text)
        r.font.name = font_name
        r.font.size = Pt(size)
        r.font.color.rgb = RGBColor(30, 30, 30)
    return p

def add_bullet(doc, text, bold_prefix=None, space_after=4):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.bold = True
        r_pre.font.name = "Calibri"
        r_pre.font.size = Pt(10.5)
    if text:
        r = p.add_run(text)
        r.font.name = "Calibri"
        r.font.size = Pt(10.5)
        r.font.color.rgb = RGBColor(30, 30, 30)
    return p

def add_heading_1(doc, text, space_before=14, space_after=6):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.bold = True
    r.font.name = "Calibri"
    r.font.size = Pt(13)
    r.font.color.rgb = RGBColor(0, 0, 0)
    return p

def add_heading_2(doc, text, space_before=10, space_after=4):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.bold = True
    r.font.name = "Calibri"
    r.font.size = Pt(11.5)
    r.font.color.rgb = RGBColor(30, 30, 30)
    return p

def add_chapter_title(doc, chap_num, title):
    p_chap = doc.add_paragraph()
    p_chap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_chap.paragraph_format.space_before = Pt(6)
    p_chap.paragraph_format.space_after = Pt(2)
    p_chap.paragraph_format.keep_with_next = True
    r_c = p_chap.add_run(f"CHAPTER - {chap_num}")
    r_c.bold = True
    r_c.font.name = "Calibri"
    r_c.font.size = Pt(14)
    r_c.font.color.rgb = RGBColor(0, 0, 0)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(2)
    p_title.paragraph_format.space_after = Pt(14)
    p_title.paragraph_format.keep_with_next = True
    r_t = p_title.add_run(title)
    r_t.bold = True
    r_t.font.name = "Calibri"
    r_t.font.size = Pt(15)
    r_t.font.color.rgb = RGBColor(0, 0, 0)

def add_diagram(doc, img_name, fig_title, width_inches=6.0):
    img_path = os.path.join(ASSETS_DIR, img_name)
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(6)
        p_img.paragraph_format.space_after = Pt(4)
        run = p_img.add_run()
        run.add_picture(img_path, width=Inches(width_inches))

        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(2)
        p_cap.paragraph_format.space_after = Pt(10)
        r_cap = p_cap.add_run(fig_title)
        r_cap.bold = True
        r_cap.italic = True
        r_cap.font.name = "Calibri"
        r_cap.font.size = Pt(10)
        r_cap.font.color.rgb = RGBColor(60, 60, 60)

def build_docx_report():
    doc = docx.Document()

    # Set Margins (1 inch everywhere)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        section.page_width = Inches(8.27)  # A4
        section.page_height = Inches(11.69)

    # ════════════════════════════════════════════════════════════════
    # PAGE 1: TITLE PAGE
    # ════════════════════════════════════════════════════════════════
    p_u = doc.add_paragraph()
    p_u.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_u.paragraph_format.space_before = Pt(10)
    p_u.paragraph_format.space_after = Pt(2)
    r_u = p_u.add_run("ATMIYA UNIVERSITY")
    r_u.bold = True
    r_u.font.name = "Calibri"
    r_u.font.size = Pt(18)
    r_u.font.color.rgb = RGBColor(0, 0, 0)

    p_r = doc.add_paragraph()
    p_r.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_r.paragraph_format.space_before = Pt(0)
    p_r.paragraph_format.space_after = Pt(12)
    r_r = p_r.add_run("RAJKOT")
    r_r.bold = True
    r_r.font.name = "Calibri"
    r_r.font.size = Pt(14)
    r_r.font.color.rgb = RGBColor(0, 0, 0)

    # Emblem (Black and White)
    logo_path = os.path.join(ASSETS_DIR, "atmiya_logo.png")
    if os.path.exists(logo_path):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_before = Pt(0)
        p_logo.paragraph_format.space_after = Pt(12)
        p_logo.add_run().add_picture(logo_path, width=Inches(1.8))

    p_rep = doc.add_paragraph()
    p_rep.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_rep.paragraph_format.space_before = Pt(6)
    p_rep.paragraph_format.space_after = Pt(4)
    r_rep = p_rep.add_run("A\nReport On")
    r_rep.font.name = "Calibri"
    r_rep.font.size = Pt(12)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(4)
    p_title.paragraph_format.space_after = Pt(8)
    r_t = p_title.add_run("StockSphere: Virtual Stock Trading & AI-Powered Market Forecasting System with Explainable AI")
    r_t.bold = True
    r_t.font.name = "Calibri"
    r_t.font.size = Pt(15)
    r_t.font.color.rgb = RGBColor(0, 0, 0)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(4)
    p_sub.paragraph_format.space_after = Pt(2)
    r_sub = p_sub.add_run("Under subject of\n")
    r_sub.font.name = "Calibri"
    r_sub.font.size = Pt(11)
    r_sub_b = p_sub.add_run("MINI PROJECT\n")
    r_sub_b.bold = True
    r_sub_b.font.name = "Calibri"
    r_sub_b.font.size = Pt(12)
    r_sub_c = p_sub.add_run("B.TECH, Semester – VII\n(Computer Engineering)")
    r_sub_c.font.name = "Calibri"
    r_sub_c.font.size = Pt(11)

    p_by = doc.add_paragraph()
    p_by.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_by.paragraph_format.space_before = Pt(12)
    p_by.paragraph_format.space_after = Pt(4)
    r_by_lbl = p_by.add_run("Submitted by:\n")
    r_by_lbl.bold = True
    r_by_lbl.font.size = Pt(10.5)
    r_by_names = p_by.add_run("Kavy Gami [Enrollment No. 1]\n[STUDENT NAME 2] [ENROLLMENT NO. 2]")
    r_by_names.bold = True
    r_by_names.font.size = Pt(11)

    p_guide = doc.add_paragraph()
    p_guide.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_guide.paragraph_format.space_before = Pt(8)
    p_guide.paragraph_format.space_after = Pt(2)
    r_g = p_guide.add_run("Prof. [GUIDE NAME]\n(Faculty Guide)")
    r_g.bold = True
    r_g.font.size = Pt(11)

    p_hod = doc.add_paragraph()
    p_hod.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_hod.paragraph_format.space_before = Pt(6)
    p_hod.paragraph_format.space_after = Pt(2)
    r_h = p_hod.add_run("Prof. Tosal M. Bhalodia\n(Head of the Department)")
    r_h.bold = True
    r_h.font.size = Pt(11)

    p_ay = doc.add_paragraph()
    p_ay.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_ay.paragraph_format.space_before = Pt(6)
    p_ay.paragraph_format.space_after = Pt(0)
    r_ay = p_ay.add_run("Academic Year\n(2026-27)")
    r_ay.bold = True
    r_ay.font.size = Pt(11)

    doc.add_page_break()

    # ════════════════════════════════════════════════════════════════
    # PAGE 2: CANDIDATE’S DECLARATION
    # ════════════════════════════════════════════════════════════════
    add_para(doc, "CANDIDATE'S DECLARATION", space_before=20, space_after=20, align=WD_ALIGN_PARAGRAPH.CENTER, size=15)
    add_para(
        doc,
        "We hereby declare that the work presented in this project entitled \"StockSphere: Virtual Stock Trading & AI-Powered Market Forecasting System with Explainable AI\" submitted towards completion of the project in 7th Semester of B.Tech. (Computer Engineering) is an authentic record of our original work carried out under the guidance of Prof. [GUIDE NAME].",
        space_after=14, size=11
    )
    add_para(
        doc,
        "We have not submitted the matter embodied in this project for the award of any other degree or diploma.",
        space_after=24, size=11
    )
    add_para(doc, "Semester: 7th", space_after=4, align=WD_ALIGN_PARAGRAPH.LEFT, size=11)
    add_para(doc, "Place: Rajkot", space_after=4, align=WD_ALIGN_PARAGRAPH.LEFT, size=11)
    add_para(doc, "Date: ______________", space_after=30, align=WD_ALIGN_PARAGRAPH.LEFT, size=11)

    t_decl = doc.add_table(rows=2, cols=2)
    t_decl.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_decl.rows[0].cells[0].paragraphs[0].text = "Signature: __________________________\nKavy Gami ([ENROLLMENT NO. 1])"
    t_decl.rows[0].cells[1].paragraphs[0].text = "Signature: __________________________\n[STUDENT NAME 2] ([ENROLLMENT NO. 2])"
    for r in t_decl.rows:
        for c in r.cells:
            for p in c.paragraphs:
                p.paragraph_format.line_spacing = 1.2
                for run in p.runs:
                    run.font.name = "Calibri"
                    run.font.size = Pt(10.5)

    doc.add_page_break()

    # ════════════════════════════════════════════════════════════════
    # PAGE 3: CERTIFICATE (Student 1)
    # ════════════════════════════════════════════════════════════════
    add_para(doc, "ATMIYA UNIVERSITY", space_before=10, space_after=2, align=WD_ALIGN_PARAGRAPH.CENTER, size=16)
    add_para(doc, "RAJKOT", space_before=0, space_after=12, align=WD_ALIGN_PARAGRAPH.CENTER, size=13)
    if os.path.exists(logo_path):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_after = Pt(14)
        p_logo.add_run().add_picture(logo_path, width=Inches(1.5))
    add_para(doc, "CERTIFICATE", space_before=6, space_after=14, align=WD_ALIGN_PARAGRAPH.CENTER, size=14)
    add_para(doc, "Date: ______________", space_after=14, align=WD_ALIGN_PARAGRAPH.LEFT, size=10.5)
    add_para(
        doc,
        "This is to certify that the \"StockSphere: Virtual Stock Trading & AI-Powered Market Forecasting System with Explainable AI\" has been carried out by Kavy Gami [Enrollment No. 1] under my guidance in fulfillment of the subject Mini Project in COMPUTER ENGINEERING (7th Semester) of Atmiya University, Rajkot during the academic year 2026-27.",
        space_after=40, size=11
    )

    t_cert = doc.add_table(rows=1, cols=2)
    t_cert.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_cert.rows[0].cells[0].paragraphs[0].text = "Prof. [GUIDE NAME]\n(Project Guide)"
    t_cert.rows[0].cells[1].paragraphs[0].text = "Prof. Tosal M. Bhalodia\n(Head of the Department)"
    for r in t_cert.rows:
        for c in r.cells:
            for p in c.paragraphs:
                p.paragraph_format.line_spacing = 1.2
                for run in p.runs:
                    run.font.name = "Calibri"
                    run.font.size = Pt(11)
                    run.bold = True

    doc.add_page_break()

    # ════════════════════════════════════════════════════════════════
    # PAGE 4: CERTIFICATE (Student 2)
    # ════════════════════════════════════════════════════════════════
    add_para(doc, "ATMIYA UNIVERSITY", space_before=10, space_after=2, align=WD_ALIGN_PARAGRAPH.CENTER, size=16)
    add_para(doc, "RAJKOT", space_before=0, space_after=12, align=WD_ALIGN_PARAGRAPH.CENTER, size=13)
    if os.path.exists(logo_path):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_after = Pt(14)
        p_logo.add_run().add_picture(logo_path, width=Inches(1.5))
    add_para(doc, "CERTIFICATE", space_before=6, space_after=14, align=WD_ALIGN_PARAGRAPH.CENTER, size=14)
    add_para(doc, "Date: ______________", space_after=14, align=WD_ALIGN_PARAGRAPH.LEFT, size=10.5)
    add_para(
        doc,
        "This is to certify that the \"StockSphere: Virtual Stock Trading & AI-Powered Market Forecasting System with Explainable AI\" has been carried out by [STUDENT NAME 2] [Enrollment No. 2] under my guidance in fulfillment of the subject Mini Project in COMPUTER ENGINEERING (7th Semester) of Atmiya University, Rajkot during the academic year 2026-27.",
        space_after=40, size=11
    )
    t_cert2 = doc.add_table(rows=1, cols=2)
    t_cert2.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_cert2.rows[0].cells[0].paragraphs[0].text = "Prof. [GUIDE NAME]\n(Project Guide)"
    t_cert2.rows[0].cells[1].paragraphs[0].text = "Prof. Tosal M. Bhalodia\n(Head of the Department)"
    for r in t_cert2.rows:
        for c in r.cells:
            for p in c.paragraphs:
                p.paragraph_format.line_spacing = 1.2
                for run in p.runs:
                    run.font.name = "Calibri"
                    run.font.size = Pt(11)
                    run.bold = True

    doc.add_page_break()

    # ════════════════════════════════════════════════════════════════
    # PAGE 5: ACKNOWLEDGEMENT
    # ════════════════════════════════════════════════════════════════
    add_para(doc, "ACKNOWLEDGEMENT", space_before=16, space_after=16, align=WD_ALIGN_PARAGRAPH.CENTER, size=15)
    add_para(
        doc,
        "We have taken many efforts in this project. However, it would not have been possible without the kind support and help of many individuals and organizations. We would like to extend our sincere thanks to all of them.",
        space_after=10, size=11
    )
    add_para(
        doc,
        "We are highly indebted to Prof. [GUIDE NAME] for guidance, continuous supervision, valuable suggestions, and encouragement throughout the development of the project titled \"StockSphere: Virtual Stock Trading & AI-Powered Market Forecasting System with Explainable AI\".",
        space_after=10, size=11
    )
    add_para(
        doc,
        "We express our gratitude to the faculty members and staff of the Computer Engineering Department, Atmiya University, Rajkot, for their cooperation, technical guidance, and academic support.",
        space_after=10, size=11
    )
    add_para(
        doc,
        "We also thank our classmates, friends, and everyone who contributed directly or indirectly to the successful completion of this mini project.",
        space_after=10, size=11
    )
    add_para(
        doc,
        "Finally, we appreciate the efforts of every project team member in requirements analysis, architecture design, machine learning econometric modeling, Generative AI prompt engineering, frontend/backend implementation, rigorous testing, documentation, and presentation of the system.",
        space_after=30, size=11
    )
    add_para(doc, "Kavy Gami ([ENROLLMENT NO. 1])", space_after=4, align=WD_ALIGN_PARAGRAPH.RIGHT, size=11)
    add_para(doc, "[STUDENT NAME 2] ([ENROLLMENT NO. 2])", space_after=0, align=WD_ALIGN_PARAGRAPH.RIGHT, size=11)

    doc.add_page_break()

    # ════════════════════════════════════════════════════════════════
    # PAGE 6: ABSTRACT
    # ════════════════════════════════════════════════════════════════
    add_para(doc, "ABSTRACT", space_before=16, space_after=16, align=WD_ALIGN_PARAGRAPH.CENTER, size=15)
    add_para(
        doc,
        "StockSphere is a modern full-stack web application designed to democratize equity market education, virtual paper trading, and algorithmic investment intelligence. Traditional retail stock market onboarding is plagued by severe cognitive friction, high financial risk of capital loss, fragmented information sources, and complex quantitative indicators that novice investors struggle to interpret. StockSphere resolves these systemic challenges by delivering an end-to-end, zero-risk simulation platform powered by real-time market data, interactive financial charting, machine learning forecasting, and generative institutional-grade research synthesis.",
        space_after=10, size=11
    )
    add_para(
        doc,
        "The system provides a comprehensive virtual trading environment where users register, authenticate via secure JSON Web Tokens (JWT), receive a virtual capital allocation ($100,000), execute instant simulated Buy and Sell orders on real-world equities, and monitor their live portfolio equity and unrealized Profit & Loss (PnL). Real-time price fluctuations are streamed via bidirectional WebSockets (Socket.io) with an intelligent in-memory caching and queuing architecture that overcomes strict commercial API rate limits while ensuring hyper-responsive user interfaces.",
        space_after=10, size=11
    )
    add_para(
        doc,
        "At the core of the platform's analytical capabilities lies an innovative dual-layer quantitative engine: an econometric Machine Learning model utilizing 2nd-degree Polynomial Ordinary Least Squares (OLS) regression trained over 30-day historical candle data to forecast 5-day price trajectories with statistical validation (R² coefficient of determination, Mean Absolute Error, and standard error bounds), coupled with an Explainable AI (XAI) layer powered by Google Gemini LLM API (supported by an offline grounded neural fallback). This AI bridge translates mathematical regression metrics into institutional-grade Bull vs. Bear investment memos featuring upside catalysts, downside risk levels, and actionable virtual trading guidance in plain language.",
        space_after=10, size=11
    )
    add_para(
        doc,
        "The application is engineered using the MERN stack (MongoDB, Express.js, React 18, Node.js), Vite, Tailwind CSS, Redux Toolkit, and Chart.js. The resulting platform delivers an engaging, transparent, and educational ecosystem for mastering capital markets without financial risk.",
        space_after=14, size=11
    )
    add_para(
        doc,
        "Keywords: Virtual Stock Trading, MERN Stack, Socket.io, Machine Learning, Polynomial Regression, Explainable AI (XAI), Google Gemini API, Finnhub, Portfolio Management, Quantitative Finance.",
        bold_prefix="Keywords: ", space_after=0, size=10.5
    )

    doc.add_page_break()

    # ════════════════════════════════════════════════════════════════
    # PAGE 7 & 8: INDEX (TABLE OF CONTENTS)
    # ════════════════════════════════════════════════════════════════
    add_para(doc, "INDEX", space_before=10, space_after=12, align=WD_ALIGN_PARAGRAPH.CENTER, size=16)

    index_entries = [
        ("1", "Introduction", "10"),
        ("1.1", "Purpose", "10"),
        ("1.2", "Scope", "10"),
        ("1.3", "Technology and Tools", "10"),
        ("2", "Project Management", "11"),
        ("2.1", "Project Planning", "11"),
        ("2.2", "Project Scheduling", "11"),
        ("2.3", "Risk Management", "11"),
        ("2.3.1", "Risk Identification", "11"),
        ("2.3.2", "Risk Analysis", "12"),
        ("3", "System Requirements Study", "13"),
        ("3.1", "Hardware and Software Requirements", "13"),
        ("3.1.1", "Server-side Hardware Requirement", "13"),
        ("3.1.2", "Software Requirement", "13"),
        ("3.1.3", "Client-side Requirements", "13"),
        ("3.2", "Constraints", "13"),
        ("3.2.1", "Hardware Limitations", "14"),
        ("3.2.2", "Reliability Requirements", "14"),
        ("3.2.3", "Safety and Security Consideration", "14"),
        ("4", "System Analysis", "15"),
        ("4.1", "Study of Current System", "15"),
        ("4.2", "Problems and Weaknesses of Current System", "15"),
        ("4.3", "Requirements of New System", "15"),
        ("4.3.1", "User Requirements", "15"),
        ("4.3.2", "System Requirements (Functional Requirements)", "15"),
        ("4.3.3", "Non-Functional Requirements", "16"),
        ("4.4", "Feasibility Study", "16"),
        ("4.4.1", "Technical Feasibility", "16"),
        ("4.4.2", "Economic Feasibility", "16"),
        ("4.4.3", "Operational Feasibility", "17"),
        ("4.4.4", "Schedule Feasibility", "17"),
        ("4.5", "Feature of New System", "17"),
        ("5", "System Design", "18"),
        ("5.1", "Input / Output Interface", "18"),
        ("5.2", "Interface Design", "18"),
        ("5.2.1", "Class Diagram", "18"),
        ("5.2.2", "Use Case Diagram", "19"),
        ("5.2.3", "Activity Diagram", "20"),
        ("5.2.4", "Data Flow Diagram (Level-0)", "20"),
        ("5.2.5", "State Diagram", "21"),
        ("5.2.6", "E-R Diagram", "21"),
        ("5.2.7", "Sequence Diagram", "22"),
        ("5.2.8", "System Architecture", "23"),
        ("6", "Code Implementation", "24"),
        ("6.1", "Implementation Environment", "24"),
        ("6.2", "Program / Module Specification", "24"),
        ("6.3", "Coding Standards", "25"),
        ("7", "Testing", "26"),
        ("7.1", "Testing Strategy", "26"),
        ("7.2", "Testing Method", "26"),
        ("7.2.1", "Unit Testing", "26"),
        ("7.2.2", "Integration Testing", "26"),
        ("7.2.3", "Validation Testing", "26"),
        ("7.3", "Test Cases", "26"),
        ("7.3.1", "Test Suite", "27"),
        ("8", "Limitations and Future Enhancement", "28"),
        ("8.1", "Limitations", "28"),
        ("8.2", "Future Enhancement", "28"),
        ("9", "Conclusion", "29"),
        ("10", "References", "30"),
        ("11", "Project Module Summary", "31"),
    ]

    t_idx = doc.add_table(rows=len(index_entries) + 1, cols=3)
    t_idx.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_idx, color="CCCCCC")

    add_header_cell(t_idx.rows[0], 0, "Sr. No.", width=Inches(1.0))
    add_header_cell(t_idx.rows[0], 1, "Title", width=Inches(4.5))
    add_header_cell(t_idx.rows[0], 2, "Page No.", width=Inches(1.0))

    for idx, (sr, title, pg) in enumerate(index_entries):
        row = t_idx.rows[idx + 1]
        is_main = "." not in sr
        add_data_cell(row, 0, sr, width=Inches(1.0), bold=is_main)
        add_data_cell(row, 1, title, width=Inches(4.5), bold=is_main)
        add_data_cell(row, 2, pg, width=Inches(1.0), bold=is_main)

    doc.add_page_break()

    # ════════════════════════════════════════════════════════════════
    # PAGE 9: LIST OF FIGURES & LIST OF TABLES
    # ════════════════════════════════════════════════════════════════
    add_para(doc, "LIST OF FIGURES", space_before=10, space_after=10, align=WD_ALIGN_PARAGRAPH.CENTER, size=15)
    figures_list = [
        ("Figure 5.1", "System Architecture Diagram", "23"),
        ("Figure 5.2", "Class Diagram", "18"),
        ("Figure 5.3", "Use Case Diagram", "19"),
        ("Figure 5.4", "Activity Diagram - Stock Analysis, Prediction & Trade Workflow", "20"),
        ("Figure 5.5", "Data Flow Diagram - Level 0", "20"),
        ("Figure 5.6", "Order State Diagram", "21"),
        ("Figure 5.7", "Entity Relationship Diagram", "22"),
        ("Figure 5.8", "Sequence Diagram - Order Placement and AI Analysis", "22"),
    ]
    t_fig = doc.add_table(rows=len(figures_list) + 1, cols=3)
    t_fig.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_fig, color="CCCCCC")
    add_header_cell(t_fig.rows[0], 0, "Fig. No.", width=Inches(1.5))
    add_header_cell(t_fig.rows[0], 1, "Figure Title", width=Inches(4.0))
    add_header_cell(t_fig.rows[0], 2, "Page No.", width=Inches(1.0))
    for i, (fn, ft, fp) in enumerate(figures_list):
        row = t_fig.rows[i + 1]
        add_data_cell(row, 0, fn, width=Inches(1.5), bold=True)
        add_data_cell(row, 1, ft, width=Inches(4.0))
        add_data_cell(row, 2, fp, width=Inches(1.0))

    add_para(doc, "LIST OF TABLES", space_before=18, space_after=10, align=WD_ALIGN_PARAGRAPH.CENTER, size=15)
    tables_list = [
        ("Table 1.1", "Technology and Development Tools", "10"),
        ("Table 2.1", "Project Schedule", "11"),
        ("Table 2.2", "Risk Register & Mitigation", "12"),
        ("Table 3.1", "Hardware Requirements", "13"),
        ("Table 3.2", "Software Requirements", "13"),
        ("Table 4.1", "Functional Requirements", "15"),
        ("Table 4.2", "Non-Functional Requirements", "16"),
        ("Table 5.1", "Input / Output Interface", "18"),
        ("Table 6.1", "Implementation Environment", "24"),
        ("Table 6.2", "Program / Module Specification", "24"),
        ("Table 7.1", "System Test Cases", "26"),
        ("Table 7.2", "Test Suite Summary", "27"),
    ]
    t_tbl = doc.add_table(rows=len(tables_list) + 1, cols=3)
    t_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_tbl, color="CCCCCC")
    add_header_cell(t_tbl.rows[0], 0, "Table No.", width=Inches(1.5))
    add_header_cell(t_tbl.rows[0], 1, "Table Title", width=Inches(4.0))
    add_header_cell(t_tbl.rows[0], 2, "Page No.", width=Inches(1.0))
    for i, (tn, tt, tp) in enumerate(tables_list):
        row = t_tbl.rows[i + 1]
        add_data_cell(row, 0, tn, width=Inches(1.5), bold=True)
        add_data_cell(row, 1, tt, width=Inches(4.0))
        add_data_cell(row, 2, tp, width=Inches(1.0))

    doc.add_page_break()

    # ════════════════════════════════════════════════════════════════
    # PAGE 10: CHAPTER 1 - INTRODUCTION
    # ════════════════════════════════════════════════════════════════
    add_chapter_title(doc, "1", "INTRODUCTION")
    add_heading_1(doc, "1.1 Purpose")
    add_para(
        doc,
        "The purpose of StockSphere is to provide a comprehensive, real-time virtual stock trading, portfolio tracking, and quantitative market forecasting platform. Designed to eliminate the barrier of financial risk for students, researchers, and beginner retail investors, StockSphere creates an authentic simulation of modern equity trading desks. By coupling live market data streams with machine learning and generative artificial intelligence, the platform transforms abstract financial theories and raw market metrics into accessible, actionable educational experiences.",
        space_after=8
    )
    add_para(
        doc,
        "The system replaces risky capital exposure and fragmented educational tools with a centralized, professional MERN-based web environment. Users can safely analyze live asset prices, test investment hypotheses, track trade executions, monitor portfolio risk metrics, and leverage explainable AI to comprehend why algorithmic models reach specific market outlooks.",
        space_after=12
    )

    add_heading_1(doc, "1.2 Scope")
    add_para(doc, "The scope of StockSphere encompasses end-to-end simulated equity trading workflows and predictive data services:", space_after=6)
    add_bullet(doc, " User registration, secure JWT authentication, encrypted password storage, and persistent trading sessions.", "• Secure User Lifecycle:")
    add_bullet(doc, " Streaming live ticker quotes via Finnhub REST and bidirectional WebSockets (Socket.io) with rate-limit immune caching.", "• Live Market Ingestion:")
    add_bullet(doc, " Instant Buy/Sell trade execution, holdings valuation, cash balance management, and dynamic Profit & Loss (PnL) computation.", "• Virtual Portfolio Management:")
    add_bullet(doc, " Historical price candle exploration across multiple timeframes using interactive Chart.js graphs.", "• Interactive Financial Visualizations:")
    add_bullet(doc, " 2nd-degree Polynomial Least-Squares regression predicting 5-day trajectories with R² and MAE statistical validation.", "• Econometric ML Trend Forecaster:")
    add_bullet(doc, " Generative AI layer translating mathematical regression coefficients into structured Bull vs. Bear institutional memos.", "• Explainable AI (XAI) Thesis:")
    add_bullet(doc, " Real-time personalized quote monitoring and live peer discussion feeds.", "• Watchlists & Community Forum:")

    add_heading_1(doc, "1.3 Technology and Tools")
    add_para(doc, "Table 1.1 enumerates the modern software technologies, libraries, and external cloud services utilized in the implementation of StockSphere.", space_after=6)

    tech_items = [
        ("React.js (v18) + Vite", "High-performance client user interface and rapid build bundling"),
        ("Tailwind CSS", "Responsive utility-first modern styling and clean design system"),
        ("Redux Toolkit", "Centralized state management for live stock quotes and portfolio holdings"),
        ("Node.js & Express.js", "Scalable RESTful API backend, rate limiting, and business controllers"),
        ("MongoDB & Mongoose", "NoSQL document storage for users, transactions, holdings, and forum posts"),
        ("Socket.io", "Bidirectional WebSocket streaming for live stock price fluctuations"),
        ("Chart.js & React-Chartjs-2", "Interactive price charts and visual regression forecast overlays"),
        ("Yahoo Finance & Finnhub APIs", "External data ingestion for live market quotes and 30-day historical candles"),
        ("Polynomial ML Model (OLS)", "Degree-2 ordinary least squares regression for 5-day price trend projection"),
        ("Google Gemini API (Flash)", "Generative AI layer synthesizing econometric data into Explainable AI theses"),
    ]
    t_tech = doc.add_table(rows=len(tech_items) + 1, cols=2)
    t_tech.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_tech, color="CCCCCC")
    add_header_cell(t_tech.rows[0], 0, "Technology / Tool", width=Inches(2.5))
    add_header_cell(t_tech.rows[0], 1, "Purpose", width=Inches(4.0))
    for i, (tool, purp) in enumerate(tech_items):
        row = t_tech.rows[i + 1]
        add_data_cell(row, 0, tool, width=Inches(2.5), bold=True)
        add_data_cell(row, 1, purp, width=Inches(4.0))

    doc.add_page_break()

    # ════════════════════════════════════════════════════════════════
    # PAGE 11 & 12: CHAPTER 2 - PROJECT MANAGEMENT
    # ════════════════════════════════════════════════════════════════
    add_chapter_title(doc, "2", "PROJECT MANAGEMENT")
    add_heading_1(doc, "2.1 Project Planning")
    add_para(
        doc,
        "Project planning defines the systematic engineering workflow required to transform the stock trading and market forecasting requirements into a robust web application. The project is organized into requirement analysis, architecture design, database and API design, full-stack implementation, econometric modeling, Generative AI prompt engineering, rigorous testing, and technical documentation.",
        space_after=8
    )
    add_bullet(doc, " Identify retail investor pain points, market simulation requirements, and expected ML capabilities.", "1.")
    add_bullet(doc, " Formulate functional and non-functional specifications for live trading and AI forecasting.", "2.")
    add_bullet(doc, " Design the layered system architecture, MongoDB collections, WebSocket feeds, and UML/DFD models.", "3.")
    add_bullet(doc, " Implement authentication, virtual wallet, real-time charting, ML regression, and Explainable AI modules.", "4.")
    add_bullet(doc, " Integrate React client, Express REST APIs, Finnhub/Yahoo market streams, and Google Gemini API.", "5.")
    add_bullet(doc, " Perform unit, integration, validation, and mathematical regression error verification.", "6.")
    add_bullet(doc, " Prepare technical documentation, architectural diagrams, viva demonstration assets, and project reports.", "7.")

    add_heading_1(doc, "2.2 Project Scheduling")
    add_para(doc, "Scheduling divides development activities into a structured sequence across the semester. Table 2.1 outlines the academic project lifecycle:", space_after=6)

    sched_data = [
        ("1", "Requirement collection, market API evaluation & scope", "SRS & requirement specification"),
        ("2", "System design, UML diagrams, DFD, ER schemas", "Architecture, UML, DFD, ER design"),
        ("3", "Database & API design, schema definition", "Mongoose schemas, API specifications"),
        ("4", "Authentication & user wallet management", "Registration, login, JWT, $100k balance"),
        ("5", "Market data, WebSocket streaming, Chart.js", "Live ticker feed & interactive charts"),
        ("6", "Virtual trading engine & portfolio module", "Buy/Sell execution, PnL tracking"),
        ("7", "Polynomial ML predictor & GenAI thesis (XAI)", "OLS regression & AI thesis memo"),
        ("8", "Testing, error handling & edge-case validation", "Test logs, regression verification"),
        ("9", "Documentation, project report & demonstration", "Final report & live viva presentation"),
    ]
    t_sched = doc.add_table(rows=len(sched_data) + 1, cols=3)
    t_sched.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_sched, color="CCCCCC")
    add_header_cell(t_sched.rows[0], 0, "Phase", width=Inches(0.8))
    add_header_cell(t_sched.rows[0], 1, "Major Activities", width=Inches(3.7))
    add_header_cell(t_sched.rows[0], 2, "Deliverables", width=Inches(2.0))
    for i, (ph, act, deliv) in enumerate(sched_data):
        row = t_sched.rows[i + 1]
        add_data_cell(row, 0, ph, width=Inches(0.8), bold=True)
        add_data_cell(row, 1, act, width=Inches(3.7))
        add_data_cell(row, 2, deliv, width=Inches(2.0))

    add_heading_1(doc, "2.3 Risk Management", space_before=14)
    add_para(
        doc,
        "Risk management identifies technical, architectural, operational, and data-integrity risks that may affect development, execution, or market forecasting accuracy. Proactive identification allows mitigation strategies to be established early.",
        space_after=8
    )
    add_heading_2(doc, "2.3.1 Risk Identification")
    add_bullet(doc, " Finnhub Free-Tier Rate Limiting: 30 requests/minute can trigger HTTP 429 errors during live market hours.", "•")
    add_bullet(doc, " Data Provider Outages: Temporary unavailability of Yahoo Finance candle endpoints can disrupt ML training.", "•")
    add_bullet(doc, " Matrix Inversion Singularity: Highly collinear price points can cause determinant det(A) ≈ 0 in polynomial regression.", "•")
    add_bullet(doc, " Generative AI Latency or Quota Exhaustion: Upstream API timeouts or quota limits from Gemini Cloud.", "•")
    add_bullet(doc, " Trade Balance Race Conditions: Rapid concurrent buy clicks could overdraft virtual cash balances.", "•")
    add_bullet(doc, " Authentication and Session Expiry: Stale JWT tokens disrupting active trading sessions.", "•")

    add_heading_2(doc, "2.3.2 Risk Analysis", space_before=12)
    add_para(doc, "Table 2.2 analyzes the identified risks along with their probability, impact, and concrete architectural mitigations.", space_after=6)

    risk_data = [
        ("Finnhub API 429 rate limit", "High", "High", "In-memory caching (60s quote, 1h profile) and a serialized promise queue with 300ms throttling delays."),
        ("Database connection failure", "Low-Medium", "High", "MongoDB Atlas replica sets, automated reconnection handlers, connection pooling, and graceful error handling."),
        ("Singular matrix in OLS regression", "Low-Medium", "High", "Cramer's rule determinant threshold check (|det| < 1e-6) with automatic fallback to 1st-degree linear regression."),
        ("Generative AI service failure", "Medium", "Medium", "Dual-engine architecture: calls Google Gemini Flash, with automated zero-failure fallback to grounded neural thesis."),
        ("Trade balance race condition", "Low-Medium", "High", "Atomic Mongoose findOneAndUpdate operations verifying available cash balance before finalizing purchase transactions."),
        ("Data-entry & validation errors", "Medium", "Medium", "Comprehensive frontend form validation, input type coercion, and strict backend Express schema checks."),
    ]
    t_risk = doc.add_table(rows=len(risk_data) + 1, cols=4)
    t_risk.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_risk, color="CCCCCC")
    add_header_cell(t_risk.rows[0], 0, "Risk Event", width=Inches(1.8))
    add_header_cell(t_risk.rows[0], 1, "Probability", width=Inches(1.0))
    add_header_cell(t_risk.rows[0], 2, "Impact", width=Inches(0.9))
    add_header_cell(t_risk.rows[0], 3, "Mitigation Strategy", width=Inches(2.8))
    for i, (re, pr, im, mi) in enumerate(risk_data):
        row = t_risk.rows[i + 1]
        add_data_cell(row, 0, re, width=Inches(1.8), bold=True)
        add_data_cell(row, 1, pr, width=Inches(1.0))
        add_data_cell(row, 2, im, width=Inches(0.9))
        add_data_cell(row, 3, mi, width=Inches(2.8))

    doc.add_page_break()

    # ════════════════════════════════════════════════════════════════
    # PAGE 13 & 14: CHAPTER 3 - SYSTEM REQUIREMENTS STUDY
    # ════════════════════════════════════════════════════════════════
    add_chapter_title(doc, "3", "SYSTEM REQUIREMENTS STUDY")
    add_heading_1(doc, "3.1 Hardware and Software Requirements Study")
    add_para(
        doc,
        "StockSphere operates across modern full-stack web environments. The client requires a standard browser with JavaScript enabled, while backend and database services require adequate memory and network bandwidth to manage WebSockets and quantitative computation.",
        space_after=8
    )

    add_heading_2(doc, "3.1.1 Server-side Hardware Requirement")
    hw_server = [
        ("Processor", "Intel Core i5 / AMD Ryzen 5 (4 cores, 2.5 GHz+) or Cloud vCPU"),
        ("RAM", "8 GB DDR4 minimum (16 GB recommended for concurrent WebSocket feeds)"),
        ("Storage", "20 GB available SSD space for Node dependencies and MongoDB database"),
        ("Network", "Broadband connection (10 Mbps+) with static IP or cloud DNS mapping"),
        ("Display Resolution", "1920 × 1080 recommended for development and administration"),
    ]
    t_hw = doc.add_table(rows=len(hw_server) + 1, cols=2)
    t_hw.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_hw, color="CCCCCC")
    add_header_cell(t_hw.rows[0], 0, "Component", width=Inches(2.2))
    add_header_cell(t_hw.rows[0], 1, "Recommended Minimum", width=Inches(4.3))
    for i, (comp, req) in enumerate(hw_server):
        row = t_hw.rows[i + 1]
        add_data_cell(row, 0, comp, width=Inches(2.2), bold=True)
        add_data_cell(row, 1, req, width=Inches(4.3))

    add_heading_2(doc, "3.1.2 Software Requirement", space_before=12)
    sw_req = [
        ("Operating System", "Windows 10/11, Ubuntu 20.04+, or macOS"),
        ("Runtime Environment", "Node.js (v18.x or v20.x LTS)"),
        ("Application Framework", "Express.js (REST API framework)"),
        ("Frontend Client", "React.js 18 + Vite (SPA Client)"),
        ("State Management", "Redux Toolkit (@reduxjs/toolkit, react-redux)"),
        ("Database & ODM", "MongoDB Atlas & Mongoose ODM (v7+)"),
        ("Real-Time Communications", "Socket.io & Socket.io-Client (v4.x)"),
        ("Authentication & Security", "JSON Web Tokens (jsonwebtoken), bcryptjs"),
        ("Styling Framework", "Tailwind CSS & PostCSS"),
        ("Data Visualization", "Chart.js & react-chartjs-2"),
        ("Machine Learning Engine", "Built-in OLS Polynomial Regression Module (Degree 2)"),
        ("Generative AI Service", "Google Gemini 1.5 Flash API with Grounded Local Fallback"),
    ]
    t_sw = doc.add_table(rows=len(sw_req) + 1, cols=2)
    t_sw.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_sw, color="CCCCCC")
    add_header_cell(t_sw.rows[0], 0, "Software / Platform", width=Inches(2.4))
    add_header_cell(t_sw.rows[0], 1, "Requirement / Purpose", width=Inches(4.1))
    for i, (sw, purp) in enumerate(sw_req):
        row = t_sw.rows[i + 1]
        add_data_cell(row, 0, sw, width=Inches(2.4), bold=True)
        add_data_cell(row, 1, purp, width=Inches(4.1))

    add_heading_2(doc, "3.1.3 Client-side Requirements", space_before=12)
    client_req = [
        ("Desktop / Laptop", "Any modern OS with JavaScript enabled and 4GB+ RAM"),
        ("Mobile Client", "Responsive mobile browser supporting HTML5 WebSockets (iOS Safari / Android Chrome)"),
        ("Supported Browsers", "Google Chrome 90+, Mozilla Firefox 88+, Microsoft Edge 90+, Apple Safari 14+"),
    ]
    t_cl = doc.add_table(rows=len(client_req) + 1, cols=2)
    t_cl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_cl, color="CCCCCC")
    add_header_cell(t_cl.rows[0], 0, "Client", width=Inches(2.2))
    add_header_cell(t_cl.rows[0], 1, "Requirement", width=Inches(4.3))
    for i, (cl, rq) in enumerate(client_req):
        row = t_cl.rows[i + 1]
        add_data_cell(row, 0, cl, width=Inches(2.2), bold=True)
        add_data_cell(row, 1, rq, width=Inches(4.3))

    add_heading_1(doc, "3.2 Constraints", space_before=14)
    add_para(
        doc,
        "System operation is subject to technical constraints including third-party API rate quotas, computational complexity of polynomial regressions, and network latency over WebSocket connections.",
        space_after=8
    )
    add_heading_2(doc, "3.2.1 Hardware Limitations")
    add_bullet(doc, " Server Memory: Intensive real-time WebSocket broadcasting to multiple simultaneous clients requires adequate memory headroom.", "•")
    add_bullet(doc, " Client Display Resolution: Advanced Chart.js candlestick charts require minimum 768px width for detailed multi-indicator analysis.", "•")

    add_heading_2(doc, "3.2.2 Reliability Requirements", space_before=10)
    add_para(
        doc,
        "The platform preserves portfolio financial integrity by executing all trade operations through atomic Mongoose database mutations. If an order fails midway, changes roll back cleanly without leaving orphan records.",
        space_after=8
    )

    add_heading_2(doc, "3.2.3 Safety and Security Consideration", space_before=10)
    add_bullet(doc, " Passwords hashed with bcrypt (salt rounds = 10); plaintext credentials are never logged or stored.", "• Credential Protection:")
    add_bullet(doc, " REST endpoints verify bearer JWT tokens, protecting portfolio and trading routes.", "• Tokenized Security:")
    add_bullet(doc, " API keys and secrets loaded strictly from .env and never bundled into client scripts.", "• Secret Isolation:")

    doc.add_page_break()

    # ════════════════════════════════════════════════════════════════
    # PAGE 15, 16, 17: CHAPTER 4 - SYSTEM ANALYSIS
    # ════════════════════════════════════════════════════════════════
    add_chapter_title(doc, "4", "SYSTEM ANALYSIS")
    add_heading_1(doc, "4.1 Study of Current System")
    add_para(
        doc,
        "In traditional academic and retail environments, individuals learning stock market mechanics face severe limitations. They either trade with real money on live brokerages—risking substantial personal capital—or use outdated spreadsheet logs and disjointed news channels. Existing simulator platforms often lack live price updates, offer poor mobile user experiences, and provide zero assistance in interpreting complex technical charts.",
        space_after=8
    )

    add_heading_1(doc, "4.2 Problems and Weaknesses of Current System")
    add_bullet(doc, " High Capital Risk: Novice traders incur direct financial losses while learning fundamental market dynamics.", "•")
    add_bullet(doc, " Stale Data Feeds: Many free educational tools display 15-minute delayed quotes, failing to recreate live trading environments.", "•")
    add_bullet(doc, " Inaccessible Quantitative Indicators: Retail investors struggle to understand statistical indicators without institutional training.", "•")
    add_bullet(doc, " Disconnected Social Learning: Most platforms isolate traders, preventing peer collaboration and thesis discussion.", "•")

    add_heading_1(doc, "4.3 Requirements of New System")
    add_heading_2(doc, "4.3.1 User Requirements")
    add_bullet(doc, " Users must register, authenticate securely, and receive an initial $100,000 virtual cash balance.", "•")
    add_bullet(doc, " Users must search any US stock ticker and view live market prices, day highs/lows, and market capitalization.", "•")
    add_bullet(doc, " Users must execute instant virtual Buy and Sell orders with automatic validation and PnL re-calculation.", "•")
    add_bullet(doc, " Users must generate 5-day polynomial ML price forecasts with confidence intervals at the click of a button.", "•")
    add_bullet(doc, " Users must receive plain-English Explainable AI Bull/Bear investment memos clarifying quantitative signals.", "•")
    add_bullet(doc, " Users must maintain a personal watchlist and engage in community discussions.", "•")

    add_heading_2(doc, "4.3.2 System Requirements (Functional Requirements)", space_before=12)
    add_para(doc, "Table 4.1 defines the formal functional requirements implemented in StockSphere.", space_after=6)

    fr_data = [
        ("FR-01", "The system shall support user registration, bcrypt password hashing, and JWT login."),
        ("FR-02", "The system shall automatically initialize a virtual portfolio with $100,000 upon registration."),
        ("FR-03", "The system shall stream real-time price quotes using WebSockets and in-memory rate-limit caching."),
        ("FR-04", "The system shall provide ticker symbol search with autocomplete via Finnhub API integration."),
        ("FR-05", "The system shall render interactive historical charts across daily and weekly intervals using Chart.js."),
        ("FR-06", "The system shall execute Buy/Sell orders atomically, updating holdings, trade history, and cash balance."),
        ("FR-07", "The system shall compute real-time portfolio metrics: total equity, unrealized PnL, and ROI%."),
        ("FR-08", "The system shall compute 2nd-degree polynomial regression forecasts over 30-day historical candle data."),
        ("FR-09", "The system shall calculate and display R² coefficient of determination and Mean Absolute Error (MAE)."),
        ("FR-10", "The system shall invoke Google Gemini API to produce structured Bull/Bear Explainable AI memos."),
        ("FR-11", "The system shall execute an offline grounded neural fallback if upstream LLM APIs are unreachable."),
        ("FR-12", "The system shall support custom watchlists and community forum posts with live peer updates."),
    ]
    t_fr = doc.add_table(rows=len(fr_data) + 1, cols=2)
    t_fr.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_fr, color="CCCCCC")
    add_header_cell(t_fr.rows[0], 0, "ID", width=Inches(1.2))
    add_header_cell(t_fr.rows[0], 1, "Functional Requirement Specification", width=Inches(5.3))
    for i, (fid, fdesc) in enumerate(fr_data):
        row = t_fr.rows[i + 1]
        add_data_cell(row, 0, fid, width=Inches(1.2), bold=True)
        add_data_cell(row, 1, fdesc, width=Inches(5.3))

    add_heading_2(doc, "4.3.3 Non-Functional Requirements", space_before=14)
    nfr_data = [
        ("Security", "Stateless JWT token authentication, bcrypt password encryption, and input sanitization"),
        ("Usability", "Modern dark-mode interface, financial palettes, and intuitive one-click AI analysis"),
        ("Performance", "Sub-100ms response time for cached quotes; sub-1.5s for polynomial ML regression"),
        ("Reliability", "Zero-failure fallback for Explainable AI; atomic database updates preventing trade corruption"),
        ("Scalability", "Event-driven WebSocket rooms allowing targeted broadcast only to active viewers"),
        ("Maintainability", "Clean MERN modular architecture with distinct controllers, routes, models, and slices"),
    ]
    t_nfr = doc.add_table(rows=len(nfr_data) + 1, cols=2)
    t_nfr.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_nfr, color="CCCCCC")
    add_header_cell(t_nfr.rows[0], 0, "Category", width=Inches(1.8))
    add_header_cell(t_nfr.rows[0], 1, "Non-Functional Requirement Specification", width=Inches(4.7))
    for i, (cat, spec) in enumerate(nfr_data):
        row = t_nfr.rows[i + 1]
        add_data_cell(row, 0, cat, width=Inches(1.8), bold=True)
        add_data_cell(row, 1, spec, width=Inches(4.7))

    add_heading_1(doc, "4.4 Feasibility Study", space_before=14)
    add_para(
        doc,
        "A multi-dimensional feasibility study was conducted to confirm the viability of developing, deploying, and maintaining StockSphere within academic and operational boundaries.",
        space_after=6
    )
    add_bullet(doc, " The MERN stack, Socket.io, Chart.js, and Google Gemini API provide robust full-stack capabilities.", "• Technical Feasibility:")
    add_bullet(doc, " StockSphere is constructed entirely using open-source packages and free-tier cloud APIs, requiring zero licensing expenses.", "• Economic Feasibility:")
    add_bullet(doc, " Requires no software installations on end-user machines beyond a modern web browser.", "• Operational Feasibility:")
    add_bullet(doc, " The modular project plan allowed all milestones to be achieved within the semester timeframe.", "• Schedule Feasibility:")

    add_heading_1(doc, "4.5 Features of New System", space_before=12)
    add_bullet(doc, " Zero-Risk Virtual Capital Trading with $100,000 Starting Cash.", "•")
    add_bullet(doc, " Hyper-Responsive Live Tickers via Socket.io Price Broadcasting.", "•")
    add_bullet(doc, " Multi-Horizon Interactive Candlestick Visualizations via Chart.js.", "•")
    add_bullet(doc, " Mathematical 2nd-Degree Polynomial Least-Squares Regression Model.", "•")
    add_bullet(doc, " Explainable AI (XAI) Institutional Bull vs. Bear Thesis Synthesis.", "•")
    add_bullet(doc, " High-Fidelity Grounded Local Neural Fallback Engine.", "•")
    add_bullet(doc, " Real-Time Personalized Watchlist & Community Social Trading Feed.", "•")

    doc.add_page_break()

    # ════════════════════════════════════════════════════════════════
    # PAGE 18 TO 23: CHAPTER 5 - SYSTEM DESIGN
    # ════════════════════════════════════════════════════════════════
    add_chapter_title(doc, "5", "SYSTEM DESIGN")
    add_heading_1(doc, "5.1 Input / Output Interface")
    add_para(
        doc,
        "StockSphere implements a responsive user interface designed for intuitive navigation across desktop and mobile devices. Table 5.1 outlines user input parameters and resulting system outputs.",
        space_after=6
    )

    io_data = [
        ("Registration / Login", "Name, email, password", "JWT session token, initial $100k wallet, dashboard view"),
        ("Market Search", "Ticker symbol (e.g. AAPL) or company", "Autocomplete search results with exchange and description"),
        ("Interactive Chart", "Selected stock symbol, interval (1D, 1W)", "Rendered Chart.js price candles, high/low indicators"),
        ("ML Predictor", "Click 'AI Predictor' button", "5-day price projection curve, R² score, MAE, trend"),
        ("AI Investment Thesis", "Click 'Generate AI Thesis'", "Structured Bull vs. Bear memo with catalysts and verdict"),
        ("Order Execution", "Order type (BUY/SELL), quantity", "Immediate trade confirmation, updated cash & holdings"),
        ("Community Post", "Discussion text, ticker references", "Broadcasted post in forum, like & comment updates"),
    ]
    t_io = doc.add_table(rows=len(io_data) + 1, cols=3)
    t_io.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_io, color="CCCCCC")
    add_header_cell(t_io.rows[0], 0, "Interface Module", width=Inches(1.8))
    add_header_cell(t_io.rows[0], 1, "Main Inputs", width=Inches(2.2))
    add_header_cell(t_io.rows[0], 2, "Expected Outputs", width=Inches(2.5))
    for i, (mod, inp, out) in enumerate(io_data):
        row = t_io.rows[i + 1]
        add_data_cell(row, 0, mod, width=Inches(1.8), bold=True)
        add_data_cell(row, 1, inp, width=Inches(2.2))
        add_data_cell(row, 2, out, width=Inches(2.5))

    add_heading_1(doc, "5.2 Interface Design and UML Models", space_before=14)
    add_para(
        doc,
        "System design models define domain objects, user interactions, workflows, data flows, and physical deployments using standard UML and DFD notations.",
        space_after=8
    )

    # 5.2.1 Class Diagram
    add_heading_2(doc, "5.2.1 Class Diagram")
    add_diagram(doc, "figure_5_2_class.png", "Figure 5.2: Object-Oriented Class Diagram of StockSphere System", width_inches=6.0)
    add_para(
        doc,
        "Figure 5.2 captures core domain classes: User, Portfolio, Trade, StockQuote, PredictionEngine (OLS ML), GenAIThesis (XAI Layer), and CommunityPost. Methods capture business logic such as portfolio PnL computation, Cramer's rule matrix inversion, and generative memo synthesis.",
        space_after=12
    )

    # 5.2.2 Use Case Diagram
    add_heading_2(doc, "5.2.2 Use Case Diagram", space_before=14)
    add_diagram(doc, "figure_5_3_usecase.png", "Figure 5.3: Use Case Diagram – Trader & System Operations", width_inches=5.8)
    add_para(
        doc,
        "Figure 5.3 models the interactions between the Virtual Trader (actor) and external services (Finnhub, Yahoo, Gemini) across trading, portfolio, forecasting, and community use cases.",
        space_after=12
    )

    # 5.2.3 Activity Diagram
    add_heading_2(doc, "5.2.3 Activity Diagram", space_before=14)
    add_diagram(doc, "figure_5_4_activity.png", "Figure 5.4: Activity Diagram – Stock Analysis, Prediction & Trade Workflow", width_inches=6.0)
    add_para(
        doc,
        "Figure 5.4 outlines the user workflow: logging in, searching a stock, loading live candles, generating ML forecasts and GenAI theses, and executing validated Buy/Sell orders with atomic balance checks.",
        space_after=12
    )

    # 5.2.4 Data Flow Diagram (DFD Level 0)
    add_heading_2(doc, "5.2.4 Data Flow Diagram (DFD Level 0)", space_before=14)
    add_diagram(doc, "figure_5_5_dfd.png", "Figure 5.5: Level-0 Data Flow Diagram of StockSphere System", width_inches=6.0)
    add_para(
        doc,
        "Figure 5.5 models high-level information exchanges between the central StockSphere process, external entities (Trader, Finnhub, Yahoo, Gemini), and core MongoDB data stores (Users, Portfolios, Trades, Watchlists).",
        space_after=12
    )

    # 5.2.5 State Diagram
    add_heading_2(doc, "5.2.5 State Diagram", space_before=14)
    add_diagram(doc, "figure_5_6_state.png", "Figure 5.6: Trade Order Lifecycle State Diagram", width_inches=6.0)
    add_para(
        doc,
        "Figure 5.6 details the lifecycle of a virtual order: Initiated -> Validating Funds -> [Rejected if insufficient] or [Execution Engine -> Position Active -> Closed].",
        space_after=12
    )

    # 5.2.6 Entity Relationship Diagram
    add_heading_2(doc, "5.2.6 Entity Relationship Diagram (ERD)", space_before=14)
    add_diagram(doc, "figure_5_7_er.png", "Figure 5.7: Entity-Relationship Diagram of StockSphere Database", width_inches=6.0)
    add_para(
        doc,
        "Figure 5.7 defines the MongoDB schemas and relational associations: User (1:1 with Portfolio, 1:N with Trades, 1:N with Watchlists and Posts) and Portfolio (1:N with Holdings).",
        space_after=12
    )

    # 5.2.7 Sequence Diagram
    add_heading_2(doc, "5.2.7 Sequence Diagram", space_before=14)
    add_diagram(doc, "figure_5_8_sequence.png", "Figure 5.8: Sequence Diagram – Real-Time Order Placement and AI Analysis", width_inches=6.0)
    add_para(
        doc,
        "Figure 5.8 models the chronological message sequences across the Trader, React Client, Express API, ML Predictor, and Gemini GenAI Engine.",
        space_after=12
    )

    # 5.2.8 System Architecture
    add_heading_2(doc, "5.2.8 System Architecture", space_before=14)
    add_diagram(doc, "figure_5_1_architecture.png", "Figure 5.1: Multi-Tier System Architecture Diagram", width_inches=6.0)
    add_para(
        doc,
        "Figure 5.1 illustrates the complete multi-tier architecture: Presentation Layer (React 18 + Vite), Security Layer (JWT & Bcrypt), Business Services Layer (Node.js & Express Controllers), and Data & External Cloud Layer (MongoDB Atlas, Finnhub, Yahoo, Gemini).",
        space_after=12
    )

    doc.add_page_break()

    # ════════════════════════════════════════════════════════════════
    # PAGE 24 & 25: CHAPTER 6 - CODE IMPLEMENTATION
    # ════════════════════════════════════════════════════════════════
    add_chapter_title(doc, "6", "CODE IMPLEMENTATION")
    add_heading_1(doc, "6.1 Implementation Environment")
    add_para(
        doc,
        "StockSphere is implemented using a modern JavaScript/Node.js full-stack development environment. Express.js orchestrates REST endpoints and WebSocket events, MongoDB Atlas handles persistence, and React 18 with Redux Toolkit renders the user interface.",
        space_after=6
    )

    impl_env = [
        ("Presentation Layer", "React.js 18 + Vite", "Component architecture, SPA routing, hooks, Redux store"),
        ("Styling System", "Tailwind CSS + PostCSS", "Responsive dark-mode UI, flexbox/grid layouts, micro-animations"),
        ("State Management", "Redux Toolkit", "Centralized slices for auth, active stock quotes, and portfolio"),
        ("Server Framework", "Node.js + Express.js", "REST endpoints, CORS security, input validation, rate limiting"),
        ("Database Layer", "MongoDB + Mongoose", "Document schemas, validations, atomic queries, indexing"),
        ("Real-Time Engine", "Socket.io (v4)", "WebSockets for live stock price broadcasting and community events"),
        ("Data Visualization", "Chart.js + React-Chartjs-2", "Dynamic candlestick, line charts, and ML forecast overlays"),
        ("Machine Learning", "OLS Polynomial Regressor", "2nd-degree regression, Cramer's rule determinant solver, R²/MAE"),
        ("Generative AI", "Google Gemini API (Flash)", "Prompt engineering for institutional Bull/Bear Explainable AI"),
    ]
    t_ie = doc.add_table(rows=len(impl_env) + 1, cols=3)
    t_ie.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_ie, color="CCCCCC")
    add_header_cell(t_ie.rows[0], 0, "Layer / Area", width=Inches(1.8))
    add_header_cell(t_ie.rows[0], 1, "Technology / Library", width=Inches(2.0))
    add_header_cell(t_ie.rows[0], 2, "Implementation Responsibility", width=Inches(2.7))
    for i, (la, te, re) in enumerate(impl_env):
        row = t_ie.rows[i + 1]
        add_data_cell(row, 0, la, width=Inches(1.8), bold=True)
        add_data_cell(row, 1, te, width=Inches(2.0))
        add_data_cell(row, 2, re, width=Inches(2.7))

    add_heading_1(doc, "6.2 Program / Module Specification", space_before=14)
    add_para(doc, "Table 6.2 defines the major functional software modules and their implementation details.", space_after=6)

    mod_spec = [
        ("Auth Controller", "authController.js", "Handles user registration, bcrypt password hashing, and JWT token issuance."),
        ("Portfolio Controller", "portfolioController.js", "Executes Buy/Sell orders atomically, updates holdings, and calculates PnL."),
        ("Stock Controller", "stockController.js", "Coordinates Finnhub cached quotes, Yahoo candle ingestion, and market status."),
        ("ML Predictor Engine", "stockController.js", "Extracts 30-day candles, trains 2nd-degree polynomial regression, and outputs 5-day projections."),
        ("Explainable AI (XAI)", "stockController.js", "Passes ML metrics to Gemini Flash; triggers grounded local fallback if offline."),
        ("Socket Service", "socketService.js", "Manages symbol rooms, simulates ±0.2% live market ticks, and broadcasts to active clients."),
        ("Community Controller", "communityController.js", "Manages forum discussion feeds, posts, likes, and comment threads."),
    ]
    t_ms = doc.add_table(rows=len(mod_spec) + 1, cols=3)
    t_ms.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_ms, color="CCCCCC")
    add_header_cell(t_ms.rows[0], 0, "Module Name", width=Inches(1.8))
    add_header_cell(t_ms.rows[0], 1, "Source File", width=Inches(1.7))
    add_header_cell(t_ms.rows[0], 2, "Operational Responsibility", width=Inches(3.0))
    for i, (mn, sf, op) in enumerate(mod_spec):
        row = t_ms.rows[i + 1]
        add_data_cell(row, 0, mn, width=Inches(1.8), bold=True)
        add_data_cell(row, 1, sf, width=Inches(1.7), italic=True)
        add_data_cell(row, 2, op, width=Inches(3.0))

    add_heading_1(doc, "6.3 Coding Standards", space_before=14)
    add_bullet(doc, " Predictable naming conventions across React components, Redux slices, and Express controllers.", "• Clean Code Architecture:")
    add_bullet(doc, " Comprehensive server-side validation rejecting invalid quantities, negative prices, or missing symbols.", "• Defensive Input Validation:")
    add_bullet(doc, " Zero hardcoded credentials; all secrets stored strictly in environment variables.", "• Secure Environment Isolation:")
    add_bullet(doc, " Standardized JSON responses ({ success: Boolean, data: Object, message: String }).", "• Unified API Envelope:")

    doc.add_page_break()

    # ════════════════════════════════════════════════════════════════
    # PAGE 26 & 27: CHAPTER 7 - TESTING
    # ════════════════════════════════════════════════════════════════
    add_chapter_title(doc, "7", "TESTING")
    add_heading_1(doc, "7.1 Testing Strategy")
    add_para(
        doc,
        "The testing strategy employs a multi-tiered approach: Unit Testing of isolated financial calculations and regression formulas, Integration Testing of API endpoints and WebSockets, and End-to-End Validation Testing of simulated trading workflows.",
        space_after=8
    )

    add_heading_1(doc, "7.2 Testing Method")
    add_heading_2(doc, "7.2.1 Unit Testing")
    add_para(doc, "Validates individual logic modules: Cramer's rule 3x3 determinant computation, R² formula verification, portfolio cash subtraction, and average buy price recalculation.", space_after=6)

    add_heading_2(doc, "7.2.2 Integration Testing", space_before=10)
    add_para(doc, "Verifies data flows between client, Express REST APIs, MongoDB Atlas, and Socket.io price broadcasting.", space_after=6)

    add_heading_2(doc, "7.2.3 Validation Testing", space_before=10)
    add_para(doc, "Evaluates user interactions from registration through order execution and AI thesis generation against business requirements.", space_after=8)

    add_heading_1(doc, "7.3 Test Cases", space_before=12)
    add_para(doc, "Table 7.1 details the system test cases executed to verify functionality, security, and algorithmic integrity.", space_after=6)

    test_cases = [
        ("TC-01", "Registration", "Register new user with valid email & password", "User created, password hashed, $100k balance", "Pass"),
        ("TC-02", "Registration", "Register duplicate existing email", "HTTP 400 error: 'User already exists'", "Pass"),
        ("TC-03", "Login", "Login with valid registered credentials", "HTTP 200, JWT token returned, dashboard opens", "Pass"),
        ("TC-04", "Login", "Login with invalid password", "HTTP 401 error: 'Invalid credentials'", "Pass"),
        ("TC-05", "Auth Guard", "Access /api/portfolio without JWT header", "HTTP 401: 'Not authorized, token missing'", "Pass"),
        ("TC-06", "Stock Search", "Query '/api/stocks/search?q=AAPL'", "Top 10 matching Common Stock symbols returned", "Pass"),
        ("TC-07", "Live Quote", "Fetch quote for symbol 'TSLA'", "Current price, day open, high, low returned", "Pass"),
        ("TC-08", "Rate Limit Cache", "Send 5 rapid quote requests for 'NVDA'", "Requests 2-5 served from cache within 60s TTL", "Pass"),
        ("TC-09", "Buy Order", "Buy 10 shares of AAPL ($150/share = $1500)", "Cash drops by $1500, AAPL holding added", "Pass"),
        ("TC-10", "Insufficient Funds", "Buy 1000 shares of MSFT ($400k > $100k)", "HTTP 400 error: 'Insufficient cash balance'", "Pass"),
        ("TC-11", "Sell Order", "Sell 5 of 10 owned AAPL shares", "Holding reduces to 5, cash increases by proceeds", "Pass"),
        ("TC-12", "Excess Sell", "Sell 20 shares when owning only 5", "HTTP 400 error: 'Cannot sell more than owned'", "Pass"),
        ("TC-13", "Portfolio PnL", "Price tick received over WebSocket (+2%)", "Holdings valuation and PnL re-render live", "Pass"),
        ("TC-14", "ML Predictor", "Request ML prediction for 'AAPL'", "2nd-degree formula, R², MAE & 5-day forecast returned", "Pass"),
        ("TC-15", "Singular Fallback", "Simulate singular matrix (|det| < 1e-6)", "System falls back to 1st-degree linear regression", "Pass"),
        ("TC-16", "Gemini AI Thesis", "Request AI thesis with valid GEMINI_API_KEY", "Structured JSON with bull/bear catalysts returned", "Pass"),
        ("TC-17", "Grounded Fallback", "Request AI thesis with GEMINI_API_KEY unset", "Grounded local neural thesis returned seamlessly", "Pass"),
        ("TC-18", "Community Post", "Submit new trade analysis post to forum", "Post saved in DB and broadcast via Socket.io", "Pass"),
    ]
    t_tc = doc.add_table(rows=len(test_cases) + 1, cols=5)
    t_tc.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_tc, color="CCCCCC")
    add_header_cell(t_tc.rows[0], 0, "ID", width=Inches(0.8))
    add_header_cell(t_tc.rows[0], 1, "Module", width=Inches(1.2))
    add_header_cell(t_tc.rows[0], 2, "Test Condition", width=Inches(2.0))
    add_header_cell(t_tc.rows[0], 3, "Expected Result", width=Inches(2.0))
    add_header_cell(t_tc.rows[0], 4, "Status", width=Inches(0.6))
    for i, (t_id, mod, cond, exp, res) in enumerate(test_cases):
        row = t_tc.rows[i + 1]
        add_data_cell(row, 0, t_id, width=Inches(0.8), bold=True)
        add_data_cell(row, 1, mod, width=Inches(1.2))
        add_data_cell(row, 2, cond, width=Inches(2.0))
        add_data_cell(row, 3, exp, width=Inches(2.0))
        add_data_cell(row, 4, res, width=Inches(0.6), bold=True)

    add_heading_2(doc, "7.3.1 Test Suite Summary", space_before=14)
    add_para(doc, "Table 7.2 summarizes the execution status of all testing modules across the platform.", space_after=6)

    suite_summary = [
        ("Authentication & Security", "TC-01 to TC-05", "User registration, password encryption, JWT authorization", "Verified / Passed"),
        ("Market Data & Caching", "TC-06 to TC-08", "Finnhub quote streaming, search autocomplete, cache TTL", "Verified / Passed"),
        ("Virtual Trading Engine", "TC-09 to TC-13", "Order validation, cash subtraction, PnL recalculation", "Verified / Passed"),
        ("Machine Learning Predictor", "TC-14 to TC-15", "Polynomial OLS regression, Cramer's rule determinant", "Verified / Passed"),
        ("Explainable AI (XAI)", "TC-16 to TC-17", "Google Gemini synthesis and grounded neural fallback", "Verified / Passed"),
        ("Watchlist & Community", "TC-18", "Watchlist CRUD and WebSocket community post broadcasting", "Verified / Passed"),
    ]
    t_ts = doc.add_table(rows=len(suite_summary) + 1, cols=4)
    t_ts.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_ts, color="CCCCCC")
    add_header_cell(t_ts.rows[0], 0, "Test Area", width=Inches(1.8))
    add_header_cell(t_ts.rows[0], 1, "Test Cases", width=Inches(1.2))
    add_header_cell(t_ts.rows[0], 2, "Expected Outcome", width=Inches(2.5))
    add_header_cell(t_ts.rows[0], 3, "Status", width=Inches(1.0))
    for i, (ta, tc, eo, st) in enumerate(suite_summary):
        row = t_ts.rows[i + 1]
        add_data_cell(row, 0, ta, width=Inches(1.8), bold=True)
        add_data_cell(row, 1, tc, width=Inches(1.2))
        add_data_cell(row, 2, eo, width=Inches(2.5))
        add_data_cell(row, 3, st, width=Inches(1.0), bold=True)

    doc.add_page_break()

    # ════════════════════════════════════════════════════════════════
    # PAGE 28: CHAPTER 8 - LIMITATIONS AND FUTURE ENHANCEMENT
    # ════════════════════════════════════════════════════════════════
    add_chapter_title(doc, "8", "LIMITATIONS AND FUTURE ENHANCEMENT")
    add_heading_1(doc, "8.1 Limitations")
    add_bullet(doc, " Simulated Fills: Market orders fill instantly at current quote price without order-book depth or slippage.", "• Virtual Simulation Model:")
    add_bullet(doc, " Free-tier API rate limits require in-memory caching (60s), creating brief delays between real-world ticks.", "• API Quota Constraints:")
    add_bullet(doc, " Polynomial regression assumes historical continuation; sudden unexpected geopolitical events cannot be factored into the quadratic curve.", "• OLS Regression Assumptions:")
    add_bullet(doc, " Focuses on US equity markets; international exchanges and derivative contracts are not yet modeled.", "• Asset Coverage:")

    add_heading_1(doc, "8.2 Future Enhancement", space_before=14)
    add_bullet(doc, " Deep Learning Forecasting: Integrating LSTM (Long Short-Term Memory) recurrent neural networks to capture multi-scale time-series patterns.", "•")
    add_bullet(doc, " Derivative Contracts: Expanding the virtual engine to support Call/Put Options trading with Black-Scholes Greeks calculation.", "•")
    add_bullet(doc, " Multi-Exchange Coverage: Adding Indian (NSE/BSE), European, and Crypto market feeds via unified financial data providers.", "•")
    add_bullet(doc, " Algorithmic Trading Bots: Enabling users to author automated Python or JavaScript trading scripts executed against simulated accounts.", "•")
    add_bullet(doc, " Mobile PWA Application: Packaging the React client as an installable Progressive Web App with push notifications for price breakout alerts.", "•")

    doc.add_page_break()

    # ════════════════════════════════════════════════════════════════
    # PAGE 29: CHAPTER 9 - CONCLUSION
    # ════════════════════════════════════════════════════════════════
    add_chapter_title(doc, "9", "CONCLUSION")
    add_para(
        doc,
        "StockSphere successfully demonstrates how modern web engineering, real-time streaming architectures, and artificial intelligence can be combined to solve the long-standing challenge of retail financial education. By creating a zero-risk paper trading ecosystem backed by realistic $100,000 virtual wallets, the platform allows users to master trading without risking personal capital.",
        space_after=10
    )
    add_para(
        doc,
        "The project delivers significant innovation through its dual-tier artificial intelligence architecture: first, by training a 2nd-degree Polynomial Least-Squares econometric regression model directly over 30-day historical candle data to forecast 5-day price trajectories with statistical rigor (R² and MAE), and second, by employing an Explainable AI (XAI) layer powered by Google Gemini (supported by an offline grounded neural fallback) to translate mathematical coefficients into plain-English institutional research memos.",
        space_after=10
    )
    add_para(
        doc,
        "Built on the MERN stack (MongoDB, Express.js, React 18, Node.js) with Tailwind CSS, Redux Toolkit, Socket.io, and Chart.js, StockSphere establishes a scalable, responsive, and robust foundation that can easily be expanded to encompass deep-learning LSTM models, algorithmic bot trading, and international markets in the future.",
        space_after=0
    )

    doc.add_page_break()

    # ════════════════════════════════════════════════════════════════
    # PAGE 30: CHAPTER 10 - REFERENCES
    # ════════════════════════════════════════════════════════════════
    add_chapter_title(doc, "10", "REFERENCES")
    add_para(doc, "The following academic textbooks, technical documentation, and scientific resources were referenced during the design and implementation of StockSphere:", space_after=8)

    references = [
        ("1", "React.js Documentation", "Meta Open Source (https://react.dev)"),
        ("2", "Node.js & Express.js Documentation", "OpenJS Foundation (https://expressjs.com)"),
        ("3", "MongoDB & Mongoose ODM Manual", "MongoDB Inc. (https://mongoosejs.com)"),
        ("4", "Socket.io Engine Documentation", "Socket.io Community (https://socket.io/docs/v4)"),
        ("5", "Chart.js Data Visualization Library", "Chart.js Documentation (https://www.chartjs.org)"),
        ("6", "Finnhub Financial Stock Market API", "Finnhub Documentation (https://finnhub.io/docs/api)"),
        ("7", "Yahoo Finance Rapid API Service", "Yahoo Finance Engine Documentation"),
        ("8", "Google Gemini Generative AI SDK", "Google Cloud AI (https://ai.google.dev)"),
        ("9", "Introductory Econometrics: A Modern Approach", "Wooldridge, J. M. (Cengage Learning, 7th Edition)"),
        ("10", "Options, Futures, and Other Derivatives", "Hull, J. C. (Pearson Education, 10th Edition)"),
        ("11", "OWASP Web Application Security Guide", "OWASP Foundation (https://owasp.org)"),
    ]
    t_ref = doc.add_table(rows=len(references) + 1, cols=3)
    t_ref.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_ref, color="CCCCCC")
    add_header_cell(t_ref.rows[0], 0, "No.", width=Inches(0.6))
    add_header_cell(t_ref.rows[0], 1, "Reference Title / Publication", width=Inches(3.2))
    add_header_cell(t_ref.rows[0], 2, "Source / Publisher", width=Inches(2.8))
    for i, (num, tit, src) in enumerate(references):
        row = t_ref.rows[i + 1]
        add_data_cell(row, 0, num, width=Inches(0.6), bold=True)
        add_data_cell(row, 1, tit, width=Inches(3.2))
        add_data_cell(row, 2, src, width=Inches(2.8), italic=True)

    doc.add_page_break()

    # ════════════════════════════════════════════════════════════════
    # PAGE 31: PROJECT MODULE SUMMARY
    # ════════════════════════════════════════════════════════════════
    add_para(doc, "PROJECT MODULE SUMMARY", space_before=10, space_after=10, align=WD_ALIGN_PARAGRAPH.CENTER, size=15)
    add_para(
        doc,
        "This section provides a concise module-to-requirement mapping designed for quick navigation during project viva, practical evaluations, and institutional accreditation reviews.",
        space_after=8
    )

    module_summary = [
        ("Authentication & Wallet", "All Users", "Register, login, JWT issuance, password hashing, and $100k wallet initialization"),
        ("Live Ticker Streaming", "All Traders", "Stream real-time price ticks via WebSockets with in-memory caching"),
        ("Stock Search & Profile", "All Traders", "Search US tickers, fetch company profile, sector, and market cap"),
        ("Interactive Charting", "All Traders", "Render interactive multi-period price charts using Chart.js"),
        ("Virtual Trading Engine", "All Traders", "Execute simulated Buy/Sell orders with atomic balance verification"),
        ("Portfolio & PnL Tracking", "All Traders", "Monitor holdings, total equity, cost basis, and unrealized profit/loss"),
        ("Polynomial ML Predictor", "All Traders", "Train 2nd-degree OLS model over 30-day candles; project 5-day curve"),
        ("Explainable AI (XAI)", "All Traders", "Synthesize econometric parameters into plain-English Bull/Bear thesis memo"),
        ("Watchlist Management", "All Traders", "Personalized stock tracking list updating alongside market ticks"),
        ("Community Trading Forum", "All Traders", "Share trade setups, analysis, and engage in real-time discussion"),
    ]
    t_mod = doc.add_table(rows=len(module_summary) + 1, cols=3)
    t_mod.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_mod, color="CCCCCC")
    add_header_cell(t_mod.rows[0], 0, "Module Name", width=Inches(2.0))
    add_header_cell(t_mod.rows[0], 1, "Target Users", width=Inches(1.2))
    add_header_cell(t_mod.rows[0], 2, "Primary Functional Purpose", width=Inches(3.4))
    for i, (mn, tu, pr) in enumerate(module_summary):
        row = t_mod.rows[i + 1]
        add_data_cell(row, 0, mn, width=Inches(2.0), bold=True)
        add_data_cell(row, 1, tu, width=Inches(1.2))
        add_data_cell(row, 2, pr, width=Inches(3.4))

    add_para(doc, "End of Report", space_before=20, space_after=0, align=WD_ALIGN_PARAGRAPH.CENTER, size=11)

    # Save document
    doc.save(DOCX_PATH)
    print(f"Word document report successfully generated at: {DOCX_PATH}")

if __name__ == "__main__":
    build_docx_report()
