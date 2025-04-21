import streamlit as st

# Сетап інтерфейсу
st.set_page_config(page_title="Universal Unit Converter", layout="centered")
st.title("🔄 Universal Unit Converter")
st.markdown("Convert between units of **length**, **weight**, **temperature**, **volume**, and **currency** (mocked).")

# --- Length conversion ---
def convert_length(value, from_unit, to_unit):
    factors = {
        "meters": 1,
        "kilometers": 0.001,
        "miles": 0.000621371,
        "feet": 3.28084,
        "inches": 39.3701
    }
    return value / factors[from_unit] * factors[to_unit]

# --- Weight conversion ---
def convert_weight(value, from_unit, to_unit):
    factors = {
        "kilograms": 1,
        "grams": 1000,
        "pounds": 2.20462,
        "ounces": 35.274
    }
    return value / factors[from_unit] * factors[to_unit]

# --- Temperature conversion ---
def convert_temperature(value, from_unit, to_unit):
    if from_unit == to_unit:
        return value
    if from_unit == "Celsius":
        return value * 9/5 + 32 if to_unit == "Fahrenheit" else value + 273.15
    if from_unit == "Fahrenheit":
        return (value - 32) * 5/9 if to_unit == "Celsius" else (value - 32) * 5/9 + 273.15
    if from_unit == "Kelvin":
        return value - 273.15 if to_unit == "Celsius" else (value - 273.15) * 9/5 + 32

# --- Volume conversion ---
def convert_volume(value, from_unit, to_unit):
    factors = {
        "liters": 1,
        "milliliters": 1000,
        "gallons": 0.264172,
        "cups": 4.22675
    }
    return value / factors[from_unit] * factors[to_unit]

# --- Currency conversion (mocked) ---
def convert_currency(value, from_unit, to_unit):
    rates = {
        "USD": 1,
        "EUR": 0.9,
        "UAH": 38,
        "GBP": 0.78
    }
    return value / rates[from_unit] * rates[to_unit]

# --- Selector ---
category = st.selectbox("Choose category:", ["Length", "Weight", "Temperature", "Volume", "Currency"])

if category:
    value = st.number_input("Enter value:", format="%.4f")

    if category == "Length":
        units = ["meters", "kilometers", "miles", "feet", "inches"]
        from_unit = st.selectbox("From:", units)
        to_unit = st.selectbox("To:", units)
        result = convert_length(value, from_unit, to_unit)

    elif category == "Weight":
        units = ["kilograms", "grams", "pounds", "ounces"]
        from_unit = st.selectbox("From:", units)
        to_unit = st.selectbox("To:", units)
        result = convert_weight(value, from_unit, to_unit)

    elif category == "Temperature":
        units = ["Celsius", "Fahrenheit", "Kelvin"]
        from_unit = st.selectbox("From:", units)
        to_unit = st.selectbox("To:", units)
        result = convert_temperature(value, from_unit, to_unit)

    elif category == "Volume":
        units = ["liters", "milliliters", "gallons", "cups"]
        from_unit = st.selectbox("From:", units)
        to_unit = st.selectbox("To:", units)
        result = convert_volume(value, from_unit, to_unit)

    elif category == "Currency":
        units = ["USD", "EUR", "UAH", "GBP"]
        from_unit = st.selectbox("From:", units)
        to_unit = st.selectbox("To:", units)
        st.caption("Note: Currency rates are for demo purposes only.")
        result = convert_currency(value, from_unit, to_unit)

    st.success(f"**Result:** {result:.4f} {to_unit}")

