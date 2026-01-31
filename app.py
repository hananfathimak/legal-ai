import streamlit as st
import json

st.set_page_config(page_title="Legal Draft Generator", layout="centered")

st.title("⚖️ Civil Plaintiff Input Form")

# Load schema
with open("input_schema.json", "r") as f:
    schema = json.load(f)

user_data = {}

st.subheader("Fill the case details:")

for field in schema["fields"]:
    label = field["label"]
    name = field["name"]
    field_type = field["type"]

    if field_type == "text":
        user_data[name] = st.text_input(label)

    elif field_type == "number":
        # Force manual typing instead of spinner
        user_data[name] = st.text_input(label)

    elif field_type == "date":
        # Keep calendar picker for date
        user_data[name] = st.date_input(label)

    elif field_type == "textarea":
        user_data[name] = st.text_area(label)

st.divider()

if st.button("Generate JSON"):
    st.subheader("Collected Input Data")
    st.json(user_data)
