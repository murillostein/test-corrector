import pandas as pd

from corrector_utils import manipulate_language
from corrector_utils import correct_data_type
from corrector_utils import manipulate_language
from corrector_utils import get_alternatives_from_sum
from corrector_utils import get_answers
from corrector_utils import sorting_data
from corrector_utils import calculate_score
from corrector_utils import clean_discursive

df_raw_objectives = pd.read_csv('data/raw/df_all.csv')
df_raw_answ_day_1_eng = pd.read_excel('data/raw/df_answers_day_1_eng.xlsx')
df_raw_answ_day_1_spa = pd.read_excel('data/raw/df_answers_day_1_spa.xlsx')
df_raw_answ_day_2 = pd.read_excel('data/raw/df_answers_day_2.xlsx')

df_raw_answ_day_1_eng['language'] = 'English'
df_raw_answ_day_1_spa['language'] = 'Spanish'
df_raw_answ_day_2['language'] = '2º day'
df_answers = pd.concat([df_raw_answ_day_1_eng, df_raw_answ_day_1_spa,df_raw_answ_day_2])

df_clean_objectives = (df_raw_objectives.pipe(manipulate_language)
                                        .pipe(correct_data_type)
                                        .pipe(get_alternatives_from_sum,'student_answer')
                                        .pipe(get_answers, get_alternatives_from_sum(df_answers,'test_answer'))
                                        .pipe(sorting_data))

df_clean_objectives['score'] = df_clean_objectives.apply(calculate_score, axis=1)

df_clean_objectives.to_pickle('data/processed/df_objectives.pkl')

# Dealing with Writting test and Discursive questions
df_raw_write = pd.read_csv('data/raw/df_writing.csv')
df_raw_disc = pd.read_csv('data/raw/df_discursive.csv')

df_raw_write.fillna('', inplace=True)
df_raw_disc.fillna('', inplace=True)
df_disc = clean_discursive(df_raw_disc)

df_disc.to_pickle('data/processed/df_discursive.pkl')
df_raw_write.to_pickle('data/processed/df_writing.pkl')