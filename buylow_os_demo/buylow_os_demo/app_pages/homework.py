import streamlit as st
from datetime import datetime

# 안전한 데이터 접근을 위한 유틸리티
from utils.data_utils import load_json, save_json, get_next_id


def render():
    """과제 제출 페이지 렌더링"""
    
    # CSS
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Space+Mono:wght@400;700&family=Noto+Sans+KR:wght@300;400;500;600;700&display=swap');
        
        :root {
            --bg-dark: #0f0f14;
            --bg-card: #18181f;
            --border: rgba(255,255,255,0.08);
            --text-primary: #ffffff;
            --text-secondary: rgba(255,255,255,0.6);
            --text-muted: rgba(255,255,255,0.4);
            --accent-primary: #6366f1;
            --success: #22c55e;
            --warning: #f59e0b;
            --danger: #ef4444;
        }
        
        @keyframes fadeInUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
        
        .page-header { padding: 2rem 0; animation: fadeInUp 0.6s ease-out; }
        .page-title { font-family: 'Outfit', sans-serif; font-size: clamp(1.75rem, 4vw, 2.5rem); font-weight: 800; color: var(--text-primary); margin: 0; }
        .page-subtitle { font-family: 'Noto Sans KR', sans-serif; font-size: 1rem; color: var(--text-secondary); margin-top: 0.25rem; }
        
        .unlock-preview { background: linear-gradient(135deg, rgba(34,197,94,0.1), rgba(34,197,94,0.05)); border: 1px solid rgba(34,197,94,0.3); border-radius: 12px; padding: 1rem; margin: 1rem 0; }
        .unlock-title { font-family: 'Outfit', sans-serif; font-size: 0.9rem; font-weight: 600; color: var(--success); margin-bottom: 0.5rem; }
        .unlock-item { font-family: 'Noto Sans KR', sans-serif; font-size: 0.85rem; color: var(--text-secondary); padding: 0.25rem 0; }
        
        .hint-box { background: rgba(99,102,241,0.1); border: 1px solid rgba(99,102,241,0.3); border-radius: 8px; padding: 1rem; margin: 0.75rem 0; }
        .hint-title { font-family: 'Outfit', sans-serif; font-size: 0.85rem; font-weight: 600; color: var(--accent-primary); margin-bottom: 0.5rem; }
        .hint-text { font-family: 'Noto Sans KR', sans-serif; font-size: 0.85rem; color: var(--text-secondary); }
        
        .checklist-item { display: flex; align-items: center; gap: 0.75rem; padding: 0.5rem 0; }
        .check-icon { font-size: 1rem; }
        .check-text { font-family: 'Noto Sans KR', sans-serif; font-size: 0.9rem; }
        .check-pass { color: var(--success); }
        .check-fail { color: var(--danger); }
        .check-warn { color: var(--warning); }
        
        .result-card { background: var(--bg-card); border: 1px solid var(--border); border-radius: 16px; padding: 1.5rem; margin: 1rem 0; }
        .result-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; }
        .result-score { font-family: 'Space Mono', monospace; font-size: 2rem; font-weight: 700; }
        
        .disclaimer { font-family: 'Noto Sans KR', sans-serif; font-size: 0.8rem; color: var(--text-muted); background: rgba(239,68,68,0.1); border: 1px solid rgba(239,68,68,0.2); border-radius: 8px; padding: 0.75rem 1rem; margin: 1rem 0; }
    </style>
    """, unsafe_allow_html=True)

    # 데이터 파일명 상수
    SUBMISSIONS_FILE = "homework_submissions.json"
    PROFILES_FILE = "member_profiles.json"
    UNLOCKS_FILE = "unlocks.json"

    # 과제 주제
    TOPICS = {
        "다이버전스": {"icon": "📊", "desc": "RSI/MACD 다이버전스 분석", "hints": ["가격과 지표 방향 비교", "일반 vs 히든 구분", "추세 약화 신호 해석"], "unlock_1": "다이버전스 해설 페이지", "unlock_2": "다이버전스 심화 문제"},
        "지지저항": {"icon": "📉", "desc": "지지선과 저항선 분석", "hints": ["과거 반등/저항 구간", "거래량 집중 구간", "심리적 가격대"], "unlock_1": "지지저항 해설 페이지", "unlock_2": "지지저항 심화 문제"},
        "SRL": {"icon": "📈", "desc": "SRL 지표 설정과 해석", "hints": ["트레이딩뷰 설정", "구간 해석", "다른 지표와 조합"], "unlock_1": "SRL 해설 페이지", "unlock_2": "SRL 심화 문제"},
        "아래꼬리": {"icon": "🕯️", "desc": "아래꼬리 캔들 패턴 분석", "hints": ["꼬리와 몸통 비율", "거래량 확인", "위치와 맥락"], "unlock_1": "아래꼬리 해설 페이지", "unlock_2": "아래꼬리 심화 문제"}
    }

    FORBIDDEN = ["추천", "매수하세요", "매도하세요", "사세요", "파세요", "무조건", "100%", "확실", "수익 보장"]
    REQUIRED = {"risk": ["손절", "리스크", "위험", "관리", "스탑"], "position": ["포지션", "비중", "사이징", "%"], "reason": ["근거", "이유", "분석", "판단", "확인"]}

    def evaluate(content, topic):
        results = []
        forbidden_found = [kw for kw in FORBIDDEN if kw in content]
        if forbidden_found:
            results.append({"status": "fail", "text": f"금지 표현 발견: {', '.join(forbidden_found[:2])}"})
        else:
            results.append({"status": "pass", "text": "투자 권유 표현 없음"})
        
        topic_kw = {"다이버전스": ["다이버전스", "rsi", "macd", "괴리"], "지지저항": ["지지", "저항", "구간", "레벨"], "SRL": ["srl", "지표", "구간"], "아래꼬리": ["꼬리", "캔들", "망치", "윅"]}
        if any(kw in content.lower() for kw in topic_kw.get(topic, [])):
            results.append({"status": "pass", "text": f"{topic} 관련 내용 포함"})
        else:
            results.append({"status": "warn", "text": f"{topic} 관련 키워드 부족"})
        
        if any(kw in content for kw in REQUIRED['risk']):
            results.append({"status": "pass", "text": "리스크 관리 언급"})
        else:
            results.append({"status": "warn", "text": "리스크 관리 언급 부족"})
        
        if any(kw in content for kw in REQUIRED['reason']) and len(content) >= 100:
            results.append({"status": "pass", "text": "충분한 근거 제시"})
        else:
            results.append({"status": "warn", "text": "근거 보강 필요"})
        
        if len(content) >= 150:
            results.append({"status": "pass", "text": f"충분한 분량 ({len(content)}자)"})
        elif len(content) >= 80:
            results.append({"status": "warn", "text": f"분량 다소 부족 ({len(content)}자)"})
        else:
            results.append({"status": "fail", "text": f"분량 부족 ({len(content)}자)"})
        
        return results

    # 헤더
    st.markdown("""
    <div class="page-header">
        <h1 class="page-title">📤 과제 제출</h1>
        <p class="page-subtitle">주제별 과제를 제출하고 추가 콘텐츠를 언락하세요</p>
    </div>
    """, unsafe_allow_html=True)

    if 'nickname' not in st.session_state:
        st.session_state.nickname = ''
    if 'hw_submitted' not in st.session_state:
        st.session_state.hw_submitted = False

    nickname = st.text_input("닉네임", value=st.session_state.nickname, placeholder="온보딩에서 사용한 닉네임", key="hw_nickname")
    st.session_state.nickname = nickname

    if not st.session_state.hw_submitted:
        st.markdown("### 📋 과제 주제 선택")
        selected_topic = st.radio("", list(TOPICS.keys()), format_func=lambda x: f"{TOPICS[x]['icon']} {x}", horizontal=True, label_visibility="collapsed", key="hw_topic")
        topic_data = TOPICS[selected_topic]
        
        st.markdown(f"""
        <div class="unlock-preview">
            <p class="unlock-title">🔓 제출 시 언락되는 콘텐츠</p>
            <p class="unlock-item">• 1회 제출: {topic_data['unlock_1']}</p>
            <p class="unlock-item">• 2회 제출: {topic_data['unlock_2']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="hint-box">
            <p class="hint-title">💡 작성 힌트</p>
            {"".join([f'<p class="hint-text">• {h}</p>' for h in topic_data['hints']])}
        </div>
        """, unsafe_allow_html=True)
        
        content = st.text_area("📝 분석 내용", placeholder=f"{selected_topic} 분석 내용을 작성하세요...", height=250, key="hw_content")
        st.caption(f"{len(content)} / 150+ 권장")
        
        st.markdown("""<div class="disclaimer">⚠️ 과제는 학습 목적입니다. 매매 추천, 가격 예측, 종목 추천을 포함하지 마세요.</div>""", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("📤 제출하기", type="primary", use_container_width=True, key="hw_submit"):
                if not nickname:
                    st.error("닉네임을 입력해주세요")
                elif len(content.strip()) < 50:
                    st.error("최소 50자 이상 작성해주세요")
                else:
                    results = evaluate(content, selected_topic)
                    submissions = load_json(SUBMISSIONS_FILE, default=[])
                    new_id = get_next_id(SUBMISSIONS_FILE)
                    submissions.append({"id": new_id, "nickname": nickname, "topic": selected_topic, "content": content, "submitted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "reviewed": False, "review_result": None})
                    save_json(SUBMISSIONS_FILE, submissions)
                    
                    profiles = load_json(PROFILES_FILE, default={})
                    if nickname not in profiles:
                        profiles[nickname] = {"nickname": nickname, "homework_count": 0, "homework_streak": 0}
                    profiles[nickname]['homework_count'] = profiles[nickname].get('homework_count', 0) + 1
                    profiles[nickname]['last_homework_date'] = datetime.now().strftime("%Y-%m-%d")
                    save_json(PROFILES_FILE, profiles)
                    
                    unlocks = load_json(UNLOCKS_FILE, default={})
                    if nickname not in unlocks:
                        unlocks[nickname] = {}
                    topic_submissions = [s for s in submissions if s.get('nickname') == nickname and s.get('topic') == selected_topic]
                    topic_map = {'다이버전스': ('divergence_lesson', 'divergence_advanced'), '지지저항': ('support_resistance_lesson', 'support_resistance_advanced'), 'SRL': ('srl_lesson', 'srl_advanced'), '아래꼬리': ('tail_candle_lesson', 'tail_candle_advanced')}
                    if selected_topic in topic_map:
                        lesson_key, advanced_key = topic_map[selected_topic]
                        if len(topic_submissions) >= 1:
                            unlocks[nickname][lesson_key] = True
                        if len(topic_submissions) >= 2:
                            unlocks[nickname][advanced_key] = True
                        save_json(UNLOCKS_FILE, unlocks)
                    
                    st.session_state.hw_submitted = True
                    st.session_state.hw_results = results
                    st.session_state.hw_topic = selected_topic
                    st.session_state.topic_count = len(topic_submissions)
                    st.rerun()

    else:
        results = st.session_state.hw_results
        topic = st.session_state.hw_topic
        topic_count = st.session_state.topic_count
        
        pass_count = sum(1 for r in results if r['status'] == 'pass')
        fail_count = sum(1 for r in results if r['status'] == 'fail')
        score_color = "#22c55e" if fail_count == 0 else "#ef4444"
        
        st.success(f"✅ {topic} 과제가 제출되었습니다!")
        
        st.markdown(f"""
        <div class="result-card">
            <div class="result-header">
                <span style="font-family: 'Noto Sans KR', sans-serif; color: var(--text-secondary);">자동 체크 결과</span>
                <span class="result-score" style="color: {score_color};">{pass_count}/{len(results)}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        for r in results:
            icon = "✅" if r['status'] == 'pass' else "⚠️" if r['status'] == 'warn' else "❌"
            color_class = "check-pass" if r['status'] == 'pass' else "check-warn" if r['status'] == 'warn' else "check-fail"
            st.markdown(f"""<div class="checklist-item"><span class="check-icon">{icon}</span><span class="check-text {color_class}">{r['text']}</span></div>""", unsafe_allow_html=True)
        
        if topic_count == 1:
            st.success(f"🔓 '{TOPICS[topic]['unlock_1']}' 언락!")
        elif topic_count == 2:
            st.success(f"🔓 '{TOPICS[topic]['unlock_2']}' 언락!")
        
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🔄 새 과제", use_container_width=True, key="hw_new"):
                st.session_state.hw_submitted = False
                st.rerun()
        with col2:
            if st.button("🔓 해설 보기", use_container_width=True, key="hw_to_lesson"):
                st.session_state.route = "unlocked_lessons"
                st.rerun()
        with col3:
            if st.button("🎯 심화 문제", use_container_width=True, key="hw_to_advanced"):
                st.session_state.route = "advanced_practice"
                st.rerun()

    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🏠 홈", use_container_width=True, key="hw_nav1"):
            st.session_state.route = "home"
            st.rerun()
    with col2:
        if st.button("📚 교육 콘텐츠", use_container_width=True, key="hw_nav2"):
            st.session_state.route = "content_library"
            st.rerun()
    with col3:
        if st.button("🛡️ 리스크 체크", use_container_width=True, key="hw_nav3"):
            st.session_state.route = "risk_check"
            st.rerun()
