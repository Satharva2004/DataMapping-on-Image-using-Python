# 🧾 Receipt Generator for ICETI4T 2025 using Streamlit + FPDF
--
This project is built to generate official **receipts for ICETI4T 2025** based on participant data uploaded via an Excel sheet. It uses a professional template image and a clean font to produce PDF files for each entry — downloadable individually or in bulk.

While this tool is currently tailored for generating **receipts**, you can easily repurpose it for:
- Participation **certificates**
- **Invoices**
- **Event passes**
- Or **any document** where dynamic data needs to be placed on a pre-designed template.

> ⚙️ **Note:** The text placement (X, Y coordinates) is fixed inside the code under the `COORDINATES` dictionary. You are free to adjust the positions and template to suit your layout.

---

## 💼 Features

- Upload Excel files with structured participant data.
- Preview and filter uploaded data.
- Generate single or bulk PDFs.
- Preview PDFs live in the browser.
- Download all generated documents as a `.zip`.
- Easy to modify for any custom layout or use-case.

---

## 🗂 Required Files

Make sure you have the following in the root directory:

- **Template Image**: `Black and White Minimalist Business Invoice.png`  
  Used as the background for each receipt (can be replaced with any design).

- **Font File**: `Ubuntu-Medium.ttf`  
  Used to render the text professionally onto the PDF.

---

## 🛠 COORDINATE SETTINGS

Text placement is handled by this dictionary:

```python
COORDINATES = {
    "InvoiceID": (135, 57),
    "Date": (135, 75),
    "ClientName": (10, 75),
    "Amount": (10, 187),
    "Description": (10, 135),
}
```
### App preview
![image](https://github.com/user-attachments/assets/c4f1547b-404b-4847-a44c-ee0b36162698)
![image](https://github.com/user-attachments/assets/a9ffbc67-9bc7-4769-9ee1-32a67db350d1)

### Example reciept
![image](https://github.com/user-attachments/assets/18da7a61-6993-4afa-8364-e0feb366e3b0)

You can easily adapt this same method to create certificates, invoices, ID cards, or any other document where data needs to be placed on a custom design — just update the template and coordinates!
