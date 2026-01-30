# BuyLow OS

트레이딩 팀을 위한 운영 플랫폼 데모

## 주요 기능

- 💬 **CS 챗봇** - 키워드 기반 FAQ 검색
- 🧭 **진단 퀴즈** - 트레이딩 기초 지식 점검
- 📤 **과제 제출** - 주제별 분석 과제 및 콘텐츠 언락
- 🛡️ **리스크 체크** - 매매 전 위험 요소 점검
- 📢 **공지 허브** - 팀 공지 통합 관리
- 📊 **운영자 대시보드** - 팀 현황 모니터링

## 중요 안내

⚠️ **본 플랫폼은 교육 및 팀 운영 목적으로 설계되었습니다.**

- 매매 추천, 가격 예측, 종목 추천 기능이 없습니다
- 투자 권유가 아닙니다
- LLM API를 사용하지 않습니다
- 거래소 연동, 자금 접근 기능이 없습니다

---

## 로컬 실행

### 1. 요구사항

- Python 3.9 이상
- pip (패키지 관리자)

### 2. 설치

```bash
# 가상환경 생성 (권장)
python -m venv venv

# 가상환경 활성화
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 의존성 설치
pip install -r requirements.txt
```

### 3. 실행

```bash
streamlit run Home.py
```

브라우저에서 `http://localhost:8501` 접속

---

## Streamlit Community Cloud 배포

### 1단계: GitHub에 업로드

1. GitHub에 새 저장소 생성 (예: `buylow-os-demo`)
2. 이 폴더의 모든 파일을 해당 저장소에 업로드
   - `Home.py` (루트에 위치)
   - `requirements.txt`
   - `.streamlit/config.toml`
   - `app_pages/` 폴더
   - `ui/` 폴더
   - `utils/` 폴더
   - `data/` 폴더
   - `assets/` 폴더

### 2단계: Streamlit Cloud 연결

1. [share.streamlit.io](https://share.streamlit.io) 접속
2. GitHub 계정으로 로그인
3. **New app** 클릭
4. 설정:
   - **Repository**: `your-username/buylow-os-demo`
   - **Branch**: `main`
   - **Main file path**: `Home.py`
5. **Deploy** 클릭

### 3단계: 배포 확인

배포 완료 후 `https://your-app-name.streamlit.app` 형태의 URL이 생성됩니다.

---

## 프로젝트 구조

```
buylow_os_demo/
├── Home.py                 # 메인 엔트리 포인트
├── requirements.txt        # 의존성 목록
├── README.md
├── .gitignore
│
├── .streamlit/
│   └── config.toml         # Streamlit 설정 (다크 테마)
│
├── app_pages/              # 페이지 모듈
│   ├── __init__.py         # 라우트 매핑
│   ├── cs_chat.py
│   ├── quiz.py
│   ├── homework.py
│   ├── risk_check.py
│   ├── admin.py
│   ├── announcements.py
│   ├── onboarding.py
│   ├── operator_dashboard.py
│   ├── content_library.py
│   ├── grading_assistant.py
│   ├── unlocked_lessons.py
│   └── advanced_practice.py
│
├── ui/                     # UI 컴포넌트
│   ├── __init__.py
│   ├── theme.py            # 테마 및 CSS
│   └── sidebar.py
│
├── utils/                  # 유틸리티
│   ├── __init__.py
│   └── data_utils.py       # 안전한 파일 읽기/쓰기
│
├── data/                   # 데이터 파일 (JSON)
│   ├── kb.json             # CS 챗봇 지식베이스
│   ├── logs.json
│   ├── tickets.json
│   ├── announcements.json
│   ├── homework_submissions.json
│   ├── homework_reviews.json
│   ├── unlocks.json
│   ├── content_versions.json
│   ├── member_profiles.json
│   └── risk_history.json
│
└── assets/                 # 정적 에셋
    └── .gitkeep
```

---

## 배포 전 체크리스트

- [ ] `requirements.txt`에 모든 의존성 포함 확인
- [ ] `.streamlit/config.toml` 존재 확인
- [ ] `Home.py`가 루트에 위치 확인
- [ ] `data/` 폴더와 기본 JSON 파일 존재 확인
- [ ] `utils/__init__.py` 존재 확인
- [ ] `app_pages/__init__.py` 존재 확인
- [ ] `ui/__init__.py` 존재 확인

### 로컬 테스트

```bash
# 의존성만 설치하고 실행 (가상환경 권장)
pip install -r requirements.txt
streamlit run Home.py

# data 폴더 삭제 후 테스트 (자동 생성 확인)
# rm -rf data/
# streamlit run Home.py
```

---

## 문제 해결

### ModuleNotFoundError 발생 시

1. `utils/__init__.py`, `app_pages/__init__.py`, `ui/__init__.py` 존재 확인
2. `requirements.txt`에 필요한 패키지 포함 확인
3. Streamlit Cloud에서 재배포 시도

### data 파일 관련 오류

- `data/` 폴더와 JSON 파일은 앱 첫 실행 시 자동 생성됩니다
- Streamlit Cloud에서는 파일 쓰기가 제한될 수 있으나, 읽기는 정상 동작합니다

### 화면이 다르게 보이는 경우

- `.streamlit/config.toml` 파일이 GitHub에 포함되었는지 확인
- 브라우저 캐시 삭제 후 재접속

---

## 라이선스

본 프로젝트는 교육 및 데모 목적으로 제작되었습니다.
