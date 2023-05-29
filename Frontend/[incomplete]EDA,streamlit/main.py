import streamlit as st
import hydralit as hy
import contents

if __name__ == '__main__':
    
    # 호스트 및 기본 옵션
    app = hy.HydraApp(
        title='Cookpang : 요리 정보 및 개인 성향 기반 레시피 추천 서비스',
        favicon='👨‍🍳',
        layout = 'wide',
        hide_streamlit_markers = True, # 햄버거 버튼과 워터마크 숨기기
                  
        use_navbar=True, # 네비 사용여부
        allow_url_nav=True, # 네비 간 url 사용 여부
        nav_container=None, # 네비 컨테이너
        navbar_sticky=True, # 네비 상단 고정
        navbar_animation=True, # 전환 애니메이션

                  
        banner_spacing =[1,5], # 배너 간 간격 설정
        use_banner_images=['./static/img/cookpang_logo.png',
                           {'header':"<h2 style='text-align:left;padding: 30px 0px;color:black;font-size:100%;'>RecSys 08 : 요리 정보 및 개인 성향 기반 레시피 추천 서비스</h2>"}],
    )
    
    # 비로그인은 손님 권한 부여
    app.enable_guest_access()

    # 비로그인과 로그인 회원 구분을 위한 접근 수준 체크
    user_access_level, username = app.check_access()
    
    
    query_params = st.experimental_get_query_params()
    if 'contents' in query_params:
        app.session_state.contents = query_params['contents'][0]

    # app 설정
    app.add_app("메인 페이지", icon="🏠", app=contents.HomeTab(username=username, title='home'))
    app.add_app("키워드로 레시피 찾기", icon="🔍", app=contents.KeywordTab(title="keyword"))
    app.add_app("재료로 레시피 찾기",icon="🍲", app=contents.IngredientTab(title="ingredient"))
    app.add_app("사용자 대시보드",icon="📊", app=contents.DashboardTab(title="dashboard"))
    app.add_app("로그인", icon="🔑", app=contents.LoginTab(title="login"), is_login=True)


    # 0 : enable_guest_access 꺼짐
    # 1 : 비로그인 상태
    # 2 : 로그인 상태
    #if user_access_level > 1:

    # https://discuss.streamlit.io/t/new-release-hydralit-multi-page-apps-even-nicer/16588/2
    
    
    # ----------USE QUERY PARAMETER NAVIGATION----------------------------------------
    # If we want to use query parameters to control the navigation, 
    # for example we could bookmark a specific app and jump straight to it.
    # --------------------------------------------------------------------------------

    
    
    
    app.run()
