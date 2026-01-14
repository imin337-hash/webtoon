import streamlit as st

# 1. 페이지 설정
st.set_page_config(page_title="나노바나나프로 인스타툰 생성기", page_icon="🍌", layout="wide")

# 2. 타이틀 및 이론 설명
st.title("🍌 나노바나나프로: 인스타툰 프롬프트 생성기")
st.markdown("""
**웹툰의 핵심 3요소(스토리, 연출, 그림)**를 조합하여 인스타그램용(4:5) 이미지 프롬프트를 생성합니다.
""")

with st.expander("ℹ️ 적용된 웹툰 이론 보기"):
    st.info("""
    - **스토리(Story):** 3막 구조(시작-중간-결말), 갈등과 해소, 캐릭터 성장
    - **연출(Direction):** 컷 배분, 카메라 앵글(클로즈업/롱샷), 시선 유도
    - **그림(Art):** 색채 심리학, 비주얼 내러티브, 일관된 캐릭터 묘사
    """)

# 3. 옵션 선택 (사이드바)
st.sidebar.header("🎨 요소 선택")

# 스토리
st.sidebar.subheader("1. 스토리 (Story)")
story_theme = st.sidebar.radio("에피소드 테마", ["성장/도전 (Level Up)", "직장인 공감 (Empathy)", "정보 전달 (Info)"])

# 연출
st.sidebar.subheader("2. 연출 (Direction)")
angle_mode = st.sidebar.selectbox("카메라 앵글", ["다이내믹 혼합 (Dynamic Mix)", "감정 중심 (Close-up)", "상황 중심 (Full-shot)"])
use_comic_fx = st.sidebar.checkbox("만화적 효과 (집중선/말풍선)", value=True)

# 그림
st.sidebar.subheader("3. 그림 (Art)")
color_tone = st.sidebar.select_slider("색감 분위기", options=["차분/감성", "표준", "밝고/팝(Pop)"])

# 4. 프롬프트 생성 로직
def make_prompts(theme, angle, tone, fx):
    # 캐릭터 고정 (Nano Banana Pro)
    char_desc = "Cute anthropomorphic Banana character named 'Nano', wearing a futuristic pro-headset, 2D flat vector art, thick outlines, webtoon style"
    
    # 톤 설정
    if tone == "차분/감성":
        style = "soft pastel colors, warm lighting, healing vibe"
    elif tone == "밝고/팝(Pop)":
        style = "vivid pop colors, high contrast, energetic yellow and blue"
    else:
        style = "clean balanced colors, bright daylight"
        
    # 효과 설정
    fx_text = ", comic book speech bubbles, sound effect text 'BAM!', speed lines" if fx else ""
    
    # 컷별 시나리오 (10컷)
    climax = "Character looking confused at a computer screen error" # 기본
    if "공감" in theme: climax = "Character lying on desk totally exhausted, funny tired face"
    if "성장" in theme: climax = "Character failing a task, shocked expression"
    
    scenes = [
        "Cut 1 (Title): Character posing confidently, space for title text",
        "Cut 2 (Intro): Character walking into office, happy vibe",
        "Cut 3 (Setup): Character working at desk, side view",
        "Cut 4 (Focus): Close-up on eyes or hands, intense focus",
        f"Cut 5 (Climax): {climax}",
        "Cut 6 (Idea): Lightbulb moment, sudden realization",
        "Cut 7 (Action): Character typing fast, energy flowing",
        "Cut 8 (Result): Success screen, sparkles, happy face",
        "Cut 9 (Reaction): Thumbs up to the camera",
        "Cut 10 (Outro): Waving goodbye, 'Follow Me' sign"
    ]
    
    # 최종 조합
    final_list = []
    for scene in scenes:
        p = f"/imagine prompt: **[Subject]** {char_desc} **[Action]** {scene} **[Style]** {style}, {angle}, {fx_text} --ar 4:5 --niji 6"
        final_list.append(p)
    return final_list

# 5. 결과 출력
if st.button("🚀 프롬프트 생성하기"):
    st.divider()
    prompts = make_prompts(story_theme, angle_mode, color_tone, use_comic_fx)
    
    st.subheader(f"✅ 생성 결과: {story_theme}")
    for i, p in enumerate(prompts):
        st.text_area(f"Cut {i+1}", value=p, height=70)