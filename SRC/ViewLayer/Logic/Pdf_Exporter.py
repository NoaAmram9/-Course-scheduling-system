# pdf_exporter.py

from reportlab.lib.pagesizes import landscape, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from SRC.ViewLayer.Logic.TimeTable import DAYS, HOURS

def generate_pdf_from_data(file_path, slot_map, title, return_elements=False):
    """
    Generates a landscape PDF timetable from a given slot_map.

    Parameters:
        file_path (str): Path to save the generated PDF file.
        slot_map (dict): Dictionary mapping (day, hour) tuples to course details.
        title (str): The title shown on top of the timetable.
        return_elements (bool): If True, return the list of ReportLab elements instead of building the PDF.

    Returns:
        list (optional): If return_elements=True, returns a list of flowable elements for external PDF composition.
    """
    
    styles = getSampleStyleSheet()

    # Define a custom paragraph style for table cells
    cell_style = ParagraphStyle(
        name='CellStyle',
        parent=styles['Normal'],
        fontSize=8,             # Slightly reduced font size for fitting content
        leading=10,             # Line spacing
        alignment=1,            # Center alignment
        spaceAfter=2            # Small space below each paragraph
    )

    elements = []

    # Add the title of the timetable
    elements.append(Paragraph(f"Timetable Option {title}", styles['Title']))
    elements.append(Spacer(1, 12))  # Add space after title

    # Define the table header: one column for hours, and the rest for days
    header = ["Hour"] + DAYS
    data = [header]

    # Populate the timetable rows
    for hour in HOURS:
        row = [f"{hour}:00"]  # First column is the hour label
        for day in DAYS:
            cell = slot_map.get((day, hour))
            if cell:
                # Build the cell content with course name, code, type, instructor, and location
                text = f"<b>{cell['name']}</b> ({cell['code']})<br/>{cell['type']}<br/>{cell['instructor']}<br/>{cell['location']}"
                para = Paragraph(text, cell_style)
            else:
                para = Paragraph("", cell_style)  # Empty cell
            row.append(para)
        data.append(row)

    # Create the table and align it to the center
    table = Table(data, repeatRows=1, hAlign='CENTER')

    # Define table styling (header background, borders, padding, etc.)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#4a90e2")),   # Header background color
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),                  # Header text color
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),               # Header font
        ('FONTSIZE', (0, 0), (-1, 0), 10),                             # Header font size
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),                          # Center header horizontally
        ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),                         # Center header vertically
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),                         # Header padding
        ('TOPPADDING', (1, 1), (-1, -1), 6),                           # Body top padding
        ('BOTTOMPADDING', (1, 1), (-1, -1), 6),                        # Body bottom padding
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),                  # Grid lines
        ('ALIGN', (0, 1), (-1, -1), 'CENTER'),                         # Center align all cells
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),                        # Vertically center all cells
    ]))

    # Add alternating row background colors for better readability
    for i in range(1, len(data)):
        if i % 2 == 0:
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, i), (-1, i), colors.whitesmoke)
            ]))

    # Add the final table to the document flow
    elements.append(table)

    # Either return the elements (if building externally), or generate the PDF here
    if return_elements:
        return elements
    else:
        doc = SimpleDocTemplate(
            file_path,
            pagesize=landscape(A4),
            rightMargin=20,
            leftMargin=20,
            topMargin=20,
            bottomMargin=20
        )
        doc.build(elements)

        
# from reportlab.lib.pagesizes import landscape, A4
# from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
# from reportlab.lib import colors
# from reportlab.lib.styles import getSampleStyleSheet
# from SRC.ViewLayer.Logic.TimeTable import DAYS, HOURS

# def generate_pdf_from_data(file_path, slot_map, title, return_elements=False):

#     styles = getSampleStyleSheet()
#     elements = []

#     elements.append(Paragraph(f"Timetable Option {title}", styles['Title']))
#     elements.append(Spacer(1, 12))

#     header = ["Hour"] + DAYS
#     data = [header]

#     for hour in HOURS:
#         row = [f"{hour}:00"]
#         for day in DAYS:
#             cell = slot_map.get((day, hour))
#             text = f"{cell['name']} {cell['code']}\n({cell['type']})\n{cell['instructor']}\n{cell['location']}" if cell else ""
#             row.append(text)
#         data.append(row)

#     table = Table(data, repeatRows=1)
#     table.setStyle(TableStyle([
#         ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#4a90e2")),
#         ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
#         ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#         ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#         ('FONTSIZE', (0, 0), (-1, -1), 9),
#         ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
#         ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
#     ]))

#     elements.append(table)

#     if return_elements:
#         return elements
#     else:
#         doc = SimpleDocTemplate(file_path, pagesize=landscape(A4))
#         doc.build(elements)    
