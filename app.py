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
        .stTextInput input:focus::placeholder, .stNumberInput input:focus::placeholder {
            color: transparent;
        }
        .stNumberInput input::placeholder {
            color: grey;
        }
        .right-align-download .css-1offfwp.e1y5xkzn3 {
            justify-content: flex-end;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">Універсальний Конвертер Одиниць</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Конвертація довжини, ваги, температури, обʼєму, валюти та з історією</div><br>', unsafe_allow_html=True)

if "history" not in st.session_state:
    st.session_state["history"] = []

# Відмінювання одиниць
unit_ending_map = {
    "метри": "метрів",
    "кілометри": "кілометрів",
    "милі": "миль",
    "фути": "футів",
    "дюйми": "дюймів",
    "кілограми": "кілограми",
    "грами": "грамів",
    "фунти": "фунтів",
    "унції": "унцій",
    "літри": "літрів",
    "мілілітри": "мілілітрів",
    "галони": "галонів",
    "чашки": "чашок",
    "Цельсій": "°C",
    "Фаренгейт": "°F",
    "Кельвін": "K",
    "USD": "USD",
    "EUR": "EUR",
    "UAH": "UAH",
    "GBP": "GBP"
}

# Функції конвертації
# (... залишаємо без змін ...)

# --- Інтерфейс ---
# (... залишаємо без змін ...)

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

        unit_display = unit_ending_map.get(to_unit, to_unit)
        st.markdown(f'<div class="result-box">Результат: {result:.4f} {unit_display}</div>', unsafe_allow_html=True)
        st.session_state["history"].append(f"{category}: {value} {from_unit} → {result:.4f} {unit_display}")

# --- Відображення історії ---
st.subheader("Історія конвертацій")
if st.session_state["history"]:
    st.dataframe(pd.DataFrame(st.session_state["history"], columns=["Операція"]))

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Очистити історію"):
            st.session_state["history"] = []
            st.experimental_rerun()
    with col2:
        df = pd.DataFrame(st.session_state["history"], columns=["Операція"])
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ Завантажити CSV", data=csv, file_name="history.csv", mime="text/csv", help="Завантажити історію у вигляді таблиці")
