import streamlit as st
from src.backend.schema import APP_INFO


def header():
    # -------------- SETTINGS --------------
    page_title = APP_INFO.title
    page_icon = (
        APP_INFO.icon
    )  # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/

    # --- HIDE STREAMLIT STYLE ---: uncomment in production
    # hide_st_style = """
    #             <style>
    #             #MainMenu {visibility: hidden;}
    #             footer {visibility: hidden;}
    #             header {visibility: hidden;}
    #             </style>
    #             """
    # st.markdown(hide_st_style, unsafe_allow_html=True)

    st.title(f"{page_icon} {page_title}")
    st.write(APP_INFO.description)
    st.markdown("---")
    st.subheader(APP_INFO.subtitle)
    st.write(APP_INFO.subtitle_description)
