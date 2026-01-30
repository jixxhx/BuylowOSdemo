# app_pages 모듈 초기화
# 각 페이지 모듈을 임포트하여 render() 함수로 접근 가능하게 함

from app_pages import (
    cs_chat,
    quiz,
    homework,
    risk_check,
    admin,
    announcements,
    onboarding,
    operator_dashboard,
    content_library,
    grading_assistant,
    unlocked_lessons,
    advanced_practice
)

# 라우트 매핑
ROUTES = {
    "home": None,  # Home은 Home.py에서 직접 처리
    "cs_chat": cs_chat,
    "quiz": quiz,
    "homework": homework,
    "risk_check": risk_check,
    "admin": admin,
    "announcements": announcements,
    "onboarding": onboarding,
    "operator_dashboard": operator_dashboard,
    "content_library": content_library,
    "grading_assistant": grading_assistant,
    "unlocked_lessons": unlocked_lessons,
    "advanced_practice": advanced_practice,
}

__all__ = ["ROUTES"]
