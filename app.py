import json
import streamlit as st

# 1. 페이지 기본 설정 및 브라우저 탭 아이콘
st.set_page_config(
    page_title="클래식 영문법 노트",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 2. 책 감성을 살리기 위한 커스텀 CSS 스타일 적용
st.markdown(
    """
    <style>
    .main {
        background-color: #FAF8F5;
    }
    .book-page {
        background-color: #FFFFFF;
        border: 1px solid #EAE5D9;
        border-radius: 12px;
        padding: 40px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.04);
        margin-top: 10px;
    }
    .chapter-badge {
        display: inline-block;
        background-color: #EFECE6;
        color: #555047;
        font-size: 0.85rem;
        font-weight: bold;
        padding: 4px 12px;
        border-radius: 20px;
        margin-bottom: 12px;
    }
    section[data-testid="stSidebar"] {
        background-color: #F3EFEA;
        border-right: 1px solid #E5DFD5;
    }
    </style>
""",
    unsafe_allow_html=True,
)


# 3. 데이터 로드 함수
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

if not data:
    st.warning("등록된 문법 데이터가 없습니다. grammar.json을 확인해 주세요.")
    st.stop()

# 4. 사이드바 - 책 목차 (Topics) 구성
st.sidebar.title("📖 목차 (Contents)")
st.sidebar.markdown("---")

categories = list(dict.fromkeys([item["category"] for item in data]))

for cat in categories:
    st.sidebar.markdown(f"**{cat}**")
    cat_items = [item for item in data if item["category"] == cat]

    for item in cat_items:
        button_label = f"📄 {item['title']}"
        if st.sidebar.button(button_label, key=item["title"]):
            st.session_state["selected_title"] = item["title"]

    st.sidebar.markdown("<br>", unsafe_allow_html=True)

if "selected_title" not in st.session_state:
    st.session_state["selected_title"] = data[0]["title"]

current_item = next(
    (
        item
        for item in data
        if item["title"] == st.session_state["selected_title"]
    ),
    data[0],
)

# 5. 메인 영역 - 책 한 페이지처럼 출력
st.markdown("<div class='book-page'>", unsafe_allow_html=True)

st.markdown(
    f"<div class='chapter-badge'>{current_item['category']}</div>",
    unsafe_allow_html=True,
)
st.title(f"🖋️ {current_item['title']}")
st.markdown("---")

st.subheader("💡 Key Point & Formula")
st.code(current_item["formula"], language="text")

st.markdown("<br>", unsafe_allow_html=True)

st.subheader("📚 개념 상세 원리")
st.write(current_item["explanation"])

st.markdown("<br>", unsafe_allow_html=True)

st.subheader("✍️ 실전 예문 노트")
for ex in current_item["examples"]:
    if "[오답]" in ex or "(X)" in ex or "X" in ex:
        st.error(f"❌ {ex}")
    elif "[정답]" in ex or "(O)" in ex or "O" in ex:
        st.success(f"✅ {ex}")
    else:
        st.info(f"🔹 {ex}")

if "tips" in current_item and current_item["tips"]:
    st.markdown("<br>", unsafe_allow_html=True)
    st.warning(f"📌 **Teacher's Secret Note**\n\n{current_item['tips']}")

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")
st.caption("👈 왼쪽 목차에서 원하는 토픽을 클릭하면 해당 페이지로 이동합니다.")
