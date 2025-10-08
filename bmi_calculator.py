import streamlit as st

st.set_page_config(page_title="BMI Calculator", layout="centered")

st.title("Body Mass Index (BMI) Calculator")

st.write("Enter your height in feet and inches, and your weight in pounds to calculate your BMI.")

st.subheader("Enter Your Information")

col1, col2, col3 = st.columns(3)

with col1:
    feet = st.number_input("Height (feet)", min_value=0, step=1, value=5)
with col2:
    inches = st.number_input("Height (inches)", min_value=0, step=1, value=8)
with col3:
    weight_lbs = st.number_input("Weight (pounds)", min_value=0.0, step=0.1, value=150.0)

total_inches = feet * 12 + inches

if total_inches > 0 and weight_lbs > 0:
    bmi = (weight_lbs / (total_inches ** 2)) * 703
    st.markdown(f"### Your BMI: **{bmi:.2f}**")
else:
    st.info("Please enter your height and weight to calculate BMI.")