# -*- coding: utf-8 -*-
import streamlit as st
import random

# 1. 페이지 설정
st.set_page_config(page_title="마이툰: AI 인스타툰 메이커", page_icon="🎨", layout="wide")

# 2. 헤더
st.title("🎨 마이툰(MyToon): AI 인스타툰 생성기")
st.markdown("""
**캐릭터, 스토리, 그림체**를 선택하면 AI가 인스타툰 프롬프트를 완성해줍니다.
그림체 농도를 **10단계**로 조절하여 원하는 스타일을 찾아보세요.
""")

# ==========================================
# 3. 데이터 및 헬퍼 함수
# ==========================================

# (1) 캐릭터 기본값
CHAR_DEFAULTS = {
    "고양이 (Cat)": ("white fur, pointy ears, pink nose", "red ribbon collar"),
    "강아지 (Dog)": ("golden curly fur, floppy ears", "green scarf"),
    "토끼 (Rabbit)": ("long ears, fluffy white fur", "cute pink dress"),
    "곰 (Bear)": ("brown fur, round ears, teddy bear look", "striped t-shirt"),
    "사람-여자 (Girl)": ("long brown hair, cute face, k-pop style", "pastel hoodie, denim skirt"),
    "사람-남자 (Boy)": ("short black hair, casual look, glasses", "oversized sweatshirt, cargo pants"),
    "직접 입력 (Custom)": ("", "")
}

# (2) 테마별 랜덤 소재
THEME_IDEAS = {
    "일상": ["월요병 탈출", "다이어트 실패", "택배 언박싱", "비 오는 날 감성", "주말 순삭", "미용실 망함"],
    "성장": ["첫 헬스장 도전", "영어 공부 시작", "운전면허 따기", "요리 초보 탈출", "나쁜 습관 고치기"],
    "꿀팁": ["아이폰 꿀팁", "자취생 필수템", "사진 잘 찍는 법", "여행 짐 싸기", "돈 모으는 법"],
    "감동": ["퇴근길 위로", "오랜 친구와의 만남", "반려동물의 위로", "나를 사랑하는 법", "작은 행복 찾기"],
    "여행": ["일본 편의점 털기", "제주도 바다 여행", "공항 여권 샷", "기차 여행의 낭만", "호캉스 즐기기"],
    "연애": ["첫 데이트 코디", "기념일 선물", "사소한 다툼", "심쿵 포인트", "집 데이트"],
    "공포": ["엘리베이터 괴담", "잘 때 들리는 소리", "가위 눌림", "내 뒤에 누구?", "밤길 조심"],
    "리뷰": ["신상 간식 리뷰", "내돈내산 립스틱", "편의점 도시락", "삶의 질 상승템", "블루투스 스피커"],
    "요리": ["한강 라면 끓이기", "김치볶음밥 만들기", "홈베이킹 실패", "야식의 유혹", "브런치 만들기"],
    "덕질": ["콘서트 티켓팅", "최애 생일 카페", "굿즈 언박싱", "덕질 투어", "새벽 스밍"]
}

# (3) 그림체 10단계 매핑 데이터
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

# (4) 콜백 함수들
def update_char_defaults():
    selected_type = st.session_state.char_type_selector
    defaults = CHAR_DEFAULTS.get(selected_type, ("", ""))
    st.session_state.char_feature_input = defaults[0]
    st.session_state.char_outfit_input = defaults[1]

def generate_random_idea():
    current_theme_key = next((k for k in THEME_IDEAS.keys() if k in st.session_state.theme_selector), "일상")
    idea = random.choice(THEME_IDEAS[current_theme_key])
    st.session_state.story_detail_input = idea

# ==========================================
# 4. 사이드바 UI
# ==========================================
st.sidebar.header("1️⃣ 캐릭터 설정")
char_type = st.sidebar.selectbox("주인공 유형", list(CHAR_DEFAULTS.keys()), key="char_type_selector", on_change=update_char_defaults)

custom_species = ""
if char_type == "직접 입력 (Custom)":
    custom_species = st.sidebar.text_input("캐릭터 종족 입력", "Hamster")

if 'char_feature_input' not in st.session_state: st.session_state.char_feature_input = CHAR_DEFAULTS["고양이 (Cat)"][0]
if 'char_outfit_input' not in st.session_state: st.session_state.char_outfit_input = CHAR_DEFAULTS["고양이 (Cat)"][1]

char_feature = st.sidebar.text_input("외모 특징 (자동/수정)", key="char_feature_input")
char_outfit = st.sidebar.text_input("착용 의상 (자동/수정)", key="char_outfit_input")

st.sidebar.divider()
st.sidebar.header("2️⃣ 스토리 설정")
story_theme = st.sidebar.selectbox(
    "이야기 테마",
    ["1. 일상 공감 (Daily)", "2. 성장/도전 (Growth)", "3. 꿀팁 정보 (Info)", "4. 감동/힐링 (Healing)", "5. ✈️ 여행/휴가 (Travel)", 
     "6. 💕 연애/사랑 (Romance)", "7. 👻 공포/미스터리 (Horror)", "8. 📦 제품 리뷰 (Review)", "9. 🍳 요리/먹방 (Cooking)", "10. 🎨 덕질/취미 (Hobby)"],
    key="theme_selector"
)

col_btn, col_text = st.sidebar.columns([0.4, 0.6])
with col_btn:
    st.write("")
    st.write("")
    st.button("🎲 소재 추천", on_click=generate_random_idea)

if 'story_detail_input' not in st.session_state: st.session_state.story_detail_input = "월요병 탈출"
with col_text:
    story_detail = st.text_input("세부 소재 (직접 입력)", key="story_detail_input")

st.sidebar.divider()
st.sidebar.header("3️⃣ 스타일 & 연출")

# [NEW] 그림체 10단계 선택
st.sidebar.subheader("🎨 그림체 농도 (Art Style)")
selected_style_name = st.sidebar.select_slider(
    "스타일 강도 선택",
    options=list(ART_STYLE_MAP.keys()),
    value="5. 웹툰/셀식 채색 (Webtoon)"
)

layout_mode = st.sidebar.selectbox(
    "카메라 연출",
    ["1. 안정적 (Standard)", "2. 다이내믹 (Dynamic)", "3. 시네마틱 (Cinematic)", "4. 셀카 모드 (Selfie)", "5. 1인칭 시점 (POV)",
     "6. 아이소메트릭 (Isometric)", "7. 항공 샷 (Drone)", "8. 로우 앵글 (Low Angle)", "9. 어안 렌즈 (Fish-eye)", "10. 실루엣 (Silhouette)"]
)

output_mode = st.sidebar.radio("출력 방식", ["단일 컷 (1장 추천)", "캐릭터 시트"], index=0)
text_lang = st.sidebar.radio("말풍선 언어", ["한국어", "영어", "없음"])
seed_num = st.sidebar.number_input("시드(Seed)", value=1234)

# ==========================================
# 5. 로직 구현
# ==========================================
def make_prompts(mode, ctype, cspec, cfeat, coutfit, theme, detail, layout, style_name, lang, seed):
    
    # 1. 캐릭터
    if ctype == "직접 입력 (Custom)": species = cspec
    else: species = ctype.split("(")[1].replace(")", "")
    
    if species in ["Cat", "Dog", "Rabbit", "Bear", "Hamster", "Tiger"]: base_char = f"Cute anthropomorphic {species} character"
    else: base_char = f"Cute {species} character"

    full_char_desc = f"{base_char}, {cfeat}, wearing {coutfit}"

    # 2. 스타일 (10단계 매핑)
    style_kw = ART_STYLE_MAP[style_name]
    
    # 3. 레이아웃
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

    # 4. 출력 모드
    if "단일" in mode:
        mode_kw = "single panel, independent illustration, full shot, one image"
        neg_kw = "--no comic grid, storyboard, multiple panels, split view"
    else:
        mode_kw = "character sheet, multiple poses"
        neg_kw = ""

    # 5. 시나리오 생성 (간소화 로직)
    context_str = f"Concept: {detail}"
    
    # 테마별 기본 템플릿 (상황에 맞춰 detail 주입)
    if "일상" in theme:
        scenarios = [("posing confident", "시작", "Start"), ("waking up", "준비", "Ready"), (f"dealing with {detail}", "어?", "Huh?"), ("struggling", "힘들어", "Hard"), ("panic face", "으아아", "Argh"), ("mistake", "망했다", "Oops"), ("small happy", "그래도..", "Good"), ("relaxing", "휴식", "Rest"), ("thumbs up", "공감?", "Like"), ("waving", "안녕", "Bye")]
    elif "여행" in theme:
        scenarios = [("packing bag", "짐싸기", "Pack"), ("airport", "출발!", "Go"), (f"arriving at {detail}", "도착", "Arrive"), ("selfie", "인생샷", "Selfie"), ("eating", "냠냠", "Yum"), ("scenery", "예쁘다", "Pretty"), ("healing", "힐링", "Healing"), ("night", "야경", "Night"), ("tired", "피곤", "Tired"), ("waving", "또 봐요", "See ya")]
    else:
        scenarios = [(f"intro {detail}", "주목", "Look"), ("walking", "안녕", "Hello"), ("looking", "뭐지?", "What?"), ("surprised", "대박", "Wow"), (f"doing {detail}", "영차", "Action"), ("funny", "헤헤", "Hehe"), ("result", "짠!", "Ta-da"), ("happy", "좋아요", "Like"), ("thumbs up", "최고", "Best"), ("waving", "잘가요", "Bye")]

    prompts = []
    for action, ko, en in scenarios:
        if "한국어" in lang: text_p = f'speech bubble with text "{ko}", written in Korean Hangul font'
        elif "영어" in lang: text_p = f'speech bubble with text "{en}", written in English'
        else: text_p = "no text"

        p = f"/imagine prompt: **[Topic]** {context_str} **[Subject]** {full_char_desc} **[Action]** {action} **[Text]** {text_p} **[Style]** {style_kw}, {angle_kw}, {mode_kw} --ar 4:5 --niji 6 --seed {seed} {neg_kw}"
        prompts.append(p)

    return prompts, scenarios

# ==========================================
# 6. 결과 출력 UI
# ==========================================
if 'generated_prompts' not in st.session_state:
    st.session_state.generated_prompts = []
    st.session_state.current_scenarios = []

if st.button("🚀 마이툰 프롬프트 생성하기 (Click)"):
    with st.spinner(f"AI가 '{st.session_state.story_detail_input}' 내용을 그리는 중..."):
        prompts, scenes = make_prompts(
            output_mode, char_type, custom_species, char_feature, char_outfit, 
            story_theme, st.session_state.story_detail_input, layout_mode, selected_style_name, text_lang, seed_num
        )
        st.session_state.generated_prompts = prompts
        st.session_state.current_scenarios = scenes

if st.session_state.generated_prompts:
    st.divider()
    st.success(f"✅ 생성 완료! (주제: {st.session_state.story_detail_input} / 스타일: {selected_style_name})")
    
    st.caption("👇 각 컷의 설명을 확인하고, 아래 검은 박스의 코드를 복사하세요. (복사 버튼은 코드 박스 오른쪽 위에 나타납니다)")

    for i, p in enumerate(st.session_state.generated_prompts):
        # 장면 텍스트 추출
        scene_txt = st.session_state.current_scenarios[i][1] if "한국어" in text_lang else st.session_state.current_scenarios[i][2]
        
        # [Layout Update] 글자를 왼쪽 위에 크게 배치하여 '왼쪽 정렬' 느낌 강조
        st.markdown(f"#### 🎞️ Cut {i+1}: {scene_txt}")
        st.code(p, language="markdown")
