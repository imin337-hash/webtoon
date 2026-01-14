# -*- coding: utf-8 -*-
import streamlit as st
import random

# 1. 페이지 설정
st.set_page_config(page_title="마이툰: 하이브리드 에디터", page_icon="🎨", layout="wide")

# 2. 헤더
st.title("🎨 마이툰(MyToon): 하이브리드 스토리 에디터")
st.markdown("""
**방식 1. 테마 선택:** 검증된 인기 테마(일상, 여행 등)의 시나리오를 불러옵니다.
**방식 2. 주제 입력:** 원하는 주제를 입력하면 AI가 새로운 시나리오를 짜줍니다.
**결과 수정:** 생성된 시나리오는 아래 표에서 자유롭게 수정할 수 있습니다.
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
# 4. 시나리오 생성 로직 (두 가지 방식)
# ==========================================

# [방식 A] 테마별 고정 템플릿 (Theme Presets)
def get_theme_preset(theme):
    if theme == "일상 공감":
        return [
            {"Cut": 1, "Action": "posing lazily on sofa, holding phone", "Text": "주말 순삭"},
            {"Cut": 2, "Action": "looking at clock, shocked face", "Text": "벌써 저녁?!"},
            {"Cut": 3, "Action": "opening fridge, empty inside", "Text": "먹을 게 없네.."},
            {"Cut": 4, "Action": "scrolling delivery app on phone", "Text": "배달 시킬까?"},
            {"Cut": 5, "Action": "looking at expensive delivery fee", "Text": "배달비 실화?"},
            {"Cut": 6, "Action": "cooking ramen instead, boiling pot", "Text": "라면이나 먹자"},
            {"Cut": 7, "Action": "spilling soup on table, disaster", "Text": "앗 뜨거!"},
            {"Cut": 8, "Action": "cleaning up mess, crying face", "Text": "내 주말 돌려줘"},
            {"Cut": 9, "Action": "eating ramen finally, happy face", "Text": "그래도 맛있다"},
            {"Cut": 10, "Action": "lying in bed, peaceful", "Text": "내일은 월요일.."}
        ]
    elif theme == "여행/휴가":
        return [
            {"Cut": 1, "Action": "packing suitcase with excitement", "Text": "여행 D-Day!"},
            {"Cut": 2, "Action": "running at airport with passport", "Text": "공항 도착!"},
            {"Cut": 3, "Action": "looking out airplane window", "Text": "구름 위둥둥"},
            {"Cut": 4, "Action": "arriving at destination, wide view", "Text": "우와 대박!"},
            {"Cut": 5, "Action": "eating exotic local food", "Text": "현지의 맛"},
            {"Cut": 6, "Action": "taking selfie with landmark", "Text": "인생샷 건짐"},
            {"Cut": 7, "Action": "getting lost, looking at map confused", "Text": "여긴 어디?"},
            {"Cut": 8, "Action": "local helping with directions, smiling", "Text": "친절해라"},
            {"Cut": 9, "Action": "watching sunset on beach", "Text": "힐링 그 자체"},
            {"Cut": 10, "Action": "waving goodbye with souvenir", "Text": "또 올게!"}
        ]
    elif theme == "성장/도전":
        return [
            {"Cut": 1, "Action": "wearing headband, determined look", "Text": "오늘부터 갓생!"},
            {"Cut": 2, "Action": "making a plan list on notebook", "Text": "계획은 완벽해"},
            {"Cut": 3, "Action": "starting to work out or study hard", "Text": "시작이 반이다"},
            {"Cut": 4, "Action": "feeling tired, sweating profusely", "Text": "벌써 힘들어.."},
            {"Cut": 5, "Action": "temptation appearing (game or snack)", "Text": "조금만 쉴까?"},
            {"Cut": 6, "Action": "shaking head, refusing temptation", "Text": "안돼! 참자!"},
            {"Cut": 7, "Action": "focusing deeply again, burning eyes", "Text": "집중! 집중!"},
            {"Cut": 8, "Action": "achieving small goal, sparkling effect", "Text": "해냈다!"},
            {"Cut": 9, "Action": "flexing arm or holding trophy", "Text": "뿌듯함"},
            {"Cut": 10, "Action": "thumbs up to camera", "Text": "너도 할 수 있어"}
        ]
    elif theme == "연애/사랑":
        return [
            {"Cut": 1, "Action": "checking phone nervous face", "Text": "연락 올 때 됐는데"},
            {"Cut": 2, "Action": "phone ringing, happy surprise", "Text": "왔다!!"},
            {"Cut": 3, "Action": "getting ready, choosing clothes", "Text": "뭐 입지?"},
            {"Cut": 4, "Action": "meeting partner, shy smile", "Text": "안녕?"},
            {"Cut": 5, "Action": "drinking coffee at cafe together", "Text": "분위기 좋다"},
            {"Cut": 6, "Action": "small misunderstanding, pouting", "Text": "흥!"},
            {"Cut": 7, "Action": "partner giving flowers or apologizing", "Text": "미안해~"},
            {"Cut": 8, "Action": "smiling brightly, holding hands", "Text": "금방 풀림"},
            {"Cut": 9, "Action": "walking in sunset silhouette", "Text": "함께라서 좋아"},
            {"Cut": 10, "Action": "blowing a heart kiss", "Text": "사랑해"}
        ]
    elif theme == "공포/미스터리":
        return [
            {"Cut": 1, "Action": "lying in bed at night, dark room", "Text": "잠이 안 와"},
            {"Cut": 2, "Action": "hearing creaking sound", "Text": "무슨 소리지?"},
            {"Cut": 3, "Action": "looking at the closet door", "Text": "저기 누구 있어?"},
            {"Cut": 4, "Action": "shadow moving slowly", "Text": "움직였다!"},
            {"Cut": 5, "Action": "hiding under blanket shaking", "Text": "살려주세요"},
            {"Cut": 6, "Action": "gathering courage holding flashlight", "Text": "확인해보자"},
            {"Cut": 7, "Action": "opening the closet door quickly", "Text": "에잇!"},
            {"Cut": 8, "Action": "revealing a cute cat inside", "Text": "야옹?"},
            {"Cut": 9, "Action": "sigh of relief wiping sweat", "Text": "너였구나.."},
            {"Cut": 10, "Action": "hugging cat, sleeping", "Text": "다행이다"}
        ]
    else: # 기본
        return generate_custom_draft(f"{theme} 이야기")

# [방식 B] 커스텀 주제 입력 (Custom Prompt Logic)
def generate_custom_draft(topic):
    """주제를 입력받아 AI가 10컷을 창작하는 로직 (템플릿 엔진)"""
    return [
        {"Cut": 1, "Action": f"holding title card '{topic}', confident", "Text": f"주제:\n{topic}"},
        {"Cut": 2, "Action": "intro scene, walking or sitting", "Text": "시작!"},
        {"Cut": 3, "Action": f"facing situation related to {topic}", "Text": "어라?"},
        {"Cut": 4, "Action": "trying to do something, focused", "Text": "열심 열심"},
        {"Cut": 5, "Action": "problem occuring, shocked face", "Text": "앗! 문제 발생"},
        {"Cut": 6, "Action": "feeling sad or confused", "Text": "어떡하지.."},
        {"Cut": 7, "Action": "having a brilliant idea, lightbulb", "Text": "좋은 생각!"},
        {"Cut": 8, "Action": f"solving {topic} problem actively", "Text": "해결해보자"},
        {"Cut": 9, "Action": "success moment, happy celebration", "Text": "성공!"},
        {"Cut": 10, "Action": "waving goodbye, happy ending", "Text": "안녕~"}
    ]

# ==========================================
# 5. 프롬프트 생성 (빌더)
# ==========================================
def build_prompts(rows, ctype, cfeat, coutfit, style_name, layout, lang, seed, use_side, side_desc, panel_mode):
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
        mode_kw = "2 panel comic strip, vertical layout, top and bottom panels"
        neg_kw = "--no 4 panel grid, single image"
    elif "3컷" in panel_mode:
        mode_kw = "3 panel comic strip, vertical webtoon layout"
        neg_kw = "--no single image, 4 panel grid"
    elif "4컷" in panel_mode:
        mode_kw = "4 panel comic, 2x2 grid layout, four distinct scenes"
        neg_kw = "--no single image, vertical strip"
    else:
        mode_kw = "character sheet, multiple poses, expression sheet, white background"
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

with st.sidebar.expander("👥 조연(Sidekick) 추가"):
    use_sidekick = st.checkbox("조연 등장시키기", value=False)
    sidekick_type = st.selectbox("조연 유형", list(SIDEKICK_DEFAULTS.keys()))
    sidekick_desc = st.text_input("조연 묘사", value=SIDEKICK_DEFAULTS[sidekick_type])

st.sidebar.divider()
st.sidebar.header("2️⃣ 스타일 설정")
style_name = st.sidebar.select_slider("그림체 농도", options=list(ART_STYLE_MAP.keys()), value="5. 웹툰/셀식 채색 (Webtoon)")
layout_mode = st.sidebar.selectbox("연출 방식", ["1. 안정적 (Standard)", "2. 다이내믹 (Dynamic)", "3. 시네마틱 (Cinematic)", "4. 셀카 모드 (Selfie)", "5. 1인칭 시점 (POV)", "6. 아이소메트릭 (Isometric)", "7. 항공 샷 (Drone)", "8. 로우 앵글 (Low Angle)", "9. 어안 렌즈 (Fish-eye)", "10. 실루엣 (Silhouette)"])
panel_choice = st.sidebar.selectbox("🎞️ 1장당 컷 수", ["1컷 (추천)", "2컷 (세로 분할)", "3컷 (웹툰형)", "4컷 (격자)", "캐릭터 시트"])
text_lang = st.sidebar.radio("말풍선 언어", ["한국어", "영어", "없음"])
seed_num = st.sidebar.number_input("시드(Seed)", value=1234)

# --- 메인 화면: 스토리 모드 선택 ---
st.subheader("📝 스토리 시나리오 설정")

# 탭을 사용하여 두 가지 방식을 구분
tab1, tab2 = st.tabs(["📚 테마 선택 (추천)", "✍️ 직접 입력 (커스텀)"])

# 세션 상태 초기화
if 'scenario_rows' not in st.session_state:
    st.session_state.scenario_rows = get_theme_preset("일상 공감")

with tab1:
    col_t1, col_t2 = st.columns([0.7, 0.3])
    with col_t1:
        selected_theme = st.selectbox("원하는 테마를 선택하세요", ["일상 공감", "여행/휴가", "성장/도전", "연애/사랑", "공포/미스터리"])
    with col_t2:
        st.write("")
        st.write("")
        if st.button("📥 테마 불러오기", type="primary"):
            st.session_state.scenario_rows = get_theme_preset(selected_theme)
            st.rerun() # 화면 갱신

with tab2:
    col_c1, col_c2 = st.columns([0.7, 0.3])
    with col_c1:
        custom_topic = st.text_input("만들고 싶은 이야기 주제 (예: 좀비 사태)", value="복권 당첨")
    with col_c2:
        st.write("")
        st.write("")
        if st.button("✨ 새 시나리오 생성", type="primary"):
            st.session_state.scenario_rows = generate_custom_draft(custom_topic)
            st.rerun() # 화면 갱신

st.divider()

# --- 시나리오 에디터 (공통) ---
st.markdown("### 🎬 시나리오 편집기")
st.caption("아래 표에서 행동(Action)과 대사(Text)를 자유롭게 수정한 뒤 '프롬프트 생성'을 누르세요.")

edited_rows = st.data_editor(
    st.session_state.scenario_rows,
    num_rows="fixed",
    column_config={
        "Cut": st.column_config.NumberColumn("컷", disabled=True, width="small"),
        "Action": st.column_config.TextColumn("행동 묘사 (영어 권장)", width="large"),
        "Text": st.column_config.TextColumn("말풍선 대사", width="medium"),
    },
    hide_index=True,
    use_container_width=True
)

st.write("")
if st.button("🚀 프롬프트 생성하기 (Click)", type="primary", use_container_width=True):
    final_prompts = build_prompts(
        edited_rows, char_type, char_feature, char_outfit, 
        style_name, layout_mode, text_lang, seed_num, use_sidekick, sidekick_desc, panel_choice
    )
    st.session_state.final_prompts = final_prompts

# --- 결과 출력 ---
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
