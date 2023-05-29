import random
import datetime
import pandas as pd
import streamlit as st
import hydralit as hy


import hydralit_components as hc

# hide_streamlit_markers=True,
# use_navbar=True,
# navbar_sticky=True,

app = hy.HydraApp(title='Cookpang : 요리 정보 및 개인 성향 기반 레시피 추천 서비스',
                  favicon='👨‍🍳',
                  layout = 'wide',
                  allow_url_nav=True,
                  use_navbar=True, # 네비 사용여부
                  nav_container=None, # 네비 컨테이너
                  navbar_sticky=True, # 네비 상단 고정
                  navbar_animation=True, # 전환 애니메이션
                  # use_navbar = # xpak wowjddml
                  hide_streamlit_markers = True, # 햄버거 버튼과 워터마크 숨기기
                  banner_spacing =[1,5], # 배너 정렬
                  use_banner_images=['./static/img/cookpang_logo.png',
                                     {'header':"<h2 style='text-align:left;padding: 30px 0px;color:black;font-size:100%;'>RecSys 08 : 요리 정보 및 개인 성향 기반 레시피 추천 서비스</h2>"}],
                  #use_banner_images='<img src="./static/img/cookpang_logo.png" width="250" height="250"/>',
                  
                  )


# 썸네일 crop 가운데 정렬
# https://stackoverflow.com/questions/11552380/how-to-automatically-crop-and-center-an-image
# .thumbnail {
#   position: relative;
#   width: 200px;
#   height: 200px;
#   overflow: hidden;
# }
# .thumbnail img {
#   position: absolute;
#   left: 50%;
#   top: 50%;
#   height: 100%;
#   width: auto;
#   -webkit-transform: translate(-50%,-50%);
#       -ms-transform: translate(-50%,-50%);
#           transform: translate(-50%,-50%);
# }
# .thumbnail img.portrait {
#   width: 100%;
#   height: auto;
# }

#-- load_session.py
def set_session_state():
    # set default values
    if 'search' not in st.session_state:
        st.session_state.search = None
    if 'tags' not in st.session_state:
        st.session_state.tags = None

    # get parameters in url
    para = st.experimental_get_query_params()
    if 'search' in para:
        st.experimental_set_query_params()
        # decode url
        new_search = urllib.parse.unquote(para['search'][0])
        st.session_state.search = new_search
    if 'tags' in para:
        st.experimental_set_query_params()
        st.session_state.tags = para['tags'][0]

        
#-- load_css.py



#-- load_template.py


# html로 네비게이션 바 렌더링
def Navigation_bar():
    # 부트스트랩 CSS 사용
    # https://getbootstrap.com/docs/4.0/getting-started/download/
    st.markdown('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">', unsafe_allow_html=True)

    st.markdown("""
    <nav class="navbar fixed-top navbar-expand-lg navbar-dark" style="background-color: #3498DB;">
      <a class="navbar-brand" href="#" target="_blank">Cookpang</a>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav">
          <li class="nav-item">
            <a class="nav-link" href="#" target="_blank">Home</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#" target="_blank">키워드로 레시피 찾기</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#" target="_blank">재료로 레시피 찾기</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#" target="_blank">데이터 대시보드</a>
          </li>
        </ul>
      </div>
    </nav>
    """, unsafe_allow_html=True)


# <li class="nav-item active">
# <a class="nav-link disabled" href="#">Home<span class="sr-only">(current)</span></a>
# </li>

# 쿼리 결과 수 출력
def number_of_results(total_hits: int, duration: float) -> str:
    """ HTML scripts to display number of results and time taken. """
    return f"""
        <div style="color:grey;font-size:95%;">
            {total_hits} results ({duration:.2f} seconds)
        </div><br>
    """


# html로 tag box 렌더링
import urllib.parse
def tag_boxes(search: str, tags: list, active_tag: str) -> str:
    html = ''
    search = urllib.parse.quote(search)
    for tag in tags:
        if tag != active_tag:
            html += f"""
            <a id="tags" href="?search={search}&tags={tag}">
                {tag.replace('-', ' ')}
            </a>
            """
        else:
            html += f"""
            <a id="active-tag" href="?search={search}">
                {tag.replace('-', ' ')}
            </a>
            """

    html += '<br><br>'
    return html



#---- page_home.py

@app.addapp(is_home=True, title='Cookpang', icon="🏠")
def home():
    # head
    user = 'guest'
    row_num, col_num = 4, 5
    max_content = row_num * col_num
    img_size = 250
    
    recipe_df = pd.read_csv('./static/dataset/레시피_메타정보_raw.csv')
    
    # body
    st.markdown(f'#### {user}님을 위한 추천 레시피')
    content = random.sample(range(recipe_df.shape[0]),max_content)
    
    for row in range(row_num):
        cols = st.columns(col_num)
        
        for col, rand in enumerate(content[row * col_num:row * col_num + col_num]):
            data = recipe_df.values[rand]
            cols[col].markdown(f'<img src="{data[2]}" width="{img_size}" height="{img_size}"/>',unsafe_allow_html=True)
            cols[col].write(f'~{data[4]}~')
        

@app.addapp(title='키워드로 레시피 찾기', icon="🔍")
def keyword_search():
    # head
    recipe_df = pd.read_csv('./static/dataset/레시피_메타정보_raw.csv')
    
    # body
    search_keyword = st.text_input("키워드로 레시피 검색", placeholder = "키워드 입력")

    
    
#---- ingredient_search.py

@app.addapp(title='재료로 레시피 찾기', icon="🍲")
def ingredient_search():
    # head
    ingre_df= pd.read_csv('./static/dataset/재료_메타정보_1.0.csv')
    ingre_name_list = ingre_df['재료_이름'].tolist()

    # body
    search_ingre = st.multiselect('원하는 재료를 입력하세요', ingre_name_list)
    
    st.write(tag_boxes(search, ingre_name_list, st.session_state.tags),unsafe_allow_html=True)
    
    st.write(len(search_ingre), "가지를 선택했습니다.")
    #age = st.slider('재료 필터링은?', 0, 0 if not len(search_ingre) else len(search_ingre), 0)
    #st.write("최종 재료 필터링은", age, '개 입니다.')

#---- dashboard.py

@app.addapp(title='사용자 대시보드', icon="📊")
def dashboard():
    print(st.session_state.mainHydralitMenuComplex)
    pass


#---- login.py
@app.addapp(title='login', icon="🔑")
def login():
    pass


app.run()
    
#main()
# TODO : 메인페이지 검색창 설정
# TODO : 메인페이지 검색에 따른 이미지 설정
# TODO : 
# TODO : 
# TODO : 
# TODO : 
