
from fpdf import FPDF

BLURB_BOOK_8X10_LANDSCAPE_DIM = [8.5000, 29.000] # height, width

pdf = FPDF('L', 'in', BLURB_BOOK_8X10_LANDSCAPE_DIM)
pdf.add_page()
pdf.set_font('Arial', 'B', 18)
pdf.set_xy(12, 2)
pdf.cell(4.5, 1, 'Art for Aleppo - Postcards Project', 1)
pdf.output('cover.pdf', 'F')
