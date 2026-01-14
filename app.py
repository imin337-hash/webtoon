# -*- coding: utf-8 -*-
import streamlit as st
import sys
import subprocess

# 1. 라이브러리 버전 확인 및 강제 로드
try:
    import google.generativeai as genai
    lib_version = genai.__version__
except ImportError:
    lib_version = "설치 안됨"

# 2. 페이지 설정
st.set_page_config(page_title="마이툰: Gemini 에디션", page_icon="💎", layout="wide")

# ==========================================
# 3. [진단용] 시스템 상태 표시 (사이드바)
# ==========================================
st.sidebar.header("🔧 시스템 진단")
st.sidebar.info(f"📚 라이브러리 버전: {lib_version}")

if lib_version == "설치 안됨" or lib_version < "0.4.0":
    st.sidebar.error("⚠️ 버전이 너무 낮습니다!")
    st.sidebar.code("pip install --upgrade google-generativeai", language="bash")
else:
    st.sidebar.success("✅ 최신 버전 사용 중")

# API 키 입력
gemini_api_key = st.sidebar.text_input("Google Gemini API Key", type="password")

# 사용 가능한 모델 확인
valid_models = []
if gemini_api_key:
    try:
        genai.configure(api_key=gemini_api_key)
        # 사용 가능한 모델 리스트 가져오기
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                valid_models.append(m.name)
        
        with st.sidebar.expander("📋 사용 가능한 모델 목록"):
            for vm in valid_models:
                st.write(f"- {vm}")
                
    except Exception as e:
        st.sidebar.error(f"키 오류: {e}")

st.sidebar.divider()

# ==========================================
# 4. 헤더 및 데이터
# ==========================================
st.title("💎 마이툰 with Gemini (진단 모드)")
st.markdown("API 연결이 안 될 때, 왼쪽 사이드바의 **버전**과 **모델 목록**을 확인하세요.")

CHAR_DEFAULTS = {
    "나노바나나": ("Cute anthropomorphic Banana character named 'Nano', wearing a sleek futuristic pro-headset", "yellow body, expressive face"),
    "고양이": ("white fur, pointy ears, pink nose", "red ribbon collar"),
    "강아지": ("golden curly fur, floppy ears", "green scarf"),
    "소녀": ("long brown hair, cute face, k-pop style", "pastel hoodie, denim skirt"),
    "소년": ("short black hair, casual look, glasses", "oversized sweatshirt, cargo pants"),
    "직접 입력": ("", "")
}

ART_STYLE_MAP = {
    "웹툰": "korean webtoon style, cel shading, vibrant colors, clean outlines",
    "수채화": "watercolor texture, soft pastel blend, dreamy atmosphere",
    "실사": "unreal engine 5 render, cinematic lighting, 8k resolution, photograph style",
    "낙서": "minimalist doodle, stick figure style, rough sketch"
}

# ==========================================
# 5. Gemini 시나리오 생성 로직
# ==========================================
def generate_gemini_story(api_key, theme, content):
    genai.configure(api_key=api_key)
    
    # [핵심] 사용 가능한 모델 중 가장 좋은 것 자동 선택
    # 1.5-flash -> 1.5-pro -> 1.0-pro 순서로 찾음
    target_model = 'gemini-pro' # 기본값
    
    preferred_order = ['models/gemini-1.5-flash', 'models/gemini-1.5-pro', 'models/gemini-1.0-pro', 'models/gemini-pro']
    
    # 사용자가 가진 모델 권한과 비교해서 선택
    for preferred in preferred_order:
        if preferred in valid_models:
            target_model = preferred
            break
            
    # 모델명에서 models/ 접두사 제거 (라이브러리 버전에 따라 필요할수도 있음)
    clean_model_name = target_model.replace("models/", "")
    
    # 최종 선택된 모델로 생성 시도
    try:
        model = genai.GenerativeModel(clean_model_name)
        
        prompt = f"""
        You are a webtoon writer. Create a 10-cut storyboard.
        Theme: {theme}
        Content: {content}
        Output format (Use | separator):
        Cut 1|Action (English)|Dialogue (Korean)
        Cut 2|Action (English)|Dialogue (Korean)
        ...
        Cut 10|Action (English)|Dialogue (Korean)
        """
        
        response = model.generate_content(prompt)
        
        # 결과 파싱
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
        return parsed_data[:10], clean_model_name

    except Exception as e:
        return None, str(e)

# 템플릿 (에러 시 사용)
def generate_template_story(topic):
    return [
        {"Cut": 1, "Action": f"holding title card '{topic}'", "Text": f"주제: {topic}"},
        {"Cut": 2, "Action": "walking happily", "Text": "시작!"},
        {"Cut": 3, "Action": "facing problem", "Text": "어라?"},
        {"Cut": 4, "Action": "shocked face", "Text": "헉!"},
        {"Cut": 5, "Action": "thinking", "Text": "음..."},
        {"Cut": 6, "Action": "idea lightbulb", "Text": "아하!"},
        {"Cut": 7, "Action": "trying hard", "Text": "도전!"},
        {"Cut": 8, "Action": "success", "Text": "성공!"},
        {"Cut": 9, "Action": "happy ending", "Text": "끝"},
        {"Cut": 10, "Action": "waving hand", "Text": "안녕"}
    ]

# ==========================================
# 6. UI 구성
# ==========================================
st.sidebar.header("1️⃣ 설정")
char_type = st.sidebar.selectbox("캐릭터", list(CHAR_DEFAULTS.keys()))
style_name = st.sidebar.selectbox("그림체", list(ART_STYLE_MAP.keys()))

st.subheader("📝 스토리 만들기")
col1, col2 = st.columns([0.7, 0.3])
with col1:
    topic_input = st.text_input("주제 입력", "편의점 알바 실수")
with col2:
    st.write("")
    st.write("")
    btn = st.button("✨ 생성하기", type="primary")

if 'scenario_rows' not in st.session_state:
    st.session_state.scenario_rows = generate_template_story("기본")

if btn:
    if gemini_api_key:
        with st.spinner("AI가 쓰고 있습니다..."):
            result, model_used = generate_gemini_story(gemini_api_key, "일상", topic_input)
            if result:
                st.session_state.scenario_rows = result
                st.toast(f"성공! 사용된 모델: {model_used}")
            else:
                st.error(f"실패했습니다. 오류: {model_used}")
                st.session_state.scenario_rows = generate_template_story(topic_input)
    else:
        st.warning("API 키가 없어 기본 템플릿을 사용합니다.")
        st.session_state.scenario_rows = generate_template_story(topic_input)

# 에디터 및 결과 표시
edited_rows = st.data_editor(st.session_state.scenario_rows, num_rows="fixed", hide_index=True)

if st.button("🚀 프롬프트 변환"):
    st.success("변환 완료! (아래 코드를 복사하세요)")
    codes = []
    char_desc = CHAR_DEFAULTS.get(char_type, ("", ""))[0]
    style_desc = ART_STYLE_MAP.get(style_name, "")
    
    for row in edited_rows:
        p = f"/imagine prompt: {char_desc}, {row['Action']}, text bubble '{row['Text']}', {style_desc} --ar 4:5 --niji 6"
        codes.append(p)
    
    st.code("\n\n".join(codes), language="markdown")
