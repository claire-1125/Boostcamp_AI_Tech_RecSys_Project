import os
import time
import pandas as pd
import streamlit as st
#http://localhost:8502/?contents=recipe&recipe_id=123

rid = st.experimental_get_query_params()['recipe_id'][0]


recipe_df = pd.read_csv('./static/dataset/레시피_메타정보_s.csv')
recipe_tag_df = pd.read_csv('./static/dataset/레시피_태그_내용_s.csv')
recipe_ingre_df= pd.read_csv('./static/dataset/레시피_재료_내용_s.csv',dtype = {'재료_아이디': object})
recipe_step_df = pd.read_csv('./static/dataset/레시피_순서_내용_s.csv')



target_1 = recipe_df[recipe_df['레시피_아이디'] == int(rid)]
target_2 = recipe_tag_df[recipe_tag_df['레시피_아이디'] == int(rid)]
target_3 = recipe_ingre_df[recipe_ingre_df['레시피_아이디'] == int(rid)]
target_4 = recipe_step_df[recipe_step_df['레시피_아이디'] == int(rid)]



col1, col2 = st.columns(2)

with col1:
    st.markdown(f"### {target_1['제목'].tolist()[0]}")
    st.markdown(f"{target_1['요약'].tolist()[0]}")
with col2:
    img = target_1['레시피_메인이미지'].tolist()[0]
    st.markdown(f'<img src="{img}" width="{400}" height="{400}"/>', unsafe_allow_html=True)

st.markdown('---')
st.markdown(f'#### 레시피 순서')
for i in target_4.values:
    st.markdown(f"## {i[1]}번")
    st.markdown(f"{i[2]}")
    #st.markdown(f"{i[3]}")
    st.markdown(f'<img src="{i[3]}"/>', unsafe_allow_html=True)
#st.dataframe(target_4)

