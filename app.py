# -*- coding: utf-8 -*-
import streamlit as st
import sys

# 0. 라이브러리 진단 및 임포트
try:
    import google.generativeai as genai
    lib_version = genai.__version__
    has_lib = True
except ImportError:
    lib_version = "설치 안됨"
    has_lib = False

# 1. 페이지 설정
st.set_page_config(page_title="마이툰: 커스텀 스튜디오", page_icon="🎨", layout="wide")

# ==========================================
# 2. 데이터 (캐릭터, 조연, 스타일 확장)
# ==========================================

# 구조: Key : (이름, 역할, 외모 묘사(En), 의상(En))
CHAR_DEFAULTS = {
    "나노바나나 (Original)": ("나노", "미래에서 온 바나나", "Cute anthropomorphic Banana character", "sleek futuristic pro-headset"),
    "나노 (오피스룩)": ("나노", "신입 사원", "Cute anthropomorphic Banana character", "formal suit and glasses, office worker vibe"),
    "고양이 (Cat)": ("치즈", "장화 신은 고양이", "yellow ginger cat, standing on two feet", "musketeer hat and cape"),
    "강아지 (Dog)": ("뭉치", "용감한 탐험가", "golden retriever puppy", "scout scarf and backpack"),
    "소녀 (K-Pop)": ("유나", "아이돌 연습생", "beautiful k-pop style girl, long brown hair", "colorful stage outfit, shiny accessories"),
    "소년 (Casual)": ("민수", "평범한 대학생", "handsome young man, short black hair", "oversized hoodie, cargo pants, headphones"),
    "토끼 (Rabbit)": ("버니", "마법 소녀", "cute white rabbit with human proportions", "pink magical girl dress, holding wand"),
    "곰 (Bear)": ("브라우니", "카페 사장님", "brown teddy bear", "green apron, holding coffee mug"),
    "기사 (Knight)": ("아서", "왕국 기사단장", "chibi knight character", "shiny silver armor, red cape, holding sword"),
    "마법사 (Wizard)": ("멀린", "대마법사", "old cute wizard, long white beard", "purple starry robe, pointed hat"),
    "탐정 (Detective)": ("셜록", "천재 탐정", "sharp look, holding magnifying glass", "beige trench coat, fedora hat"),
    "외계인 (Alien)": ("알파", "우주 비행사", "cute green skin alien, big black eyes", "orange space suit, helmet"),
    "직접 입력 (Custom)": ("", "", "", "")
}

SIDEKICK_DEFAULTS = {
    "작은 새 (Bird)": "tiny cute blue bird friend",
    "아기 고양이 (Kitten)": "tiny yellow kitten friend",
    "로봇 (Robot)": "mini floating robot friend",
    "유령 (Ghost)": "cute marshmallow ghost friend",
    "요정 (Fairy)": "tiny glowing fairy",
    "슬라임 (Slime)": "cute bouncing blue slime",
    "직접 입력 (Custom)": ""
}

# 스타일 12종으로 대폭 확대
ART_STYLE_MAP = {
    "1. 웹툰/셀식 (Webtoon)": "korean webtoon style, cel shading, vibrant colors, clean outlines, digital art",
    "2. 일본 애니풍 (Anime)": "japanese anime style, studio ghibli inspired, detailed background, soft lighting",
    "3. 미국 카툰 (Cartoon)": "western cartoon style, disney animation style, expressive, smooth shapes",
    "4. 픽셀 아트 (Pixel Art)": "pixel art, 16-bit retro game style, dot graphics",
    "5. 손그림/낙서 (Doodle)": "minimalist doodle, hand drawn sketch, pencil texture, simple lines",
    "6. 플랫 벡터 (Flat)": "flat vector illustration, corporate memphis, simple geometric shapes, no gradients",
    "7. 수채화 (Watercolor)": "watercolor painting, wet brush texture, soft pastel blend, artistic",
    "8. 유화/임파스토 (Oil Paint)": "oil painting, thick brush strokes, impressionist style, textured",
    "9. 3D 큐트 (3D Clay)": "3D render, claymorphism, cute toy texture, blender 3d, soft shadows",
    "10. 실사/영화 (Cinematic)": "unreal engine 5, cinematic lighting, 8k realistic, movie still",
    "11. 누아르 (Noir)": "black and white, film noir, high contrast, dramatic shadows, ink style",
    "12. 사이버펑크 (Cyberpunk)": "cyberpunk style, neon lights, futuristic city background, vibrant pink and blue"
}

def update_char_defaults():
    selected = st.session_state.char_type_selector
    if selected in CHAR_DEFAULTS:
        # 데이터: (이름, 역할, 외모, 의상)
        data = CHAR_DEFAULTS[selected]
        st.session_state.char_name_input = data[0]
        st.session_state.char_role_input = data[1]
        st.session_state.char_feature_input = data[2]
        st.session_state.char_outfit_input = data[3]

def update_sidekick_defaults():
    selected = st.session_state.sidekick_selector
    if selected in SIDEKICK_DEFAULTS:
        st.session_state.sidekick_desc_input = SIDEKICK_DEFAULTS[selected]

# ==========================================
# 3. 사이드바 설정
# ==========================================
st.sidebar.header("🔧 설정 및 모델 선택")
gemini_api_key = st.sidebar.text_input("Gemini API Key", type="password")

available_models = []
if gemini_api_key and has_lib:
    try:
        genai.configure(api_key=gemini_api_key)
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                name = m.name.replace("models/", "")
                available_models.append(name)
    except Exception as e:
        st.sidebar.error(f"연결 실패: {e}")

if available_models:
    selected_model_name = st.sidebar.selectbox("🤖 사용할 모델", available_models, index=0)
else:
    selected_model_name = st.sidebar.text_input("모델명 수동", "gemini-1.5-flash")

st.sidebar.divider()

# --- 캐릭터 설정 (업그레이드) ---
st.sidebar.header("1️⃣ 캐릭터 설정")
# 선택 시 update_char_defaults 콜백 실행
char_type = st.sidebar.selectbox("캐릭터 프리셋", list(CHAR_DEFAULTS.keys()), key="char_type_selector", on_change=update_char_defaults)

# 세션 상태 초기화
if 'char_name_input' not in st.session_state: st.session_state.char_name_input = CHAR_DEFAULTS["나노바나나 (Original)"][0]
if 'char_role_input' not in st.session_state: st.session_state.char_role_input = CHAR_DEFAULTS["나노바나나 (Original)"][1]
if 'char_feature_input' not in st.session_state: st.session_state.char_feature_input = CHAR_DEFAULTS["나노바나나 (Original)"][2]
if 'char_outfit_input' not in st.session_state: st.session_state.char_outfit_input = CHAR_DEFAULTS["나노바나나 (Original)"][3]

# 입력 필드 (자동 입력 + 수정 가능)
col_c1, col_c2 = st.sidebar.columns(2)
with col_c1:
    char_name = st.text_input("이름", key="char_name_input")
with col_c2:
    char_role = st.text_input("역할/직업", key="char_role_input")

char_feature = st.sidebar.text_input("외모 묘사 (English)", key="char_feature_input")
char_outfit = st.sidebar.text_input("의상 (English)", key="char_outfit_input")

with st.sidebar.expander("👥 조연(Sidekick) 추가"):
    use_sidekick = st.checkbox("조연 등장", value=False)
    if use_sidekick:
        sidekick_type = st.selectbox("조연 유형", list(SIDEKICK_DEFAULTS.keys()), key="sidekick_selector", on_change=update_sidekick_defaults)
        
        if 'sidekick_desc_input' not in st.session_state:
            st.session_state.sidekick_desc_input = SIDEKICK_DEFAULTS.get("작은 새 (Bird)", "")
        
        sidekick_desc = st.text_input("조연 묘사 (English)", key="sidekick_desc_input")
        
        # 커스텀일 경우 추가 입력
        if sidekick_type == "직접 입력 (Custom)":
             pass # 묘사에 다 적으면 됨
    else:
        sidekick_desc = ""

st.sidebar.divider()

# --- 스타일 설정 (확장됨) ---
st.sidebar.header("2️⃣ 스타일 설정")
style_name = st.sidebar.selectbox("🎨 그림체 선택 (12종)", options=list(ART_STYLE_MAP.keys()), index=0)
layout_mode = st.sidebar.selectbox("연출", ["1. 안정적", "2. 다이내믹", "3. 시네마틱", "4. 셀카 모드", "5. 1인칭 시점", "6. 아이소메트릭", "7. 항공 샷", "8. 로우 앵글", "9. 어안 렌즈", "10. 실루엣"])
seed_num = st.sidebar.number_input("Seed", value=1234)

# ==========================================
# 4. 로직 함수들
# ==========================================

# (1) 10컷 생성
def generate_10cut_story(api_key, model_name, theme, content, char_name, char_role):
    if not has_lib: return None, "라이브러리 미설치"
    genai.configure(api_key=api_key)
    
    prompt = f"""
    Create a funny 10-cut storyboard. 
    Theme: {theme}, Content: {content}
    Main Character: {char_name} ({char_role})
    Format: Cut Number|Action (English)|Dialogue (Korean)
    """
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        parsed_data = []
        for line in response.text.strip().split('\n'):
            if "|" in line and "Cut" in line:
                parts = line.split('|')
                if len(parts) >= 3:
                    parsed_data.append({
                        "Cut": parts[0].strip().replace("Cut ", "").replace("*", ""),
                        "Action": parts[1].strip(),
                        "Text": parts[2].strip()
                    })
        return parsed_data[:10] if parsed_data else None, model_name
    except Exception as e:
        return None, str(e)

# (2) 기획안 생성
def generate_webtoon_plan(api_key, model_name, theme, content, char_info_dict):
    if not has_lib: return "라이브러리 미설치"
    genai.configure(api_key=api_key)

    # 캐릭터 정보를 상세하게 구성
    c_str = f"이름: {char_info_dict['name']}, 역할: {char_info_dict['role']}, 외모: {char_info_dict['feature']}, 의상: {char_info_dict['outfit']}"
    if char_info_dict['sidekick']:
        c_str += f", 조연: {char_info_dict['sidekick']}"

    prompt = f"""
    당신은 전문 웹툰 PD입니다. 아래 정보를 바탕으로 [웹툰 기획안]을 작성하세요.
    
    [핵심 정보]
    - 장르: {theme}
    - 소재/로그라인: {content}
    - 주인공 및 조연 설정: {c_str}
    
    [작성 항목]
    1. **작품 정보**: 제목(가제), 작가명(AI), 장르, 수위, 타깃 독자, 예상 분량.
    2. **로그라인**: 1~2줄 핵심 요약.
    3. **기획 의도**: 제작 동기 및 차별점.
    4. **캐릭터 프로필**:
       - {char_info_dict['name']} ({char_info_dict['role']}): 성격, 목표, 결핍, 특징 상세 서술.
       - 조연 정보 포함.
    5. **전체 줄거리**: 기승전결 (결말 포함).
    6. **초반 에피소드(1~3화) 요약**.
    
    출력: 가독성 좋은 마크다운 포맷.
    """
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"오류: {e}"

# (3) 10컷 프롬프트 빌더
def build_10cut_prompts(rows, cfeat, coutfit, style_name, layout, seed, use_side, side_desc):
    full_char = f"{cfeat}, wearing {coutfit}, expressive face"
    if use_side: full_char += f", accompanied by {side_desc}"
    style_kw = ART_STYLE_MAP[style_name]
    
    # 레이아웃 매핑 (간소화)
    layout_map = {
        "1. 안정적": "flat composition", "2. 다이내믹": "dynamic angle", 
        "3. 시네마틱": "cinematic lighting", "4. 셀카 모드": "selfie angle",
        "5. 1인칭 시점": "pov shot", "6. 아이소메트릭": "isometric view",
        "7. 항공 샷": "top down view", "8. 로우 앵글": "low angle",
        "9. 어안 렌즈": "fisheye lens", "10. 실루엣": "silhouette"
    }
    layout_kw = layout_map.get(layout, "flat composition")
    
    prompts = []
    for row in rows:
        p = f"/imagine prompt: **[Subject]** {full_char} **[Action]** {row['Action']} **[Text]** speech bubble '{row['Text']}' **[Style]** {style_kw}, {layout_kw} --ar 4:5 --niji 6 --seed {seed}"
        prompts.append(p)
    return prompts

# (4) 캐릭터 시트 빌더
def build_sheet_prompts(cname, crole, cfeat, coutfit, style_name, seed):
    style_kw = ART_STYLE_MAP[style_name]
    full_char = f"character named {cname} ({crole}), {cfeat}, wearing {coutfit}"
    
    sheet_types = [
        ("전신 (Full Body)", f"full body shot, standing pose, character sheet, white background"),
        ("흉상 (Bust)", f"bust shot, close up face, high detail portrait, looking at camera"),
        ("표정 (Expressions)", f"expression sheet, various emotions, happy, sad, angry, surprised"),
        ("액션 포즈 (Action)", f"dynamic action poses, running, jumping, fighting pose")
    ]
    
    results = []
    for title, kw in sheet_types:
        p = f"/imagine prompt: {full_char}, {kw}, {style_kw} --ar 3:2 --niji 6 --seed {seed}"
        results.append((title, p))
    return results

# ==========================================
# 5. 메인 UI
# ==========================================
st.title("💎 마이툰 스튜디오 (Custom)")
st.caption("나만의 캐릭터와 다채로운 스타일로 웹툰을 기획하세요.")

tab1, tab2 = st.tabs(["🎬 10컷 인스타툰", "📑 웹툰 기획안"])

# --- TAB 1 ---
with tab1:
    st.markdown(f"#### 📱 {char_name}의 인스타툰")
    col1, col2, col3 = st.columns([0.3, 0.5, 0.2])
    with col1:
        t1_theme = st.selectbox("테마", ["일상/공감", "개그", "감동", "연애", "판타지", "홍보/정보"], key="t1_theme")
    with col2:
        t1_content = st.text_input("내용", value=f"{char_role} {char_name}의 하루", key="t1_content")
    with col3:
        st.write("")
        st.write("")
        if st.button("✨ 10컷 생성", key="btn_10cut"):
            if gemini_api_key:
                with st.spinner("작성 중..."):
                    res, model = generate_10cut_story(gemini_api_key, selected_model_name, t1_theme, t1_content, char_name, char_role)
                    if res:
                        st.session_state.s1_rows = res
                        st.success("완료!")
            else:
                st.warning("API 키 필요")

    if 's1_rows' not in st.session_state:
        st.session_state.s1_rows = [{"Cut": "1", "Action": "Title card", "Text": "제목"}]

    edited_rows = st.data_editor(st.session_state.s1_rows, num_rows="fixed", hide_index=True, key="editor_10cut")

    if st.button("🚀 10컷 프롬프트 변환", key="btn_trans_10cut"):
        prompts = build_10cut_prompts(
            edited_rows, char_feature, char_outfit, style_name, layout_mode, seed_num, 
            use_sidekick, sidekick_desc
        )
        st.code("\n\n".join(prompts), language="markdown")

# --- TAB 2 ---
with tab2:
    st.markdown("#### 📑 커스텀 웹툰 기획안")
    st.info(f"설정된 캐릭터 **[{char_name} / {char_role}]** 정보가 기획안에 자동 반영됩니다.")
    
    col_p1, col_p2, col_p3 = st.columns([0.3, 0.5, 0.2])
    with col_p1:
        t2_genre = st.selectbox("장르", ["로판", "현대물", "학원물", "스릴러", "일상물", "액션", "SF"], key="t2_genre")
    with col_p2:
        t2_content = st.text_input("소재/로그라인", value=f"{char_role}가 된 {char_name}의 모험", key="t2_content")
    with col_p3:
        st.write("")
        st.write("")
        if st.button("📝 기획안 생성", key="btn_plan"):
            if gemini_api_key:
                with st.spinner("기획안 작성 중..."):
                    char_info = {
                        "name": char_name, "role": char_role,
                        "feature": char_feature, "outfit": char_outfit,
                        "sidekick": sidekick_desc if use_sidekick else ""
                    }
                    plan_result = generate_webtoon_plan(gemini_api_key, selected_model_name, t2_genre, t2_content, char_info)
                    st.session_state.plan_result = plan_result
                    st.success("완료!")
            else:
                st.warning("API 키 필요")

    if 'plan_result' in st.session_state:
        st.divider()
        st.markdown(st.session_state.plan_result)
        st.divider()
        st.subheader(f"🎨 {char_name} 캐릭터 시트")
        
        sheet_prompts = build_sheet_prompts(char_name, char_role, char_feature, char_outfit, style_name, seed_num)
        c1, c2 = st.columns(2)
        for idx, (title, p) in enumerate(sheet_prompts):
            with (c1 if idx % 2 == 0 else c2):
                st.markdown(f"**{title}**")
                st.code(p, language="markdown")
