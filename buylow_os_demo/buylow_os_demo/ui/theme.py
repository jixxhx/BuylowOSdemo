# -*- coding: utf-8 -*-
"""
BuyLow OS - 통합 테마 및 UI 부트스트랩

모든 페이지에서 가장 먼저 호출해야 합니다.
전역 CSS 주입, 기본 네비게이션 숨김, 로고 렌더링을 담당합니다.
"""
import streamlit as st
import base64
from pathlib import Path


# ============================================================
# 테마 색상 (전역 통일)
# ============================================================
COLORS = {
    "bg_primary": "#0a0a10",
    "bg_secondary": "#0d0d14",
    "bg_card": "#111118",
    "bg_sidebar": "#0a0e17",
    "border": "#2d3748",
    "border_accent": "#4a5568",
    "text_primary": "#f1f5f9",
    "text_secondary": "#94a3b8",
    "text_muted": "#64748b",
    "accent": "#6366f1",
    "logo_silver": "#9ca3af",
    "logo_border": "#3d4556",
}


def inject_critical_css():
    """
    🚨 핵심: 기본 Streamlit 요소를 즉시 숨기는 CSS + 다크 모드 강제
    st.set_page_config() 직후에 호출해야 합니다.
    """
    st.markdown(
        f"""
        <style>
            /* ========================================
               0. 🚨 사이드바 토글 버튼 항상 표시 (최우선)
               ======================================== */
            [data-testid="collapsedControl"] {{
                display:flex !important;
                visibility:visible !important;
                opacity:1 !important;
                pointer-events:auto !important;
                position:fixed !important;
                top:10px !important;
                left:10px !important;
                z-index:999999 !important;
            }}
            [data-testid="stSidebar"] {{
                z-index:999998 !important;
            }}
            
            /* ========================================
               1. 다크 모드 강제 (라이트 모드 방지)
               ======================================== */
            html, body {{
                color-scheme: dark !important;
                background-color: {COLORS['bg_primary']} !important;
            }}
            
            /* ========================================
               2. 기본 네비게이션 완전 숨김 (토글 버튼 제외)
               ======================================== */
            [data-testid="stSidebarNav"],
            [data-testid="stSidebarNav"] *,
            [data-testid="stSidebarNavItems"],
            [data-testid="stSidebarNavLink"],
            [data-testid="stSidebarNavSeparator"],
            nav[data-testid="stSidebarNav"],
            section[data-testid="stSidebarNav"],
            .st-emotion-cache-1cypcdb,
            .st-emotion-cache-16idsys {{
                display: none !important;
                visibility: hidden !important;
                height: 0 !important;
                width: 0 !important;
                overflow: hidden !important;
                position: absolute !important;
                pointer-events: none !important;
                opacity: 0 !important;
            }}
            
            /* ========================================
               3. 기본 헤더/푸터/메뉴 숨김
               ======================================== */
            #MainMenu, 
            footer, 
            .stDeployButton {{
                display: none !important;
                visibility: hidden !important;
            }}
            
            /* 헤더는 숨기지 않고 투명 처리 (토글 버튼 보호) */
            [data-testid="stHeader"] {{
                background: transparent !important;
                box-shadow: none !important;
                border-bottom: none !important;
            }}
            
            /* ========================================
               4. 사이드바 스타일링
               ======================================== */
            [data-testid="stSidebar"] {{
                background: linear-gradient(180deg, {COLORS['bg_sidebar']} 0%, #0f1724 100%) !important;
            }}
            
            /* 사이드바 왼쪽 고정 및 패딩 통일 */
            [data-testid="stSidebar"] > div:first-child {{
                padding-top: 0 !important;
                padding-left: 0 !important;
                padding-right: 0 !important;
            }}
            
            [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {{
                padding: 0 !important;
                gap: 0 !important;
            }}
            
            /* ========================================
               5. 전역 배경 및 폰트
               ======================================== */
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Noto+Sans+KR:wght@300;400;500;600;700&display=swap');
            
            .stApp {{
                background: {COLORS['bg_primary']} !important;
                background-image: 
                    radial-gradient(ellipse 80% 50% at 50% -20%, rgba(99,102,241,0.06), transparent),
                    radial-gradient(ellipse 60% 40% at 80% 100%, rgba(139,92,246,0.04), transparent) !important;
            }}
            
            /* ========================================
               6. 모든 위젯 다크 모드 강제 + 가독성 강화
               ======================================== */
            
            /* ----- 6.1 Placeholder 가독성 (밝게) ----- */
            ::placeholder {{
                color: rgba(220, 230, 245, 0.7) !important;
                opacity: 1 !important;
            }}
            
            input::placeholder,
            textarea::placeholder {{
                color: rgba(220, 230, 245, 0.7) !important;
                opacity: 1 !important;
            }}
            
            [data-baseweb="input"] input::placeholder,
            [data-baseweb="textarea"] textarea::placeholder {{
                color: rgba(220, 230, 245, 0.7) !important;
                opacity: 1 !important;
            }}
            
            /* Chat input placeholder */
            [data-testid="stChatInput"] textarea::placeholder {{
                color: rgba(220, 230, 245, 0.7) !important;
                opacity: 1 !important;
            }}
            
            /* ----- 6.2 입력 텍스트 색 (거의 흰색) ----- */
            .stTextInput > div > div > input,
            .stTextArea > div > div > textarea,
            .stNumberInput > div > div > input,
            [data-testid="stChatInput"] textarea,
            input[type="text"],
            input[type="number"],
            input[type="email"],
            input[type="password"],
            input[type="date"],
            textarea {{
                background-color: {COLORS['bg_card']} !important;
                color: #ebeff5 !important;
                border: 1px solid {COLORS['border']} !important;
                border-radius: 8px !important;
                caret-color: #ebeff5 !important;
            }}
            
            /* 셀렉트박스 선택된 값 */
            [data-baseweb="select"] span,
            .stSelectbox > div > div > div {{
                color: #ebeff5 !important;
            }}
            
            /* 멀티셀렉트 태그 텍스트 */
            [data-baseweb="tag"] span {{
                color: #ebeff5 !important;
            }}
            
            /* ----- 6.3 포커스 상태 (선명하게) ----- */
            .stTextInput > div > div > input:focus,
            .stTextArea > div > div > textarea:focus,
            .stNumberInput > div > div > input:focus,
            [data-testid="stChatInput"] textarea:focus,
            input:focus,
            textarea:focus {{
                border-color: {COLORS['accent']} !important;
                box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.3) !important;
                outline: none !important;
                color: #ffffff !important;
            }}
            
            [data-baseweb="select"]:focus-within {{
                border-color: {COLORS['accent']} !important;
                box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.3) !important;
            }}
            
            /* ----- 6.4 라벨 및 설명 텍스트 가독성 ----- */
            /* 위젯 라벨 */
            .stTextInput label,
            .stTextArea label,
            .stSelectbox label,
            .stMultiSelect label,
            .stSlider label,
            .stCheckbox label,
            .stRadio label,
            .stNumberInput label,
            .stDateInput label,
            .stFileUploader label,
            [data-testid="stWidgetLabel"] {{
                color: #c8d1dc !important;
                font-weight: 500 !important;
            }}
            
            /* 본문 텍스트 */
            .stApp p,
            .stMarkdown p {{
                color: #d0d8e4 !important;
            }}
            
            /* 캡션 (st.caption) */
            .stCaption,
            [data-testid="stCaption"],
            small {{
                color: #9aa8b8 !important;
            }}
            
            /* 도움말 텍스트 */
            .stHelp,
            [data-testid="stMarkdownContainer"] small {{
                color: #8b99a8 !important;
            }}
            
            /* 링크 */
            a {{
                color: #818cf8 !important;
            }}
            
            a:hover {{
                color: #a5b4fc !important;
            }}
            
            /* 제목 */
            h1, h2, h3, h4, h5, h6,
            .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {{
                color: #f1f5f9 !important;
            }}
            
            /* 경고, 정보 박스 텍스트 */
            .stAlert p,
            [data-testid="stAlert"] p {{
                color: #e2e8f0 !important;
            }}
            
            /* ----- 6.5 셀렉트 박스 ----- */
            .stSelectbox > div > div,
            .stMultiSelect > div > div,
            [data-baseweb="select"] > div {{
                background-color: {COLORS['bg_card']} !important;
                border-color: {COLORS['border']} !important;
            }}
            
            [data-baseweb="select"] {{
                background-color: {COLORS['bg_card']} !important;
            }}
            
            /* 드롭다운 메뉴 */
            [data-baseweb="popover"] > div,
            [data-baseweb="menu"] {{
                background-color: {COLORS['bg_secondary']} !important;
                border: 1px solid {COLORS['border']} !important;
            }}
            
            [data-baseweb="menu"] li {{
                background-color: {COLORS['bg_secondary']} !important;
                color: #d0d8e4 !important;
            }}
            
            [data-baseweb="menu"] li:hover {{
                background-color: {COLORS['bg_card']} !important;
                color: #ffffff !important;
            }}
            
            /* ----- 6.6 버튼 ----- */
            .stButton > button {{
                background-color: {COLORS['bg_card']} !important;
                color: #ebeff5 !important;
                border: 1px solid {COLORS['border']} !important;
                font-weight: 500 !important;
            }}
            
            .stButton > button:hover {{
                border-color: {COLORS['accent']} !important;
                background-color: rgba(99, 102, 241, 0.15) !important;
                color: #ffffff !important;
            }}
            
            .stButton > button:active {{
                background-color: rgba(99, 102, 241, 0.25) !important;
            }}
            
            /* Primary 버튼 */
            .stButton > button[kind="primary"] {{
                background-color: {COLORS['accent']} !important;
                color: #ffffff !important;
                border: none !important;
            }}
            
            /* ----- 6.7 파일 업로더 ----- */
            [data-testid="stFileUploader"],
            [data-testid="stFileUploader"] > div {{
                background-color: {COLORS['bg_card']} !important;
                border-color: {COLORS['border']} !important;
            }}
            
            [data-testid="stFileUploader"] section {{
                background-color: {COLORS['bg_card']} !important;
                color: #c8d1dc !important;
            }}
            
            [data-testid="stFileUploader"] button {{
                color: #ebeff5 !important;
            }}
            
            /* ----- 6.8 Expander ----- */
            .streamlit-expanderHeader {{
                background-color: {COLORS['bg_card']} !important;
                color: #ebeff5 !important;
                border: 1px solid {COLORS['border']} !important;
            }}
            
            .streamlit-expanderContent {{
                background-color: {COLORS['bg_secondary']} !important;
                border: 1px solid {COLORS['border']} !important;
                border-top: none !important;
                color: #d0d8e4 !important;
            }}
            
            /* ----- 6.9 코드 블록 ----- */
            .stCodeBlock,
            code,
            pre {{
                background-color: {COLORS['bg_card']} !important;
                color: #e2e8f0 !important;
            }}
            
            /* 인라인 코드 */
            code:not(pre code) {{
                background-color: rgba(99, 102, 241, 0.15) !important;
                color: #c4b5fd !important;
                padding: 2px 6px !important;
                border-radius: 4px !important;
            }}
            
            /* ----- 6.10 슬라이더 ----- */
            .stSlider > div > div > div {{
                background-color: {COLORS['border']} !important;
            }}
            
            .stSlider [data-testid="stTickBarMin"],
            .stSlider [data-testid="stTickBarMax"] {{
                color: #9aa8b8 !important;
            }}
            
            /* ----- 6.11 체크박스, 라디오 ----- */
            .stCheckbox > label,
            .stRadio > label {{
                color: #d0d8e4 !important;
            }}
            
            .stCheckbox > label:hover,
            .stRadio > label:hover {{
                color: #ebeff5 !important;
            }}
            
            /* ----- 6.12 데이터프레임, 테이블 ----- */
            .stDataFrame,
            [data-testid="stTable"] {{
                background-color: {COLORS['bg_card']} !important;
            }}
            
            .stDataFrame th,
            [data-testid="stTable"] th {{
                color: #c8d1dc !important;
                background-color: {COLORS['bg_secondary']} !important;
            }}
            
            .stDataFrame td,
            [data-testid="stTable"] td {{
                color: #d0d8e4 !important;
            }}
            
            /* ----- 6.13 Chat Input ----- */
            [data-testid="stChatInput"] {{
                background-color: {COLORS['bg_card']} !important;
                border: 1px solid {COLORS['border']} !important;
                border-radius: 12px !important;
            }}
            
            [data-testid="stChatInput"] textarea {{
                background-color: transparent !important;
                color: #ebeff5 !important;
            }}
            
            /* Chat 메시지 */
            [data-testid="stChatMessage"] {{
                background-color: {COLORS['bg_card']} !important;
                color: #d0d8e4 !important;
            }}
            
            /* ----- 6.14 Metric ----- */
            [data-testid="stMetric"] label {{
                color: #9aa8b8 !important;
            }}
            
            [data-testid="stMetric"] [data-testid="stMetricValue"] {{
                color: #ebeff5 !important;
            }}
            
            [data-testid="stMetric"] [data-testid="stMetricDelta"] {{
                color: #4ade80 !important;
            }}
            
            /* ----- 6.15 탭 ----- */
            .stTabs [data-baseweb="tab-list"] {{
                background-color: transparent !important;
            }}
            
            .stTabs [data-baseweb="tab"] {{
                color: #9aa8b8 !important;
            }}
            
            .stTabs [data-baseweb="tab"][aria-selected="true"] {{
                color: #ebeff5 !important;
            }}
            
            /* 날짜 선택기 */
            [data-baseweb="calendar"] {{
                background-color: {COLORS['bg_secondary']} !important;
            }}
            
            /* 모든 라벨 */
            .stTextInput label,
            .stTextArea label,
            .stSelectbox label,
            .stMultiSelect label,
            .stSlider label,
            .stCheckbox label,
            .stRadio label,
            [data-testid="stWidgetLabel"] {{
                color: {COLORS['text_secondary']} !important;
            }}
            
            /* iframe 배경 투명 (로고용) */
            iframe {{
                background: transparent !important;
            }}
            
            [data-testid="stIFrame"] {{
                background: transparent !important;
            }}
            
            /* ========================================
               7. 페이지 전환 애니메이션
               ======================================== */
            @keyframes contentFadeIn {{
                from {{ opacity: 0; transform: translateY(10px); }}
                to {{ opacity: 1; transform: translateY(0); }}
            }}
            
            [data-testid="stAppViewContainer"] > section > div {{
                animation: contentFadeIn 0.35s ease-out;
            }}
            
            /* ========================================
               8. 로고 플로팅 애니메이션
               ======================================== */
            @keyframes logoFloat {{
                0%, 100% {{ transform: translateY(0); }}
                50% {{ transform: translateY(-5px); }}
            }}
            
            .buylow-logo-float {{
                animation: logoFloat 4s ease-in-out infinite;
            }}
            
            .buylow-logo-float-subtle {{
                animation: logoFloat 5s ease-in-out infinite;
            }}
            
            /* ========================================
               9. 통일된 테두리 스타일
               ======================================== */
            :root {{
                color-scheme: dark !important;
                --border-color: {COLORS['border']};
                --border-accent: {COLORS['border_accent']};
                --bg-card: {COLORS['bg_card']};
                --text-primary: {COLORS['text_primary']};
                --text-secondary: {COLORS['text_secondary']};
                --text-muted: {COLORS['text_muted']};
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_logo(size: str = "large", animate: bool = True) -> None:
    """
    BuyLow 로고를 렌더링합니다.
    
    Args:
        size: "large" (홈), "medium" (오프닝), "small" (사이드바)
        animate: 플로팅 애니메이션 적용 여부
    """
    if size == "large":
        box_padding = "24px 40px"
        title_size = "46px"
        subtitle_size = "13px"
        letter_spacing = "3px"
        sub_letter_spacing = "4px"
        line_height = "18px"
        container_height = 140
    elif size == "medium":
        box_padding = "20px 36px"
        title_size = "40px"
        subtitle_size = "12px"
        letter_spacing = "3px"
        sub_letter_spacing = "4px"
        line_height = "16px"
        container_height = 120
    else:  # small
        box_padding = "12px 20px"
        title_size = "22px"
        subtitle_size = "8px"
        letter_spacing = "1.5px"
        sub_letter_spacing = "2.5px"
        line_height = "12px"
        container_height = 80
    
    anim_css = ""
    if animate:
        anim_css = """
        @keyframes logoFloat {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-5px); }
        }
        .logo-box { animation: logoFloat 4s ease-in-out infinite; }
        """
    
    logo_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="UTF-8">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        html {{ background: {COLORS['bg_primary']}; }}
        body {{ background: {COLORS['bg_primary']}; }}
        .logo-container {{
            display: flex;
            justify-content: center;
            align-items: center;
            width: 100%;
            height: 100%;
            background: {COLORS['bg_primary']};
        }}
        .logo-box {{
            padding: {box_padding};
            background: linear-gradient(180deg, #0a0a12 0%, #0c0c16 100%);
            border: 2px solid {COLORS['logo_border']};
            border-radius: 3px;
            text-align: center;
            position: relative;
            box-shadow: 0 4px 20px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.03);
        }}
        .logo-line-top {{
            position: absolute;
            top: -2px;
            left: 30%;
            right: 30%;
            height: 2px;
            background: linear-gradient(90deg, transparent, {COLORS['border_accent']}, transparent);
        }}
        .logo-line-bottom {{
            position: absolute;
            bottom: -2px;
            left: 30%;
            right: 30%;
            height: 2px;
            background: linear-gradient(90deg, transparent, {COLORS['border_accent']}, transparent);
        }}
        .logo-title {{
            font-family: 'Times New Roman', Georgia, serif;
            font-size: {title_size};
            font-weight: 400;
            letter-spacing: {letter_spacing};
            background: linear-gradient(180deg, #d4d8e0 0%, #9ca3af 40%, #6b7280 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            line-height: 1.1;
        }}
        .logo-subtitle-row {{
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            margin-top: 6px;
        }}
        .logo-vline {{
            width: 1px;
            height: {line_height};
            background: {COLORS['border_accent']};
        }}
        .logo-subtitle {{
            font-family: Arial, sans-serif;
            font-size: {subtitle_size};
            font-weight: 400;
            letter-spacing: {sub_letter_spacing};
            color: {COLORS['logo_silver']};
        }}
        {anim_css}
    </style>
    </head>
    <body>
        <div class="logo-container">
            <div class="logo-box">
                <div class="logo-line-top"></div>
                <div class="logo-title">BUYLOW</div>
                <div class="logo-subtitle-row">
                    <div class="logo-vline"></div>
                    <div class="logo-subtitle">STRATEGY INC.</div>
                    <div class="logo-vline"></div>
                </div>
                <div class="logo-line-bottom"></div>
            </div>
        </div>
    </body>
    </html>
    """
    
    import streamlit.components.v1 as components
    components.html(logo_html, height=container_height, scrolling=False)


def render_sidebar_logo() -> None:
    """
    사이드바 전용 로고를 렌더링합니다.
    """
    logo_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="UTF-8">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500&display=swap');
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        html {{ background: {COLORS['bg_sidebar']}; }}
        body {{ background: {COLORS['bg_sidebar']}; }}
        @keyframes logoFloatSubtle {{
            0%, 100% {{ transform: translateY(0); }}
            50% {{ transform: translateY(-3px); }}
        }}
        .sidebar-logo-wrapper {{
            text-align: center;
            padding: 16px 12px 14px;
            border-bottom: 1px solid rgba(61, 69, 86, 0.3);
            background: {COLORS['bg_sidebar']};
        }}
        .sidebar-logo-box {{
            display: inline-block;
            padding: 10px 18px;
            background: linear-gradient(180deg, #0a0a12 0%, #0c0c16 100%);
            border: 1px solid {COLORS['logo_border']};
            border-radius: 3px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.3);
            animation: logoFloatSubtle 5s ease-in-out infinite;
        }}
        .sidebar-logo-title {{
            font-family: 'Times New Roman', Georgia, serif;
            font-size: 20px;
            font-weight: 400;
            letter-spacing: 1.5px;
            background: linear-gradient(180deg, #d4d8e0 0%, #9ca3af 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        .sidebar-logo-subtitle {{
            font-family: Arial, sans-serif;
            font-size: 7px;
            font-weight: 400;
            letter-spacing: 2px;
            color: {COLORS['logo_silver']};
            margin-top: 2px;
        }}
        .sidebar-tagline {{
            font-family: 'Noto Sans KR', sans-serif;
            font-size: 10px;
            color: {COLORS['text_muted']};
            margin-top: 10px;
            letter-spacing: 0.5px;
        }}
    </style>
    </head>
    <body>
        <div class="sidebar-logo-wrapper">
            <div class="sidebar-logo-box">
                <div class="sidebar-logo-title">BUYLOW</div>
                <div class="sidebar-logo-subtitle">STRATEGY INC.</div>
            </div>
            <div class="sidebar-tagline">Trading Team Platform</div>
        </div>
    </body>
    </html>
    """
    
    import streamlit.components.v1 as components
    with st.sidebar:
        components.html(logo_html, height=110, scrolling=False)


def render_sidebar_menu() -> None:
    """
    사이드바 메뉴를 렌더링합니다.
    """
    # 메뉴 스타일
    st.sidebar.markdown(
        f"""
        <style>
            /* 메뉴 섹션 라벨 */
            .sidebar-section {{
                color: {COLORS['text_muted']};
                font-family: 'Noto Sans KR', sans-serif;
                font-size: 10px;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.8px;
                padding: 14px 16px 6px;
                margin-top: 4px;
            }}
            
            /* 메뉴 버튼 스타일 */
            [data-testid="stSidebar"] .stButton > button {{
                width: 100%;
                background: transparent !important;
                border: none !important;
                color: {COLORS['text_secondary']} !important;
                padding: 10px 16px !important;
                border-radius: 8px !important;
                font-family: 'Noto Sans KR', sans-serif !important;
                font-size: 13px !important;
                font-weight: 500 !important;
                text-align: left !important;
                justify-content: flex-start !important;
                transition: all 0.2s ease !important;
                margin: 1px 8px !important;
            }}
            
            [data-testid="stSidebar"] .stButton > button:hover {{
                background: rgba(99, 102, 241, 0.08) !important;
                color: {COLORS['text_primary']} !important;
                transform: translateX(3px);
            }}
            
            [data-testid="stSidebar"] .stButton > button:active {{
                background: rgba(99, 102, 241, 0.12) !important;
            }}
            
            [data-testid="stSidebar"] .stButton > button:focus {{
                box-shadow: none !important;
                outline: none !important;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )
    
    # 메뉴 정의
    menu_structure = [
        ("section", "메인"),
        ("🏠", "홈", "home"),
        ("💬", "CS 챗봇", "cs_chat"),
        
        ("section", "교육"),
        ("🧭", "진단 퀴즈", "quiz"),
        ("📤", "과제 제출", "homework"),
        ("🔓", "언락 해설", "unlocked_lessons"),
        ("🎯", "심화 연습", "advanced_practice"),
        
        ("section", "리스크"),
        ("🛡️", "리스크 체크", "risk_check"),
        
        ("section", "정보"),
        ("📢", "공지 허브", "announcements"),
        ("📚", "교육 콘텐츠", "content_library"),
        ("🚀", "온보딩", "onboarding"),
        
        ("section", "운영자"),
        ("⚙️", "관리자", "admin"),
        ("📊", "대시보드", "operator_dashboard"),
        ("✏️", "과제 채점", "grading_assistant"),
    ]
    
    # 메뉴 렌더링
    for item in menu_structure:
        if item[0] == "section":
            st.sidebar.markdown(
                f'<div class="sidebar-section">{item[1]}</div>',
                unsafe_allow_html=True
            )
        else:
            icon, label, route = item
            if st.sidebar.button(f"{icon}  {label}", key=f"nav_{route}", use_container_width=True):
                st.session_state.route = route
                st.rerun()


def bootstrap_ui() -> None:
    """
    UI 부트스트랩 - 모든 페이지에서 가장 먼저 호출합니다.
    """
    inject_critical_css()


def render_sidebar() -> None:
    """
    완전한 사이드바를 렌더링합니다.
    """
    render_sidebar_logo()
    render_sidebar_menu()
