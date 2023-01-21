import streamlit as st
import pandas as pd
import datetime as dt

import app_utils

def show():
    st.header("Overall View")

    # /!\ Summary about the scores on the test /!\
    # ge
    df_all = pd.read_pickle('data/processed/df_objectives.pkl')

    df_summary = df_all.groupby('student_name')['score','time'].agg(['sum','mean'])

    avg_score_test = round(df_summary[[('score', 'sum')]].mean(), 2)
    avg_score_question = round(df_summary[[('score', 'mean')]].mean(),2)

    avg_time_test = df_summary[[('time', 'sum')]].mean()
    avg_time_question = df_summary[[('time', 'mean')]].mean()
    avg_time_test = str(dt.timedelta(seconds=avg_time_test.item())).split(".")[0]
    avg_time_question = str(dt.timedelta(seconds=avg_time_question.item())).split(".")[0]

    col1, col2, col3,col4 = st.columns(4)   
    with col1:
        st.metric(label='Avg student score', value=avg_score_test)
    with col2:
        st.metric(label='Avg question score', value=avg_score_question)
    with col3:
        st.metric(label='Avg time to complete the test', value=avg_time_test)
    with col4:
        st.metric(label='Avg time per question', value=avg_time_question)

    # data about the subjects
    df_overview_subjects = df_all.groupby(['subject'])["score"].agg(['sum','count','mean','std'])
    app_utils.plot_chart(title='Summation-type questions avg score', x=df_overview_subjects.index, y=df_overview_subjects['mean'])
    
    # data about writing and discursive
    df_writing = pd.read_pickle('data/processed/df_writing.pkl')
    df_writing_man = app_utils.manipulate_writing(df_writing)
    df_overview_writing = df_writing_man.groupby(['Criterion'])['Grade'].agg(['sum','count','mean','std'])

    df_discursive = pd.read_pickle('data/processed/df_discursive.pkl')
    df_overview_discursive = df_discursive.groupby(['subject'])['total score'].agg(['sum','count','mean','std'])
    
    col1, col2 = st.columns(2)
    with col1:
        app_utils.plot_chart(title='Discursive avg scores', x=df_overview_discursive.index, y=df_overview_discursive['mean'],size='small')
    with col2:
        app_utils.plot_chart(title='Writing avg scores', x=df_overview_writing.index, y=df_overview_writing['mean'],size='small')

    # /!\ Interactive panel /!\
    # Based on the selected subject on the side bar, it changes the data of next fields
    with st.sidebar:
        subject_list = list(df_overview_subjects.index)
        selected_subject =  st.sidebar.selectbox("Select the subject", subject_list)

    df_subject = df_all[df_all['subject'] == selected_subject]
  
    st.subheader("Overview about selected subject")
    df_questions = df_subject.groupby(["question", "level","area"])["score"].agg(['sum','count','mean','std'])
    df_questions_time = df_subject.groupby(["question"])["time"].agg(['mean'])
    df_questions_time.rename(columns={'mean':'average time'},inplace=True)
    df_questions = df_questions.join(df_questions_time, on='question')
    
    avg_subject_score = round(df_questions['mean'].sum(), 2)
    avg_subject_question_score = round(df_questions['mean'].mean(), 2)
    avg_subject_time = df_questions['average time'].sum()
    avg_subject_question_time = df_questions['average time'].mean()
    avg_subject_time = str(dt.timedelta(seconds=avg_subject_time.item())).split(".")[0]
    avg_subject_question_time = str(dt.timedelta(seconds=avg_subject_question_time.item())).split(".")[0]

    col1, col2, col3,col4 = st.columns(4)   
    with col1:
        st.metric(label='Avg subject score', value=avg_subject_score)
    with col2:
        st.metric(label='Avg question score', value=avg_subject_question_score)
    with col3:
        st.metric(label='Avg time to complete the subject', value=avg_subject_time)
    with col4:
        st.metric(label='Avg time per question', value=avg_subject_question_time)

    app_utils.plot_chart(title="Question's avg score",x=df_questions.index.get_level_values(0),y=df_questions['mean'])
    
    # data about each area and level
    df_questions_area = df_subject.groupby(["area"])["score"].agg(['sum','count','mean','std'])
    df_questions_level = df_subject.groupby(["level"])["score"].agg(['sum','count','mean','std'])
    col1, col2 = st.columns(2)
    with col1:
        app_utils.plot_chart(title="Question's level avg score", x=df_questions_level.index, y=df_questions_level['mean'], size='small')
    with col2:
        app_utils.plot_chart(title="Question's area avg score", x=df_questions_area.index, y=df_questions_area['mean'],size='small')
    
    df_questions.reset_index(inplace=True)
    df_questions = df_questions.round(decimals = 2)

    cols_questions = ['question','area','level','mean','average time']
    app_utils.plot_table(df_questions, cols_questions)
