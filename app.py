import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(
    page_title="타임락 축제 빙고",
    page_icon="🎪",
    layout="centered"
)

st.title("🎪 타임락 3×3 축제 빙고")
st.caption("축제 미션을 수행하고 시간 잠금 쿠폰을 받아보세요!")

st.markdown("---")

st.subheader("📍 축제 입장 QR 체크인")

name = st.text_input("이름을 입력하세요")
checked_in = st.button("QR 체크인 완료하기")

if checked_in:
    if name:
        st.success(f"{name}님, 축제 입장이 인증되었습니다!")
    else:
        st.warning("이름을 먼저 입력해주세요.")

st.markdown("---")

st.subheader("✅ 오늘의 빙고 미션")

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

selected = []

cols = st.columns(3)

for i, mission in enumerate(missions):
    with cols[i % 3]:
        if st.checkbox(mission):
            selected.append(i)

st.markdown("---")

st.subheader("🎁 나의 보상")

completed_count = len(selected)

st.write(f"현재 완료한 미션 수: **{completed_count}개**")

def count_bingo(selected_indices):
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

    count = 0
    for line in bingo_lines:
        if all(i in selected_indices for i in line):
            count += 1
    return count

bingo_count = count_bingo(selected)

st.write(f"완성한 빙고 줄 수: **{bingo_count}줄**")

if bingo_count >= 1:
    st.success("🎉 1줄 빙고 성공! 축제장 먹거리 교환권을 받을 수 있어요.")

if bingo_count >= 3:
    tomorrow = datetime.now() + timedelta(days=1)
    available_time = tomorrow.replace(hour=13, minute=0, second=0, microsecond=0)

    st.success("🎊 3줄 빙고 성공! 다음날 사용 가능한 관광지 패스권이 지급됩니다.")
    st.info(f"⏰ 쿠폰 사용 가능 시간: {available_time.strftime('%Y년 %m월 %d일 오후 1시 이후')}")

if bingo_count == 0:
    st.info("아직 빙고가 완성되지 않았어요. 미션을 더 완료해보세요!")

st.markdown("---")

st.subheader("📢 앱 설명")
st.write(
    """
    이 앱은 축제 방문객이 여러 미션을 수행하며 축제장과 주변 상권을 함께 방문하도록 유도하는 앱입니다.
    특히 3줄 빙고를 완성하면 바로 사용할 수 없는 '타임락 쿠폰'을 지급하여
    다음날 관광지, 카페, 식당 방문을 유도할 수 있습니다.
    """
)
