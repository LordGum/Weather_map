import streamlit as st

def render_sidebar():
    st.sidebar.header("Дополнительно")
    st.sidebar.info(
        "**Города для тестирования:**\n"
        "- Берлин, Каир, Дубай - в норме\n"
        "- Пекин, Москва - аномальные"
    )

    st.sidebar.header("Настройки")
    st.sidebar.markdown("Загрузите данные и введите API ключ для начала работы")

    st.sidebar.image("images/fire_meme.png", width=250)