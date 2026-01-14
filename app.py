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

CHAR_DEFAULTS = {
    "고양이 (Cat)": ("white fur, pointy ears, pink nose", "red ribbon collar"),
    "강아지 (Dog)": ("golden curly fur, floppy ears", "green scarf"),
    "토끼 (Rabbit)": ("long ears, fluffy white fur", "cute pink dress"),
    "곰 (Bear)": ("brown fur, round ears, teddy bear look", "striped t-shirt"),
    "사람-여자 (Girl)": ("long brown hair, cute face, k-pop style", "pastel hoodie, denim skirt"),
    "사람-남자 (Boy)": ("short black hair, casual look, glasses", "oversized sweatshirt, cargo pants"),
    "직접 입력 (Custom)": ("", "")
}

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
    selected_type = st.session_state.char_type_selector
    defaults = CHAR_DEFAULTS.get(selected_type, ("", ""))
    st.session_state.char_feature_input = defaults[0]
    st.session_state.char_outfit_input = defaults[1]

def generate_random_idea():
    current_theme_key = next((k for k in THEME_IDEAS.keys() if k in st.session_state.theme_selector), "일상")
    idea = random.choice(THEME_IDEAS[current_theme_key])
    st.session_state.story_detail_input = idea

# ==========================================
# 4. 딥 스토리 (짧고 굵은 단어 위주로 수정)
# ==========================================
def get_deep_story(theme, detail):
    """
    한글 생성 성공률을 높이기 위해 대사를 최대한 짧게(2~4글자) 수정했습니다.
    """
    if "일상" in theme:
        return [
            (f"posing confidently with text '{detail}'", "목표!", f"Goal: {detail}"),
            ("full of energy, fists clenched", "가자!", "Motivated!"),
            ("looking at clock", "벌써?", "Wait..."),
            ("lying on sofa, messy room", "휴식", "Rest"),
            ("scrolling phone zombie face", "폰질", "Scrolling"),
            ("looking at window, night", "밤이야?", "Night?!"),
            ("head hitting the desk", "망함", "Ruined"),
            ("eating late night snack", "냠냠", "Yum"),
            ("lying in bed", "자자", "Sleep"),
            ("waving goodbye", "공감?", "Relatable?")
        ]
    elif "성장" in theme:
        return [
            (f"worried face, concept {detail}", "고민", "Worry"),
            ("seeing others succeed", "부럽다", "Envy"),
            ("trying hard, sweating", "끙끙", "Hard"),
            ("sitting in corner, shadow", "우울", "Sad"),
            ("friend approaching", "토닥토닥", "Comfort"),
            ("receiving coffee", "힘내", "Cheer up"),
            ("wiping tears", "다시!", "Again"),
            ("focusing deeply", "성공!", "Success"),
            ("smiling brightly", "뿌듯", "Proud"),
            ("making heart hand", "응원해", "Love U")
        ]
    elif "여행" in theme:
        return [
            ("packing suitcase chaos", "짐 싸기", "Packing"),
            ("running, sweating", "지각!", "Late!"),
            ("looking at map lost", "어디지?", "Lost"),
            ("sudden rain", "비?!", "Rain?!"),
            ("finding nice view", "우와", "Wow"),
            ("drinking coffee with view", "좋다", "Good"),
            ("taking selfie", "찰칵", "Selfie"),
            ("sunset vibe", "감성", "Vibe"),
            ("tired happy face", "집으로", "Home"),
            ("holding souvenir", "끝!", "End")
        ]
    elif "연애" in theme:
        return [
            ("looking at phone", "연락?", "Reply?"),
            ("worry bubbles", "삐졌나?", "Mad?"),
            ("typing message", "고민..", "Typing"),
            ("phone ringing", "왔다!", "Msg!"),
            ("meeting awkward", "어색", "Awkward"),
            ("pouting", "흥!", "Hmph"),
            ("giving gift", "미안", "Sorry"),
            ("holding hands", "헤헤", "Hehe"),
            ("walking sunset", "좋아해", "Love U"),
            ("blowing kiss", "쪽!", "Kiss")
        ]
    elif "덕질" in theme:
        return [
            ("screaming at screen", "대박", "Crazy"),
            ("empty wallet", "텅장", "No money"),
            ("thinking face", "살까?", "Buy?"),
            ("hallucination", "사라!", "Buy it"),
            ("clicking mouse", "결제!", "Pay"),
            ("waiting door", "택배?", "Wait"),
            ("unboxing light", "영롱", "Holy"),
            ("decorating room", "행복", "Happy"),
            ("eating ramen smiling", "배불러", "Full"),
            ("holding lightstick", "사랑해", "Love")
        ]
    elif "공포" in theme:
        return [
            ("lying in bed", "잠안와", "Awake"),
            ("hearing sound", "뭐지?", "What?"),
            ("looking at door", "누구?", "Who?"),
            ("staring dark", "귀신?", "Ghost?"),
            ("shadow moving", "악!", "Ah!"),
            ("hiding blanket", "덜덜", "Shake"),
            ("turning on light", "에잇!", "Light!"),
            ("revealing cat", "냥이?", "Cat?"),
            ("sigh relief", "휴..", "Phew"),
            ("ghost costume", "조심", "Watch out")
        ]
    else:
        return [
            (f"holding card '{detail}'", "주제", "Topic"),
            ("confused face", "뭐지?", "What?"),
            ("opening book", "공부", "Study"),
            ("teacher pose", "핵심!", "Point"),
            ("good example O", "좋아", "Good"),
            ("bad example X", "안돼", "Bad"),
            (f"doing action {detail}", "도전", "Try"),
            ("sparkling effect", "성공", "Success"),
            ("thumbs up", "추천", "Best"),
            ("subscribe button", "저장!", "Save")
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
# 6. 프롬프트 생성 로직 (한글 최적화 적용)
# ==========================================
def make_prompts(mode, ctype, cspec
