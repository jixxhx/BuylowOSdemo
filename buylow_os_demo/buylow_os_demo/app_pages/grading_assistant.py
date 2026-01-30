import streamlit as st
from datetime import datetime

# 안전한 데이터 접근을 위한 유틸리티
from utils.data_utils import load_json, save_json


def render():
    """채점 보조 페이지 렌더링"""
    
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
        
        .submission-card { background: var(--bg-card); border: 1px solid var(--border); border-radius: 16px; padding: 1.5rem; margin: 1rem 0; }
        .submission-card.reviewed { border-left: 4px solid var(--success); }
        .submission-card.pending { border-left: 4px solid var(--warning); }
        
        .submission-header { display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 1rem; }
        .submission-info { flex: 1; }
        .submission-nickname { font-family: 'Outfit', sans-serif; font-size: 1rem; font-weight: 700; color: var(--text-primary); }
        .submission-meta { font-family: 'Space Mono', monospace; font-size: 0.75rem; color: var(--text-muted); margin-top: 0.25rem; }
        .topic-badge { font-family: 'Noto Sans KR', sans-serif; font-size: 0.75rem; padding: 0.3rem 0.75rem; border-radius: 12px; background: rgba(99,102,241,0.2); color: var(--accent-primary); }
        
        .submission-content { font-family: 'Noto Sans KR', sans-serif; font-size: 0.9rem; color: var(--text-secondary); line-height: 1.7; background: var(--bg-dark); border-radius: 8px; padding: 1rem; margin: 1rem 0; white-space: pre-wrap; max-height: 200px; overflow-y: auto; }
        
        .result-summary { display: flex; gap: 1rem; align-items: center; padding: 1rem; background: var(--bg-dark); border-radius: 8px; margin: 1rem 0; }
        .result-score { font-family: 'Space Mono', monospace; font-size: 1.5rem; font-weight: 700; }
    </style>
    """, unsafe_allow_html=True)

    # 헤더
    st.markdown("""
    <div class="page-header">
        <h1 class="page-title">✏️ 과제 채점 보조</h1>
    </div>
    """, unsafe_allow_html=True)

    submissions = load_json("homework_submissions.json", default=[])
    reviews = load_json("homework_reviews.json", default=[])

    # 필터
    col1, col2 = st.columns(2)
    with col1:
        topic_filter = st.selectbox("주제 필터", ["전체", "다이버전스", "지지저항", "SRL", "아래꼬리"], key="ga_topic")
    with col2:
        status_filter = st.selectbox("상태 필터", ["미채점", "전체", "채점완료"], key="ga_status")

    # 필터링
    filtered = submissions
    if topic_filter != "전체":
        filtered = [s for s in filtered if s.get('topic') == topic_filter]
    if status_filter == "미채점":
        filtered = [s for s in filtered if not s.get('reviewed')]
    elif status_filter == "채점완료":
        filtered = [s for s in filtered if s.get('reviewed')]

    st.markdown(f"**{len(filtered)}개의 제출물**")

    # 제출물 표시
    for sub in filtered:
        reviewed = sub.get('reviewed', False)
        card_class = "reviewed" if reviewed else "pending"
        status_text = "✅ 채점완료" if reviewed else "⏳ 대기중"
        
        st.markdown(f"""
        <div class="submission-card {card_class}">
            <div class="submission-header">
                <div class="submission-info">
                    <p class="submission-nickname">👤 {sub.get('nickname', '익명')}</p>
                    <p class="submission-meta">{sub.get('submitted_at', '')} | {status_text}</p>
                </div>
                <span class="topic-badge">{sub.get('topic', '기타')}</span>
            </div>
            <div class="submission-content">{sub.get('content', '내용 없음')}</div>
        </div>
        """, unsafe_allow_html=True)
        
        if not reviewed:
            with st.expander(f"📋 채점하기 (#{sub.get('id')})"):
                st.markdown("**체크리스트:**")
                
                c1 = st.checkbox("다이버전스가 어디서 보였는지 설명했는가", key=f"ga_c1_{sub.get('id')}")
                c2 = st.checkbox("지지/저항 또는 SRL 구간을 근거로 썼는가", key=f"ga_c2_{sub.get('id')}")
                c3 = st.checkbox("손절 기준이 명확한가", key=f"ga_c3_{sub.get('id')}")
                c4 = st.checkbox("포지션 비중과 레버리지가 적절한가", key=f"ga_c4_{sub.get('id')}")
                c5 = st.checkbox("감정 상태를 기록했는가", key=f"ga_c5_{sub.get('id')}")
                
                feedback = st.text_area("피드백 (선택)", placeholder="피드백을 입력하세요...", key=f"ga_fb_{sub.get('id')}")
                
                passed = sum([c1, c2, c3, c4, c5])
                score_color = "#22c55e" if passed >= 4 else "#f59e0b" if passed >= 2 else "#ef4444"
                
                st.markdown(f"""
                <div class="result-summary">
                    <span class="result-score" style="color: {score_color};">{passed}/5</span>
                    <span style="font-family: 'Noto Sans KR', sans-serif; color: var(--text-secondary);">항목 통과</span>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button("💾 채점 저장", key=f"ga_save_{sub.get('id')}", type="primary"):
                    review = {
                        "submission_id": sub.get('id'),
                        "reviewer": "operator",
                        "reviewed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "checklist": {"divergence_explained": c1, "support_resistance_mentioned": c2, "stop_loss_clear": c3, "position_size_appropriate": c4, "emotion_recorded": c5},
                        "passed_count": passed,
                        "total_count": 5,
                        "feedback": feedback
                    }
                    reviews.append(review)
                    save_json("homework_reviews.json", reviews)
                    
                    for s in submissions:
                        if s.get('id') == sub.get('id'):
                            s['reviewed'] = True
                            s['review_result'] = {"passed": passed, "total": 5}
                    save_json("homework_submissions.json", submissions)
                    
                    st.success("✅ 채점이 저장되었습니다!")
                    st.rerun()
        else:
            review = next((r for r in reviews if r.get('submission_id') == sub.get('id')), None)
            if review:
                passed = review.get('passed_count', 0)
                total = review.get('total_count', 5)
                st.markdown(f"**채점 결과:** {passed}/{total} 통과")
                if review.get('feedback'):
                    st.caption(f"피드백: {review.get('feedback')}")

    if not filtered:
        st.info("해당하는 제출물이 없습니다.")

    # 네비게이션
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🏠 홈", use_container_width=True, key="ga_nav1"):
            st.session_state.route = "home"
            st.rerun()
    with col2:
        if st.button("📊 운영자 대시보드", use_container_width=True, key="ga_nav2"):
            st.session_state.route = "operator_dashboard"
            st.rerun()
    with col3:
        if st.button("⚙️ 관리자", use_container_width=True, key="ga_nav3"):
            st.session_state.route = "admin"
            st.rerun()
