import streamlit as st
import pandas as pd

# Налаштування інтерфейсу
st.set_page_config(page_title="Універсальний Конвертер Одиниць", layout="centered")

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
st.markdown('<div class="subtitle">Конвертація довжини, ваги, температури, обʼєму, валюти та з історією</div><br>', unsafe_allow_html=True)

# Історія конвертацій
if "history" not in st.session_state:
    st.session_state["history"] = []

# --- Функції конвертацій ---
def convert_length(value, from_unit, to_unit):
    factors = {"метри": 1, "кілометри": 0.001, "милі": 0.000621371, "фути": 3.28084, "дюйми": 39.3701}
    return value / factors[from_unit] * factors[to_unit]

def convert_weight(value, from_unit, to_unit):
    factors = {"кілограми": 1, "грами": 1000, "фунти": 2.20462, "унції": 35.274}
    return value / factors[from_unit] * factors[to_unit]

def convert_temperature(value, from_unit, to_unit):
    if from_unit == to_unit:
        return value
    if from_unit == "Цельсій":
        return value * 9/5 + 32 if to_unit == "Фаренгейт" else value + 273.15
    if from_unit == "Фаренгейт":
        return (value - 32) * 5/9 if to_unit == "Цельсій" else (value - 32) * 5/9 + 273.15
    if from_unit == "Кельвін":
        return value - 273.15 if to_unit == "Цельсій" else (value - 273.15) * 9/5 + 32

def convert_volume(value, from_unit, to_unit):
    factors = {"літри": 1, "мілілітри": 1000, "галони": 0.264172, "чашки": 4.22675}
    return value / factors[from_unit] * factors[to_unit]

def convert_currency(value, from_unit, to_unit):
    rates = {"USD": 1, "EUR": 0.9, "UAH": 38, "GBP": 0.78}
    return value / rates[from_unit] * rates[to_unit]

# --- Інтерфейс ---
category = st.selectbox("Оберіть категорію:", ["Довжина", "Вага", "Температура", "Обʼєм", "Валюта"])

if category:
    st.markdown("**Наприклад:**")
    if category == "Довжина":
        st.caption("1 метр = 100 сантиметрів, 1 миля ≈ 1.609 км")
    elif category == "Вага":
        st.caption("1 кг = 1000 г, 1 фунт ≈ 0.453 кг")
    elif category == "Температура":
        st.caption("0 °C = 32 °F = 273.15 К")
    elif category == "Обʼєм":
        st.caption("1 літр = 1000 мл, 1 галон ≈ 3.785 л")
    elif category == "Валюта":
        st.caption("1 USD ≈ 38 UAH (демо)")

    value = st.number_input("Введіть значення:", format="%.4f")

    if category == "Довжина":
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
        if category == "Довжина":
            result = convert_length(value, from_unit, to_unit)
        elif category == "Вага":
            result = convert_weight(value, from_unit, to_unit)
        elif category == "Температура":
            result = convert_temperature(value, from_unit, to_unit)
        elif category == "Обʼєм":
            result = convert_volume(value, from_unit, to_unit)
        elif category == "Валюта":
            result = convert_currency(value, from_unit, to_unit)
            st.caption("*Курси валют вказані умовно для демонстрації.")

        st.markdown(f'<div class="result-box">Результат: {result:.4f} {to_unit}</div>', unsafe_allow_html=True)
        st.session_state["history"].append(f"{category}: {value} {from_unit} → {result:.4f} {to_unit}")

# --- Відображення історії ---
st.subheader("Історія конвертацій")
if st.session_state["history"]:
    st.dataframe(pd.DataFrame(st.session_state["history"], columns=["Операція"]))

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Очистити історію"):
            st.session_state["history"] = []
            st.experimental_rerun()
    with col2:
        df = pd.DataFrame(st.session_state["history"], columns=["Операція"])
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ Завантажити CSV", data=csv, file_name="history.csv", mime="text/csv")
