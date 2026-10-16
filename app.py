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
    /* 전체 배경을 따뜻한 양식지/종이 느낌으로 설정 */
    .main {
        background-color: #FAF8F5;
    }
    
    /* 책 내지 느낌의 컨테이너 박스 */
    .book-page {
        background-color: #FFFFFF;
        border: 1px solid #EAE5D9;
        border-radius: 12px;
        padding: 40px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.04);
        margin-top: 10px;
    }
    
    /* 챕터 배지 스타일 */
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

    /* 사이드바 스타일링 */
    section[data-testid="stSidebar"] {
        background-color: #F3EFEA;
        border-right: 1px solid #E5DFD5;
    }
    </style>
""",
    unsafe_allow_code=True,
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

# 카테고리(PART) 별로 아이템 그룹핑
categories = list(dict.fromkeys([item["category"] for item in data]))

# 카테고리 및 해당 토픽(Topic)을 선택하는 라디오 버튼 생성
selected_topic_title = None

for cat in categories:
    st.sidebar.markdown(f"**{cat}**")
    # 해당 카테고리에 속한 토픽들의 타이틀 리스트 추출
    cat_items = [item for item in data if item["category"] == cat]

    for item in cat_items:
        # 각 토픽을 클릭 가능한 버튼 형태로 배치
        button_label = f"📄 {item['title']}"
        if st.sidebar.button(button_label, key=item["title"]):
            st.session_state["selected_title"] = item["title"]

    st.sidebar.markdown("<br>", unsafe_allow_code=True)

# 기본 세션 상태 설정 (처음 접속 시 첫 번째 토픽 선택)
if "selected_title" not in st.session_state:
    st.session_state["selected_title"] = data[0]["title"]

# 선택된 데이터 추출
current_item = next(
    (
        item
        for item in data
        if item["title"] == st.session_state["selected_title"]
    ),
    data[0],
)

# 5. 메인 영역 - 책 한 페이지처럼 출력
st.markdown("<div class='book-page'>", unsafe_allow_code=True)

# 상단 챕터 배지 및 제목
st.markdown(
    f"<div class='chapter-badge'>{current_item['category']}</div>",
    unsafe_allow_code=True,
)
st.title(f"🖋️ {current_item['title']}")
st.markdown("---")

# [섹션 1] 핵심 공식 & 레시피 틀
st.subheader("💡 Key Point & Formula")
st.code(current_item["formula"], language="text")

st.markdown("<br>", unsafe_allow_code=True)

# [섹션 2] 상세 개념 원리 (책의 본문 설명)
st.subheader("📚 개념 핵심 원리")
st.write(current_item["explanation"])

st.markdown("<br>", unsafe_allow_code=True)

# [섹션 3] 실전 예문 노트
st.subheader("✍️ 실전 예문 노트")
for ex in current_item["examples"]:
    if "[오답]" in ex or "(X)" in ex or "X" in ex:
        st.error(f"❌ {ex}")
    elif "[정답]" in ex or "(O)" in ex or "O" in ex:
        st.success(f"✅ {ex}")
    else:
        st.info(f"🔹 {ex}")

# [섹션 4] 시험 출제 포인트 / 꿀팁
if "tips" in current_item and current_item["tips"]:
    st.markdown("<br>", unsafe_allow_code=True)
    st.warning(f"📌 **Teacher's Secret Note**\n\n{current_item['tips']}")

st.markdown("</div>", unsafe_allow_code=True)

# 6. 하단 페이지 넘김 안내
st.markdown("---")
st.caption("👈 왼쪽 목차에서 원하는 토픽을 클릭하면 해당 페이지로 이동합니다.")
