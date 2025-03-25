import streamlit as st
import pandas as pd
from fpdf import FPDF
import base64
import tempfile
from zipfile import ZipFile
import os

# Configuration - Fixed
TEMPLATE_PATH = os.path.abspath("Black and White Minimalist Business Invoice.png")
FONT_PATH = os.path.abspath("Ubuntu-Medium.ttf")  # Add this file to your project

# Verify resources exist
if not os.path.exists(TEMPLATE_PATH):
    st.error(f"Template image missing at: {TEMPLATE_PATH}")
if not os.path.exists(FONT_PATH):
    st.error(f"Font file missing at: {FONT_PATH}")

COORDINATES = {
    "InvoiceID": (135, 57),
    "Date": (135, 75),
    "ClientName": (10, 75),
    "Amount": (10, 187),
    "Description": (10, 135),
}


class CustomPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.add_page()
        self.set_margins(20, 20, 20)
        self.set_auto_page_break(True, margin=20)
        self.add_font("Arial", style="", fname=FONT_PATH, uni=True)
        self.set_font("Arial", size=12)

    def header(self):
        if os.path.exists(TEMPLATE_PATH):
            self.image(TEMPLATE_PATH, x=0, y=0, w=210, h=297)
        else:
            self.cell(0, 10, "Invoice Template Missing!", ln=True)

    def add_content(self, data):
        self.set_font("Arial", size=12)
        for field, (x, y) in COORDINATES.items():
            self.set_xy(x, y)
            self.cell(0, 10, str(data.get(field, "")))


def generate_pdf(invoice_data):
    try:
        pdf = CustomPDF()
        pdf.add_content(invoice_data)
        return pdf.output(dest="S").encode("latin-1")
    except Exception as e:
        st.error(f"PDF Generation Error: {str(e)}")
        return b""


# Rest of your Streamlit UI code remains the same...


# Streamlit UI with preview features
st.title("🧾 Professional Invoice Generator")

# Data Upload and Preview
uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])
if uploaded_file:
    df = pd.read_excel(uploaded_file)

    with st.expander("📄 Preview Uploaded Data", expanded=True):
        st.dataframe(df)

    # Client Selection
    all_clients = ["All"] + df["ClientName"].unique().tolist()
    selected_clients = st.multiselect(
        "Select Clients to Process:", options=all_clients, default=["All"]
    )

    # Filter Data
    if "All" in selected_clients:
        filtered_df = df
    else:
        filtered_df = df[df["ClientName"].isin(selected_clients)]

    # Preview Selected Invoices
    with st.expander("👀 Preview Selected Invoices"):
        if not filtered_df.empty:
            st.write(f"Selected {len(filtered_df)} invoices:")
            st.dataframe(filtered_df)
        else:
            st.warning("No invoices selected!")

    # PDF Preview Section
    if not filtered_df.empty:
        st.subheader("PDF Preview")
        preview_invoice = st.selectbox(
            "Select invoice to preview:", filtered_df["InvoiceID"].tolist()
        )

        if st.button("Generate Preview"):
            preview_data = (
                filtered_df[filtered_df["InvoiceID"] == preview_invoice]
                .iloc[0]
                .to_dict()
            )
            pdf_bytes = generate_pdf(preview_data)

            # Show PDF preview
            base64_pdf = base64.b64encode(pdf_bytes).decode("utf-8")
            pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="500" type="application/pdf">'
            st.markdown(pdf_display, unsafe_allow_html=True)

            # Preview download button
            st.download_button(
                label="Download Preview PDF",
                data=pdf_bytes,
                file_name=f"preview_{preview_invoice}.pdf",
                mime="application/pdf",
            )

    # Bulk Generation
    if st.button("🚀 Download Invoices"):
        with tempfile.TemporaryDirectory() as tmp_dir:
            zip_path = os.path.join(tmp_dir, "invoices.zip")

            with ZipFile(zip_path, "w") as zipf:
                for _, row in filtered_df.iterrows():
                    try:
                        pdf = generate_pdf(row.to_dict())
                        filename = f"{row['ClientName']}_{row['InvoiceID']}.pdf"
                        zipf.writestr(filename, pdf)
                    except Exception as e:
                        st.error(
                            f"Error generating invoice {row['InvoiceID']}: {str(e)}"
                        )

            with open(zip_path, "rb") as f:
                st.download_button(
                    "📥 Ready click to download",
                    f.read(),
                    "invoices.zip",
                    "application/zip",
                )
