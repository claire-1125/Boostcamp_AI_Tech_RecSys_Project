import os
import streamlit as st
from hydralit import HydraHeadApp


class RecipePage(HydraHeadApp):
    def __init__(self, title = 'recipe', **kwargs):
        self.__dict__.update(kwargs)
        self.title = title

    def run(self):
        # head
        st.experimental_set_query_params(contents=self.title)
        #recipe_df = pd.read_csv('./static/dataset/레시피_메타정보_raw.csv')
    
        # body
        st.dataframe(search_df)
        st.write(f'총 검색결과 {search_df.shape[0]}개')
        search_keyword = st.text_input("키워드로 레시피 검색", placeholder = "키워드 입력")