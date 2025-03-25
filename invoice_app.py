import streamlit as st
import pandas as pd
from fpdf import FPDF
import base64
import tempfile
from zipfile import ZipFile
import os

# Configuration
TEMPLATE_PATH = "Black and White Minimalist Business Invoice.png"
FONT_SIZE = 12  # Reduced from 18 for better fit
LINE_HEIGHT = 8

COORDINATES = {
    "InvoiceID": (135, 50),
    "Date": (140, 75),
    "ClientName": (10, 75),
    "Amount": (10, 187),
    "Description": (10, 135),
}


class CustomPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.add_page()
        self.set_margins(left=20, top=20, right=20)  # Add safe margins
        self.set_auto_page_break(auto=True, margin=20)  # Bottom margin
        self.set_font("Arial", size=FONT_SIZE)

    def header(self):
        self.image(TEMPLATE_PATH, x=0, y=0, w=210, h=297)

    def add_content(self, data):
        self.set_font("Arial", size=FONT_SIZE)

        for field, (x, y) in COORDINATES.items():
            self.set_xy(x, y)
            if field == "Description":
                self.multi_cell(0, LINE_HEIGHT, str(data[field]))  # Wrap text
            else:
                self.cell(0, LINE_HEIGHT, str(data[field]))


def generate_pdf(invoice_data):
    pdf = CustomPDF()
    pdf.add_content(invoice_data)
    return pdf.output(dest="S").encode("latin-1")


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
