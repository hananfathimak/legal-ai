import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle,Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
import datetime
from textwrap import wrap

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(page_title="Civil Plaint Generator – Kerala", layout="centered")
st.title("⚖️ Civil Plaint Generator (Kerala)")

# --------------------------------------------------
# COURT DETAILS
# --------------------------------------------------
st.subheader("Court Details")
court_name = st.text_input("Name of the Court *")
court_location = st.text_input("Court Location *")

# --------------------------------------------------
# PARTY DETAILS
# --------------------------------------------------
st.subheader("Plaintiff Details")
plaintiff_name = st.text_input("Plaintiff Name *")
plaintiff_age = st.text_input("Plaintiff Age *")
plaintiff_address = st.text_area("Plaintiff Address *")

st.subheader("Defendant Details")
defendant_name = st.text_input("Defendant Name *")
defendant_age = st.text_input("Defendant Age *")
defendant_address = st.text_area("Defendant Address *")

# --------------------------------------------------
# ADVOCATE DETAILS
# --------------------------------------------------
st.subheader("Advocate Details")
advocate_name = st.text_input("Advocate Name *")
advocate_enrollment = st.text_input("Enrollment Number *")
advocate_address = st.text_area("Advocate Office Address *")

# --------------------------------------------------
# CONTRACT DETAILS
# --------------------------------------------------
st.subheader("Contract Details")
contract_type = st.text_input("Type of Contract *")
agreement_date = st.date_input("Agreement Date *")
total_amount = st.text_input("Total Contract Amount (₹) *")
advance_paid = st.text_input("Advance Paid (₹)")
breach_date = st.date_input("Date of Breach *")

# --------------------------------------------------
# FACTS
# --------------------------------------------------
st.subheader("Facts of the Case")
if "facts" not in st.session_state:
    st.session_state.facts = [""]

for i in range(len(st.session_state.facts)):
    st.session_state.facts[i] = st.text_area(
        f"Fact {i + 1} *", st.session_state.facts[i], height=90
    )

if st.button("➕ Add Another Fact"):
    st.session_state.facts.append("")

# --------------------------------------------------
# JURISDICTION
# --------------------------------------------------
st.subheader("Jurisdiction")
jurisdiction_reason = st.text_area("Reason for Jurisdiction *")

# --------------------------------------------------
# CLAIM
# --------------------------------------------------
st.subheader("Claim Details")
claim_amount = st.text_input("Claim Amount (₹) *")
interest_rate = st.text_input("Interest Rate (% per annum) *")

# --------------------------------------------------
# VERIFICATION INPUT
# --------------------------------------------------
st.subheader("Verification")
verification_place = st.text_input("Place *")
verification_date = st.date_input("Date", datetime.date.today())

# --------------------------------------------------
# PROPERTY DETAILS
# --------------------------------------------------
st.subheader("Schedule of Property (Optional)")
district = st.text_input("District")
sub_district = st.text_input("Sub District")
taluk = st.text_input("Taluk")
amsom = st.text_input("Amsom")
desom = st.text_input("Desom")
avakasham = st.text_input("Avakasham")
tharam = st.text_input("Tharam")
os_no = st.text_input("O.S. No")
rs_no = st.text_input("R.S. No")
extent = st.text_input("Extent")

st.subheader("Description of Property")
property_description = st.text_area("Property Description")

st.subheader("Boundaries")
boundary_east = st.text_input("East")
boundary_north = st.text_input("North")
boundary_west = st.text_input("West")
boundary_south = st.text_input("South")

# --------------------------------------------------
# DOCUMENTS
# --------------------------------------------------
st.subheader("List of Documents")
if "documents" not in st.session_state:
    st.session_state.documents = [{
        "date": "", "by": "", "to": "", "desc": "", "purpose": ""
    }]

for i, d in enumerate(st.session_state.documents):
    d["date"] = st.text_input("Date", d["date"], key=f"d_date_{i}")
    d["by"] = st.text_input("Executed by", d["by"], key=f"d_by_{i}")
    d["to"] = st.text_input("Executed to", d["to"], key=f"d_to_{i}")
    d["desc"] = st.text_input("Description", d["desc"], key=f"d_desc_{i}")
    d["purpose"] = st.text_input("Purpose", d["purpose"], key=f"d_purpose_{i}")
    st.divider()

if st.button("➕ Add Document"):
    st.session_state.documents.append({
        "date": "", "by": "", "to": "", "desc": "", "purpose": ""
    })

# --------------------------------------------------
# COURT FEE
# --------------------------------------------------
def calculate_court_fee(amount):
    try:
        amount = float(amount)
        if amount <= 100000:
            return amount * 0.075
        elif amount <= 500000:
            return amount * 0.05
        else:
            return amount * 0.03
    except:
        return 0.0

court_fee = calculate_court_fee(claim_amount)

# --------------------------------------------------
# PDF GENERATION
# --------------------------------------------------
def generate_pdf(draft_text, documents):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    text = pdf.beginText(50, height - 50)
    text.setFont("Times-Roman", 11)

    margin_x = 50
    margin_y = 50
    usable_width = width - 2 * margin_x

    y_position = height - margin_y
    pdf.setFont("Times-Roman", 11)


    for para in draft_text.split("\n"):
        lines = wrap(para, 95) if para.strip() else [""]
        for line in lines:
            if y_position <= margin_y:
                pdf.showPage()
                pdf.setFont("Times-Roman", 11)
                y_position = height - margin_y
            pdf.drawString(margin_x, y_position, line)
            y_position -= 14

    # ---------- LIST OF DOCUMENTS ----------
    valid_docs = [d for d in documents if any(v.strip() for v in d.values())]

    if valid_docs:

        # Check remaining space BEFORE forcing new page
        if y_position <= 120:
            pdf.showPage()
            pdf.setFont("Times-Roman", 11)
            y_position = height - margin_y

        pdf.setFont("Times-Bold", 12)
        pdf.drawString(margin_x, y_position, "LIST OF DOCUMENTS")
        y_position -= 20

        styles = getSampleStyleSheet()
        normal_style = styles["Normal"]
        normal_style.fontName = "Times-Roman"
        normal_style.fontSize = 9

        header_style = styles["Normal"]
        header_style.fontName = "Times-Bold"
        header_style.fontSize = 9

        table_data = [[
            Paragraph("Sl.No", header_style),
            Paragraph("Date", header_style),
            Paragraph("Executed by", header_style),
            Paragraph("Executed to", header_style),
            Paragraph("Description", header_style),
            Paragraph("Purpose", header_style),
        ]]

        for i, d in enumerate(valid_docs):
            table_data.append([
                Paragraph(str(i+1), normal_style),
                Paragraph(d["date"], normal_style),
                Paragraph(d["by"], normal_style),
                Paragraph(d["to"], normal_style),
                Paragraph(d["desc"], normal_style),
                Paragraph(d["purpose"], normal_style),
            ])

        # Adjusted widths to fit inside margins
        col_widths = [35, 60, 75, 75, 135, 70]

        table = Table(table_data, colWidths=col_widths, repeatRows=1)
        table.setStyle(TableStyle([
            ("GRID", (0,0), (-1,-1), 1, colors.black),
            ("VALIGN", (0,0), (-1,-1), "TOP"),
        ]))

        table_width, table_height = table.wrap(usable_width, height)

        # If table won't fit remaining space → new page
        if y_position - table_height <= margin_y:
            pdf.showPage()
            pdf.setFont("Times-Roman", 11)
            y_position = height - margin_y

        table.drawOn(pdf, margin_x, y_position - table_height)
        y_position -= table_height + 20

        # Footer Verification
        pdf.setFont("Times-Roman", 11)

        if y_position <= margin_y:
            pdf.showPage()
            y_position = height - margin_y

        pdf.drawString(margin_x, y_position, f"Plaintiff : {plaintiff_name}")
        y_position -= 20

        pdf.drawString(margin_x, y_position, "VERIFICATION")
        y_position -= 15

        verification_text = (
            f"I, {plaintiff_name}, the Plaintiff in the above matter, "
            f"declare that the list of documents stated above is true."
        )

        for line in wrap(verification_text, 95):
            pdf.drawString(margin_x, y_position, line)
            y_position -= 14

        pdf.drawString(margin_x, y_position,
                       f"Verified at {verification_place} on {verification_date}.")
        y_position -= 20

        pdf.drawString(margin_x, y_position, f"Plaintiff : {plaintiff_name}")

    pdf.save()
    buffer.seek(0)
    return buffer

# --------------------------------------------------
# GENERATE PDF
# --------------------------------------------------
if st.button("📄 Generate Civil Plaint (PDF)"):
    facts_text = "\n".join(
        [f"{i+1}. {f}" for i, f in enumerate(st.session_state.facts) if f.strip()]
    )

    draft = f"""
BEFORE THE HON’BLE COURT OF {court_name}, {court_location}

CIVIL SUIT FOR BREACH OF CONTRACT

Plaintiff:
{plaintiff_name}, aged about {plaintiff_age} years,
Residing at {plaintiff_address}

Defendant:
{defendant_name}, aged about {defendant_age} years,
Residing at {defendant_address}

1. FACTS OF THE CASE
{facts_text}

2. CAUSE OF ACTION
The cause of action arose on {breach_date}.

3. JURISDICTION
{jurisdiction_reason}

4. VALUATION & COURT FEE
Suit valued at Rs.{claim_amount}
Court fee paid: Rs.{court_fee:.2f}

5. PRAYER
a) Direct the defendant to pay Rs.{claim_amount} with interest @ {interest_rate}% per annum.
b) Award costs of the suit.
c) Grant other reliefs as deemed fit.

Plaintiff : {plaintiff_name}

SCHEDULE OF PROPERTY
District : {district}
Sub District : {sub_district}
Taluk : {taluk}
Amsom : {amsom}
Desom : {desom}
Avakasham : {avakasham}
Tharam : {tharam}
O.S. No : {os_no}
R.S. No : {rs_no}
Extent : {extent}

DESCRIPTION OF PROPERTY
{property_description}

BOUNDARIES
East : {boundary_east}
North : {boundary_north}
West : {boundary_west}
South : {boundary_south}

VERIFICATION
I, {plaintiff_name}, the Plaintiff in the above matter, do hereby declare that the
averments stated above are true and correct to the best of my knowledge and belief.
Verified at {verification_place} on {verification_date}.

Plaintiff : {plaintiff_name}
"""

    pdf_file = generate_pdf(draft, st.session_state.documents)

    st.download_button(
        "⬇️ Download Civil Plaint PDF",
        pdf_file,
        "Civil_Plaint_Kerala.pdf",
        "application/pdf"
    )
