import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO
import datetime

st.set_page_config(page_title="Legal Draft Generator", layout="centered")
st.title("⚖️ Civil Plaint Generator – Breach of Contract")

# -----------------------------
# BASIC DETAILS
# -----------------------------
st.subheader("Court Details")
court_name = st.text_input("Name of the Court")
court_location = st.text_input("Court Location")

st.subheader("Plaintiff Details")
plaintiff_name = st.text_input("Plaintiff Name")
plaintiff_age = st.text_input("Plaintiff Age")
plaintiff_address = st.text_area("Plaintiff Address")

st.subheader("Defendant Details")
defendant_name = st.text_input("Defendant Name")
defendant_age = st.text_input("Defendant Age")
defendant_address = st.text_area("Defendant Address")

st.subheader("Contract Details")
contract_type = st.text_input("Type of Contract")
agreement_date = st.date_input("Agreement Date")
total_amount = st.text_input("Total Contract Amount")
advance_paid = st.text_input("Advance Paid")
breach_date = st.date_input("Date of Breach")

# -----------------------------
# DYNAMIC FACTS
# -----------------------------
st.subheader("Facts of the Case")

if "facts" not in st.session_state:
    st.session_state.facts = [""]

for i in range(len(st.session_state.facts)):
    st.session_state.facts[i] = st.text_area(
        f"Fact {i + 1}",
        st.session_state.facts[i],
        height=80
    )

if st.button("➕ Add Another Fact"):
    st.session_state.facts.append("")

# -----------------------------
# OTHER LEGAL SECTIONS
# -----------------------------
st.subheader("Jurisdiction")
jurisdiction_reason = st.text_area("Reason for Jurisdiction")

st.subheader("Claim Details")
claim_amount = st.text_input("Claim Amount")
interest_rate = st.text_input("Interest Rate (%)")

st.subheader("Relief Sought")
relief_requested = st.text_area("Relief Requested")

st.subheader("Verification")
verification_place = st.text_input("Place")
verification_date = st.date_input("Date", datetime.date.today())

# -----------------------------
# GENERATE DRAFT + PDF
# -----------------------------
def generate_pdf(draft_text):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    x_margin, y_margin = 50, height - 50

    for line in draft_text.split("\n"):
        if y_margin <= 50:
            pdf.showPage()
            y_margin = height - 50
        pdf.drawString(x_margin, y_margin, line)
        y_margin -= 14

    pdf.save()
    buffer.seek(0)
    return buffer

if st.button("Generate Civil Plaint (PDF)"):

    facts_text = ""
    count = 1
    for fact in st.session_state.facts:
        if fact.strip():
            facts_text += f"{count}. {fact}\n"
            count += 1

    draft = f"""
IN THE HON’BLE COURT OF {court_name}, {court_location}

CIVIL SUIT FOR BREACH OF CONTRACT

PLAINTIFF:
{plaintiff_name}, Aged about {plaintiff_age} years,
Residing at {plaintiff_address}

DEFENDANT:
{defendant_name}, Aged about {defendant_age} years,
Residing at {defendant_address}

1. FACTS OF THE CASE
{facts_text}

2. CAUSE OF ACTION
The cause of action arose on {breach_date} when the defendant committed breach of contract.

3. JURISDICTION
This Hon’ble Court has jurisdiction because {jurisdiction_reason}.

4. CLAIM
The plaintiff claims Rs. {claim_amount} along with interest at {interest_rate}% per annum.

5. RELIEF SOUGHT
{relief_requested}

6. VERIFICATION
I, {plaintiff_name}, verify that the contents of this plaint are true to my knowledge.

Verified at {verification_place}
On {verification_date}

Plaintiff
"""

    pdf_file = generate_pdf(draft)

    st.success("Civil Plaint Generated Successfully")
    st.download_button(
        label="📄 Download Civil Plaint PDF",
        data=pdf_file,
        file_name="Civil_Plaint_Breach_of_Contract.pdf",
        mime="application/pdf"
    )
