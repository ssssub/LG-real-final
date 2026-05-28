"""LG 냉장고 온라인 상담 — 베스트샵 매니저 경험을 웹에서."""
import streamlit as st
from data_loader import load_products, SOFT_FEATURES
import engine as E

st.set_page_config(page_title="LG 냉장고 상담 매니저", page_icon="❄️", layout="centered")

PRODUCTS, IS_SAMPLE = load_products()

if "answers" not in st.session_state:
    st.session_state.answers = {}
ans = st.session_state.answers


def reset():
    st.session_state.answers = {}


def crumbs():
    labels = []
    if ans.get("install"):
        labels.append(ans["install"])
    hh = dict(E.HOUSEHOLD_OPTS).get(ans.get("household"))
    if hh:
        labels.append(hh)
    ck = dict(E.COOKING_OPTS).get(ans.get("cooking"))
    if ck:
        labels.append(ck.split(" (")[0])
    if ans.get("door_style"):
        labels.append({"양문형": "양문형", "4도어_no_ai": "4도어",
                       "4도어_ai": "4도어 AI"}[ans["door_style"]])
    if labels:
        st.caption("선택: " + "  ·  ".join(labels))


def ask_buttons(opts, key):
    for opt in opts:
        val, label = opt[0], opt[1]
        sub = opt[2] if len(opt) > 2 else None
        btn_label = f"{label}\n\n{sub}" if sub else label
        if st.button(btn_label, key=f"{key}_{val}", use_container_width=True):
            ans[key] = val
            st.rerun()


# ── 헤더 ──
st.title("❄️ LG 냉장고 상담")
st.caption("베스트샵 매니저처럼, 몇 가지만 여쭤보고 딱 맞는 냉장고를 찾아드려요.")

if IS_SAMPLE:
    st.info(
        "⚠️ 지금은 **시연용 샘플 데이터** (13개 제품)로 동작 중이에요.\n\n"
        "실제 제품 데이터를 사용하려면 `LG_냉장고_대표상품기준_통합DB.xlsx` 파일을 "
        "`streamlit-app/` 폴더에 업로드하세요.",
        icon="📋"
    )

crumbs()

q = E.next_question(PRODUCTS, ans)

# ── 질문 단계 ──
if q == "install":
    st.info("안녕하세요! 냉장고를 **어떻게 설치**하실 계획이세요?")
    ask_buttons(E.INSTALL_OPTS, "install")

elif q == "household":
    st.info("네, 좋아요. **몇 분이** 함께 쓰실 냉장고일까요?")
    ask_buttons(E.HOUSEHOLD_OPTS, "household")

elif q == "cooking":
    st.info("**요리는 얼마나 자주** 하시는 편이에요? 보관할 식재료 양을 가늠하려고요.")
    ask_buttons(E.COOKING_OPTS, "cooking")

elif q == "door_style":
    st.info("대용량으로 보시는군요! **문 여는 방식**은 어떤 게 편하세요?")
    ask_buttons([
        ("양문형", "양문형", "좌우로 활짝 — 폭이 넉넉해요"),
        ("4도어_no_ai", "4도어", "위·아래 분리 — 합리적인 선택"),
        ("4도어_ai", "4도어 + AI", "자동 절전·신선 케어까지"),
    ], "door_style")

elif q == "space":
    st.info("설치하실 **자리 폭**은 어느 정도예요?")
    ask_buttons([
        ("slim", "좁은 편이에요", "슬림하게 들어가야 해요 (폭 60cm 이하)"),
        ("normal", "일반적이에요", "보통 주방 공간"),
        ("roomy", "넉넉해요", "공간 여유가 있어요"),
    ], "space")

elif q == "features":
    cand, _ = E.filter_candidates(PRODUCTS, ans)
    feats = E.available_soft_features(cand)
    st.info("거의 다 왔어요! **특별히 원하시는 기능**이 있으면 골라주세요. (없으면 그냥 넘어가셔도 돼요)")
    chosen = []
    for key, label in feats:
        if st.checkbox(label, key=f"feat_{key}"):
            chosen.append(key)
    if st.button("이걸로 추천받기", type="primary", use_container_width=True):
        ans["wanted_features"] = chosen
        st.rerun()

# ── 결과 ──
elif q == "result":
    cand, tier = E.filter_candidates(PRODUCTS, ans)
    if "wanted_features" not in ans:
        ans["wanted_features"] = []
    ranked = E.score_and_rank(cand, ans)

    if not ranked:
        st.warning("조건에 딱 맞는 제품을 못 찾았어요. 처음부터 다시 해볼까요?")
    else:
        top_score, top, top_hit = ranked[0]
        st.success("고객님께는 **이 냉장고**를 추천드려요!")

        def show_card(p, is_top=False):
            if is_top:
                st.markdown("### 🏆 최우선 추천")
            price_str = (f"{p['price_min']:,}원" if p["price_min"] == p["price_max"]
                         else f"{p['price_min']:,} ~ {p['price_max']:,}원") if p["price_min"] else "가격 미정"
            color_str = ", ".join(p["colors"][:4]) if p["colors"] else "-"
            feat_tags = "  ".join(
                f"`{SOFT_FEATURES[k][0].split(' (')[0]}`" for k in sorted(p["features"])
            )
            with st.container(border=True):
                st.markdown(f"**{p['name']}**")
                st.caption(f"{p['code']} · {p['install']} · {p['doors']} · 총 {p['total_l']}L · 에너지 {p['energy']}등급")
                st.markdown(f"💰 **{price_str}**")
                if feat_tags:
                    st.markdown(feat_tags)
                st.caption(f"색상: {color_str}　|　크기(WxHxD): {p['size_raw']}")

        show_card(top, is_top=True)

        st.markdown("**이 제품을 추천드리는 이유**")
        for r in E.reasons_for(top, ans, tier):
            st.markdown(f"- {r}")

        alts = ranked[1:3]
        if alts:
            st.divider()
            st.markdown("**함께 비교해 보면 좋은 제품**")
            for sc, p, hit in alts:
                show_card(p, is_top=False)

    st.divider()
    if st.button("처음부터 다시 상담", use_container_width=True, type="primary"):
        reset()
        st.rerun()

# ── 뒤로/리셋 (질문 중에만) ──
if q != "result" and ans:
    st.markdown("")
    if st.button("← 처음부터", key="restart_top"):
        reset()
        st.rerun()
