import streamlit as st
from datetime import datetime, timedelta
from collections import Counter

# 안전한 데이터 접근을 위한 유틸리티
from utils.data_utils import load_json


def render():
    """운영자 대시보드 페이지 렌더링"""
    
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
        
        .page-header { padding: 1.5rem 0; animation: fadeInUp 0.6s ease-out; }
        .page-title { font-family: 'Outfit', sans-serif; font-size: clamp(1.5rem, 3vw, 2rem); font-weight: 800; color: var(--text-primary); margin: 0; }
        
        .summary-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem; margin: 1rem 0; }
        .summary-card { background: var(--bg-card); border: 1px solid var(--border); border-radius: 16px; padding: 1.25rem; text-align: center; }
        .summary-value { font-family: 'Space Mono', monospace; font-size: 2rem; font-weight: 700; }
        .summary-label { font-family: 'Noto Sans KR', sans-serif; font-size: 0.8rem; color: var(--text-muted); margin-top: 0.25rem; }
        
        .section-card { background: var(--bg-card); border: 1px solid var(--border); border-radius: 16px; padding: 1.5rem; margin: 1rem 0; }
        .section-title { font-family: 'Outfit', sans-serif; font-size: 1.1rem; font-weight: 700; color: var(--text-primary); margin-bottom: 1rem; }
        
        .topic-item { display: flex; justify-content: space-between; align-items: center; padding: 0.75rem; background: var(--bg-dark); border-radius: 8px; margin: 0.5rem 0; }
        .topic-name { font-family: 'Noto Sans KR', sans-serif; font-size: 0.95rem; color: var(--text-primary); }
        .topic-count { font-family: 'Space Mono', monospace; font-size: 0.9rem; color: var(--accent-primary); background: rgba(99,102,241,0.15); padding: 0.25rem 0.75rem; border-radius: 12px; }
        
        .streak-bar { display: flex; gap: 0.5rem; margin: 0.5rem 0; }
        .streak-item { flex: 1; text-align: center; padding: 0.75rem 0.5rem; background: var(--bg-dark); border-radius: 8px; }
        .streak-num { font-family: 'Space Mono', monospace; font-size: 1.25rem; font-weight: 700; color: var(--accent-primary); }
        .streak-label { font-family: 'Noto Sans KR', sans-serif; font-size: 0.7rem; color: var(--text-muted); }
        
        .action-suggest { background: rgba(99,102,241,0.1); border: 1px solid rgba(99,102,241,0.3); border-radius: 8px; padding: 1rem; margin: 0.5rem 0; }
        .action-text { font-family: 'Noto Sans KR', sans-serif; font-size: 0.9rem; color: var(--text-secondary); margin-bottom: 0.5rem; }
    </style>
    """, unsafe_allow_html=True)

    def count_keywords(texts, keywords):
        counts = Counter()
        for text in texts:
            text_lower = text.lower()
            for kw in keywords:
                if kw in text_lower:
                    counts[kw] += 1
        return counts

    KEYWORDS = ["다이버전스", "지지", "저항", "srl", "아래꼬리", "손절", "레버리지", "익절", "비중", "포지션", "rsi", "캔들"]

    logs = load_json("logs.json", default=[])
    tickets = load_json("tickets.json", default=[])
    submissions = load_json("homework_submissions.json", default=[])
    reviews = load_json("homework_reviews.json", default=[])
    risk_history = load_json("risk_history.json", default={})
    profiles = load_json("member_profiles.json", default={})

    today = datetime.now().strftime("%Y-%m-%d")
    week_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

    today_tickets = [t for t in tickets if t.get('timestamp', '').startswith(today)]
    open_tickets = [t for t in tickets if t.get('status') == 'open']
    today_submissions = [s for s in submissions if s.get('submitted_at', '').startswith(today)]
    week_submissions = [s for s in submissions if s.get('submitted_at', '') >= week_ago]

    high_risk_today = 0
    for user_data in risk_history.values():
        if isinstance(user_data, dict):
            high_risk_today += user_data.get('high_risk_count', 0)

    # 헤더
    st.markdown("""
    <div class="page-header">
        <h1 class="page-title">📊 운영자 대시보드</h1>
    </div>
    """, unsafe_allow_html=True)

    cs_logs = [l for l in logs if l.get('type') == 'cs_query']
    week_cs = [l for l in cs_logs if l.get('timestamp', '') >= week_ago]
    top_topic = "없음"
    if week_cs:
        texts = [l.get('query', '') for l in week_cs]
        keyword_counts = count_keywords(texts, KEYWORDS)
        if keyword_counts:
            top_topic = keyword_counts.most_common(1)[0][0]

    st.markdown(f"""
    <div class="summary-grid">
        <div class="summary-card"><p class="summary-value" style="color: #ef4444;">{len(today_tickets)}</p><p class="summary-label">오늘 새 티켓</p></div>
        <div class="summary-card"><p class="summary-value" style="color: #f59e0b;">{len(open_tickets)}</p><p class="summary-label">미해결 티켓</p></div>
        <div class="summary-card"><p class="summary-value" style="color: #22c55e;">{len(today_submissions)}</p><p class="summary-label">오늘 과제</p></div>
        <div class="summary-card"><p class="summary-value" style="color: #ef4444;">{high_risk_today}</p><p class="summary-label">고위험 누적</p></div>
        <div class="summary-card"><p class="summary-value" style="color: #6366f1;">{top_topic}</p><p class="summary-label">이번주 핫토픽</p></div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["🔥 막힌 포인트", "📝 과제 지표", "🎫 티켓 관리"])

    with tab1:
        st.markdown("""<div class="section-card"><div class="section-title">🔥 이번 주 가장 많이 막힌 주제 Top 5</div></div>""", unsafe_allow_html=True)
        
        all_texts = [l.get('query', '') for l in week_cs]
        all_texts += [s.get('content', '') for s in week_submissions]
        all_texts += [t.get('query', '') for t in tickets if t.get('timestamp', '') >= week_ago]
        
        keyword_counts = count_keywords(all_texts, KEYWORDS)
        top_5 = keyword_counts.most_common(5)
        
        if top_5:
            for kw, count in top_5:
                col1, col2, col3 = st.columns([3, 1, 2])
                with col1:
                    st.markdown(f"**{kw}**")
                with col2:
                    st.markdown(f"**{count}회**")
                with col3:
                    if st.button(f"📝 공지 초안", key=f"op_draft_{kw}"):
                        template = f"""📢 [{kw}] 관련 안내\n\n최근 '{kw}' 관련 질문이 많아 안내드립니다.\n\n⚠️ 본 내용은 교육 목적이며, 매매 추천이나 가격 예측이 아닙니다."""
                        st.code(template, language=None)
        else:
            st.info("이번 주 데이터가 없습니다.")
        
        st.markdown("""<div class="action-suggest"><p class="action-text">💡 추천 액션: 다음 라이브에서 Top 주제를 다루거나, FAQ 문서를 보강하세요.</p></div>""", unsafe_allow_html=True)

    with tab2:
        st.markdown("### 📝 이번 주 과제 지표")
        
        total_members = len(profiles) if profiles else 1
        week_submitters = len(set(s.get('nickname') for s in week_submissions))
        participation_rate = int((week_submitters / total_members) * 100) if total_members > 0 else 0
        
        reviewed_count = len([s for s in week_submissions if s.get('reviewed')])
        completion_rate = int((reviewed_count / len(week_submissions)) * 100) if week_submissions else 0
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("이번 주 참여율", f"{participation_rate}%")
        with col2:
            st.metric("이번 주 완료율", f"{completion_rate}%")
        
        st.markdown("**주제별 제출 수**")
        topic_counts = Counter(s.get('topic', '기타') for s in week_submissions)
        for topic, count in topic_counts.most_common():
            st.markdown(f"""<div class="topic-item"><span class="topic-name">{topic}</span><span class="topic-count">{count}건</span></div>""", unsafe_allow_html=True)
        
        st.markdown("**스트릭 분포**")
        streaks = {'0일': 0, '1-2일': 0, '3-6일': 0, '7일+': 0}
        for profile in profiles.values():
            if isinstance(profile, dict):
                streak = profile.get('homework_streak', 0)
                if streak == 0: streaks['0일'] += 1
                elif streak <= 2: streaks['1-2일'] += 1
                elif streak <= 6: streaks['3-6일'] += 1
                else: streaks['7일+'] += 1
        
        st.markdown(f"""
        <div class="streak-bar">
            <div class="streak-item"><p class="streak-num">{streaks['0일']}</p><p class="streak-label">0일</p></div>
            <div class="streak-item"><p class="streak-num">{streaks['1-2일']}</p><p class="streak-label">1-2일</p></div>
            <div class="streak-item"><p class="streak-num">{streaks['3-6일']}</p><p class="streak-label">3-6일</p></div>
            <div class="streak-item"><p class="streak-num">{streaks['7일+']}</p><p class="streak-label">7일+</p></div>
        </div>
        """, unsafe_allow_html=True)

    with tab3:
        st.markdown("### 🎫 티켓 관리")
        ticket_filter = st.radio("필터", ["미해결", "전체", "해결됨"], horizontal=True, key="op_ticket_filter")
        
        if ticket_filter == "미해결":
            filtered_tickets = open_tickets
        elif ticket_filter == "해결됨":
            filtered_tickets = [t for t in tickets if t.get('status') == 'closed']
        else:
            filtered_tickets = tickets
        
        for ticket in filtered_tickets[:10]:
            status_color = "#ef4444" if ticket.get('status') == 'open' else "#22c55e"
            st.markdown(f"""
            <div class="topic-item">
                <span class="topic-name">#{ticket.get('id', 0)} - {ticket.get('query', '내용 없음')[:40]}...</span>
                <span class="topic-count" style="background: {status_color}20; color: {status_color};">{ticket.get('status', 'open')}</span>
            </div>
            """, unsafe_allow_html=True)
            
            if ticket.get('status') == 'open':
                if st.button(f"📋 알림 문구 생성", key=f"op_notify_{ticket.get('id')}"):
                    notify_text = f"🎫 새 티켓 #{ticket.get('id')}\n질문: {ticket.get('query', '')}\n시간: {ticket.get('timestamp', '')}"
                    st.code(notify_text, language=None)
        
        if not filtered_tickets:
            st.info("해당하는 티켓이 없습니다.")

    # 네비게이션
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("🏠 홈", use_container_width=True, key="op_nav1"):
            st.session_state.route = "home"
            st.rerun()
    with col2:
        if st.button("📢 공지 허브", use_container_width=True, key="op_nav2"):
            st.session_state.route = "announcements"
            st.rerun()
    with col3:
        if st.button("✏️ 채점 보조", use_container_width=True, key="op_nav3"):
            st.session_state.route = "grading_assistant"
            st.rerun()
    with col4:
        if st.button("⚙️ 관리자", use_container_width=True, key="op_nav4"):
            st.session_state.route = "admin"
            st.rerun()
