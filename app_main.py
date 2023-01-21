import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu


import app_pag1
import app_pag2
import app_pag3

hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """
def main():
    st.title('UFSC test corrector and report generator')

    with st.sidebar:
        n_sprites = option_menu('Menu',["Introduction","Overall view","Students view"],
                            icons=['body-text','bar-chart-fill','mortarboard'],
                            default_index=0, menu_icon="app-indicator",
                            styles={
            "container": {"padding": "2!important", "background-color": "#ffffff"},
            "nav-link": {"font-size": "12px", "text-align": "left", "--hover-color": "#c1d5bc","font-weight": "bold"},
            "nav-link-selected": {"background-color": "#337321"},
            }) 
    
    if n_sprites == "Introduction":
        app_pag1.show()

    if n_sprites == "Overall view":
        #app_pag1.overall_view()
        app_pag2.show()
    
    if n_sprites == "Students view":
        #app_pag2.students_view()
        app_pag3.show()
        
if __name__ == '__main__':
    main()