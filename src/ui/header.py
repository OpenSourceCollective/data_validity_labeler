import streamlit as st


def header():
    # -------------- SETTINGS --------------
    page_title = "Health Record Validity Labeler"
    page_icon = ":health_worker:"  # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
    layout = "centered"

    st.set_page_config(
        page_title=page_title, page_icon=page_icon, layout=layout
    )

    # --- HIDE STREAMLIT STYLE ---: uncomment in production
    hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
    st.markdown(hide_st_style, unsafe_allow_html=True)

    st.title(f"{page_icon} {page_title}er")
    # TODO: Add a better introduction
    st.write(
        "This is a simple app to check and label the validity of electronic health records."
    )
    st.markdown("---")
    st.subheader("Patient Vitals Validation")
    st.write("*[Insert instructions here]*")
