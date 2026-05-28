# LG 냉장고 상담 매니저

LG 베스트샵 매니저처럼 몇 가지 질문으로 딱 맞는 냉장고를 추천해주는 상담형 웹앱입니다.

## Run & Operate

- `artifacts/lg-advisor: web` 워크플로우로 Streamlit 앱 실행 (포트 5000)
- `pnpm --filter @workspace/api-server run dev` — API 서버 실행 (포트 5000은 Streamlit 전용)
- `pnpm run typecheck` — 전체 타입 체크
- 엑셀 실제 데이터 사용 시: `LG_냉장고_대표상품기준_통합DB.xlsx` 파일을 `artifacts/lg-advisor/` 폴더에 업로드

## Stack

- pnpm workspaces, Node.js 24, TypeScript 5.9
- Streamlit (Python) — 메인 상담 앱
- API: Express 5
- DB: PostgreSQL + Drizzle ORM (미사용)
- Validation: Zod (`zod/v4`), `drizzle-zod`

## Where things live

- `artifacts/lg-advisor/` — Streamlit 앱 메인 폴더
  - `app.py` — Streamlit UI (질문 흐름, 결과 카드)
  - `engine.py` — 상담 로직 (질문 순서, 하드 필터, 채점)
  - `data_loader.py` — 엑셀 DB 파싱 + 샘플 데이터 폴백
  - `.streamlit/config.toml` — Streamlit 서버 설정 (CORS 허용, 포트 5000)
- `artifacts/api-server/` — Express API 서버 (현재 미사용)

## Architecture decisions

- 엑셀 파일 없이도 13개 샘플 제품으로 동작하는 폴백 구조
- 설치형태 → 가구원수·요리습관 → 용량 → 도어방식 → 추가기능 → 결과 순서의 결정 트리
- 후보가 1개로 좁혀지면 남은 질문은 자동으로 건너뜀
- Streamlit이 Replit 프록시 도메인의 WebSocket을 허용하도록 `enableCORS = false`, `enableXsrfProtection = false` 설정

## Product

- Q1 설치형태: 빌트인 / Fit & Max / 프리스탠딩
- Q2 가구원수 + 요리습관 → 목표 용량 결정
- Q2-1 도어방식 (800L+ 대용량만): 양문형 / 4도어 / 4도어 AI
- Q3 설치공간(폭): 슬림(60cm 이하) / 일반 / 넉넉
- Q4 추가기능 선택 (후보가 가진 기능만 표시)
- 결과: 최우선 추천 1개 + 비교 제품 2개, 추천 이유 설명

## User preferences

- 한국어로 응답

## Gotchas

- 실제 엑셀 파일을 `artifacts/lg-advisor/` 폴더에 올리면 자동으로 실제 데이터 사용
- Streamlit 워크플로우는 `artifacts/lg-advisor: web` (자동 생성)
- `streamlit-app/` 폴더 대신 `artifacts/lg-advisor/` 폴더에 파일이 있음

## Pointers

- See the `pnpm-workspace` skill for workspace structure, TypeScript setup, and package details
