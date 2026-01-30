# -*- coding: utf-8 -*-
"""
BuyLow OS - 데이터 유틸리티

배포 환경(Streamlit Cloud)과 로컬 환경 모두에서 안전하게 작동하는
파일 읽기/쓰기 함수를 제공합니다.
"""
import json
import os
from pathlib import Path
from typing import Any, Optional, Union
from datetime import datetime


def get_project_root() -> Path:
    """
    프로젝트 루트 디렉토리를 반환합니다.
    Home.py가 있는 디렉토리를 기준으로 합니다.
    """
    # 현재 파일 기준으로 상위 디렉토리로 이동
    current_file = Path(__file__).resolve()
    # utils/data_utils.py -> utils -> project_root
    project_root = current_file.parent.parent
    
    # Home.py가 있는지 확인하여 루트 검증
    if (project_root / "Home.py").exists():
        return project_root
    
    # 환경변수로 설정된 경우 (Streamlit Cloud 대응)
    if os.environ.get("STREAMLIT_APP_ROOT"):
        return Path(os.environ["STREAMLIT_APP_ROOT"])
    
    # 현재 작업 디렉토리 반환 (fallback)
    return Path.cwd()


def get_data_path(filename: str = "") -> Path:
    """
    data 폴더 내 파일 경로를 반환합니다.
    
    Args:
        filename: 파일명 (빈 문자열이면 data 폴더 경로 반환)
    
    Returns:
        절대 경로 Path 객체
    """
    data_dir = get_project_root() / "data"
    if filename:
        return data_dir / filename
    return data_dir


def ensure_data_folder() -> Path:
    """
    data 폴더가 없으면 생성합니다.
    
    Returns:
        data 폴더의 Path 객체
    """
    data_dir = get_data_path()
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir


# 기본 데이터 파일 정의
DATA_FILES = {
    "kb.json": [
        {
            "id": 1,
            "title": "RSI 다이버전스란?",
            "keywords": ["RSI", "다이버전스", "divergence", "과매수", "과매도"],
            "short_answer": "RSI 다이버전스는 가격과 RSI 지표의 방향이 다를 때 발생하는 기술적 시그널입니다.",
            "detailed_answer": "RSI(Relative Strength Index) 다이버전스는 가격이 새로운 고점/저점을 만들 때 RSI는 그에 상응하는 고점/저점을 만들지 못하는 현상입니다.\n\n- 상승 다이버전스: 가격은 저점을 낮추지만 RSI는 저점을 높일 때 → 상승 반전 신호\n- 하락 다이버전스: 가격은 고점을 높이지만 RSI는 고점을 낮출 때 → 하락 반전 신호\n\n다이버전스는 추세 전환의 선행 지표로 활용되지만, 단독 사용보다는 다른 지표와 함께 확인하는 것이 좋습니다.",
            "next_actions": ["지지저항", "추세선", "볼린저밴드"]
        },
        {
            "id": 2,
            "title": "손절 기준 설정하기",
            "keywords": ["손절", "스탑로스", "stop loss", "리스크", "손실"],
            "short_answer": "손절은 손실을 제한하기 위해 미리 정한 가격에서 포지션을 청산하는 것입니다.",
            "detailed_answer": "손절(Stop Loss) 설정 원칙:\n\n1. 진입 전 반드시 손절가 설정\n2. 계좌 대비 1~2% 이내 손실로 제한 권장\n3. 주요 지지/저항선 기준 설정\n4. ATR(Average True Range) 활용 가능\n\n감정적 손절을 피하고, 정해진 규칙대로 실행하는 것이 중요합니다.",
            "next_actions": ["리스크 관리", "포지션 사이징", "레버리지"]
        },
        {
            "id": 3,
            "title": "레버리지 사용 주의사항",
            "keywords": ["레버리지", "leverage", "마진", "청산", "배율"],
            "short_answer": "레버리지는 적은 자본으로 큰 포지션을 잡을 수 있게 하지만, 손실도 그만큼 증폭됩니다.",
            "detailed_answer": "레버리지 사용 시 주의사항:\n\n1. 초보자는 낮은 레버리지(2~5배) 권장\n2. 높은 레버리지 = 높은 청산 위험\n3. 레버리지 올리기 전 손절 설정 필수\n4. 전체 자산의 일부만 마진으로 사용\n\n레버리지는 도구일 뿐, 수익을 보장하지 않습니다.",
            "next_actions": ["손절", "리스크 관리", "포지션 사이징"]
        }
    ],
    "logs.json": [],
    "tickets.json": [],
    "announcements.json": [
        {
            "id": 1,
            "title": "BuyLow OS 출시 안내",
            "content": "BuyLow OS 데모 플랫폼이 출시되었습니다. 교육 및 팀 운영 목적으로 설계된 플랫폼입니다.",
            "date": "2025-01-01",
            "tags": ["공지", "시스템"],
            "pinned": True
        }
    ],
    "homework_submissions.json": [],
    "homework_reviews.json": [],
    "unlocks.json": {},
    "content_versions.json": {},
    "member_profiles.json": {},
    "risk_history.json": []
}


def load_json(filename: str, default: Optional[Any] = None) -> Any:
    """
    JSON 파일을 안전하게 로드합니다.
    
    파일이 없거나 읽기 실패 시 기본값을 반환합니다.
    기본 데이터 파일의 경우 자동으로 생성합니다.
    
    Args:
        filename: 파일명 (예: "kb.json")
        default: 기본값 (None이면 DATA_FILES에서 찾거나 빈 리스트/딕셔너리)
    
    Returns:
        로드된 데이터 또는 기본값
    """
    ensure_data_folder()
    file_path = get_data_path(filename)
    
    # 기본값 결정
    if default is None:
        if filename in DATA_FILES:
            default = DATA_FILES[filename]
        elif filename.endswith(".json"):
            # 파일명으로 추측 (list 또는 dict)
            default = [] if "list" in filename.lower() or filename.endswith("s.json") else {}
        else:
            default = []
    
    try:
        if file_path.exists():
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    return json.loads(content)
                else:
                    # 빈 파일인 경우 기본값 저장 후 반환
                    save_json(filename, default)
                    return default
        else:
            # 파일이 없으면 기본값으로 생성
            save_json(filename, default)
            return default
            
    except (json.JSONDecodeError, IOError, OSError) as e:
        # 오류 발생 시 기본값 반환 (배포 환경에서 안전하게)
        print(f"[data_utils] Warning: Failed to load {filename}: {e}")
        return default


def save_json(filename: str, data: Any) -> bool:
    """
    JSON 파일을 안전하게 저장합니다.
    
    Args:
        filename: 파일명 (예: "logs.json")
        data: 저장할 데이터
    
    Returns:
        성공 여부
    """
    ensure_data_folder()
    file_path = get_data_path(filename)
    
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
        
    except (IOError, OSError) as e:
        # Streamlit Cloud에서 쓰기 실패할 수 있음
        print(f"[data_utils] Warning: Failed to save {filename}: {e}")
        return False


def append_to_json_list(filename: str, item: dict) -> bool:
    """
    JSON 리스트 파일에 항목을 추가합니다.
    
    Args:
        filename: 파일명
        item: 추가할 딕셔너리
    
    Returns:
        성공 여부
    """
    data = load_json(filename, default=[])
    if not isinstance(data, list):
        data = []
    data.append(item)
    return save_json(filename, data)


def get_next_id(filename: str) -> int:
    """
    JSON 리스트 파일에서 다음 ID를 반환합니다.
    
    Args:
        filename: 파일명
    
    Returns:
        다음 사용 가능한 ID
    """
    data = load_json(filename, default=[])
    if not isinstance(data, list) or not data:
        return 1
    
    max_id = max((item.get("id", 0) for item in data if isinstance(item, dict)), default=0)
    return max_id + 1
