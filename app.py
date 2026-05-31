import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(
    page_title="타임락 축제 빙고",
    page_icon="🎪",
    layout="centered"
)

# -------------------------------
# 디자인 CSS
# -------------------------------
st.markdown(
    """
    <style>
    .main-title {
        text-align: center;
        font-size: 36px;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .sub-title {
        text-align: center;
        color: #666666;
        font-size: 16px;
        margin-bottom: 30px;
    }

    .bingo-card {
        border-radius: 18px;
        padding: 22px 10px;
        text-align: center;
        font-size: 18px;
        font-weight: 700;
        min-height: 105px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 14px rgba(0,0,0,0.08);
        margin-bottom: 12px;
    }

    .done {
        background: linear-gradient(135deg, #35c77b, #7ee8a6);
        color: white;
        border: 3px solid #1fa463;
    }

    .not-done {
        background: #f7f7f9;
        color: #333333;
        border: 3px solid #e5e5e5;
    }

    .reward-box {
        background: #f3f8ff;
        border-radius: 18px;
        padding: 20px;
        margin-top: 15px;
        border: 1px solid #d7e8ff;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------------------
# 기본 데이터
# -------------------------------
missions = [
    "먹거리 부스 방문",
    "기념품 부스 방문",
    "포토존 촬영",
    "메인 공연 관람",
    "지역 카페 방문",
    "지역 식당 방문",
    "야간 프로그램 참여",
    "숙박 인증",
    "히든 미션 성공"
]

bingo_lines = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]

# -------------------------------
# session_state 초기화
# -------------------------------
if "completed" not in st.session_state:
    st.session_state.completed = [False] * 9

if "checked_in" not in st.session_state:
    st.session_state.checked_in = False

# -------------------------------
# 제목
# -------------------------------
st.markdown('<div class="main-title">🎪 타임락 3×3 축제 빙고</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">미션을 완료하고 다음날 사용 가능한 시간 잠금 쿠폰을 받아보세요!</div>', unsafe_allow_html=True)

st.markdown("---")

# -------------------------------
# QR 체크인
# -------------------------------
st.subheader("📍 축제 입장 QR 체크인")

name = st.text_input("이름을 입력하세요")

if st.button("QR 체크인 완료하기"):
    if name:
        st.session_state.checked_in = True
        st.success(f"{name}님, 축제 입장이 인증되었습니다!")
    else:
        st.warning("이름을 먼저 입력해주세요.")

if st.session_state.checked_in:
    st.info("✅ 입장 인증 완료 상태입니다.")

st.markdown("---")

# -------------------------------
# 빙고판
# -------------------------------
st.subheader("✅ 오늘의 빙고판")

st.caption("미션을 완료했다면 해당 칸의 버튼을 눌러주세요. 완료된 미션은 초록색으로 바뀝니다.")

for row in range(3):
    cols = st.columns(3)

    for col in range(3):
        idx = row * 3 + col

        with cols[col]:
            if st.session_state.completed[idx]:
                card_class = "bingo-card done"
                card_text = f"✅ 완료<br>{missions[idx]}"
                button_text = "완료 취소"
            else:
                card_class = "bingo-card not-done"
                card_text = f"⬜ 미완료<br>{missions[idx]}"
                button_text = "미션 완료"

            st.markdown(
                f'<div class="{card_class}">{card_text}</div>',
                unsafe_allow_html=True
            )

            if st.button(button_text, key=f"mission_{idx}"):
                st.session_state.completed[idx] = not st.session_state.completed[idx]
                st.rerun()

# -------------------------------
# 빙고 계산
# -------------------------------
completed_count = sum(st.session_state.completed)

bingo_count = 0
for line in bingo_lines:
    if all(st.session_state.completed[i] for i in line):
        bingo_count += 1

st.markdown("---")

# -------------------------------
# 보상
# -------------------------------
st.subheader("🎁 나의 보상")

st.write(f"현재 완료한 미션 수: **{completed_count}개**")
st.write(f"완성한 빙고 줄 수: **{bingo_count}줄**")

st.markdown('<div class="reward-box">', unsafe_allow_html=True)

if bingo_count >= 3:
    tomorrow = datetime.now() + timedelta(days=1)
    available_time = tomorrow.replace(hour=13, minute=0, second=0, microsecond=0)

    st.success("🎊 3줄 빙고 성공!")
    st.info("다음날 사용 가능한 관광지 패스권 또는 지역화폐 쿠폰이 지급됩니다.")
    st.write(f"⏰ 쿠폰 사용 가능 시간: **{available_time.strftime('%Y년 %m월 %d일 오후 1시 이후')}**")

elif bingo_count >= 1:
    st.success("🎉 1줄 빙고 성공!")
    st.info("축제장 먹거리 교환권 또는 기념품 교환권을 받을 수 있습니다.")

else:
    st.info("아직 빙고가 완성되지 않았어요. 미션을 더 완료해보세요!")

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# -------------------------------
# 초기화 버튼
# -------------------------------
if st.button("🔄 빙고판 초기화"):
    st.session_state.completed = [False] * 9
    st.session_state.checked_in = False
    st.rerun()

st.markdown("---")

# -------------------------------
# 앱 설명
# -------------------------------
st.subheader("📢 앱 설명")

st.write(
    """
    이 앱은 축제 방문객이 먹거리, 공연, 포토존, 지역 상권, 숙박 등 다양한 미션을 수행하며
    축제장과 주변 지역을 함께 방문하도록 유도하는 타임락 빙고 앱입니다.

    특히 3줄 빙고를 완성하면 바로 사용할 수 없는 시간 잠금 쿠폰을 지급하여
    다음날 관광지, 카페, 식당 방문을 유도하고 축제 체류 시간을 늘릴 수 있습니다.
    """
)
