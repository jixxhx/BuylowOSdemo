# -*- coding: utf-8 -*-
"""
BuyLow OS - 메인 엔트리 포인트
"""
import streamlit as st
from datetime import datetime
import time
import streamlit.components.v1 as components

# ============================================================
# 1. 페이지 설정 (반드시 첫 번째)
# ============================================================
st.set_page_config(
    page_title="BuyLow OS",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# 2. 🚨 핵심: UI 부트스트랩 (즉시 CSS 주입)
# ============================================================
from ui.theme import bootstrap_ui, render_sidebar, render_logo, COLORS
bootstrap_ui()

# ============================================================
# 3. 세션 상태 초기화
# ============================================================
if 'route' not in st.session_state:
    st.session_state.route = "home"

if 'intro_shown' not in st.session_state:
    st.session_state.intro_shown = False


# ============================================================
# 4. 오프닝 스플래시 (첫 방문 시에만)
# ============================================================
def show_opening_splash():
    """미래지향적 오프닝 스플래시를 표시합니다."""
    
    # 오프닝 동안 사이드바 숨김
    st.markdown(
        """
        <style>
            [data-testid="stSidebar"],
            [data-testid="collapsedControl"],
            [data-testid="stSidebarNav"] {
                display: none !important;
                visibility: hidden !important;
            }
            html, body {
                overflow: hidden !important;
            }
            .stApp, [data-testid="stAppViewContainer"] {
                overflow: hidden !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
    
    # 오프닝 HTML - 완전한 중앙 정렬 + 가로 프로그레스 바
    opening_html = """
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="UTF-8">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        html, body {
            width: 100%;
            height: 100%;
            overflow: hidden;
            background: #0a0a10;
        }
        
        /* 메인 컨테이너 - 완전한 중앙 정렬 */
        .splash-container {
            width: 100%;
            height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            background: #0a0a10;
            position: relative;
            overflow: hidden;
        }
        
        /* 배경 글로우 */
        .glow {
            position: absolute;
            border-radius: 50%;
            filter: blur(100px);
            pointer-events: none;
        }
        
        .glow-1 {
            width: 500px;
            height: 500px;
            background: rgba(99, 102, 241, 0.12);
            top: -150px;
            left: 50%;
            transform: translateX(-50%);
            animation: glowPulse 3s ease-in-out infinite;
        }
        
        .glow-2 {
            width: 400px;
            height: 400px;
            background: rgba(139, 92, 246, 0.08);
            bottom: -100px;
            right: 10%;
            animation: glowPulse 3s ease-in-out 1s infinite;
        }
        
        @keyframes glowPulse {
            0%, 100% { opacity: 0.5; }
            50% { opacity: 0.8; }
        }
        
        /* 파티클 */
        .particles {
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            pointer-events: none;
        }
        
        .particle {
            position: absolute;
            width: 2px;
            height: 2px;
            background: rgba(148, 163, 184, 0.4);
            border-radius: 50%;
            animation: floatParticle 5s ease-in-out infinite;
        }
        
        .particle:nth-child(1) { left: 12%; top: 20%; animation-delay: 0s; }
        .particle:nth-child(2) { left: 28%; top: 70%; animation-delay: 0.5s; }
        .particle:nth-child(3) { left: 45%; top: 30%; animation-delay: 1s; }
        .particle:nth-child(4) { left: 60%; top: 80%; animation-delay: 0.3s; }
        .particle:nth-child(5) { left: 75%; top: 25%; animation-delay: 0.8s; }
        .particle:nth-child(6) { left: 88%; top: 55%; animation-delay: 1.2s; }
        
        @keyframes floatParticle {
            0%, 100% { transform: translateY(0); opacity: 0.3; }
            50% { transform: translateY(-15px); opacity: 0.6; }
        }
        
        /* 중앙 콘텐츠 래퍼 */
        .content-wrapper {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            z-index: 10;
            opacity: 0;
            animation: contentFadeIn 0.6s ease-out 0.1s forwards;
        }
        
        @keyframes contentFadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        /* 로고 박스 */
        .logo-box {
            padding: 22px 42px;
            background: linear-gradient(180deg, #0a0a12 0%, #0d0d16 100%);
            border: 2px solid #3d4556;
            border-radius: 3px;
            text-align: center;
            position: relative;
            box-shadow: 0 8px 30px rgba(0,0,0,0.4);
            animation: logoFloat 3s ease-in-out 0.5s infinite;
        }
        
        @keyframes logoFloat {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-5px); }
        }
        
        /* 로고 상단/하단 라인 장식 */
        .logo-box::before {
            content: '';
            position: absolute;
            top: -2px;
            left: 20%;
            right: 20%;
            height: 2px;
            background: linear-gradient(90deg, transparent, #4a5568, transparent);
        }
        
        .logo-box::after {
            content: '';
            position: absolute;
            bottom: -2px;
            left: 20%;
            right: 20%;
            height: 2px;
            background: linear-gradient(90deg, transparent, #4a5568, transparent);
        }
        
        /* BUYLOW 텍스트 */
        .logo-title {
            font-family: 'Times New Roman', Georgia, serif;
            font-size: 44px;
            font-weight: 400;
            letter-spacing: 4px;
            background: linear-gradient(180deg, #e5e7eb 0%, #9ca3af 50%, #6b7280 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        /* STRATEGY INC. 행 */
        .logo-subtitle-row {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            margin-top: 6px;
        }
        
        .logo-line {
            width: 1px;
            height: 14px;
            background: #4a5568;
        }
        
        .logo-subtitle {
            font-family: Arial, sans-serif;
            font-size: 12px;
            font-weight: 400;
            letter-spacing: 5px;
            color: #9ca3af;
        }
        
        /* Trading Team Platform - 정확한 중앙 정렬 */
        .tagline {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            font-size: 13px;
            font-weight: 300;
            color: #64748b;
            letter-spacing: 3px;
            text-transform: uppercase;
            margin-top: 24px;
            text-align: center;
            width: 100%;
            opacity: 0;
            animation: taglineFade 0.5s ease-out 0.3s forwards;
        }
        
        @keyframes taglineFade {
            from { opacity: 0; transform: translateY(8px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        /* 가로 프로그레스 바 컨테이너 */
        .progress-wrapper {
            margin-top: 28px;
            width: 200px;
            display: flex;
            flex-direction: column;
            align-items: center;
            opacity: 0;
            animation: progressFadeIn 0.4s ease-out 0.5s forwards;
        }
        
        @keyframes progressFadeIn {
            to { opacity: 1; }
        }
        
        /* 프로그레스 바 트랙 */
        .progress-track {
            width: 100%;
            height: 2px;
            background: rgba(75, 85, 99, 0.3);
            border-radius: 1px;
            overflow: hidden;
        }
        
        /* 프로그레스 바 필 */
        .progress-fill {
            height: 100%;
            width: 0%;
            background: linear-gradient(90deg, #4a5568, #6b7280);
            border-radius: 1px;
            animation: progressGrow 1.2s ease-out 0.6s forwards;
        }
        
        @keyframes progressGrow {
            from { width: 0%; }
            to { width: 100%; }
        }
        
        /* 전체 페이드 아웃 */
        .splash-container.fade-out {
            animation: splashFadeOut 0.3s ease-in-out 1.7s forwards;
        }
        
        @keyframes splashFadeOut {
            to { opacity: 0; }
        }
    </style>
    </head>
    <body>
        <div class="splash-container fade-out">
            <!-- 배경 글로우 -->
            <div class="glow glow-1"></div>
            <div class="glow glow-2"></div>
            
            <!-- 파티클 -->
            <div class="particles">
                <div class="particle"></div>
                <div class="particle"></div>
                <div class="particle"></div>
                <div class="particle"></div>
                <div class="particle"></div>
                <div class="particle"></div>
            </div>
            
            <!-- 중앙 콘텐츠 -->
            <div class="content-wrapper">
                <!-- 로고 박스 -->
                <div class="logo-box">
                    <div class="logo-title">BUYLOW</div>
                    <div class="logo-subtitle-row">
                        <div class="logo-line"></div>
                        <div class="logo-subtitle">STRATEGY INC.</div>
                        <div class="logo-line"></div>
                    </div>
                </div>
                
                <!-- 태그라인 -->
                <div class="tagline">Trading Team Platform</div>
                
                <!-- 가로 프로그레스 바 -->
                <div class="progress-wrapper">
                    <div class="progress-track">
                        <div class="progress-fill"></div>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    
    components.html(opening_html, height=600, scrolling=False)
    time.sleep(1.8)
    st.session_state.intro_shown = True
    st.rerun()


# ============================================================
# 5. 홈 페이지 렌더링
# ============================================================
def render_home_page():
    """홈 페이지를 렌더링합니다."""
    
    # 홈 전용 CSS
    st.markdown(f"""
    <style>
        @keyframes fadeInUp {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        .home-hero {{
            text-align: center;
            padding: 2rem 1rem 1.5rem;
            animation: fadeInUp 0.6s ease-out;
        }}
        
        .home-title {{
            font-family: 'Inter', 'Noto Sans KR', sans-serif;
            font-size: clamp(1.5rem, 3vw, 2rem);
            font-weight: 600;
            color: {COLORS['text_primary']};
            margin: 1.2rem 0 0.4rem;
        }}
        
        .home-subtitle {{
            font-family: 'Noto Sans KR', sans-serif;
            font-size: 0.95rem;
            color: {COLORS['text_secondary']};
        }}
        
        .feature-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 1.1rem;
            padding: 1rem 0;
        }}
        
        .feature-card {{
            background: {COLORS['bg_card']};
            border: 1px solid {COLORS['border']};
            border-radius: 14px;
            padding: 1.4rem;
            transition: all 0.25s ease;
            animation: fadeInUp 0.5s ease-out backwards;
        }}
        
        .feature-card:hover {{
            border-color: {COLORS['border_accent']};
            transform: translateY(-3px);
        }}
        
        .feature-icon {{ font-size: 1.8rem; margin-bottom: 0.8rem; }}
        
        .feature-title {{
            font-family: 'Noto Sans KR', sans-serif;
            font-size: 1.05rem;
            font-weight: 600;
            color: {COLORS['text_primary']};
            margin-bottom: 0.4rem;
        }}
        
        .feature-desc {{
            font-family: 'Noto Sans KR', sans-serif;
            font-size: 0.88rem;
            color: {COLORS['text_secondary']};
            line-height: 1.55;
        }}
        
        .disclaimer {{
            background: rgba(239, 68, 68, 0.06);
            border: 1px solid rgba(239, 68, 68, 0.12);
            border-radius: 10px;
            padding: 1rem 1.25rem;
            margin-top: 1.5rem;
        }}
        
        .disclaimer p {{
            font-family: 'Noto Sans KR', sans-serif;
            font-size: 0.82rem;
            color: {COLORS['text_muted']};
            margin: 0.2rem 0;
        }}
        
        .home-footer {{
            text-align: center;
            padding: 1.5rem;
            margin-top: 1.5rem;
            border-top: 1px solid {COLORS['border']};
        }}
        
        .home-footer p {{
            font-family: 'Noto Sans KR', sans-serif;
            font-size: 0.78rem;
            color: {COLORS['text_muted']};
        }}
        
        .block-container {{
            padding: 1rem 2rem;
            max-width: 1100px;
        }}
    </style>
    """, unsafe_allow_html=True)

    # 히어로 섹션 - 로고
    render_logo(size="large", animate=True)
    
    # 히어로 섹션 - 타이틀
    st.markdown("""
    <div style="text-align: center; padding: 0.5rem 0 1.5rem;">
        <h1 class="home-title">BuyLow OS</h1>
        <p class="home-subtitle">트레이딩 팀을 위한 운영 플랫폼</p>
    </div>
    """, unsafe_allow_html=True)

    # 기능 카드
    st.markdown(f"""
    <div class="feature-grid">
        <div class="feature-card" style="animation-delay: 0.1s;">
            <div class="feature-icon">💬</div>
            <h3 class="feature-title">CS 챗봇</h3>
            <p class="feature-desc">자주 묻는 질문을 키워드 기반으로 즉시 검색하고 답변을 확인하세요.</p>
        </div>
        <div class="feature-card" style="animation-delay: 0.15s;">
            <div class="feature-icon">🧭</div>
            <h3 class="feature-title">진단 퀴즈</h3>
            <p class="feature-desc">트레이딩 기초 지식을 점검하고 맞춤 학습 방향을 추천받으세요.</p>
        </div>
        <div class="feature-card" style="animation-delay: 0.2s;">
            <div class="feature-icon">📤</div>
            <h3 class="feature-title">과제 제출</h3>
            <p class="feature-desc">주제별 과제를 제출하고 추가 콘텐츠를 언락하세요.</p>
        </div>
        <div class="feature-card" style="animation-delay: 0.25s;">
            <div class="feature-icon">🛡️</div>
            <h3 class="feature-title">리스크 체크</h3>
            <p class="feature-desc">매매 전 위험 요소를 점검하고 규율을 지키세요.</p>
        </div>
        <div class="feature-card" style="animation-delay: 0.3s;">
            <div class="feature-icon">📢</div>
            <h3 class="feature-title">공지 허브</h3>
            <p class="feature-desc">모든 공지를 한 곳에서 태그별로 확인하세요.</p>
        </div>
        <div class="feature-card" style="animation-delay: 0.35s;">
            <div class="feature-icon">📊</div>
            <h3 class="feature-title">운영자 대시보드</h3>
            <p class="feature-desc">팀 현황을 한눈에 파악하고 운영 효율을 높이세요.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 바로가기
    st.markdown("---")
    st.markdown("### ⚡ 바로가기")
    
    cols = st.columns(4)
    with cols[0]:
        if st.button("💬 CS 챗봇", use_container_width=True, key="home_cs"):
            st.session_state.route = "cs_chat"
            st.rerun()
    with cols[1]:
        if st.button("📚 교육 콘텐츠", use_container_width=True, key="home_edu"):
            st.session_state.route = "content_library"
            st.rerun()
    with cols[2]:
        if st.button("📤 과제 제출", use_container_width=True, key="home_hw"):
            st.session_state.route = "homework"
            st.rerun()
    with cols[3]:
        if st.button("🛡️ 리스크 체크", use_container_width=True, key="home_risk"):
            st.session_state.route = "risk_check"
            st.rerun()

    # 면책 조항
    st.markdown("""
    <div class="disclaimer">
        <p><strong>⚠️ 중요 안내</strong></p>
        <p>본 플랫폼은 교육 및 팀 운영 목적으로 설계되었습니다.</p>
        <p>매매 추천, 가격 예측, 종목 추천 기능이 없으며, 투자 권유가 아닙니다.</p>
        <p>모든 투자 결정은 본인 책임이며, 본 플랫폼은 어떠한 투자 손실에도 책임지지 않습니다.</p>
    </div>
    """, unsafe_allow_html=True)

    # 푸터
    st.markdown(f"""
    <div class="home-footer">
        <p>BuyLow OS • Trading Team Platform</p>
        <p>© {datetime.now().year} • 교육 및 정보 제공 목적 • LLM API 미사용</p>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# 6. 메인 실행 로직
# ============================================================

# 오프닝 표시 (첫 방문 시에만)
if not st.session_state.intro_shown:
    show_opening_splash()
else:
    # 사이드바 렌더링
    render_sidebar()
    
    # 라우팅 처리
    current_route = st.session_state.get('route', 'home')
    
    if current_route == "home":
        render_home_page()
    else:
        from app_pages import ROUTES
        page_module = ROUTES.get(current_route)
        if page_module and hasattr(page_module, 'render'):
            page_module.render()
        else:
            st.error(f"페이지를 찾을 수 없습니다: {current_route}")
            if st.button("홈으로 돌아가기"):
                st.session_state.route = "home"
                st.rerun()
