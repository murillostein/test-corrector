import pandas as pd
import streamlit as st
import plotly.graph_objects as go

def plot_chart(title = '',x_name='', y_name='', x = '', y = '',size='big'):
    """Function to plot bar charts
    Args:
        title (str, optional): Title of figure. Defaults to ''.
        x_name (str, optional): name of X line. Defaults to ''.
        y_name (str, optional): name of Y line. Defaults to ''.
        x (str, optional): values of x. Defaults to ''.
        y (str, optional): values of y. Defaults to ''.
        size (str): defines if the chart will fill all the width or only half of it.
    """
    if size=='big':
        width = 800
    else:
        width = 400

    layout = go.Layout(title = title)
    fig = go.Figure(layout = layout)
    fig.update_layout(height=500, width=width,barmode='group',title={
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'
        })
    fig.add_trace(go.Bar(x=x, y=y, text=y.round(2),textposition='outside', marker_color='#337321'))
    fig.update_yaxes(showticklabels=False)
    fig.update_layout( showlegend=False, paper_bgcolor='rgba(255,255,255,0.9)', plot_bgcolor='rgba(255,255,255,0.9)') 
    fig.update_yaxes(showgrid=True, gridwidth=0.1, gridcolor = '#3e3a39')
    st.plotly_chart(fig)

def plot_table(df, columns):
    values = []
    for col in columns:
        values.append(df[col].to_list())
    fig = go.Figure(data=[go.Table(
        header=dict(values=list(columns),
                    fill_color='#337321',
                    line_color='darkslategray',
                    font=dict(color='white',size=12),
                    align='left'),
        cells=dict(values=values,
                fill_color='white',
                line_color='darkslategray',
                font_size=12,
                align='left'))
    ])
    fig.update_layout(height=500, width=800)
    st.plotly_chart(fig)
    

def manipulate_writing(df):
    """
    This function converts the writing table from ['student','grade criterion 1','comments criterio 1',...'final grade','final comment']
    to ['student', 'criterion','grade'], makeing easier to visualize the data.
    """
    score_writing = df[['student_name','Grade criterion 1','Grade criterion 2','Grade criterion 3','Grade criterion 4',  'Final grade']]
    comment_writing = df[['student_name','Comments criterion 1','Comments criterion 2', 'Comments criterion 3','Comments criterion 4','Overall comment']]

    score_writing = score_writing.rename(columns={'Grade criterion 1': "Criterion 1",'Grade criterion 2': "Criterion 2",'Grade criterion 3': "Criterion 3",'Grade criterion 4': "Criterion 4",'Final grade': "Grade"})
    comment_writing = comment_writing.rename(columns={'Comments criterion 1': "Criterion 1",'Comments criterion 2': "Criterion 2",'Comments criterion 3': "Criterion 3",'Comments criterion 4': "Criterion 4",'Overall comment': "Grade"})

    score_writing = pd.melt(score_writing, id_vars=['student_name'], value_vars=['Criterion 1','Criterion 2','Criterion 3','Criterion 4','Grade'], var_name='Criterion', value_name='Grade')
    comment_writing = pd.melt(comment_writing, id_vars=['student_name'], value_vars=['Criterion 1','Criterion 2','Criterion 3','Criterion 4','Grade'], var_name='Criterion', value_name='Comment')

    df_writ = pd.merge(score_writing, comment_writing, how='left', left_on=['student_name','Criterion'], right_on=['student_name','Criterion'])
    return df_writ