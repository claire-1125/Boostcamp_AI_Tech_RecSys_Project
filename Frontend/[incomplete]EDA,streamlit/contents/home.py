import os
import random
import pandas as pd
import streamlit as st
from hydralit import HydraHeadApp


class HomeTab(HydraHeadApp):
    def __init__(self, username, title = 'Home', **kwargs):
        self.__dict__.update(kwargs)
        self.title = title
        self.user = username
        self.row_num = 4
        self.col_num = 5
        self.max_content = self.row_num * self.col_num
        self.img_size = 250
        self.max_title = 15

    def run(self):
        # head
        st.experimental_set_query_params(contents=self.title)
        recipe_df = pd.read_csv('./static/dataset/레시피_메타정보_s.csv')

        # body
        st.markdown(f'#### 🍽️ {self.user}님을 위한 추천 레시피')
        content = random.sample(range(recipe_df.shape[0]),self.max_content)

        for row in range(self.row_num):
            cols = st.columns(self.col_num)
            size = row * self.col_num 
            for col, rand in enumerate(content[size : size + self.col_num]):
                data = recipe_df.values[rand]
                cols[col].markdown(f'<img src="{data[2]}" width="{self.img_size}" height="{self.img_size}"/>', unsafe_allow_html=True)
                #cols[col].markdown(f'<img src="{data[2]}" width="{self.img_size}" height="{self.img_size}"/>', unsafe_allow_html=True)
                data[4] = data[4][:self.max_title]+'...' if len(data[4]) >= self.max_title else data[4][:self.max_title]
                cols[col].markdown(f'**{data[4]}**')
        