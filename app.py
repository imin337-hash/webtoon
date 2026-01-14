# -*- coding: utf-8 -*-
import streamlit as st
import random

# 1. 페이지 설정
st.set_page_config(page_title="마이툰: AI 인스타툰 메이커", page_icon="🎨", layout="wide")

# 2. 헤더
st.title("🎨 마이툰(MyToon): 공감 100% 인스타툰 생성기")
st.markdown("""
**캐릭터, 스토리, 그림체**를 선택하면 10컷의 인스타툰 프롬프트를 완성해줍니다.
주제만 던져주면 사람들이 공감할 수 있는 **깊이 있는 이야기**를 만들어드립니다.
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

# (2) 테마별 심화 소재 (Deep Ideas)
THEME_IDEAS = {
    "일상": ["아무것도 안 했는데 벌써 밤", "다이어트 결심하고 야식 먹음", "월급 스치고 지나감", "미용실에서 머리 망했을 때"],
    "성장": ["남들과 비교되어 우울할 때", "작심삼일 극복하기", "처음으로 혼자 해낸 일", "서툴러도 괜찮아"],
    "꿀팁": ["자취생 식비 아끼는 법", "사진 똥손 탈출하기", "면접 긴장 푸는 법", "여행 짐 싸기 만렙"],
    "감동": ["힘든 하루 끝의 위로", "무지개다리 건넌 반려동물", "오랜 친구의 전화 한 통", "나에게 주는 선물"],
    "여행": ["P의 좌충우돌 여행기", "혼자 떠난 여행의 묘미", "여행지에서 만난 인연", "돌아오기 싫은 순간"],
    "연애": ["썸 탈 때의 미묘한 기류", "장거리 연애의 애틋함", "사소한 걸로 싸우고 화해", "권태기 극복"],
    "공포": ["엘리베이터 거울 괴담", "자취방 낯선 소리", "야근 중 사무실 귀신", "중고거래 괴담"],
    "리뷰": ["광고 보고 샀다가 후회한 템", "삶의 질 수직 상승템", "편의점 신상 솔직 후기", "내돈내산 찐추천"],
    "요리": ["지옥에서 온 요리(실패)", "엄마 레시피 도전", "배달보다 맛있는 집밥", "자취 요리왕"],
    "덕질": ["최애가 나를 봤을 때", "티켓팅 광탈의 슬픔", "굿즈 사려고 오픈런", "휴덕은 있어도 탈덕은 없다"]
}

# (3) 그림체 매핑
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
# 4. 딥 스토리(Deep Story) 생성 로직
# ==========================================
def get_deep_story(theme, detail):
    """
    기대-좌절-극복-공감의 서사 구조 (10컷)
    """
    if "일상" in theme:
        return [
            (f"posing confidently with text '{detail}'", f"오늘의 목표:\n{detail}", f"Goal: {detail}"),
            ("full of energy, fists clenched, burning eyes", "의욕 활활!", "Motivated!"),
            ("looking at clock, time passed quickly", "어... 잠깐만", "Wait..."),
            ("lying on sofa or bed, holding phone, messy room", "조금만 쉴까?", "Just 5 mins"),
            ("scrolling phone zombie face, dark circles", "알고리즘의 늪", "Doom scrolling"),
            ("looking at window, it became night", "벌써 밤이야?!", "Already night?!"),
            ("head hitting the desk, despair", "망했다...", "Ruined..."),
            ("eating late night snack, slightly happy", "일단 먹자", "Eat first"),
            ("lying in bed, staring at ceiling", "내일의 나야 부탁해", "Tomorrow me"),
            ("waving goodbye with tired smile", "다들 공감?", "Relatable?")
        ]
    elif "성장" in theme:
        return [
            (f"looking at mirror or computer, worried face, concept {detail}", "잘 할 수 있을까?", "Can I do it?"),
            ("seeing others succeed on social media, jealous", "남들은 다 잘하네", "Everyone fits in"),
            ("trying hard but making mistakes, sweating", "역시 난 안돼..", "I'm not good"),
            ("sitting in corner, hugging knees, shadow", "자존감 바닥", "Depressed"),
            ("friend or pet approaching gently", "그때 다가온 위로", "Comfort"),
            ("receiving a small note or warm coffee", "괜찮아, 천천히 해", "Take your time"),
            ("wiping tears and standing up", "그래, 다시 한번!", "Try again"),
            ("focusing deeply, glowing eyes", "작은 성공!", "Small win"),
            ("smiling brightly, sunlight hitting face", "나만의 속도로", "My own pace"),
            ("making a heart with hands", "당신을 응원해요", "Cheer for U")
        ]
    elif "여행" in theme:
        return [
            ("packing suitcase with chaos, messy room", "짐 싸다 지침", "Packing chaos"),
            ("running to catch transport, sweating", "늦었다 늦었어!", "Late!!"),
            ("looking at map, lost in strange street", "여긴 어디?", "Lost..."),
            ("sudden rain or bad weather, umbrella", "비까지 오네", "Raining?!"),
            ("finding a hidden cafe or nice view", "우연히 발견한 곳", "Found it"),
            ("drinking warm coffee/beer with view", "이거지...", "This is it"),
            ("taking a selfie with beautiful scenery", "오길 잘했다", "So good"),
            ("looking at sunset, sentimental vibe", "시간이 멈췄으면", "Stop time"),
            ("returning home, tired but happy face", "다시 현생으로", "Back home"),
            ("holding souvenir", "여행은 계속된다", "Travel goes on")
        ]
    elif "연애" in theme:
        return [
            ("looking at phone waiting for message", "왜 연락이 없지?", "No reply?"),
            ("imagining bad scenarios, worry bubbles", "혹시 화났나?", "Is he mad?"),
            ("typing message and deleting it repeatedly", "뭐라고 보내지..", "Typing..."),
            ("phone ringing, shocked face", "왔다!!", "Msg!"),
            ("meeting face to face, awkward atmosphere", "어색...", "Awkward"),
            ("pouting or looking away", "사실 서운했어", "I was sad"),
            ("partner giving small gift or apology", "미안해", "Sorry"),
            ("holding hands tight, blushing", "금방 풀림", "Happy"),
            ("walking together in sunset", "싸우지 말자", "Love U"),
            ("blowing a kiss to camera", "연애란...", "Love is...")
        ]
    elif "덕질" in theme:
        return [
            ("seeing idol's new photo on screen, screaming", "미쳤다..", "Crazy visual"),
            ("checking bank account, empty wallet, fly flying", "텅장...", "No money"),
            ("thinking deeply with serious face", "살까 말까?", "Buy or not?"),
            ("hallucination of idol saying 'Buy it'", "사라고 속삭임", "Buy it!"),
            ("clicking 'Buy' button furiously", "결제 완료!", "Ordered!"),
            ("waiting for delivery, looking at door", "언제 와?", "Waiting"),
            ("unboxing package with holy light", "영롱하다", "Holy..."),
            ("decorating room with merch", "이게 행복이지", "Happiness"),
            ("eating cheap ramen but smiling", "밥 안 먹어도 배불러", "Full heart"),
            ("holding lightstick", "어덕행덕", "Fan life")
        ]
    elif "공포" in theme:
        return [
            ("lying in bed at night, looking at phone", "잠이 안 와", "Can't sleep"),
            ("hearing strange creaking sound", "무슨 소리지?", "What sound?"),
            ("looking at the slightly open door", "분명 닫았는데..", "I closed it.."),
            ("staring into the dark corner", "옷가지인가?", "Clothes?"),
            ("shadow moving slightly", "움직였어!!", "Moved!"),
            ("hiding under blanket, shaking", "살려줘...", "Help"),
            ("gathering courage to turn on light", "에라 모르겠다!", "Light on!"),
            ("revealing it was just a cat or falling object", "아...", "Ah..."),
            ("sigh of relief, wiping sweat", "간 떨어질 뻔", "Phew"),
            ("waving goodbye with ghost costume", "오늘 밤 조심해", "Watch out")
        ]
    else:
        # 기타 테마 템플릿
        return [
            (f"holding topic card '{detail}'", "오늘의 주제", "Topic"),
            ("showing question mark, confused face", "모르겠다고?", "Confused?"),
            ("opening book or searching laptop", "제가 알려드림", "I'll teach U"),
            ("holding pointer stick, teacher pose", "핵심 포인트!", "Key Point"),
            ("showing good example O", "이건 좋아요", "Good!"),
            ("showing bad example X", "이건 안돼요", "Bad!"),
            (f"doing main action of {detail}", "직접 해보니..", "Trying..."),
            ("sparkling effect around character", "확실히 다르죠?", "Difference"),
            ("thumbs up winking", "도전해보세요", "Try it"),
            ("holding subscribe button", "저장 필수!", "Save it")
        ]

# ==========================================
# 5. 사이드바 UI
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

if 'story_detail_input' not in st.session_state: st.session_state.story_detail_input = "아무것도 안 했는데 벌써 밤"
with col_text:
    story_detail = st.text_input("세부 소재 (직접 입력)", key="story_detail_input")

st.sidebar.divider()
st.sidebar.header("3️⃣ 스타일 & 연출")
selected_style_name = st.sidebar.select_slider("그림체 농도", options=list(ART_STYLE_MAP.keys()), value="5. 웹툰/셀식 채색 (Webtoon)")

layout_mode = st.sidebar.selectbox(
    "카메라 연출",
    ["1. 안정적 (Standard)", "2. 다이내믹 (Dynamic)", "3. 시네마틱 (Cinematic)", "4. 셀카 모드 (Selfie)", "5. 1인칭 시점 (POV)",
     "6. 아이소메트릭 (Isometric)", "7. 항공 샷 (Drone)", "8. 로우 앵글 (Low Angle)", "9. 어안 렌즈 (Fish-eye)", "10. 실루엣 (Silhouette)"]
)

output_mode = st.sidebar.radio("출력 방식", ["단일 컷 (1장 추천)", "캐릭터 시트"], index=0)
text_lang = st.sidebar.radio("말풍선 언어", ["한국어", "영어", "없음"])
seed_num = st.sidebar.number_input("시드(Seed)", value=1234)

# ==========================================
# 6. 프롬프트 생성 로직
# ==========================================
def make_prompts(mode, ctype, cspec, cfeat, coutfit, theme, detail, layout, style_name, lang, seed):
    
    # 캐릭터 Prompt
    if ctype == "직접 입력 (Custom)": species = cspec
    else: species = ctype.split("(")[1].replace(")", "")
    
    if species in ["Cat", "Dog", "Rabbit", "Bear", "Hamster", "Tiger"]: base_char = f"Cute anthropomorphic {species} character"
    else: base_char = f"Cute {species} character"
    
    full_char_desc = f"{base_char}, {cfeat}, wearing {coutfit}, expressive face"

    # 스타일 & 레이아웃
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

    # 출력 모드
    if "단일" in mode:
        mode_kw = "single panel, independent illustration, full shot, one image"
        neg_kw = "--no comic grid, storyboard, multiple panels, split view"
    else:
        mode_kw = "character sheet, multiple poses"
        neg_kw = ""

    # 시나리오 가져오기
    scenarios = get_deep_story(theme, detail)
    prompts = []
    context_str = f"Story about {detail}"

    for action, ko, en in scenarios:
        if "한국어" in lang: text_p = f'speech bubble with text "{ko}", written in Korean Hangul font'
        elif "영어" in lang: text_p = f'speech bubble with text "{en}", written in English'
        else: text_p = "no text"

        p = f"/imagine prompt: **[Story]** {context_str} **[Subject]** {full_char_desc} **[Action]** {action} **[Text]** {text_p} **[Style]** {style_kw}, {angle_kw}, {mode_kw} --ar 4:5 --niji 6 --seed {seed} {neg_kw}"
        prompts.append(p)

    return prompts, scenarios

# ==========================================
# 7. 결과 출력 UI
# ==========================================
if 'generated_prompts' not in st.session_state:
    st.session_state.generated_prompts = []
    st.session_state.current_scenarios = []

if st.button("🚀 감성 100% 마이툰 생성하기 (Click)"):
    with st.spinner(f"'{st.session_state.story_detail_input}' 이야기를 만드는 중..."):
        prompts, scenes = make_prompts(
            output_mode, char_type, custom_species, char_feature, char_outfit, 
            story_theme, st.session_state.story_detail_input, layout_mode, selected_style_name, text_lang, seed_num
        )
        st.session_state.generated_prompts = prompts
        st.session_state.current_scenarios = scenes

if st.session_state.generated_prompts:
    st.divider()
    st.success(f"✅ 생성 완료! (주제: {st.session_state.story_detail_input})")
    
    # [NEW] 전체 복사 기능 부활
    st.subheader("📋 전체 프롬프트 한 번에 복사하기")
    st.warning("⚠️ 주의: 디스코드에 한 번에 붙여넣으면 첫 번째 컷만 생성될 수 있습니다. 메모장 저장용으로 추천합니다.")
    all_text = "\n\n".join(st.session_state.generated_prompts)
    st.code(all_text, language="markdown")
    
    st.divider()

    st.subheader("✂️ 컷별 상세 확인 & 복사")
    st.caption("👇 제목을 확인하고, 아래 박스의 📄 아이콘을 눌러 복사하세요.")

    for i, p in enumerate(st.session_state.generated_prompts):
        scene_txt = st.session_state.current_scenarios[i][1] if "한국어" in text_lang else st.session_state.current_scenarios[i][2]
        
        # 제목을 코드 블록 왼쪽 위에 크게 배치
        st.markdown(f"#### 🎞️ Cut {i+1}: {scene_txt}")
        st.code(p, language="markdown")
