import streamlit as st
import pandas as pd
import datetime as dt
from streamlit_option_menu import option_menu

import app_utils

def show():
    st.header("Students view")

    df_all = pd.read_pickle('data/processed/df_objectives.pkl')

    cols_students = ['student_name', 'question',
    'std_alternatives', 'answ_alternatives','subject', 'level', 'area', 'score', 'time']
    df_students = df_all[cols_students].sort_values(by=['student_name','subject', 'question']).set_index(['student_name','subject', 'question'])
    
    df_students_score = df_all.groupby(["student_name"])['score'].sum()

    # writing and discursive
    df_writing = pd.read_pickle('data/processed/df_writing.pkl')
    df_writing_total = df_writing[['student_name','Final grade']]

    df_discursive = pd.read_pickle('data/processed/df_discursive.pkl')
    df_discursive_total = df_discursive.groupby("student_name")['total score'].sum()

    df_total_score = pd.merge(df_students_score, df_writing_total, on="student_name",how = 'outer')
    df_total_score = pd.merge(df_total_score, df_discursive_total, on="student_name",how = 'outer')
    df_total_score.fillna(0,inplace=True)
    
    df_total_score = df_total_score.rename(columns={'score': 'Objective score', 'Final grade': 'Writing score','total score': 'Discursive score'})
    df_total_score['Total score'] = df_total_score.sum(axis=1)
    df_total_score = df_total_score.sort_values(by='Total score',ascending=False).reset_index()
    df_total_score['Ranking'] = df_total_score.index + 1
    df_total_score['Ranking'] = df_total_score['Ranking'].astype(str) + 'º'
    cols_total_score = ['student_name', 'Objective score','Writing score','Discursive score','Total score','Ranking']
    app_utils.plot_table(df_total_score, cols_total_score)
    # /!\ Interactive panel /!\
    # Based on the selected student on the side bar, it changes the data of next fields
    st.subheader("Data about the selected student")
    with st.sidebar:
        students_list = list(df_all['student_name'].unique())
        selected_student = st.sidebar.selectbox("Select the student", students_list)

    df_student = df_all[df_all['student_name'] == selected_student]
    df_student_writing = df_writing[df_writing['student_name'] == selected_student]
    df_student_discusive = df_discursive[df_discursive['student_name'] == selected_student]
    df_student_summary = df_total_score[df_total_score['student_name'] == selected_student]

    # /!\ Perfomance overview /!\
    st.subheader("Perfomance overview")
    # KPIs
    student_total_score = round(df_student_summary['Total score'],2)
    student_obj_score = round(df_student_summary['Objective score'],2)
    student_writ_score = round(df_student_summary['Writing score'],2)
    student_disc_score = round(df_student_summary['Discursive score'],2)
    student_time = df_student['time'].sum()
    student_time = str(dt.timedelta(seconds=student_time))

    col1, col2, col3,col4,col5 = st.columns(5)   
    with col1:
        st.metric(label='Total score', value=student_total_score)
    with col2:
        st.metric(label='Objectives', value=student_obj_score)
    with col3:
        st.metric(label='Writing', value=student_writ_score)
    with col4:
        st.metric(label='Discursive', value=student_disc_score)
    with col5: 
        st.metric(label='Total time', value=student_time)

    # Subjects, writing and discursive overview
    df_student_overview = df_student.groupby(['subject'])["score"].agg(['sum','count','mean','std'])
    app_utils.plot_chart(title="Student's perfomance on summatize-type questions", x=df_student_overview.index,y=df_student_overview['sum'])
 
    df_student_writing_manip = app_utils.manipulate_writing(df_student_writing)
    cols_writ = ['Criterion','Grade','Comment']
    app_utils.plot_table(df_student_writing_manip, cols_writ)

    cols_disc = ['subject','a)','b)','c)','total score','comments']
    app_utils.plot_table(df_student_discusive[cols_disc], cols_disc)

    # /!\ Students answers and scores /!\
    st.subheader("Student data on questions")
    cols_student = ['subject','question','std_alternatives','answ_alternatives','score','time']
    app_utils.plot_table(df_student,cols_student)