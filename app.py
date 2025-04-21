import streamlit as st
import pandas as pd
import math

# Налаштування інтерфейсу
st.set_page_config(page_title="Універсальний Конвертер Одиниць", layout="centered", initial_sidebar_state="collapsed")

# Стиль заголовка та блоку результату
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
        .result-box {
            background: #eef7f1;
            border: 2px solid #4CAF50;
            border-radius: 8px;
            padding: 12px;
            margin-top: 10px;
            font-weight: bold;
            text-align: center;
            color: #1b4d3e;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">Універсальний Конвертер Одиниць</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Конвертація довжини, ваги, температури, обʼєму, валюти, часу, площі, швидкості — з історією</div><br>', unsafe_allow_html=True)

if "history" not in st.session_state:
    st.session_state["history"] = []

unit_ending_map = {
    "метри": "метрів", "кілометри": "кілометрів", "милі": "миль", "фути": "футів", "дюйми": "дюймів",
    "кілограми": "кілограми", "грами": "грамів", "фунти": "фунтів", "унції": "унцій",
    "літри": "літрів", "мілілітри": "мілілітрів", "галони": "галонів", "чашки": "чашок",
    "Цельсій": "°C", "Фаренгейт": "°F", "Кельвін": "K",
    "секунди": "секунд", "хвилини": "хвилин", "години": "годин", "дні": "днів",
    "метри²": "м²", "кілометри²": "км²", "фути²": "фут²", "акри": "акрів",
    "км/год": "км/год", "м/с": "м/с", "мили/год": "мили/год",
    "USD": "USD", "EUR": "EUR", "UAH": "UAH", "GBP": "GBP"
}

def convert_time(value, from_unit, to_unit):
    factors = {"секунди": 1, "хвилини": 60, "години": 3600, "дні": 86400}
    return value * factors[from_unit] / factors[to_unit]

def convert_area(value, from_unit, to_unit):
    factors = {"метри²": 1, "кілометри²": 1e6, "фути²": 0.092903, "акри": 4046.86}
    return value * factors[from_unit] / factors[to_unit]

def convert_speed(value, from_unit, to_unit):
    factors = {"км/год": 1, "м/с": 3.6, "мили/год": 1.60934}
    return value * factors[from_unit] / factors[to_unit]

def convert_length(value, from_unit, to_unit):
    factors = {"метри": 1, "кілометри": 1000, "милі": 1609.34, "фути": 0.3048, "дюйми": 0.0254}
    return value * factors[from_unit] / factors[to_unit]

def convert_weight(value, from_unit, to_unit):
    factors = {"кілограми": 1, "грами": 0.001, "фунти": 0.453592, "унції": 0.0283495}
    return value * factors[from_unit] / factors[to_unit]

def convert_temperature(value, from_unit, to_unit):
    if from_unit == to_unit:
        return value
    if from_unit == "Цельсій":
        return value * 9 / 5 + 32 if to_unit == "Фаренгейт" else value + 273.15
    if from_unit == "Фаренгейт":
        return (value - 32) * 5 / 9 if to_unit == "Цельсій" else (value - 32) * 5 / 9 + 273.15
    if from_unit == "Кельвін":
        return value - 273.15 if to_unit == "Цельсій" else (value - 273.15) * 9 / 5 + 32

def convert_volume(value, from_unit, to_unit):
    factors = {"літри": 1, "мілілітри": 0.001, "галони": 3.78541, "чашки": 0.24}
    return value * factors[from_unit] / factors[to_unit]

def convert_currency(value, from_unit, to_unit):
    rates = {"USD": 1, "EUR": 0.93, "UAH": 38.0, "GBP": 0.8}
    return value / rates[from_unit] * rates[to_unit]

category = st.selectbox("Оберіть категорію:", ["Довжина", "Вага", "Температура", "Обʼєм", "Валюта", "Час", "Площа", "Швидкість"])

value = st.number_input("Введіть значення:", format="%.4f")

if category == "Час":
    units = ["секунди", "хвилини", "години", "дні"]
elif category == "Площа":
    units = ["метри²", "кілометри²", "фути²", "акри"]
elif category == "Швидкість":
    units = ["км/год", "м/с", "мили/год"]
elif category == "Довжина":
    units = ["метри", "кілометри", "милі", "фути", "дюйми"]
elif category == "Вага":
    units = ["кілограми", "грами", "фунти", "унції"]
elif category == "Температура":
    units = ["Цельсій", "Фаренгейт", "Кельвін"]
elif category == "Обʼєм":
    units = ["літри", "мілілітри", "галони", "чашки"]
elif category == "Валюта":
    units = ["USD", "EUR", "UAH", "GBP"]

from_unit = st.selectbox("З одиниці:", units)
to_unit = st.selectbox("В одиницю:", units)

if st.button("Конвертувати"):
    if category == "Час":
        result = convert_time(value, from_unit, to_unit)
    elif category == "Площа":
        result = convert_area(value, from_unit, to_unit)
    elif category == "Швидкість":
        result = convert_speed(value, from_unit, to_unit)
    elif category == "Довжина":
        result = convert_length(value, from_unit, to_unit)
    elif category == "Вага":
        result = convert_weight(value, from_unit, to_unit)
    elif category == "Температура":
        result = convert_temperature(value, from_unit, to_unit)
    elif category == "Обʼєм":
        result = convert_volume(value, from_unit, to_unit)
    elif category == "Валюта":
        result = convert_currency(value, from_unit, to_unit)

    unit_display = unit_ending_map.get(to_unit, to_unit)
    st.markdown(f'<div class="result-box">Результат: {result:.4f} {unit_display}</div>', unsafe_allow_html=True)
    st.session_state["history"].append(f"{category}: {value} {from_unit} → {result:.4f} {unit_display}")

st.subheader("Історія конвертацій")
if st.session_state["history"]:
    st.dataframe(pd.DataFrame(st.session_state["history"], columns=["Операція"]))
