# -*- coding: utf-8 -*-
import streamlit as st
import random

# 1. 페이지 설정
st.set_page_config(page_title="마이툰: 시나리오 에디터", page_icon="🎨", layout="wide")

# 2. 헤더
st.title("🎨 마이툰(MyToon): 인스타툰 시나리오 에디터")
st.markdown("""
**API 키 필요 없이 바로 사용하세요.**
주제를 입력하면 **10컷 시나리오 초안**을 만들어줍니다. 내용을 수정하고 프롬프트를 생성하세요.
""")

# ==========================================
# 3. 데이터 및 설정 (확장된 캐릭터/조연 리스트 유지)
# ==========================================

# [주인공] 총 17종
CHAR_DEFAULTS = {
    "나노바나나 (Original)": ("Cute anthropomorphic Banana character named 'Nano', wearing a sleek futuristic pro-headset", "yellow body, expressive face"),
    "나노 (오피스룩)": ("Cute anthropomorphic Banana character named 'Nano', wearing a formal suit and glasses", "office worker vibe"),
    "고양이 (Cat)": ("white fur, pointy ears, pink nose", "red ribbon collar"),
    "강아지 (Dog)": ("golden curly fur, floppy ears", "green scarf"),
    "사람-여자 (Girl)": ("long brown hair, cute face, k-pop style", "pastel hoodie, denim skirt"),
    "사람-남자 (Boy)": ("short black hair, casual look, glasses", "oversized sweatshirt, cargo pants"),
    "토끼 (Rabbit)": ("long floppy ears, fluffy white fur", "cute pink dress"),
    "곰 (Bear)": ("brown fur, round ears, teddy bear look", "striped t-shirt"),
    "외계인 (Alien)": ("cute green skin alien, big black eyes", "space suit"),
    "기사 (Knight)": ("chibi knight character, shiny silver armor", "red cape, holding small sword"),
    "마법사 (Wizard)": ("cute wizard character, holding magic wand", "purple robe, wizard hat"),
    "탐정 (Detective)": ("clever look, holding magnifying glass", "beige trench coat, fedora hat"),
    "학생 (Student)": ("young energetic student look", "school uniform, backpack"),
    "아기 공룡 (Dino)": ("cute green baby t-rex", "spiked tail, tiny roar pose"),
    "펭귄 (Penguin)": ("cute round penguin", "winter scarf, earmuffs"),
    "나무늘보 (Sloth)": ("sleepy cute sloth", "pajamas, holding pillow"),
    "유령 (Ghost)": ("cute white sheet ghost", "blue bow tie"),
    "직접 입력 (Custom)": ("", "")
}

# [조연] 총 15종
SIDEKICK_DEFAULTS = {
    "작은 새 (Bird)": "tiny cute blue bird friend",
    "아기 고양이 (Kitten)": "tiny yellow kitten friend",
    "로봇 (Robot)": "mini floating robot friend",
    "유령 (Ghost)": "cute marshmallow ghost friend",
    "사람 친구 (Friend)": "best friend character wearing casual clothes",
    "요정 (Fairy)": "tiny glowing fairy with wings",
    "아기 용 (Dragon)": "tiny red baby dragon breathing smoke",
    "오리 (Duck)": "yellow rubber ducky character",
    "선인장 (Cactus)": "walking cute cactus in a pot",
    "스마트폰 (Phone)": "anthropomorphic smartphone character with arms",
    "구름 (Cloud)": "floating fluffy cloud with a face",
    "햄스터 (Hamster)": "round chubby hamster eating sunflower seed",
    "늑대 (Wolf)": "cool mini wolf friend",
    "부엉이 (Owl)": "wise looking owl with glasses",
    "돌멩이 (Rock)": "pet rock with googly eyes",
    "직접 입력 (Custom)": ""
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

def update_sidekick_defaults():
    selected = st.session_state.sidekick_selector
    if selected in SIDEKICK_DEFAULTS:
        st.session_state.sidekick_desc_input = SIDEKICK_DEFAULTS[selected]

# ==========================================
# 4. 스마트 템플릿 로직 (규칙 기반)
# ==========================================
def generate_smart_template(topic):
    """
    사용자가 입력한 주제(topic)를 기승전결 구조 템플릿에 끼워넣어 반환합니다.
    """
    return [
        {"Cut": 1, "Action": f"holding title card '{topic}', confident pose", "Text": f"오늘의 주제:\n{topic}"},
        {"Cut": 2, "Action": "walking happily, full of expectation", "Text": "시작해볼까!"},
        {"Cut": 3, "Action": f"facing the situation of {topic}", "Text": "어라? 이게 뭐지?"},
        {"Cut": 4, "Action": "concentrating deeply on the task", "Text": "집중..."},
        {"Cut": 5, "Action": "sudden problem or mistake occurring, shocked", "Text": "앗!! 실수!"},
        {"Cut": 6, "Action": "feeling frustrated, messy background", "Text": "망했다..."},
        {"Cut": 7, "Action": "lightbulb appearing over head, idea", "Text": "잠깐! 좋은 생각!"},
        {"Cut": 8, "Action": f"solving the problem of {topic} actively", "Text": "다시 도전!"},
        {"Cut": 9, "Action": "success moment, sparkling effect, happy", "Text": "완벽해!"},
        {"Cut": 10, "Action": "waving goodbye, holding subscribe button", "Text": "다들 화이팅!"}
    ]

# ==========================================
# 5. 프롬프트 빌더
# ==========================================
def build_prompts(rows, cfeat, coutfit, style_name, layout, lang, seed, use_side, side_desc, panel_mode):
    full_char = f"{cfeat}, wearing {coutfit}, expressive face"
    if use_side: full_char += f", accompanied by {side_desc}"
    
    style_kw = ART_STYLE_MAP[style_name]
    
    # 레이아웃 매핑
    layout_kws = {
        "1. 안정적": "flat composition, symmetrical balance, eye-level shot",
        "2. 다이내믹": "dynamic dutch angle, action lines",
        "3. 시네마틱": "cinematic lighting, depth of field",
        "4. 셀카 모드": "holding smartphone camera, selfie angle, face focus",
        "5. 1인칭 시점": "first-person point of view (POV), hands visible",
        "6. 아이소메트릭": "isometric view, 3D cute game style",
        "7. 항공 샷": "bird's-eye view, top-down shot",
        "8. 로우 앵글": "low angle shot, looking up",
        "9. 어안 렌즈": "fish-eye lens effect",
        "10. 실루엣": "silhouette, backlighting"
    }
    angle_kw = layout_kws.get(layout.split(" (")[0], "flat composition")

    # 컷 수 매핑
    if "1컷" in panel_mode:
        mode_kw = "single panel, independent illustration, full shot, one image, no borders"
        neg_kw = "--no comic grid, storyboard, multiple panels, split view"
    elif "2컷" in panel_mode:
        mode_kw = "2 panel comic strip, vertical layout"
        neg_kw = "--no 4 panel grid, single image"
    elif "3컷" in panel_mode:
        mode_kw = "3 panel comic strip, vertical webtoon layout"
        neg_kw = "--no single image, 4 panel grid"
    elif "4컷" in panel_mode:
        mode_kw = "4 panel comic, 2x2 grid layout"
        neg_kw = "--no single image, vertical strip"
    else:
        mode_kw = "character sheet, multiple poses, white background"
        neg_kw = ""

    prompts = []
    for row in rows:
        action = row["Action"]
        text = row["Text"]
        if lang == "한국어": text_p = f'speech bubble with text "{text}", written in legible Korean Hangul font, manhwa style speech bubble'
        elif lang == "영어": text_p = f'speech bubble with text "{text}", written in English comic font'
        else: text_p = "no text"
            
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

# 조연 설정
with st.sidebar.expander("👥 조연(Sidekick) 추가"):
    use_sidekick = st.checkbox("조연 등장시키기", value=False)
    
    if use_sidekick:
        sidekick_type = st.selectbox("조연 유형", list(SIDEKICK_DEFAULTS.keys()), key="sidekick_selector", on_change=update_sidekick_defaults)
        
        # 직접 입력
        custom_sidekick_species = ""
        if sidekick_type == "직접 입력 (Custom)":
            custom_sidekick_species = st.text_input("조연 종족 입력", "Baby Elephant")

        # 묘사 (자동 채움)
        if 'sidekick_desc_input' not in st.session_state:
            st.session_state.sidekick_desc_input = SIDEKICK_DEFAULTS.get("작은 새 (Bird)", "")
            
        sidekick_desc = st.text_input("조연 묘사", key="sidekick_desc_input")

        if sidekick_type == "직접 입력 (Custom)":
            final_sidekick_desc = f"cute {custom_sidekick_species}, {sidekick_desc}"
        else:
            final_sidekick_desc = sidekick_desc
    else:
        final_sidekick_desc = ""

st.sidebar.divider()
st.sidebar.header("2️⃣ 스타일 설정")
style_name = st.sidebar.select_slider("그림체 농도", options=list(ART_STYLE_MAP.keys()), value="5. 웹툰/셀식 채색 (Webtoon)")
layout_mode = st.sidebar.selectbox("연출 방식", ["1. 안정적 (Standard)", "2. 다이내믹 (Dynamic)", "3. 시네마틱 (Cinematic)", "4. 셀카 모드 (Selfie)", "5. 1인칭 시점 (POV)", "6. 아이소메트릭 (Isometric)", "7. 항공 샷 (Drone)", "8. 로우 앵글 (Low Angle)", "9. 어안 렌즈 (Fish-eye)", "10. 실루엣 (Silhouette)"])
panel_choice = st.sidebar.selectbox("🎞️ 1장당 컷 수", ["1컷 (추천)", "2컷 (세로 분할)", "3컷 (웹툰형)", "4컷 (격자)", "캐릭터 시트"])
text_lang = st.sidebar.radio("말풍선 언어", ["한국어", "영어", "없음"])
seed_num = st.sidebar.number_input("시드(Seed)", value=1234)

# --- 메인 화면 ---
st.subheader("📝 주제 입력 & 시나리오 편집")

col1, col2 = st.columns([0.7, 0.3])
with col1:
    topic_input = st.text_input("어떤 이야기를 만들까요?", value="편의점 알바 첫 출근")
with col2:
    st.write("") 
    st.write("")
    if st.button("✨ 시나리오 초안 생성", type="primary"):
        st.session_state.scenario_rows = generate_smart_template(topic_input)
        st.toast("시나리오 초안이 생성되었습니다! 아래 표를 수정하세요.")

if 'scenario_rows' not in st.session_state:
    st.session_state.scenario_rows = generate_smart_template("편의점 알바 첫 출근")

# 에디터
edited_rows = st.data_editor(
    st.session_state.scenario_rows,
    num_rows="fixed",
    column_config={
        "Cut": st.column_config.NumberColumn("컷", disabled=True, width="small"),
        "Action": st.column_config.TextColumn("행동 (영어 권장)", width="large"),
        "Text": st.column_config.TextColumn("대사", width="medium"),
    },
    hide_index=True,
    use_container_width=True
)

st.write("")
if st.button("🚀 프롬프트 변환하기 (Click)", type="primary", use_container_width=True):
    final_prompts = build_prompts(
        edited_rows, char_feature, char_outfit, 
        style_name, layout_mode, text_lang, seed_num, 
        use_sidekick, final_sidekick_desc, panel_choice
    )
    st.session_state.final_prompts = final_prompts

# 결과 출력
if 'final_prompts' in st.session_state and st.session_state.final_prompts:
    st.divider()
    st.success("✅ 프롬프트 생성 완료!")
    
    with st.expander("📋 전체 프롬프트 (메모장 저장용)"):
        st.code("\n\n".join(st.session_state.final_prompts), language="markdown")

    st.markdown("### 👇 컷별 상세 확인 & 복사")
    for i, p in enumerate(st.session_state.final_prompts):
        current_text = edited_rows[i]["Text"]
        st.markdown(f"#### 🎞️ Cut {i+1}: {current_text}")
        st.code(p, language="markdown")
