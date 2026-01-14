# -*- coding: utf-8 -*-
import streamlit as st

# 1. 페이지 설정
st.set_page_config(page_title="나이툰: 나만의 인스타툰 메이커", page_icon="🎨", layout="wide")

# 2. 헤더 및 소개
st.title("🎨 MyToon: AI 인스타툰 생성기")
st.markdown("""
**나만의 캐릭터**를 설정하고, 스토리와 연출을 더해 **10컷의 인스타툰 프롬프트**를 만드세요.
모든 컷을 한 번에 복사하거나, 필요한 컷만 골라서 복사할 수 있습니다.
""")

# ==========================================
# 3. 사이드바: 캐릭터 및 옵션 설정
# ==========================================
st.sidebar.header("1️⃣ 캐릭터 설정 (Character)")

# (1) 캐릭터 종족/유형 선택
char_type = st.sidebar.selectbox(
    "주인공의 유형은?",
    ["고양이 (Cat)", "강아지 (Dog)", "토끼 (Rabbit)", "곰 (Bear)", "사람-여자 (Girl)", "사람-남자 (Boy)", "직접 입력 (Custom)"]
)

custom_species = ""
if char_type == "직접 입력 (Custom)":
    custom_species = st.sidebar.text_input("캐릭터 유형 입력 (예: Alien, Robot)", "Hamster")

# (2) 외모 특징
char_feature = st.sidebar.text_input(
    "외모 특징 (색상, 생김새)", 
    "white fur, big round eyes, pink cheeks" if "사람" not in char_type else "brown bob hair, cute face"
)

# (3) 의상/스타일
char_outfit = st.sidebar.text_input(
    "착용 의상 (Outfit)", 
    "yellow hoodie, casual jeans"
)

st.sidebar.divider()
st.sidebar.header("2️⃣ 연출 및 스타일")

# (4) 서사 테마
story_theme = st.sidebar.radio(
    "이야기 테마",
    ["일상 공감 (Daily Life)", "성장/도전 (Growth)", "꿀팁 정보 (Information)", "감동/힐링 (Healing)"]
)

# (5) 그림체 스타일
art_style = st.sidebar.select_slider(
    "그림체 스타일",
    options=["손그림/낙서", "깔끔한 웹툰", "고퀄리티 일러스트"]
)

# (6) 레이아웃 구성
layout_mode = st.sidebar.selectbox(
    "컷 연출 방식",
    ["안정적 (설명 위주)", "다이내믹 (만화적 과장)", "시네마틱 (영화 느낌)"]
)

# 시드 번호
seed_num = st.sidebar.number_input("일관성 시드(Seed)", value=1234, min_value=0)


# ==========================================
# 4. 프롬프트 생성 로직
# ==========================================
def make_general_prompts(ctype, cspec, cfeat, coutfit, theme, style, layout, seed):
    
    # 1. 캐릭터 조립
    if ctype == "직접 입력 (Custom)":
        species = cspec
    else:
        species = ctype.split("(")[1].replace(")", "")
    
    if species in ["Cat", "Dog", "Rabbit", "Bear", "Hamster", "Tiger"]:
        base_char = f"Cute anthropomorphic {species} character"
    else:
        base_char = f"Cute {species} character"

    full_char_desc = f"{base_char}, {cfeat}, wearing {coutfit}, simple iconic design"

    # 2. 스타일
    if style == "손그림/낙서":
        style_kw = "doodle style, rough pencil lines, crayon texture, loose and cute, minimalist"
    elif style == "고퀄리티 일러스트":
        style_kw = "high quality vector art, detailed shading, vibrant colors, pixar style lighting"
    else: 
        style_kw = "flat vector art, thick outlines, webtoon style, cel shading, clean solid colors"

    # 3. 레이아웃
    if layout == "다이내믹":
        angle_kw = "dynamic dutch angle, exaggerated perspective, speed lines, comic book action"
    elif layout == "시네마틱":
        angle_kw = "cinematic lighting, depth of field, dramatic angles, rule of thirds"
    else:
        angle_kw = "flat composition, symmetrical balance, clear eye-level shot"

    # 4. 스토리 템플릿
    intro_action = "waving hello happily"
    climax_action = "looking confused at a problem"
    
    if theme == "일상 공감 (Daily Life)":
        intro_action = "lying on a sofa looking bored"
        climax_action = "spilling coffee or making a clumsy mistake, shocked face"
    elif theme == "성장/도전 (Growth)":
        intro_action = "tying headband, looking determined"
        climax_action = "failing a task, sweating and panting, frustrated"
    elif theme == "감동/힐링 (Healing)":
        intro_action = "looking at the sky with a soft smile"
        climax_action = "tearing up with emotion, hugging something"
    elif theme == "꿀팁 정보 (Information)":
        intro_action = "holding a pointer stick, teacher pose"
        climax_action = "pointing at a complex chart, explaining seriously"

    # 10컷 시나리오
    scenario_list = [
        f"Cut 1 (Title): {full_char_desc}, {intro_action}, large title space composition",
        "Cut 2 (Intro): Character walking into the scene, wide shot",
        "Cut 3 (Setup): Character sitting at a desk or table, side profile",
        "Cut 4 (Detail): Extreme close-up on character's eyes or hands",
        f"Cut 5 (Climax): {full_char_desc}, {climax_action}, {angle_kw}",
        "Cut 6 (Reaction): Character with a lightbulb symbol over head, realization",
        "Cut 7 (Action): Character doing the main activity energetically",
        "Cut 8 (Result): Success background, sparkles, happy jumping pose",
        "Cut 9 (Message): Character holding a sign or giving a thumbs up",
        "Cut 10 (Outro): Character waving goodbye, 'Like & Subscribe' visual elements"
    ]

    prompts = []
    for scn in scenario_list:
        p = f"/imagine prompt: **[Subject]** {full_char_desc} **[Action]** {scn} **[Style]** {style_kw}, {angle_kw} --ar 4:5 --niji 6 --seed {seed}"
        prompts.append(p)
    
    return prompts, full_char_desc

# ==========================================
# 5. 결과 출력 화면 (복사 기능 강화)
# ==========================================

# 상태 저장 초기화
if 'generated_prompts' not in st.session_state:
    st.session_state.generated_prompts = []
    st.session_state.char_summary = ""

# 생성 버튼
if st.button("🚀 인스타툰 프롬프트 생성 (Click)"):
    with st.spinner("AI가 시나리오를 작성 중입니다..."):
        prompts, summary = make_general_prompts(
            char_type, custom_species, char_feature, char_outfit, 
            story_theme, art_style, layout_mode, seed_num
        )
        st.session_state.generated_prompts = prompts
        st.session_state.char_summary = summary

# 결과 표시
if st.session_state.generated_prompts:
    st.divider()
    st.success(f"✅ 생성 완료! 캐릭터: {st.session_state.char_summary}")
    
    # [1] 전체 복사
    st.subheader("📋 전체 한 번에 복사하기")
    st.caption("우측 상단의 📄 아이콘을 누르면 10개가 전부 복사됩니다.")
    all_text = "\n\n".join(st.session_state.generated_prompts)
    st.code(all_text, language="markdown")
    
    st.divider()
    
    # [2] 개별 복사 (리스트 형태)
    st.subheader("✂️ 컷별로 골라서 복사하기")
    st.caption("각 상자를 열 필요 없이, 바로 우측의 📄 아이콘을 눌러 복사하세요.")

    # 10개의 컷을 Expander(접이식)로 나열하여 제목과 내용을 명확히 구분
    for i, p in enumerate(st.session_state.generated_prompts):
        # 컷 내용 요약 추출
        desc = p.split("**[Action]**")[1].split("**[Style]**")[0].strip()
        
        # 접이식 메뉴 사용 (제목에 내용 미리보기 표시)
        with st.expander(f"Cut {i+1}: {desc}", expanded=True):

            st.code(p, language="markdown")
