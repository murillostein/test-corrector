import pandas as pd
from itertools import combinations


def manipulate_language(df):
    df['language'] = df['test_name'].str.extract(
        '\((.*?)\)', expand=False).str.strip()
    df['language'].fillna("2º day", inplace=True)
    return df


def correct_data_type(df):
    df['student_answer'].fillna(0, inplace=True)
    df['student_answer'].replace(r'[\D]', '', regex=True, inplace=True)
    df['student_answer'].replace('', 0, inplace=True)
    df['question'] = df['question'].astype(int)
    df['student_answer'] = df['student_answer'].astype(int)
    return df


def get_alternatives_from_sum(df, col):
    """
    This functions extract each choosen alternative based on the total sum.
    First, it creates all possible combination based on the avaiable alternatives.
    Then, merges it in the dataframe.
    """
    possible_alternatives = [1, 2, 4, 8, 16, 32, 64]
    df_combinations = pd.DataFrame(
        columns=['alternatives', 'sum', '1', '2', '4', '8', '16', '32', '64'])
    i = 1
    while i < len(possible_alternatives):
        combinations_i = combinations(possible_alternatives, i)
        for alternatives in combinations_i:
            temp_dict = {
                'alternatives': alternatives,
                'sum': sum(alternatives)
            }
            for alternative in alternatives:
                temp_dict.update({
                    str(alternative): 1
                })
                temp_df = pd.DataFrame([temp_dict])
            df_combinations = df_combinations.append(temp_df)
        i += 1
    df_combinations.fillna(0, inplace=True)

    if col == 'student_answer':
        prefix = 'std_'
    else:
        prefix = 'answ_'
    df_comb_masked = df_combinations.add_prefix(prefix)
    df_merged = pd.merge(df, df_comb_masked, left_on=col,
                         right_on=f'{prefix}sum')
    df_merged.fillna(0, inplace=True)
    return df_merged


def get_answers(df_students, df_answer):
    df_merged = pd.merge(df_students, df_answer, on=["question", "language"])
    return df_merged


def sorting_data(df):
    subjects_order_dict = {"Língua Portuguesa": 0,
                           "Inglês": 1,
                           "Espanhol": 1,
                           "Matemática": 2,
                           "Biologia": 3,
                           "História": 7,
                           "Geografia": 5,
                           "Filosofia/Sociologia": 6,
                           "Física": 8,
                           "Química": 4
                           }
    subjects_order_df = pd.DataFrame(
        list(subjects_order_dict.items()), columns=['subject', 'order'])
    df_merged = pd.merge(df, subjects_order_df, on='subject')
    df_sorted = df_merged.sort_values(by=['student_name', 'order', 'question'])
    return df_sorted


def calculate_score(row):
    """
    This function analyses each student's answer and calculate the socre achieved based on the UFSC's rule.
    """
    CPS = 0
    ICS = 0
    TCP = 0
    i = 0
    n = 0
    possible_alternatives = [1, 2, 4, 8, 16, 32, 64]

    # In case of an "ABERTA" question, there's no partial score. In case of summation-type question, there's partial score
    if (row["TP"] != "ABERTA"):
        # this loop counts the number of CPS and CPI
        while n < int(row['TP']):
            alternative = str(possible_alternatives[i])
            TCP += int(row["answ_" + alternative])
            if row["answ_" + alternative] == row["std_" + alternative] and row["std_" + alternative] == 1.0:
                CPS += 1
            elif row["answ_" + alternative] != row["std_" + alternative] and row["std_" + alternative] == 1.0:
                ICS += 1
            n += 1
            i += 1

        # calculus of score
        if (CPS > ICS):
            s = (int(row['TP']) - (TCP - (CPS - ICS))) / int(row['TP'])
        else:
            s = 0
    else:
        if str(row["answ_alternatives"]) == str(row["std_alternatives"]):
            s = 1
        else:
            s = 0
    return round(s, 2)


def clean_discursive(df):
    df = df.rename(columns={"Grade exercise 'a' (ex.: 0.3)": 'a)',
                            "Grade exercise 'b' (ex.: 0.3)": 'b)', "Grade exercise 'c' (ex.: 0.3)": 'c)', "Total score (ex.:2.5)": 'total score'})
    df[['c)', 'total score']] = df[['c)', 'total score']].replace('', 0)
    df[['c)', 'total score']] = df[['c)', 'total score']].astype(float)
    return df