from fpdf import FPDF
import streamlit as st

st.title("🔍 Template Position Finder")

# Configuration
TEMPLATE_PATH = "Black and White Minimalist Business Invoice.png"


class PDF(FPDF):
    def __init__(self):
        super().__init__()  # Add parent initialization
        self.add_page()
        self.set_font("Arial", size=12)  # Set default font

    def header(self):
        self.image(TEMPLATE_PATH, x=0, y=0, w=210, h=297)


def preview_pdf(x, y):
    pdf = PDF()
    pdf.set_xy(x, y)
    pdf.cell(0, 10, "X MARK HERE")

    with st.expander("Preview PDF"):
        pdf_output = pdf.output(dest="S").encode("latin-1")
        st.download_button("Download Test PDF", pdf_output, "test.pdf")
        st.write(f"Current coordinates: X={x}mm, Y={y}mm")


x = st.slider("X Position (mm)", 0, 210, 30)
y = st.slider("Y Position (mm)", 0, 297, 150)
preview_pdf(x, y)
