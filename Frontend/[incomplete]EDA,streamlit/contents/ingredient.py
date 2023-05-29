import os
import time
import pandas as pd
import streamlit as st
from hydralit import HydraHeadApp


class IngredientTab(HydraHeadApp):
    def __init__(self, title = 'ingredient', **kwargs):
        self.__dict__.update(kwargs)
        self.title = title
        self.row_num = 4
        self.col_num = 5
        self.max_content = self.row_num * self.col_num
        self.img_size = 250
        self.max_title = 15
        
    def run(self):
        # head
        st.experimental_set_query_params(contents=self.title)
        ingre_df= pd.read_csv('./static/dataset/재료_메타정보_s.csv')
        recipe_ingre_df= pd.read_csv('./static/dataset/레시피_재료_내용_s.csv',dtype = {'재료_아이디': object})
        recipe_df = pd.read_csv('./static/dataset/레시피_메타정보_s.csv')
        ingre_name_list = ingre_df['재료_이름'].tolist()

        # body
        st.markdown(f'#### 🍳 지금 만들 수 있는 요리는 무엇일까요? 가진 재료를 알려주세요!')
        search_ingre = st.multiselect('✅ 재료를 선택하세요', ingre_name_list)

        #st.write(tag_boxes(search, ingre_name_list, st.session_state.tags),unsafe_allow_html=True)

        threshold = 0
        if search_ingre:
            threshold = st.slider('✅ 최소 필요한 재료 갯수는?', 0, len(search_ingre), len(search_ingre))
        # --검색엔진 (추후 변경)
        
        # 검색 테이블 생성
        check_time = time.time()
        key2id_dic = {v[1]:v[0] for v in ingre_df.values}
        search_ingre_id = [key2id_dic[i] for i in search_ingre]
        engine_table = recipe_ingre_df.groupby('레시피_아이디').agg({'재료_아이디': lambda x: '_'.join('_'+x+'_')}).reset_index()
        
        # 검색엔진 탐색
        
        result = {}
        for k,v in engine_table.values:
            result[k] = 0
            for target in search_ingre_id:
                if str(target) in v:
                    result[k] += 1

        # 결과 출력
        if search_ingre:
            #search_df = recipe_df[recipe_df['레시피_아이디'].isin([k for k,v in result.items() if v >= threshold])]
            #st.write(f'총 검색결과 {search_df.shape[0]}개 ({time.time()-check_time:.2f}초)')
            #st.dataframe(search_df)
            
            
            # 이미지 박스 형태로 표시
            content = [k for k,v in result.items() if v >= threshold]
            st.write(f'총 검색결과 {len(content)}개 ({time.time()-check_time:.2f}초)')
            for row in range(self.row_num):
                cols = st.columns(self.col_num)
                size = row * self.col_num 
                for col, rand in enumerate(content[size : size + self.col_num]):
                    data = recipe_df[recipe_df['레시피_아이디'] == rand].values[0]
                    cols[col].markdown(f'<img src="{data[2]}" width="{self.img_size}" height="{self.img_size}"/>', unsafe_allow_html=True)
                    #cols[col].markdown(f'<img src="{data[2]}" width="{self.img_size}" height="{self.img_size}"/>', unsafe_allow_html=True)
                    data[4] = data[4][:self.max_title]+'...' if len(data[4]) >= self.max_title else data[4][:self.max_title]
                    cols[col].markdown(f'**{data[4]}**')