import streamlit as st
import re
from datetime import datetime

# 안전한 데이터 접근을 위한 유틸리티
from utils.data_utils import load_json, save_json, append_to_json_list, get_next_id


def render():
    """CS 챗봇 페이지 렌더링"""
    
    # CSS
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Space+Mono:wght@400;700&family=Noto+Sans+KR:wght@300;400;500;600;700&display=swap');
        
        :root {
            --bg-dark: #0f0f14;
            --bg-card: #18181f;
            --bg-card-hover: #1e1e28;
            --border: rgba(255,255,255,0.08);
            --border-hover: rgba(255,255,255,0.15);
            --text-primary: #ffffff;
            --text-secondary: rgba(255,255,255,0.6);
            --text-muted: rgba(255,255,255,0.4);
            --accent-primary: #6366f1;
            --accent-secondary: #8b5cf6;
            --accent-glow: rgba(99, 102, 241, 0.3);
            --success: #22c55e;
            --warning: #f59e0b;
            --danger: #ef4444;
            --gradient-primary: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #a855f7 100%);
        }
        
        @keyframes fadeInUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
        
        .page-header {
            padding: 2rem 0;
            animation: fadeInUp 0.6s ease-out;
        }
        
        .page-title {
            font-family: 'Outfit', sans-serif;
            font-size: clamp(1.75rem, 4vw, 2.5rem);
            font-weight: 800;
            color: var(--text-primary);
            margin: 0;
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }
        
        .page-subtitle {
            font-family: 'Noto Sans KR', sans-serif;
            font-size: 1rem;
            color: var(--text-secondary);
            margin-top: 0.25rem;
        }
        
        .search-container {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 20px;
            padding: 1.5rem;
            margin: 1.5rem 0;
            animation: fadeInUp 0.6s ease-out 0.1s backwards;
        }
        
        .search-label {
            font-family: 'Outfit', sans-serif;
            font-size: 0.85rem;
            font-weight: 600;
            color: var(--accent-primary);
            margin-bottom: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .result-card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 20px;
            padding: 1.5rem;
            margin: 1rem 0;
            animation: fadeInUp 0.5s ease-out;
        }
        
        .result-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 0.75rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid var(--border);
            margin-bottom: 1rem;
        }
        
        .result-title {
            font-family: 'Outfit', sans-serif;
            font-size: 1.25rem;
            font-weight: 700;
            color: var(--text-primary);
            margin: 0;
        }
        
        .result-badge {
            font-family: 'Space Mono', monospace;
            font-size: 0.75rem;
            padding: 0.35rem 0.75rem;
            border-radius: 20px;
            background: rgba(99,102,241,0.15);
            color: var(--accent-primary);
        }
        
        .answer-box {
            background: linear-gradient(135deg, rgba(99,102,241,0.1), rgba(139,92,246,0.05));
            border-left: 3px solid var(--accent-primary);
            border-radius: 0 12px 12px 0;
            padding: 1rem 1.25rem;
            margin: 1rem 0;
        }
        
        .answer-box p {
            font-family: 'Noto Sans KR', sans-serif;
            color: var(--text-primary);
            margin: 0;
            line-height: 1.7;
        }
        
        .detail-text {
            font-family: 'Noto Sans KR', sans-serif;
            color: var(--text-secondary);
            line-height: 1.8;
            white-space: pre-wrap;
        }
        
        .status-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.75rem 1.25rem;
            border-radius: 12px;
            font-family: 'Outfit', sans-serif;
            font-weight: 600;
            font-size: 0.9rem;
            animation: fadeIn 0.3s ease-out;
        }
        
        .status-success {
            background: rgba(34, 197, 94, 0.15);
            border: 1px solid rgba(34, 197, 94, 0.3);
            color: var(--success);
        }
        
        .status-warning {
            background: rgba(245, 158, 11, 0.15);
            border: 1px solid rgba(245, 158, 11, 0.3);
            color: var(--warning);
        }
        
        .status-error {
            background: rgba(239, 68, 68, 0.15);
            border: 1px solid rgba(239, 68, 68, 0.3);
            color: var(--danger);
        }
        
        .tag-container {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin: 1rem 0;
        }
        
        .tag {
            font-family: 'Noto Sans KR', sans-serif;
            font-size: 0.85rem;
            color: var(--text-secondary);
            background: var(--bg-card);
            border: 1px solid var(--border);
            padding: 0.5rem 1rem;
            border-radius: 20px;
            cursor: pointer;
            transition: all 0.2s ease;
        }
        
        .tag:hover {
            border-color: var(--accent-primary);
            color: var(--accent-primary);
        }
        
        .stats-row {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
            gap: 1rem;
            margin: 1rem 0;
        }
        
        .stat-item {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1rem;
            text-align: center;
        }
        
        .stat-value {
            font-family: 'Space Mono', monospace;
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--accent-primary);
        }
        
        .stat-label {
            font-family: 'Noto Sans KR', sans-serif;
            font-size: 0.75rem;
            color: var(--text-muted);
            margin-top: 0.25rem;
        }
        
        .footer {
            text-align: center;
            padding: 2rem;
            margin-top: 2rem;
            border-top: 1px solid var(--border);
        }
        
        .footer p {
            font-family: 'Noto Sans KR', sans-serif;
            font-size: 0.8rem;
            color: var(--text-muted);
            margin: 0.25rem 0;
        }
    </style>
    """, unsafe_allow_html=True)

    @st.cache_data
    def load_kb():
        return load_json("kb.json")

    def save_log(query, matched_doc, score):
        append_to_json_list("logs.json", {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "cs_query",
            "query": query,
            "matched_doc_id": matched_doc['id'] if matched_doc else None,
            "matched_title": matched_doc['title'] if matched_doc else None,
            "score": score
        })

    def create_ticket(query, reason):
        ticket_id = get_next_id("tickets.json")
        success = append_to_json_list("tickets.json", {
            "id": ticket_id,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "query": query,
            "reason": reason,
            "status": "open"
        })
        return ticket_id if success else None

    def normalize_text(text):
        text = text.lower().strip()
        text = re.sub(r'[^\w\s가-힣]', ' ', text)
        return re.sub(r'\s+', ' ', text)

    def match_query(query, kb):
        query_norm = normalize_text(query)
        query_words = set(query_norm.split())
        best_match, best_score = None, 0
        
        for doc in kb:
            score = 0
            for kw in [normalize_text(k) for k in doc['keywords']]:
                if kw in query_norm: score += 10
                else: score += len(query_words & set(kw.split())) * 3
            
            title_norm = normalize_text(doc['title'])
            if title_norm in query_norm: score += 15
            else: score += len(query_words & set(title_norm.split())) * 5
            
            if score > best_score:
                best_score, best_match = score, doc
        
        return best_match, best_score

    # 헤더
    st.markdown("""
    <div class="page-header">
        <h1 class="page-title">💬 CS 챗봇</h1>
        <p class="page-subtitle">궁금한 점을 검색해보세요</p>
    </div>
    """, unsafe_allow_html=True)

    # 검색
    st.markdown('<div class="search-container"><div class="search-label">🔍 질문 검색</div></div>', unsafe_allow_html=True)
    query = st.text_input("", placeholder="예: RSI 다이버전스가 뭔가요?", label_visibility="collapsed", key="cs_query")

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        search_btn = st.button("검색하기", type="primary", use_container_width=True, key="cs_search")

    # 검색 처리
    if search_btn and query:
        kb = load_kb()
        matched_doc, score = match_query(query, kb)
        save_log(query, matched_doc, score)
        
        if score >= 10 and matched_doc:
            st.markdown('<div class="status-badge status-success">✓ 관련 정보를 찾았습니다</div>', unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="result-card">
                <div class="result-header">
                    <h3 class="result-title">{matched_doc['title']}</h3>
                    <span class="result-badge">점수 {score}</span>
                </div>
                <div class="answer-box">
                    <p><strong>💡 답변:</strong> {matched_doc['short_answer']}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            with st.expander("📖 상세 내용 보기", expanded=True):
                st.markdown(f'<div class="detail-text">{matched_doc["detailed_answer"]}</div>', unsafe_allow_html=True)
            
            if matched_doc.get('next_actions'):
                st.markdown("**🔗 관련 검색어:**")
                for action in matched_doc['next_actions']:
                    st.markdown(f"→ {action}")
        
        elif score >= 5 and matched_doc:
            st.markdown('<div class="status-badge status-warning">⚠️ 부분 일치하는 정보를 찾았습니다</div>', unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="result-card">
                <div class="result-header">
                    <h3 class="result-title">{matched_doc['title']}</h3>
                    <span class="result-badge">점수 {score}</span>
                </div>
                <div class="answer-box">
                    <p>{matched_doc['short_answer']}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            with st.expander("📖 상세 내용 보기"):
                st.markdown(f'<div class="detail-text">{matched_doc["detailed_answer"]}</div>', unsafe_allow_html=True)
            
            st.info("💡 더 구체적인 키워드로 검색해보세요")
            
            if st.button("🎫 상담 티켓 생성", key="ticket_low"):
                if tid := create_ticket(query, "부분 매칭"):
                    st.success(f"✓ 티켓 #{tid} 생성 완료!")
        
        else:
            st.markdown('<div class="status-badge status-error">✗ 관련 정보를 찾을 수 없습니다</div>', unsafe_allow_html=True)
            
            st.markdown("**💡 이런 키워드로 검색해보세요:**")
            col1, col2, col3, col4 = st.columns(4)
            with col1: st.button("RSI", key="s1")
            with col2: st.button("손절", key="s2")
            with col3: st.button("레버리지", key="s3")
            with col4: st.button("다이버전스", key="s4")
            
            if st.button("🎫 상담 티켓 생성하기", type="primary", key="ticket_none"):
                if tid := create_ticket(query, "매칭 실패"):
                    st.success(f"✓ 티켓 #{tid} 생성 완료!")

    elif search_btn:
        st.warning("검색어를 입력해주세요")

    # 빠른 태그
    st.markdown("---")
    st.markdown("**인기 검색어**")
    st.markdown("""
    <div class="tag-container">
        <span class="tag">RSI</span>
        <span class="tag">손절</span>
        <span class="tag">레버리지</span>
        <span class="tag">다이버전스</span>
        <span class="tag">지지저항</span>
        <span class="tag">멤버십</span>
        <span class="tag">리스크</span>
    </div>
    """, unsafe_allow_html=True)

    # 통계
    st.markdown("---")
    try:
        logs = load_json("logs.json", default=[])
        cs_logs = [l for l in logs if l.get('type') == 'cs_query']
        today = datetime.now().strftime("%Y-%m-%d")
        today_logs = [l for l in cs_logs if l.get('timestamp', '').startswith(today)]
        
        st.markdown(f"""
        <div class="stats-row">
            <div class="stat-item"><div class="stat-value">{len(cs_logs)}</div><div class="stat-label">전체 질문</div></div>
            <div class="stat-item"><div class="stat-value">{len(today_logs)}</div><div class="stat-label">오늘 질문</div></div>
            <div class="stat-item"><div class="stat-value">{len([l for l in today_logs if l.get('score', 0) >= 10])}</div><div class="stat-label">해결됨</div></div>
        </div>
        """, unsafe_allow_html=True)
    except: pass

    # 푸터
    st.markdown("""
    <div class="footer">
        <p>💬 BuyLow CS 챗봇</p>
        <p>키워드 기반 규칙 시스템 | LLM API 미사용</p>
    </div>
    """, unsafe_allow_html=True)
