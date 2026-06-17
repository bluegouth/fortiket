import math
from PIL import Image

import streamlit as st
from streamlit_image_coordinates import streamlit_image_coordinates

st.set_page_config(
    page_title="포티켓 챌린지",
    page_icon="📸",
    layout="wide"
)

# =========================
# 초기화
# =========================

if "quiz_stamp" not in st.session_state:
    st.session_state.quiz_stamp = False

if "spot_stamp" not in st.session_state:
    st.session_state.spot_stamp = False

if "ai_stamp" not in st.session_state:
    st.session_state.ai_stamp = False

if "found_1" not in st.session_state:
    st.session_state.found_1 = []

if "found_2" not in st.session_state:
    st.session_state.found_2 = []

# =========================
# 유틸
# =========================

def stamp_count():
    return sum([
        st.session_state.quiz_stamp,
        st.session_state.spot_stamp,
        st.session_state.ai_stamp
    ])

def check_click(x, y, answers, found):
    RADIUS = 50

    for i, (ax, ay) in enumerate(answers):

        if i in found:
            continue

        dist = math.sqrt((x-ax)**2 + (y-ay)**2)

        if dist <= RADIUS:
            return i

    return None

# =========================
# 사이드바
# =========================

page = st.sidebar.radio(
    "메뉴",
    [
        "홈",
        "퀴즈",
        "틀린 그림 찾기",
        "AI 합성 체험"
    ]
)

# =========================
# 홈
# =========================

if page == "홈":

    st.title("📸 포티켓 챌린지")

    st.write("3개의 체험을 완료하고 도장을 모아보세요!")

    c1, c2, c3 = st.columns(3)

    with c1:
        if st.session_state.quiz_stamp:
            st.success("📝 퀴즈 완료")
        else:
            st.info("📝 퀴즈")

    with c2:
        if st.session_state.spot_stamp:
            st.success("🔍 틀린 그림 찾기 완료")
        else:
            st.info("🔍 틀린 그림 찾기")

    with c3:
        if st.session_state.ai_stamp:
            st.success("🤖 AI 체험 완료")
        else:
            st.info("🤖 AI 체험")

    st.divider()

    st.metric(
        "획득한 도장",
        f"{stamp_count()} / 3"
    )

    if stamp_count() == 3:
        st.balloons()
        st.success("🏆 포티켓 마스터!")

# =========================
# 퀴즈
# =========================

elif page == "퀴즈":

    st.title("📝 포티켓 퀴즈")

    score = 0

    q1 = st.radio(
        "1. 사진 관련 피해 예방 방법으로 적절하지 않은 것은?",
        [
            "친구 사진을 올리기 전에 동의를 받는다",
            "개인정보가 보이는 사진은 올리지 않는다",
            "SNS 공개 범위를 설정한다",
            "촬영 허락을 받았으니 마음대로 SNS에 업로드한다"
        ],
        key="q1"
    )

    q2 = st.radio(
        "2. 초상권 보호의 근거가 되는 법은?",
        [
            "특허법",
            "개인정보보호법",
            "헌법",
            "초상권보호법"
        ],
        key="q2"
    )

    q3 = st.radio(
        "3. 사실을 드러내어 타인의 명예를 훼손한 경우 받을 수 있는 처벌은?",
        [
            "3천만원 이상 벌금",
            "3년 이하 징역",
            "3년 이상의 유기징역",
            "7년 이하 징역"
        ],
        key="q3"
    )

    q4 = st.radio(
        "4. 딥페이크 편집물을 시청한 경우 받을 수 있는 처벌은?",
        [
            "처벌받지 않는다",
            "상습범만 처벌",
            "3년 이하 징역 또는 3천만원 이하 벌금",
            "5천만원 이하 벌금"
        ],
        key="q4"
    )

    q5 = st.radio(
        "5. 원치 않는 사진이 SNS에 게시되었을 때 가장 먼저 해야 할 행동은?",
        [
            "친구들에게 공유",
            "증거 확보 후 도움 요청",
            "참고 넘김",
            "SNS 삭제"
        ],
        key="q5"
    )

    if st.button("채점하기"):

        if q1 == "촬영 허락을 받았으니 마음대로 SNS에 업로드한다":
            score += 1

        if q2 == "헌법":
            score += 1

        if q3 == "3년 이하 징역":
            score += 1

        if q4 == "3년 이하 징역 또는 3천만원 이하 벌금":
            score += 1

        if q5 == "증거 확보 후 도움 요청":
            score += 1

        st.subheader(f"점수 : {score}/5")

        if score >= 4:
            st.success("🏅 퀴즈 도장 획득!")
            st.session_state.quiz_stamp = True

# =========================
# 틀린 그림 찾기
# =========================

elif page == "틀린 그림 찾기":

    st.title("🔍 틀린 그림 찾기")

    st.write("오른쪽 그림을 클릭해 차이점을 찾아보세요.")

    # 좌표 직접 수정
    
    ANSWERS_1 = [
        (300, 200),
        (600, 400),
        (450, 700)
    ]

    ANSWERS_2 = [
        (250, 300),
        (500, 500),
        (700, 200)
    ]
    
    # -----------------
    # 문제 1
    # -----------------

    if len(st.session_state.found_1) < len(ANSWERS_1):

        st.subheader("문제 1")

        c1, c2 = st.columns(2)

        with c1:
            st.image("images/1-1.png")

        with c2:

            img = Image.open("images/1-2.png")

            value = streamlit_image_coordinates(
                img,
                key="img1"
            )

        st.write(
            f"찾은 개수 : {len(st.session_state.found_1)} / {len(ANSWERS_1)}"
        )

        if value:

            idx = check_click(
                value["x"],
                value["y"],
                ANSWERS_1,
                st.session_state.found_1
            )

            st.write(value)

            if idx is not None:

                st.session_state.found_1.append(idx)
                st.success("정답!")

                st.rerun()

    # -----------------
    # 문제2
    # -----------------

    else:

        st.subheader("문제 2")

        c1, c2 = st.columns(2)

        with c1:
            st.image("images/2-1.png")

        with c2:

            img = Image.open("images/2-2.png")

            value = streamlit_image_coordinates(
                img,
                key="img2"
            )

        st.write(
            f"찾은 개수 : {len(st.session_state.found_2)} / {len(ANSWERS_2)}"
        )

        if value:

            idx = check_click(
                value["x"],
                value["y"],
                ANSWERS_2,
                st.session_state.found_2
            )

            st.write(value)

            if idx is not None:

                st.session_state.found_2.append(idx)
                st.success("정답!")

                st.rerun()

        if len(st.session_state.found_2) == len(ANSWERS_2):

            st.success("🏅 틀린 그림 찾기 완료!")
            st.session_state.spot_stamp = True

# =========================
# AI 체험
# =========================

elif page == "AI 합성 체험":

    st.title("🤖 AI 합성 체험")

    st.info("준비 중입니다.")

    st.button(
        "임시 도장 획득",
        on_click=lambda:
        setattr(st.session_state, "ai_stamp", True)
    )