import streamlit as st
import pandas as pd
from fpdf import FPDF
import base64
import tempfile
import os
from zipfile import ZipFile

# PDF Generation Function
def create_pdf(invoice):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Add invoice content
    pdf.cell(200, 10, txt=f"Invoice ID: {invoice['InvoiceID']}", ln=1)
    pdf.cell(200, 10, txt=f"Client: {invoice['ClientName']}", ln=1)
    pdf.cell(200, 10, txt=f"Date: {invoice['Date']}", ln=1)
    pdf.cell(200, 10, txt=f"Amount: ${invoice['Amount']}", ln=1)
    pdf.cell(200, 10, txt=f"Description: {invoice['Description']}", ln=1)
    
    return pdf.output(dest='S').encode('latin-1')

# Main App
st.title("📄 Invoice Generator")

# File Upload
uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx", "xls"])
if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.success("File uploaded successfully!")
    
    # Show data preview
    with st.expander("Show Data Preview"):
        st.dataframe(df)

    # Client selection
    all_clients = df['ClientName'].unique().tolist()
    selected_clients = st.multiselect(
        "Select Clients to Generate Invoices",
        options=['All Clients'] + all_clients,
        default='All Clients'
    )

    # Handle 'All Clients' selection
    if 'All Clients' in selected_clients:
        selected_clients = all_clients

    # Generate PDFs
    if st.button("Generate Invoices"):
        if not selected_clients:
            st.warning("Please select at least one client")
        else:
            # Create temporary directory
            with tempfile.TemporaryDirectory() as temp_dir:
                zip_path = os.path.join(temp_dir, "invoices.zip")
                
                # Create zip file
                with ZipFile(zip_path, 'w') as zipf:
                    for _, row in df[df['ClientName'].isin(selected_clients)].iterrows():
                        pdf_data = create_pdf(row)
                        filename = f"{row['ClientName']}_{row['InvoiceID']}.pdf"
                        zipf.writestr(filename, pdf_data)
                
                # Create download link
                with open(zip_path, "rb") as f:
                    b64 = base64.b64encode(f.read()).decode()
                    href = f'<a href="data:file/zip;base64,{b64}" download="invoices.zip">Download Invoices</a>'
                    st.markdown(href, unsafe_allow_html=True)