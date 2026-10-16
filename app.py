import json
import streamlit as st

# 1. 웹페이지 기본 설정을 지정합니다.
st.set_page_config(
    page_title="고등 핵심 영어 문법 정리책", page_icon="📘", layout="wide"
)


# 2. JSON 데이터 불러오기 함수 (성능 최적화를 위해 캐싱 처리)
@st.cache_data
def load_data():
    try:
        with open("data/grammar.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        st.error(
            "data/grammar.json 파일을 찾을 수 없습니다. 경로를 확인해 주세요."
        )
        return []


data = load_data()

# 3. 메인 상단 헤더 영역
st.title("📘 고등 핵심 영어 문법 정복 가이드")
st.caption(
    "초등학생도 한눈에 이해할 수 있는 명쾌하고 구체적인 문법 핵심 정리 노트"
)
st.markdown("---")

if not data:
    st.warning("등록된 문법 데이터가 없습니다.")
    st.stop()

# 4. 사이드바 구성 (검색 및 카테고리 선택)
st.sidebar.header("🔍 문법 검색 & 목차")

# 4-1. 키워드 검색창
search_query = st.sidebar.text_input(
    "검색할 단어나 문법 개념 입력",
    placeholder="예: 사역동사, 부정사, 현재완료...",
)

# 4-2. 카테고리 목록 추출 및 선택 박스
categories = sorted(list(set(item["category"] for item in data)))
selected_category = st.sidebar.selectbox("📖 PART 별 선택", categories)

# 5. 검색어 여부에 따른 데이터 필터링
if search_query:
    filtered_data = [
        item
        for item in data
        if search_query.lower() in item["title"].lower()
        or search_query.lower() in item["explanation"].lower()
        or search_query.lower() in item["category"].lower()
    ]
    st.subheader(f"🔍 '{search_query}' 검색 결과 ({len(filtered_data)}건)")
else:
    filtered_data = [
        item for item in data if item["category"] == selected_category
    ]
    st.subheader(f"📌 {selected_category}")

st.write("")

# 6. 본문 화면에 문법 내용 카드(Expander) 형태로 출력
if not filtered_data:
    st.info("검색 결과에 해당하는 문법 내용이 없습니다.")
else:
    for entry in filtered_data:
        # 각 문법 주제별 카드 열기
        with st.expander(f"✨ {entry['title']}", expanded=True):
            # 핵심 공식 / 형태
            st.markdown(f"**📌 핵심 공식 / 기본 틀:**")
            st.code(entry["formula"], language="text")

            # 개념 원리 및 상황별 상세 설명
            st.markdown("**📖 개념 상세 원리 & 언제 쓰는가?**")
            st.write(entry["explanation"])

            st.markdown("---")

            # 실전 예문 및 오답 파악
            st.markdown("**💬 대표 예문 & 실전 적용**")
            for ex in entry["examples"]:
                if ex.startswith("[오답]") or "X" in ex:
                    st.markdown(f"- ❌ {ex}")
                elif ex.startswith("[정답]") or "O" in ex:
                    st.markdown(f"- ✅ {ex}")
                else:
                    st.markdown(f"- 🔹 {ex}")

            # 시험 출제 포인트 & Tip
            if "tips" in entry and entry["tips"]:
                st.write("")
                st.info(f"{entry['tips']}")

# 7. 하단 안내 문구
st.markdown("---")
st.caption(
    "💡 Tip: 새로운 문법 내용을 추가하거나 수정하고 싶다면 `data/grammar.json` 파일만 업데이트해 주세요!"
)
