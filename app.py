import streamlit as st
import streamlit.components.v1 as components

# Налаштування інтерфейсу
st.set_page_config(page_title="Універсальний Конвертер Одиниць", layout="centered")

# Стиль заголовка
st.markdown("""
    <style>
        .title {
            font-size: 36px;
            font-weight: bold;
            text-align: center;
            color: #3f72af;
        }
        .subtitle {
            font-size: 18px;
            text-align: center;
            color: #555;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">Універсальний Конвертер Одиниць</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Конвертація довжини, ваги, температури, обʼєму та валюти (демо)</div><br>', unsafe_allow_html=True)

# --- Конвертація довжини ---
def convert_length(value, from_unit, to_unit):
    factors = {
        "метри": 1,
        "кілометри": 0.001,
        "милі": 0.000621371,
        "фути": 3.28084,
        "дюйми": 39.3701
    }
    return value / factors[from_unit] * factors[to_unit]

# --- Конвертація ваги ---
def convert_weight(value, from_unit, to_unit):
    factors = {
        "кілограми": 1,
        "грами": 1000,
        "фунти": 2.20462,
        "унції": 35.274
    }
    return value / factors[from_unit] * factors[to_unit]

# --- Конвертація температури ---
def convert_temperature(value, from_unit, to_unit):
    if from_unit == to_unit:
        return value
    if from_unit == "Цельсій":
        return value * 9/5 + 32 if to_unit == "Фаренгейт" else value + 273.15
    if from_unit == "Фаренгейт":
        return (value - 32) * 5/9 if to_unit == "Цельсій" else (value - 32) * 5/9 + 273.15
    if from_unit == "Кельвін":
        return value - 273.15 if to_unit == "Цельсій" else (value - 273.15) * 9/5 + 32

# --- Конвертація обʼєму ---
def convert_volume(value, from_unit, to_unit):
    factors = {
        "літри": 1,
        "мілілітри": 1000,
        "галони": 0.264172,
        "чашки": 4.22675
    }
    return value / factors[from_unit] * factors[to_unit]

# --- Конвертація валюти (демо) ---
def convert_currency(value, from_unit, to_unit):
    rates = {
        "USD": 1,
        "EUR": 0.9,
        "UAH": 38,
        "GBP": 0.78
    }
    return value / rates[from_unit] * rates[to_unit]

# --- Категорія ---
category = st.selectbox("Оберіть категорію:", ["Довжина", "Вага", "Температура", "Обʼєм", "Валюта"])

if category:
    value = st.number_input("Введіть значення:", format="%.4f")

    if category == "Довжина":
        units = ["метри", "кілометри", "милі", "фути", "дюйми"]
        from_unit = st.selectbox("З одиниці:", units)
        to_unit = st.selectbox("В одиницю:", units)
        result = convert_length(value, from_unit, to_unit)

    elif category == "Вага":
        units = ["кілограми", "грами", "фунти", "унції"]
        from_unit = st.selectbox("З одиниці:", units)
        to_unit = st.selectbox("В одиницю:", units)
        result = convert_weight(value, from_unit, to_unit)

    elif category == "Температура":
        units = ["Цельсій", "Фаренгейт", "Кельвін"]
        from_unit = st.selectbox("З одиниці:", units)
        to_unit = st.selectbox("В одиницю:", units)
        result = convert_temperature(value, from_unit, to_unit)

    elif category == "Обʼєм":
        units = ["літри", "мілілітри", "галони", "чашки"]
        from_unit = st.selectbox("З одиниці:", units)
        to_unit = st.selectbox("В одиницю:", units)
        result = convert_volume(value, from_unit, to_unit)

    elif category == "Валюта":
        units = ["USD", "EUR", "UAH", "GBP"]
        from_unit = st.selectbox("З валюти:", units)
        to_unit = st.selectbox("У валюту:", units)
        st.caption("*Курси валют вказані умовно для демонстрації.")
        result = convert_currency(value, from_unit, to_unit)

    st.success(f"**Результат:** {result:.4f} {to_unit}")
