# -*- coding: utf-8 -*-
import streamlit as st
import random
from openai import OpenAI  # OpenAI 라이브러리 추가

# 1. 페이지 설정
st.set_page_config(page_title="마이툰: AI 시나리오 작가", page_icon="🎨", layout="wide")

# 2. 헤더
st.title("🎨 마이툰(MyToon): AI 시나리오 작가 & 프롬프트 생성")
st.markdown("""
**1. API 연결:** OpenAI API Key를 입력하면 AI가 **진짜 스토리**를 창작해줍니다. (없으면 기본 템플릿 사용)
**2. 주제 입력:** "좀비가 나타난 학교", "복권 1등 당첨" 등 자유롭게 적어보세요.
**3. 결과 수정:** AI가 쓴 시나리오를 내 입맛대로 수정하고 프롬프트로 변환하세요.
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
# 4. 시나리오 생성 로직 (Real AI vs Template)
# ==========================================

# [Logic A] 진짜 AI (GPT)를 이용한 창작
def generate_ai_story(api_key, topic):
    client = OpenAI(api_key=api_key)
    
    # 프롬프트 설계 (AI에게 포맷을 지시)
    system_prompt = """
    You are a creative webtoon writer. 
    Create a funny and relatable 10-cut storyboard based on the user's topic.
    Format your response EXACTLY like this line by line (Use '|' to separate):
    Cut 1|Action Description (in English)|Dialogue (in Korean)
    Cut 2|Action Description (in English)|Dialogue (in Korean)
    ...
    Cut 10|Action Description (in English)|Dialogue (in Korean)
    
    Keep the action description simple for image generation.
    Keep the dialogue short and funny.
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", # 비용이 저렴하고 빠른 모델
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Topic: {topic}"}
            ]
        )
        content = response.choices[0].message.content
        
        # 텍스트 파싱 (AI의 응답을 표 데이터로 변환)
        parsed_data = []
        lines = content.strip().split('\n')
        for line in lines:
            if "|" in line and "Cut" in line:
                parts = line.split('|')
                if len(parts) >= 3:
                    cut_num = parts[0].strip().replace("Cut ", "")
                    action = parts[1].strip()
                    text = parts[2].strip()
                    parsed_data.append({"Cut": cut_num, "Action": action, "Text": text})
        
        # 만약 파싱 실패 시 기본값 반환
        if not parsed_data:
            return generate_template_story(topic)
            
        return parsed_data[:10] # 10개만 보장

    except Exception as e:
        st.error(f"AI 생성 중 오류가 발생했습니다: {e}")
        return generate_template_story(topic) # 에러나면 템플릿 사용

# [Logic B] 기존 템플릿 (규칙 기반) - API 키 없을 때
def generate_template_story(topic):
    return [
        {"Cut": 1, "Action": f"holding title card '{topic}', confident", "Text": f"주제:\n{topic}"},
        {"Cut": 2, "Action": "walking happily, full of expectation", "Text": "시작해볼까!"},
        {"Cut": 3, "Action": f"facing situation of {topic}", "Text": "어라?"},
        {"Cut": 4, "Action": "concentrating deeply", "Text": "집중..."},
        {"Cut": 5, "Action": "sudden problem occurring, shocked", "Text": "앗!! 실수!"},
        {"Cut": 6, "Action": "feeling frustrated, messy background", "Text": "망했다..."},
        {"Cut": 7, "Action": "lightbulb appearing, idea", "Text": "잠깐! 좋은 생각!"},
        {"Cut": 8, "Action": f"solving {topic} actively", "Text": "다시 도전!"},
        {"Cut": 9, "Action": "success moment, happy smile", "Text": "완벽해!"},
        {"Cut": 10, "Action": "waving goodbye, subscribe button", "Text": "다들 화이팅!"}
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
        neg_kw = "--no 4 panel grid
