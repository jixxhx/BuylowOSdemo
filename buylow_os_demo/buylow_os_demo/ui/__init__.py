# -*- coding: utf-8 -*-
"""
BuyLow OS - UI 모듈

공통 UI 컴포넌트와 테마를 제공합니다.
"""
from ui.theme import (
    bootstrap_ui,
    inject_critical_css,
    render_logo,
    render_sidebar,
    render_sidebar_logo,
    render_sidebar_menu,
    COLORS,
)

# 하위 호환성
from ui.theme import bootstrap_ui as init_ui

__all__ = [
    "bootstrap_ui",
    "init_ui",
    "inject_critical_css",
    "render_logo",
    "render_sidebar",
    "render_sidebar_logo",
    "render_sidebar_menu",
    "COLORS",
]
