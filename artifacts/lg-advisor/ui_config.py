"""범용 LG 가전 상담 UI 설정 — 카테고리, 질문, 선택지를 모두 데이터로 주입.
이 파일만 교체하면 냉장고/세탁기/TV/에어컨 등 어떤 가전이든 동작합니다.
"""
from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class OptionConfig:
    value: str
    label: str
    desc: str
    icon_key: str = "default"


@dataclass
class QuestionConfig:
    q_id: str
    text: str          # HTML 가능 — <strong>, <span class="accent">
    options: List[OptionConfig]


@dataclass
class CategoryConfig:
    name: str          # "냉장고", "세탁기", "TV" …
    subtitle: str
    questions: Dict[str, QuestionConfig] = field(default_factory=dict)


# ── SVG 라인 아이콘 (24×24 viewBox, stroke-based) ──────────────────────────
ICONS: Dict[str, str] = {
    "builtin": (
        '<path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>'
        '<polyline points="9,22 9,12 15,12 15,22"/>'
    ),
    "fitmax": (
        '<rect x="2" y="3" width="8" height="18" rx="1.5"/>'
        '<rect x="14" y="3" width="8" height="18" rx="1.5"/>'
        '<path d="M10 12h4"/>'
    ),
    "freestanding": (
        '<rect x="4" y="2" width="16" height="20" rx="2"/>'
        '<line x1="8" y1="7" x2="13" y2="7"/>'
        '<line x1="8" y1="11" x2="11" y2="11"/>'
    ),
    "solo": (
        '<circle cx="12" cy="7" r="4"/>'
        '<path d="M5.2 21a8.8 8.8 0 0 1 13.6 0"/>'
    ),
    "couple": (
        '<circle cx="8" cy="8" r="3.5"/>'
        '<path d="M2 21a7 7 0 0 1 12 0"/>'
        '<circle cx="17.5" cy="8" r="3"/>'
        '<path d="M14 21a5.5 5.5 0 0 1 7 0"/>'
    ),
    "family": (
        '<circle cx="9" cy="7" r="3"/>'
        '<path d="M3 21a7 7 0 0 1 12 0"/>'
        '<path d="M16 3.13a4 4 0 0 1 0 7.75"/>'
        '<path d="M21 21c0-2.4-1.9-4.4-4.4-5"/>'
    ),
    "no-cooking": (
        '<path d="M3 11h18v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-7z"/>'
        '<path d="M3 11l2-7h14l2 7"/>'
        '<path d="M12 11v9"/>'
    ),
    "sometimes-cooking": (
        '<path d="M8 2v4M12 2v4M16 2v4"/>'
        '<rect x="3" y="6" width="18" height="15" rx="2"/>'
        '<path d="M6 12h4M6 16h3"/>'
    ),
    "often-cooking": (
        '<path d="M3 2v7c0 1.1.9 2 2 2h4a2 2 0 0 0 2-2V2"/>'
        '<path d="M7 2v20"/>'
        '<path d="M21 15V2c-2.8 0-5 2.2-5 5v6c0 1.1.9 2 2 2h3"/>'
        '<path d="M18 15v7"/>'
    ),
    "love-cooking": (
        '<path d="M3 2v7c0 1.1.9 2 2 2h4a2 2 0 0 0 2-2V2"/>'
        '<path d="M7 2v20"/>'
        '<path d="M21 15V2c-2.8 0-5 2.2-5 5v6c0 1.1.9 2 2 2h3"/>'
        '<path d="M18 15v7"/>'
        '<path d="M12 8h4"/>'
    ),
    "side-by-side": (
        '<rect x="2" y="3" width="9" height="18" rx="2"/>'
        '<rect x="13" y="3" width="9" height="18" rx="2"/>'
        '<path d="M6 9h2M6 13h2M16 9h2M16 13h2"/>'
    ),
    "4door": (
        '<rect x="2" y="3" width="20" height="8" rx="2"/>'
        '<rect x="2" y="13" width="9" height="8" rx="2"/>'
        '<rect x="13" y="13" width="9" height="8" rx="2"/>'
        '<path d="M6 7h3M15 7h3"/>'
    ),
    "4door-ai": (
        '<rect x="2" y="3" width="20" height="8" rx="2"/>'
        '<rect x="2" y="13" width="9" height="8" rx="2"/>'
        '<rect x="13" y="13" width="9" height="8" rx="2"/>'
        '<circle cx="17.5" cy="5.5" r="1"/><circle cx="20" cy="7" r="1"/>'
        '<circle cx="15" cy="7" r="1"/>'
    ),
    "slim": (
        '<rect x="8" y="2" width="8" height="20" rx="2"/>'
        '<path d="M4 5v14M20 5v14"/>'
    ),
    "normal": (
        '<rect x="4" y="2" width="16" height="20" rx="2"/>'
        '<path d="M8 8h5M8 13h3"/>'
    ),
    "wide": (
        '<rect x="2" y="2" width="20" height="20" rx="2"/>'
        '<path d="M8 2v20M16 2v20"/>'
    ),
    "default": (
        '<circle cx="12" cy="12" r="9"/>'
        '<path d="M12 8v4l3 3"/>'
    ),
}


# ── 냉장고 카테고리 설정 ────────────────────────────────────────────────────
REFRIGERATOR_CONFIG = CategoryConfig(
    name="냉장고",
    subtitle="몇 가지만 답하면, 딱 맞는 제품을 찾아드려요.",
    questions={
        "install": QuestionConfig(
            q_id="install",
            text="냉장고를 <strong>어떻게 설치</strong>하실 계획이세요?",
            options=[
                OptionConfig("빌트인",     "빌트인",      "가구장에 완전히 통합",       "builtin"),
                OptionConfig("Fit & Max",  "Fit & Max",  "기존 가구 사이에 빈틈 없이",  "fitmax"),
                OptionConfig("프리스탠딩", "프리스탠딩",  "원하는 자리에 자유롭게",     "freestanding"),
            ],
        ),
        "household": QuestionConfig(
            q_id="household",
            text="<strong>몇 분이</strong> 함께 사용하시나요?",
            options=[
                OptionConfig("solo",   "혼자 살아요",         "1인 가구에 최적화된 용량으로",  "solo"),
                OptionConfig("two",    "둘이 살아요",         "2인 생활에 딱 맞는 사이즈로",   "couple"),
                OptionConfig("family", "3인 이상 가족이에요", "넉넉한 용량으로 여유롭게",      "family"),
            ],
        ),
        "cooking": QuestionConfig(
            q_id="cooking",
            text="<strong>요리는 얼마나 자주</strong> 하세요?",
            options=[
                OptionConfig("none",      "거의 안 해요",  "배달·간편식 위주로",       "no-cooking"),
                OptionConfig("sometimes", "가끔 해요",     "가끔 직접 요리해요",       "sometimes-cooking"),
                OptionConfig("often",     "자주 해요",     "식재료를 꽤 많이 둬요",    "often-cooking"),
                OptionConfig("love",      "요리를 즐겨요", "신선 재료를 가득 보관해요", "love-cooking"),
            ],
        ),
        "door_style": QuestionConfig(
            q_id="door_style",
            text="<strong>문 여는 방식</strong>은 어떤 게 편하세요?",
            options=[
                OptionConfig("양문형",      "양문형",       "좌우로 활짝 — 넓은 수납공간",    "side-by-side"),
                OptionConfig("4도어_no_ai", "4도어",        "위·아래 분리 — 합리적인 선택",   "4door"),
                OptionConfig("4도어_ai",    "4도어 + AI",   "AI 자동 절전·신선 케어",         "4door-ai"),
            ],
        ),
        "space": QuestionConfig(
            q_id="space",
            text="설치 공간의 <strong>폭</strong>은 어느 정도예요?",
            options=[
                OptionConfig("slim",   "슬림  (60cm 이하)", "좁은 공간에도 꼭 맞게",   "slim"),
                OptionConfig("normal", "일반  (60~90cm)",   "표준 주방 공간에 맞게",   "normal"),
                OptionConfig("roomy",  "넉넉  (90cm 이상)", "공간 여유가 있어요",      "wide"),
            ],
        ),
    },
)
