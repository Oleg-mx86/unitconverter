import streamlit as st
import pint
import pandas as pd
from datetime import datetime
import os

# Ініціалізація pint для конвертації одиниць
ureg = pint.UnitRegistry()

# Налаштування стилів для темного і світлого режимів
def set_theme(theme):
    if theme == "Темний":
        st.markdown("""
            <style>
                body, .stApp {
                    background-color: #1E1E1E;
                    color: #FFFFFF;
                }
                .stButton>button {
                    background-color: #4CAF50;
                    color: white;
                    border-radius: 8px;
                    padding: 10px 20px;
                    font-size: 16px;
                }
                .stButton>button:hover {
                    background-color: #45a049;
                }
                .stSelectbox, .stTextInput, .stNumberInput {
                    background-color: #2E2E2E;
                    color: #FFFFFF;
                    border-radius: 5px;
                }
                h1, h2, h3, p, label {
                    color: #FFFFFF;
                }
                .stDataFrame {
                    background-color: #2E2E2E;
                    color: #FFFFFF;
                }
            </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <style>
                body, .stApp {
                    background-color: #F5F5F5;
                    color: #000000;
                }
                .stButton>button {
                    background-color: #2196F3;
                    color: white;
                    border-radius: 8px;
                    padding: 10px 20px;
                    font-size: 16px;
                }
                .stButton>button:hover {
                    background-color: #1976D2;
                }
                .stSelectbox, .stTextInput, .stNumberInput {
                    background-color: #FFFFFF;
                    color: #000000;
                    border-radius: 5px;
                }
                h1, h2, h3, p, label {
                    color: #000000;
                }
                .stDataFrame {
                    background-color: #FFFFFF;
                    color: #000000;
                }
            </style>
        """, unsafe_allow_html=True)

# Словник категорій і одиниць вимірювання
units = {
    "Довжина": ["meter", "kilometer", "centimeter", "millimeter", "inch", "foot", "yard", "mile"],
    "Маса": ["kilogram", "gram", "milligram", "tonne", "pound", "ounce"],
    "Температура": ["celsius", "fahrenheit", "kelvin"],
    "Час": ["second", "minute", "hour", "day"],
    "Площа": ["square_meter", "square_kilometer", "hectare", "acre", "square_foot"],
    "Об'єм": ["cubic_meter", "liter", "milliliter", "gallon", "cubic_foot"],
    "Швидкість": ["meter/second", "kilometer/hour", "mile/hour"],
    "Енергія": ["joule", "kilojoule", "calorie", "kilocalorie", "watt_hour"]
}

# Функція для збереження історії
def save_history(value, from_unit, to_unit, result, category):
    history_file = "conversion_history.csv"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_entry = pd.DataFrame({
        "Дата": [timestamp],
        "Категорія": [category],
        "Значення": [value],
        "З одиниці": [from_unit],
        "В одиницю": [to_unit],
        "Результат": [result]
    })
    
    if os.path.exists(history_file):
        history = pd.read_csv(history_file)
        history = pd.concat([history, new_entry], ignore_index=True)
    else:
        history = new_entry
    
    history.to_csv(history_file, index=False)

# Основна програма
def main():
    # Налаштування сторінки
    st.set_page_config(page_title="Конвертер одиниць вимірювання", layout="wide")
    
    # Вибір теми
    theme = st.sidebar.selectbox("Виберіть тему", ["Світлий", "Темний"])
    set_theme(theme)
    
    # Заголовок
    st.title("Конвертер одиниць вимірювання")
    st.write("Перетворюйте одиниці вимірювання швидко та зручно!")
    
    # Вибір категорії
    category = st.selectbox("Оберіть категорію", list(units.keys()))
    
    # Вибір одиниць
    col1, col2 = st.columns(2)
    with col1:
        from_unit = st.selectbox("З одиниці", units[category], key="from_unit")
    with col2:
        to_unit = st.selectbox("В одиницю", units[category], key="to_unit")
    
    # Введення значення
    value = st.number_input("Введіть значення", min_value=0.0, step=0.1, format="%.4f")
    
    # Кнопка для конвертації
    if st.button("Конвертувати"):
        try:
            # Виконання конвертації
            quantity = value * ureg(from_unit)
            result = quantity.to(to_unit)
            st.success(f"Результат: {result:.4f}")
            
            # Збереження в історію
            save_history(value, from_unit, to_unit, f"{result:.4f}", category)
        except Exception as e:
            st.error(f"Помилка: {str(e)}")
    
    # Відображення історії
    st.subheader("Історія конвертацій")
    history_file = "conversion_history.csv"
    if os.path.exists(history_file):
        history = pd.read_csv(history_file)
        st.dataframe(history, use_container_width=True)
    else:
        st.write("Історія порожня")

if __name__ == "__main__":
    main()
