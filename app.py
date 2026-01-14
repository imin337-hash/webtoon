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
st.set_page_config(page_title="마이툰: 풀옵션 스튜디오", page_icon="💎", layout="wide")

# ==========================================
# 2. 데이터 (캐릭터, 조연, 스타일)
# ==========================================
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

# --- 1. 캐릭터 설정 ---
st.sidebar.header("1️⃣ 캐릭터 설정")
char_type = st.sidebar.selectbox("캐릭터 프리셋", list(CHAR_DEFAULTS.keys()), key="char_type_selector", on_change=update_char_defaults)

if 'char_name_input' not in st.session_state: st.session_state.char_name_input = CHAR_DEFAULTS["나노바나나 (Original)"][0]
if 'char_role_input' not in st.session_state: st.session_state.char_role_input = CHAR_DEFAULTS["나노바나나 (Original)"][1]
if 'char_feature_input' not in st.session_state: st.session_state.char_feature_input = CHAR_DEFAULTS["나노바나나 (Original)"][2]
if 'char_outfit_input' not in st.session_state: st.session_state.char_outfit_input = CHAR_DEFAULTS["나노바나나 (Original)"][3]

c1, c2 = st.sidebar.columns(2)
with c1: char_name = st.text_input("이름", key="char_name_input")
with c2: char_role = st.text_input("역할", key="char_role_input")

char_feature = st.sidebar.text_input("외모 (Eng)", key="char_feature_input")
char_outfit = st.sidebar.text_input("의상 (Eng)", key="char_outfit_input")

# --- 조연 설정 (기능 강화됨!) ---
with st.sidebar.expander("👥 조연(Sidekick) 설정"):
    use_sidekick = st.checkbox("조연 등장", value=False)
    
    if use_sidekick:
        sidekick_type = st.selectbox("조연 유형", list(SIDEKICK_DEFAULTS.keys()), key="sidekick_selector", on_change=update_sidekick_defaults)
        
        # [NEW] 조연 이름과 관계 입력
        sk_c1, sk_c2 = st.columns(2)
        with sk_c1:
            sidekick_name = st.text_input("조연 이름", value="삐삐")
        with sk_c2:
            sidekick_relation = st.text_input("관계", value="단짝 친구")
            
        if 'sidekick_desc_input' not in st.session_state:
            st.session_state.sidekick_desc_input = SIDEKICK_DEFAULTS.get("작은 새 (Bird)", "")
        
        sidekick_desc = st.text_input("조연 외모 묘사 (Eng)", key="sidekick_desc_input")
    else:
        sidekick_name = ""
        sidekick_relation = ""
        sidekick_desc = ""

st.sidebar.divider()

# --- 2. 스타일 & 연출 설정 ---
st.sidebar.header("2️⃣ 스타일 & 옵션")
style_name = st.sidebar.selectbox("🎨 그림체", options=list(ART_STYLE_MAP.keys()), index=0)

layout_mode = st.sidebar.selectbox("연출/앵글", ["1. 안정적 (Standard)", "2. 다이내믹 (Dynamic)", "3. 시네마틱 (Cinematic)", "4. 셀카 모드 (Selfie)", "5. 1인칭 시점 (POV)", "6. 아이소메트릭 (Isometric)", "7. 항공 샷 (Top-down)", "8. 로우 앵글 (Low Angle)", "9. 어안 렌즈 (Fisheye)", "10. 실루엣 (Silhouette)"])

panel_choice = st.sidebar.selectbox("🎞️ 1장당 컷 수", ["1컷 (추천)", "2컷 (세로 분할)", "3컷 (웹툰형)", "4컷 (격자)", "캐릭터 시트"])

text_lang = st.sidebar.radio("💬 말풍선 언어", ["한국어", "영어", "없음"])

seed_num = st.sidebar.number_input("Seed (고정값)", value=1234)

# ==========================================
# 4. 로직 함수들
# ==========================================

# (1) 10컷 생성 (조연 정보 포함)
def generate_10cut_story(api_key, model_name, theme, content, char_info, sidekick_info):
    if not has_lib: return None, "라이브러리 미설치"
    genai.configure(api_key=api_key)
    
    # 조연 정보 문자열 구성
    sk_prompt = ""
    if sidekick_info['use']:
        sk_prompt = f"Sidekick: {sidekick_info['name']} (Relationship: {sidekick_info['relation']}). Interact with them."

    prompt = f"""
    Create a funny and creative 10-cut storyboard. 
    
    [Settings]
    - Theme: {theme}
    - Content/Topic: {content}
    - Main Character: {char_info['name']} ({char_info['role']})
    - {sk_prompt}
    
    [Format]
    Cut Number|Action (English visual description)|Dialogue (Korean)
    
    Example:
    Cut 1|Nano looking at the calendar|오늘이 그날인가?
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

# (2) 기획안 생성 (조연 정보 포함)
def generate_webtoon_plan(api_key, model_name, theme, content, char_info, sidekick_info):
    if not has_lib: return "라이브러리 미설치"
    genai.configure(api_key=api_key)

    c_str = f"이름: {char_info['name']}, 역할: {char_info['role']}, 외모: {char_info['feature']}, 의상: {char_info['outfit']}"
    
    # 조연 정보 추가
    if sidekick_info['use']:
        c_str += f"\n- 주요 조연: {sidekick_info['name']} (관계: {sidekick_info['relation']}, 외모: {sidekick_info['desc']})"

    prompt = f"""
    당신은 전문 웹툰 PD입니다. 아래 정보를 바탕으로 [웹툰 기획안]을 작성하세요.
    
    - 장르: {theme}
    - 소재: {content}
    - 등장인물 설정: 
    {c_str}
    
    [작성 항목]
    1. **작품 정보**: 제목, 작가(AI), 장르, 수위, 타깃, 분량.
    2. **로그라인**: 1~2줄 핵심 요약.
    3. **기획 의도**: 동기 및 차별점.
    4. **캐릭터 프로필**:
       - 주인공과 조연의 성격, 서사, 관계성을 상세히 서술.
    5. **전체 줄거리**: 기승전결 (결말 포함).
    6. **초반 에피소드(1~3화)** 요약.
    
    출력: 마크다운 포맷.
    """
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"오류: {e}"

# (3) 10컷 프롬프트 빌더
def build_10cut_prompts(rows, cfeat, coutfit, style_name, layout, lang, panel_mode, seed, sidekick_info):
    full_char = f"{cfeat}, wearing {coutfit}, expressive face"
    
    # 이미지 프롬프트에 조연 묘사 추가
    if sidekick_info['use']: 
        full_char += f", accompanied by {sidekick_info['desc']} ({sidekick_info['name']})"
    
    style_kw = ART_STYLE_MAP[style_name]
    
    layout_map = {
        "1. 안정적": "flat composition", "2. 다이내믹": "dynamic angle", 
        "3. 시네마틱": "cinematic lighting", "4. 셀카 모드": "selfie angle",
        "5. 1인칭 시점": "pov shot", "6. 아이소메트릭": "isometric view",
        "7. 항공 샷": "top down view", "8. 로우 앵글": "low angle",
        "9. 어안 렌즈": "fisheye lens", "10. 실루엣": "silhouette"
    }
    layout_kw = layout_map.get(layout.split(" (")[0], "flat composition")

    if "1컷" in panel_mode:
        mode_kw = "single panel, independent illustration, full shot"
        neg_kw = "--no comic grid, storyboard, multiple panels"
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
        text = row['Text']
        if lang == "한국어":
            text_p = f'speech bubble with text "{text}", written in legible Korean Hangul font'
        elif lang == "영어":
            text_p = f'speech bubble with text "{text}", written in English'
        else:
            text_p = "no text, no speech bubble"

        p = f"/imagine prompt: **[Subject]** {full_char} **[Action]** {row['Action']} **[Text]** {text_p} **[Style]** {style_kw}, {layout_kw}, {mode_kw} --ar 4:5 --niji 6 --seed {seed} {neg_kw}"
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
        ("액션 (Action)", f"dynamic action poses, running, jumping, fighting pose")
    ]
    
    results = []
    for title, kw in sheet_types:
        p = f"/imagine prompt: {full_char}, {kw}, {style_kw} --ar 3:2 --niji 6 --seed {seed}"
        results.append((title, p))
    return results

# ==========================================
# 5. 메인 UI
# ==========================================
st.title("💎 마이툰 스튜디오 (Full Option)")
st.caption("나만의 캐릭터와 다채로운 스타일로 웹툰을 기획하세요.")

# 정보 딕셔너리 구성
char_info_dict = {
    "name": char_name, "role": char_role, 
    "feature": char_feature, "outfit": char_outfit
}
sidekick_info_dict = {
    "use": use_sidekick,
    "name": sidekick_name, "relation": sidekick_relation, "desc": sidekick_desc
}

tab1, tab2 = st.tabs(["🎬 10컷 인스타툰", "📑 웹툰 기획안"])

# --- TAB 1 ---
with tab1:
    st.markdown(f"#### 📱 {char_name}의 인스타툰")
    col1, col2, col3 = st.columns([0.3, 0.5, 0.2])
    with col1:
        t1_theme = st.selectbox("테마", ["일상/공감", "개그", "감동", "연애", "판타지", "홍보"], key="t1_theme")
    with col2:
        t1_content = st.text_input("내용", value=f"{char_role} {char_name}의 하루", key="t1_content")
    with col3:
        st.write("")
        st.write("")
        if st.button("✨ 10컷 생성", key="btn_10cut"):
            if gemini_api_key:
                with st.spinner("작성 중..."):
                    res, model = generate_10cut_story(gemini_api_key, selected_model_name, t1_theme, t1_content, char_info_dict, sidekick_info_dict)
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
            edited_rows, char_feature, char_outfit, style_name, 
            layout_mode, text_lang, panel_choice, seed_num, 
            sidekick_info_dict
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
                    plan_result = generate_webtoon_plan(gemini_api_key, selected_model_name, t2_genre, t2_content, char_info_dict, sidekick_info_dict)
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
