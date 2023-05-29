import os
import time
import pandas as pd
import streamlit as st
from hydralit import HydraHeadApp


class KeywordTab(HydraHeadApp):
    def __init__(self, title = 'keyword', **kwargs):
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
        recipe_df = pd.read_csv('./static/dataset/레시피_메타정보_s.csv')
        recipe_tag_df = pd.read_csv('./static/dataset/레시피_태그_내용_s.csv')
    
        # body
        st.markdown(f'#### 😋 지금 먹고싶은 요리가 있나요? 생각나는 음식을 알려주세요!')
        search_keyword = st.text_input('✅ 단어를 입력하세요',placeholder = "단어 입력")
        
        
        # --검색엔진 (추후 변경)
        
        # 검색 테이블 생성
        check_time = time.time()
        recipe_df_join = recipe_df[['레시피_아이디','제목','요약']]
        recipe_tag_df_join = recipe_tag_df.groupby('레시피_아이디').agg({'내용': lambda x: '_'.join('_'+x+'_')}).reset_index()
        engine_table = pd.merge(recipe_df_join,recipe_tag_df_join)

        # 검색엔진 탐색
        result = {}
        for i in pd.merge(recipe_df_join,recipe_tag_df_join).values:
            target_id = i[0]
            target_str = str(i[1])+str(i[2])+str(i[3])
            result[target_id] = target_str.count(search_keyword)
            
        # 결과 출력
        if search_keyword:
            result = sorted(result.items(), key = lambda item: item[1], reverse = True)
            #search_df = recipe_df[recipe_df['레시피_아이디'].isin([k for k,v in result if v >= 1])]
            #st.write(f'총 검색결과 {search_df.shape[0]}개 ({time.time()-check_time:.2f}초)')
            #st.dataframe(search_df)
            
            
            # 이미지 박스 형태로 표시
            content = [k for k,v in result if v >= 1]
            st.write(f'총 검색결과 {len(content)}개 ({time.time()-check_time:.2f}초)')
            for row in range(self.row_num):
                cols = st.columns(self.col_num)
                size = row * self.col_num 
                for col, rand in enumerate(content[size : size + self.col_num]):
                    data = recipe_df[recipe_df['레시피_아이디'] == rand].values[0]
                    cols[col].markdown(f'<img src="{data[2]}" width="{self.img_size}" height="{self.img_size}"/>', unsafe_allow_html=True)
                    #cols[col].markdown(f'<img src="{data[2]}" width="{self.img_size}" height="{self.img_size}"/>', unsafe_allow_html=True)
                    data[4] = data[4][:self.max_title]+'...' if len(data[4]) >= self.max_title else data[4][:self.max_title]
                    #cols[col].markdown(f'**{data[4]}**')
                    cols[col].markdown(f'<a href="http://localhost:8502/?contents=recipe&recipe_id={data[0]}">**{data[4]}**</a>', unsafe_allow_html=True)