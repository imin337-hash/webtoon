# -*- coding: utf-8 -*-
import streamlit as st
import random

# 1. 페이지 설정
st.set_page_config(page_title="마이툰: 시나리오 에디터", page_icon="🎨", layout="wide")

# 2. 헤더
st.title("🎨 마이툰(MyToon): 커스텀 시나리오 에디터")
st.markdown("""
**1. 주제 입력:** 원하는 이야기 주제를 쓰면 10컷 시나리오가 자동 생성됩니다.
**2. 내용 수정:** 표에서 행동(Action)과 대사(Text)를 자유롭게 고치세요.
**3. 컷 수 선택:** 1장에 **1컷 / 2컷 / 4컷** 중 원하는 구성을 선택하세요.
""")

# ==========================================
# 3. 데이터 및 설정
# ==========================================

CHAR_DEFAULTS = {
    "나노바나나 (Original)": ("Cute anthropomorphic Banana character named 'Nano', wearing a sleek futuristic pro-headset", "yellow body, expressive face"),
    "나노 (오피스룩)": ("Cute anthropomorphic Banana character named 'Nano', wearing a formal suit and glasses", "office worker vibe"),
    "고양이 (Cat)": ("white fur, pointy ears, pink nose", "red ribbon collar"),
    "강아지 (Dog)": ("golden curly fur, floppy ears", "green scarf"),
    "사람-여자 (Girl)": ("long brown hair, cute face, k-pop style", "pastel hoodie, denim skirt"),
    "사람-남자 (Boy)": ("short black hair, casual look, glasses", "oversized sweatshirt, cargo pants"),
    "직접 입력 (Custom)": ("", "")
}

SIDEKICK_DEFAULTS = {
    "작은 새 (Bird)": "tiny cute blue bird friend",
    "아기 고양이 (Kitten)": "tiny yellow kitten friend",
    "로봇 (Robot)": "mini floating robot friend",
    "유령 (Ghost)": "cute marshmallow ghost friend",
    "사람 친구 (Friend)": "best friend character wearing casual clothes"
}

ART_STYLE_MAP = {
    "1. 초간단 낙서 (Doodle)": "minimalist doodle, stick figure style, rough sketch, black and white, simple lines",
    "2. 단순한 선화 (Simple Line)": "simple line art, coloring book style, thin lines, minimal detail, white background",
    "3. 플랫 일러스트 (Flat Vector)": "flat vector art, clean solid colors, no gradients, corporate memphis style, minimal",
    "4. 카툰/명랑만화 (Cartoon)": "classic cartoon style, funny proportions, bold colors, nickelodeon style, expressive",
    "5. 웹툰/셀식 채색 (Webtoon)": "korean webtoon style, cel shading, vibrant colors, clean outlines, digital art",
    "6. 부드러운 수채화 (Watercolor)": "watercolor texture, soft pastel blend, dreamy atmosphere, wet brush style, hand drawn",
    "7. 유화/아크릴 (Oil Paint)": "oil painting texture, brush strokes, artistic, impressionist style, rich colors",
    "8. 세밀한 펜화 (Detailed Ink)": "detailed cross-hatching, comic book inking, manga style, high detail, noir vibe",
    "9. 세미 리얼리스틱 (3D Cute)": "3D pixar style render, cute but realistic lighting, octane render, clay texture, soft shadows",
    "10. 초고화질 실사풍 (Realistic)": "unreal engine 5 render, cinematic lighting, 8k resolution, highly detailed texture, photograph style"
}

def update_char_defaults():
    selected = st.session_state.char_type_selector
    if selected in CHAR_DEFAULTS:
        st.session_state.char_feature_input = CHAR_DEFAULTS[selected][0]
        st.session_state.char_outfit_input = CHAR_DEFAULTS[selected][1]

# ==========================================
# 4. 시나리오 초안 생성 로직
# ==========================================
def create_draft(topic):
    return [
        {"Cut": 1, "Action (행동)": f"holding a title card '{topic}', confident pose", "Text (대사)": f"오늘의 주제:\n{topic}"},
        {"Cut": 2, "Action (행동)": "walking happily, full of expectation", "Text (대사)": "시작해볼까!"},
        {"Cut": 3, "Action (행동)": f"facing the situation of {topic}, looking interested", "Text (대사)": "오호라?"},
        {"Cut": 4, "Action (행동)": "concentrating deeply on the task", "Text (대사)": "집중..."},
        {"Cut": 5, "Action (행동)": "sudden problem or mistake occurring, shocked face", "Text (대사)": "앗!! 실수!"},
        {"Cut": 6, "Action (행동)": "feeling frustrated or sad, messy background", "Text (대사)": "망했다..."},
        {"Cut": 7, "Action (행동)": "lightbulb appearing over head, having a good idea", "Text (대사)": "잠깐! 좋은 생각!"},
        {"Cut": 8, "Action (행동)": f"solving the problem related to {topic}, energetic", "Text (대사)": "다시 도전!"},
        {"Cut": 9, "Action (행동)": "successful result, sparkling effect, happy smile", "Text (대사)": "완벽해!"},
        {"Cut": 10, "Action (행동)": "waving goodbye to camera, holding subscribe button", "Text (대사)": "다들 화이팅!"}
    ]

# ==========================================
# 5. 프롬프트 조립 로직 (컷 수 옵션 적용)
# ==========================================
def build_prompts(rows, ctype, cfeat, coutfit, style_name, layout, lang, seed, use_side, side_desc, panel_mode):
    
    # 1. 캐릭터
    full_char = f"{cfeat}, wearing {coutfit}, expressive face"
    if use_side:
        full_char += f", accompanied by {side_desc}"

    # 2. 스타일 & 레이아웃
    style_kw = ART_STYLE_MAP[style_name]
    
    if "다이내믹" in layout: angle_kw = "dynamic dutch angle, action lines"
    elif "셀카" in layout: angle_kw = "holding smartphone camera, selfie angle, face focus"
    elif "1인칭" in layout: angle_kw = "first-person point of view (POV), hands visible"
    elif "항공" in layout: angle_kw = "bird's-eye view, top-down shot"
    elif "로우" in layout: angle_kw = "low angle shot, looking up"
    elif "어안" in layout: angle_kw = "fish-eye lens effect"
    elif "실루엣" in layout: angle_kw = "silhouette, backlighting"
    elif "아이소메트릭" in layout: angle_kw = "isometric view, 3D cute game style"
    elif "시네마틱" in layout: angle_kw = "cinematic lighting, depth of field"
    else: angle_kw = "flat composition, symmetrical balance, eye-level shot"

    # 3. [NEW] 컷 수(Panel Count) 설정 로직
    if "1컷" in panel_mode:
        # 단일 이미지 강조
        mode_kw = "single panel, independent illustration, full shot, one image, no borders"
        neg_kw = "--no comic grid, storyboard, multiple panels, split view"
    elif "2컷" in panel_mode:
        # 세로 2분할
        mode_kw = "2 panel comic strip, vertical layout, top and bottom panels, storytelling sequence"
        neg_kw = "--no 4 panel grid, single image"
    elif "3컷" in panel_mode:
        # 웹툰형 3분할
        mode_kw = "3 panel comic strip, vertical webtoon layout, storytelling flow"
        neg_kw = "--no single image, 4 panel grid"
    elif "4컷" in panel_mode:
        # 2x2 격자
        mode_kw = "4 panel comic, 2x2 grid layout, four distinct scenes, comic strip style"
        neg_kw = "--no single image, vertical strip"
    else: # 캐릭터 시트
        mode_kw = "character sheet, multiple poses, expression sheet, white background"
        neg_kw = ""

    prompts = []
    
    for row in rows:
        action = row["Action (행동)"]
        text = row["Text (대사)"]
        
        # 언어 처리
        if lang == "한국어":
            text_p = f'speech bubble with text "{text}", written in legible Korean Hangul font, manhwa style speech bubble'
        elif lang == "영어":
            text_p = f'speech bubble with text "{text}", written in English comic font'
        else:
            text_p = "no text"
            
        p = f"/imagine prompt: **[Subject]** {full_char} **[Action]** {action} **[Text]** {text_p} **[Style]** {style_kw}, {angle_kw}, {mode_kw} --ar 4:5 --niji 6 --seed {seed} {neg_kw}"
        prompts.append(p)
        
    return prompts

# ==========================================
# 6. UI 구성
# ==========================================

# --- 사이드바 ---
st.sidebar.header("1️⃣ 캐릭터 설정")
char_type = st.sidebar.selectbox("주인공 선택", list(CHAR_DEFAULTS.keys()), key="char_type_selector", on_change=update_char_defaults)

if 'char_feature_input' not in st.session_state: st.session_state.char_feature_input = CHAR_DEFAULTS["나노바나나 (Original)"][0]
if 'char_outfit_input' not in st.session_state: st.session_state.char_outfit_input = CHAR_DEFAULTS["나노바나나 (Original)"][1]

char_feature = st.sidebar.text_input("외모/종족 특징", key="char_feature_input")
char_outfit = st.sidebar.text_input("의상/스타일", key="char_outfit_input")

with st.sidebar.expander("👥 조연(Sidekick) 추가"):
    use_sidekick = st.checkbox("조연 등장시키기", value=False)
    sidekick_type = st.selectbox("조연 유형", list(SIDEKICK_DEFAULTS.keys()))
    sidekick_desc = st.text_input("조연 묘사", value=SIDEKICK_DEFAULTS[sidekick_type])

st.sidebar.divider()
st.sidebar.header("2️⃣ 스타일 설정")
style_name = st.sidebar.select_slider("그림체 농도", options=list(ART_STYLE_MAP.keys()), value="5. 웹툰/셀식 채색 (Webtoon)")
layout_mode = st.sidebar.selectbox("연출 방식", ["1. 안정적 (Standard)", "2. 다이내믹 (Dynamic)", "3. 시네마틱 (Cinematic)", "4. 셀카 모드 (Selfie)", "5. 1인칭 시점 (POV)", "6. 아이소메트릭 (Isometric)", "7. 항공 샷 (Drone)", "8. 로우 앵글 (Low Angle)", "9. 어안 렌즈 (Fish-eye)", "10. 실루엣 (Silhouette)"])

# [NEW] 컷 수 선택 옵션 추가
panel_choice = st.sidebar.selectbox(
    "🎞️ 1장당 컷 수 (Panel Count)", 
    ["1컷 (단일 이미지 추천)", "2컷 (세로 분할)", "3컷 (웹툰 스타일)", "4컷 (격자/Grid)", "캐릭터 시트 (다양한 포즈)"]
)

text_lang = st.sidebar.radio("말풍선 언어", ["한국어", "영어", "없음"])
seed_num = st.sidebar.number_input("시드(Seed)", value=1234)


# --- 메인 화면: 시나리오 에디터 ---
st.subheader("📝 주제 입력 & 시나리오 편집")

col1, col2 = st.columns([0.7, 0.3])
with col1:
    topic_input = st.text_input("이야기 주제를 입력하세요", value="복권 당첨된 하루")
with col2:
    st.write("") 
    st.write("")
    if st.button("✨ 시나리오 초안 생성"):
        st.session_state.scenario_rows = create_draft(topic_input)

# 세션 상태 초기화
if 'scenario_rows' not in st.session_state:
    st.session_state.scenario_rows = create_draft("복권 당첨된 하루")

# 데이터 에디터 (수정 가능)
edited_rows = st.data_editor(
    st.session_state.scenario_rows,
    num_rows="fixed",
    column_config={
        "Cut": st.column_config.NumberColumn("컷", disabled=True, width="small"),
        "Action (행동)": st.column_config.TextColumn("행동 (영어 권장)", width="large"),
        "Text (대사)": st.column_config.TextColumn("대사 (말풍선)", width="medium"),
    },
    hide_index=True
)

st.divider()

# --- 프롬프트 생성 버튼 ---
if st.button("🚀 프롬프트 변환하기 (Click)"):
    # 에디터의 내용을 바탕으로 프롬프트 생성
    final_prompts = build_prompts(
        edited_rows, char_type, char_feature, char_outfit, 
        style_name, layout_mode, text_lang, seed_num, use_sidekick, sidekick_desc, panel_choice
    )
    st.session_state.final_prompts = final_prompts

# --- 결과 출력 ---
if 'final_prompts' in st.session_state and st.session_state.final_prompts:
    st.success(f"✅ 생성 완료! (설정: {panel_choice})")
    
    # 1. 전체 복사 (접이식)
    with st.expander("📋 전체 프롬프트 한 번에 보기 (메모장 저장용)"):
        st.warning("주의: 디스코드에 한 번에 붙여넣으면 1장만 생성될 수 있습니다.")
        st.code("\n\n".join(st.session_state.final_prompts), language="markdown")

    st.divider()
    st.markdown("### 👇 컷별 상세 확인 & 복사")
    st.caption("제목(대사)을 확인하고 코드 박스 오른쪽 위의 📄 버튼을 눌러 복사하세요.")

    for i, p in enumerate(st.session_state.final_prompts):
        current_text = edited_rows[i]["Text (대사)"]
        current_action = edited_rows[i]["Action (행동)"]
        
        st.markdown(f"#### 🎞️ Cut {i+1}: {current_text}")
        st.caption(f"Action: {current_action}")
        st.code(p, language="markdown")
