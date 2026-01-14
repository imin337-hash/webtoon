# -*- coding: utf-8 -*-
import streamlit as st
import google.generativeai as genai

# 1. 페이지 설정
st.set_page_config(page_title="마이툰: Gemini 에디션", page_icon="💎", layout="wide")

# 2. 헤더
st.title("💎 마이툰 with Gemini: AI 시나리오 작가")
st.markdown("""
**Google Gemini**가 당신의 아이디어를 완벽한 10컷 인스타툰 시나리오로 만들어줍니다.
**테마**와 **상세 내용**을 입력하고 생성 버튼을 누르세요!
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
# 4. Gemini 시나리오 생성 로직
# ==========================================
def generate_gemini_story(api_key, theme, content):
    """Gemini API를 호출하여 10컷 시나리오를 생성합니다."""
    
    # 1. API 설정
    genai.configure(api_key=api_key)
    
    # [수정됨] 모델명을 'gemini-pro'로 변경 (가장 안정적)
    model = genai.GenerativeModel('gemini-pro') 

    # 2. 프롬프트 작성
    prompt = f"""
    You are a professional webtoon writer.
    Create a funny and relatable 10-cut storyboard based on the user's Theme and Content.
