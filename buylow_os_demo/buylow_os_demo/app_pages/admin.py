import streamlit as st
import pandas as pd
from datetime import datetime

# 안전한 데이터 접근을 위한 유틸리티
from utils.data_utils import load_json, save_json, get_next_id


def render():
    """관리자 페이지 렌더링"""
    
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
        
        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 1rem; margin: 1rem 0; }
        .stat-card { background: var(--bg-card); border: 1px solid var(--border); border-radius: 16px; padding: 1.25rem; text-align: center; }
        .stat-value { font-family: 'Space Mono', monospace; font-size: 1.75rem; font-weight: 700; }
        .stat-label { font-family: 'Noto Sans KR', sans-serif; font-size: 0.8rem; color: var(--text-muted); margin-top: 0.25rem; }
        
        .section-header { font-family: 'Outfit', sans-serif; font-size: 1.1rem; font-weight: 700; color: var(--text-primary); margin: 1.5rem 0 1rem; }
        
        .ticket-card { background: var(--bg-card); border: 1px solid var(--border); border-radius: 12px; padding: 1rem; margin: 0.5rem 0; }
        .ticket-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem; }
        .ticket-id { font-family: 'Space Mono', monospace; font-size: 0.8rem; color: var(--accent-primary); background: rgba(99,102,241,0.15); padding: 0.2rem 0.6rem; border-radius: 12px; }
        .ticket-status { font-family: 'Noto Sans KR', sans-serif; font-size: 0.7rem; padding: 0.2rem 0.6rem; border-radius: 12px; }
        .status-open { background: rgba(239,68,68,0.2); color: var(--danger); }
        .status-closed { background: rgba(34,197,94,0.2); color: var(--success); }
        .ticket-query { font-family: 'Noto Sans KR', sans-serif; font-size: 0.9rem; color: var(--text-primary); }
        .ticket-meta { font-family: 'Space Mono', monospace; font-size: 0.7rem; color: var(--text-muted); margin-top: 0.25rem; }
        
        .template-output { background: var(--bg-dark); border: 1px solid var(--border); border-radius: 8px; padding: 1rem; font-family: 'Noto Sans KR', sans-serif; font-size: 0.85rem; color: var(--text-secondary); white-space: pre-wrap; margin: 1rem 0; max-height: 300px; overflow-y: auto; }
    </style>
    """, unsafe_allow_html=True)

    # 헤더
    st.markdown("""
    <div class="page-header">
        <h1 class="page-title">⚙️ 관리자 페이지</h1>
    </div>
    """, unsafe_allow_html=True)

    logs = load_json("logs.json", default=[])
    tickets = load_json("tickets.json", default=[])
    announcements = load_json("announcements.json", default=[])

    today = datetime.now().strftime("%Y-%m-%d")
    today_logs = [l for l in logs if l.get('timestamp', '').startswith(today)]
    open_tickets = [t for t in tickets if t.get('status') == 'open']
    cs_logs = [l for l in logs if l.get('type') == 'cs_query']
    homework_logs = [l for l in logs if l.get('type') == 'homework_submission']
    risk_logs = [l for l in logs if l.get('type') == 'risk_check']

    # 통계
    st.markdown(f"""
    <div class="stats-grid">
        <div class="stat-card"><p class="stat-value" style="color: #6366f1;">{len(logs)}</p><p class="stat-label">전체 로그</p></div>
        <div class="stat-card"><p class="stat-value" style="color: #22c55e;">{len(today_logs)}</p><p class="stat-label">오늘 로그</p></div>
        <div class="stat-card"><p class="stat-value" style="color: {'#ef4444' if open_tickets else '#22c55e'};">{len(open_tickets)}</p><p class="stat-label">미처리 티켓</p></div>
        <div class="stat-card"><p class="stat-value" style="color: #f59e0b;">{len(announcements)}</p><p class="stat-label">공지 수</p></div>
    </div>
    """, unsafe_allow_html=True)

    # 빠른 링크
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📊 운영자 대시보드", use_container_width=True, key="admin_to_dash"):
            st.session_state.route = "operator_dashboard"
            st.rerun()
    with col2:
        if st.button("✏️ 채점 보조", use_container_width=True, key="admin_to_grade"):
            st.session_state.route = "grading_assistant"
            st.rerun()

    # 탭
    tab1, tab2, tab3, tab4 = st.tabs(["📢 공지 템플릿", "🎫 티켓", "📋 로그", "📊 통계"])

    with tab1:
        st.markdown('<p class="section-header">공지 템플릿 생성기</p>', unsafe_allow_html=True)
        template_type = st.selectbox("공지 타입", ["교육 공지", "이벤트 공지", "주간 브리핑", "주의사항 공지", "과제 안내"], key="admin_template_type")
        
        col1, col2 = st.columns(2)
        with col1:
            title = st.text_input("공지 제목", placeholder="제목을 입력하세요", key="admin_title")
        with col2:
            tag = st.selectbox("태그", ["교육 일정", "이벤트", "브리핑", "주의사항", "과제 안내", "멤버십 안내"], key="admin_tag")
        
        if template_type == "교육 공지":
            schedule = st.text_input("일정", placeholder="예: 화요일 20:00", key="admin_schedule")
            condition = st.text_input("참여 조건", placeholder="예: 기초 과제 1회 이상 제출", key="admin_condition")
            content = st.text_area("교육 내용", placeholder="교육 내용을 입력하세요", key="admin_content")
            template = f"""📚 [{title}] 교육 안내\n\n📅 일정: {schedule}\n👥 참여 조건: {condition}\n\n📋 내용:\n{content}\n\n⚠️ 본 교육은 매매 추천, 가격 예측, 종목 추천이 아니며, 교육 및 정보 제공 목적입니다."""
        elif template_type == "이벤트 공지":
            period = st.text_input("기간", placeholder="예: 1/27 ~ 2/3", key="admin_period")
            benefit = st.text_input("혜택", placeholder="예: 과제 제출 시 추가 포인트", key="admin_benefit")
            method = st.text_area("참여 방법", placeholder="참여 방법을 입력하세요", key="admin_method")
            template = f"""🎉 [{title}] 이벤트 안내\n\n📅 기간: {period}\n🎁 혜택: {benefit}\n\n📋 참여 방법:\n{method}\n\n⚠️ 본 이벤트는 교육 참여 독려 목적이며, 투자 권유가 아닙니다."""
        else:
            template = f"""📢 [{title}] 공지\n\n내용을 입력하세요.\n\n⚠️ 본 내용은 교육 및 정보 제공 목적입니다."""
        
        st.markdown(f'<div class="template-output">{template}</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📋 텔레그램용 복사", use_container_width=True, key="admin_copy"):
                st.code(template, language=None)
                st.success("위 내용을 복사해서 텔레그램에 붙여넣기 하세요!")
        with col2:
            pinned = st.checkbox("상단 고정", key="admin_pinned")
            if st.button("💾 공지로 저장", use_container_width=True, key="admin_save"):
                if title:
                    new_id = get_next_id("announcements.json")
                    announcements.append({"id": new_id, "title": title, "tag": tag, "content": template, "pinned": pinned, "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "related_faq": [], "next_actions": []})
                    save_json("announcements.json", announcements)
                    st.success(f"✅ 공지 #{new_id} 저장 완료!")
                else:
                    st.error("제목을 입력해주세요")

    with tab2:
        st.markdown('<p class="section-header">티켓 관리</p>', unsafe_allow_html=True)
        ticket_filter = st.radio("상태", ["미처리", "전체", "완료"], horizontal=True, key="admin_ticket_filter")
        
        if ticket_filter == "미처리":
            filtered_tickets = open_tickets
        elif ticket_filter == "완료":
            filtered_tickets = [t for t in tickets if t.get('status') == 'closed']
        else:
            filtered_tickets = tickets
        
        if filtered_tickets:
            for ticket in filtered_tickets[:15]:
                status_class = "status-open" if ticket.get('status') == 'open' else "status-closed"
                status_text = "미처리" if ticket.get('status') == 'open' else "완료"
                st.markdown(f"""
                <div class="ticket-card">
                    <div class="ticket-header">
                        <span class="ticket-id">#{ticket.get('id', 0):04d}</span>
                        <span class="ticket-status {status_class}">{status_text}</span>
                    </div>
                    <p class="ticket-query">{ticket.get('query', '내용 없음')[:60]}...</p>
                    <p class="ticket-meta">{ticket.get('timestamp', '')}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if ticket.get('status') == 'open':
                    if st.button("✓ 처리 완료", key=f"close_{ticket.get('id')}"):
                        for t in tickets:
                            if t.get('id') == ticket.get('id'):
                                t['status'] = 'closed'
                                t['closed_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        save_json("tickets.json", tickets)
                        st.rerun()
        else:
            st.info("해당하는 티켓이 없습니다")

    with tab3:
        st.markdown('<p class="section-header">최근 로그</p>', unsafe_allow_html=True)
        log_filter = st.selectbox("유형", ["전체", "CS", "과제", "리스크"], key="admin_log_filter")
        
        if log_filter == "CS":
            filtered = cs_logs
        elif log_filter == "과제":
            filtered = homework_logs
        elif log_filter == "리스크":
            filtered = risk_logs
        else:
            filtered = logs
        
        if filtered:
            df_data = []
            for l in filtered[-30:][::-1]:
                log_type = l.get('type', 'unknown')
                type_labels = {'cs_query': '💬', 'quiz_result': '📚', 'homework_submission': '📤', 'risk_check': '🛡️'}
                summary = ""
                if log_type == 'cs_query':
                    summary = l.get('query', '')[:30]
                elif log_type == 'homework_submission':
                    summary = l.get('topic', '')
                elif log_type == 'risk_check':
                    summary = f"{l.get('symbol', '')} {l.get('risk_score', 0)}점"
                df_data.append({"시간": l.get('timestamp', '')[:16], "유형": type_labels.get(log_type, '?'), "내용": summary})
            st.dataframe(pd.DataFrame(df_data), use_container_width=True, height=350)
        else:
            st.info("로그가 없습니다")

    with tab4:
        st.markdown('<p class="section-header">통계</p>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**기능별 사용량**")
            usage = pd.DataFrame({"기능": ["CS", "과제", "리스크"], "횟수": [len(cs_logs), len(homework_logs), len(risk_logs)]})
            st.bar_chart(usage.set_index("기능"))
        with col2:
            if risk_logs:
                st.markdown("**리스크 점수 분포**")
                high = len([l for l in risk_logs if l.get('risk_score', 0) >= 50])
                med = len([l for l in risk_logs if 30 <= l.get('risk_score', 0) < 50])
                low = len([l for l in risk_logs if l.get('risk_score', 0) < 30])
                st.metric("🔴 고위험", high)
                st.metric("🟡 주의", med)
                st.metric("🟢 안전", low)

    # 네비게이션
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("🏠 홈", use_container_width=True, key="admin_n1"):
            st.session_state.route = "home"
            st.rerun()
    with col2:
        if st.button("📢 공지 허브", use_container_width=True, key="admin_n2"):
            st.session_state.route = "announcements"
            st.rerun()
    with col3:
        if st.button("📊 대시보드", use_container_width=True, key="admin_n3"):
            st.session_state.route = "operator_dashboard"
            st.rerun()
    with col4:
        if st.button("✏️ 채점", use_container_width=True, key="admin_n4"):
            st.session_state.route = "grading_assistant"
            st.rerun()
