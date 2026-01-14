# -*- coding: utf-8 -*-
import streamlit as st

# 1. 페이지 설정
st.set_page_config(page_title="나이툰: 나만의 인스타툰 메이커", page_icon="🎨", layout="wide")

# 2. 헤더 및 소개
st.title("🎨 마이툰(MyToon): AI 인스타툰 생성기 (Pro)")
st.markdown("""
**캐릭터, 스토리(10종), 연출(10종)**을 조합하여 다채로운 인스타툰을 만드세요.
**[단일 컷]** 모드를 켜면 미드저니에서 이미지가 깔끔하게 한 장씩 나옵니다.
""")

# ==========================================
# 3. 사이드바: 옵션 설정
# ==========================================
st.sidebar.header("1️⃣ 생성 모드")
output_mode = st.sidebar.radio(
    "이미지 출력 방식",
    ["단일 컷 (1장당 그림 1개)", "캐릭터 시트 (한 장에 여러 동작)"],
    index=0
)
st.sidebar.caption("※ '단일 컷'을 추천합니다.")

st.sidebar.divider()
st.sidebar.header("2️⃣ 캐릭터 (Character)")
char_type = st.sidebar.selectbox(
    "주인공 유형",
    ["고양이 (Cat)", "강아지 (Dog)", "토끼 (Rabbit)", "곰 (Bear)", "사람-여자 (Girl)", "사람-남자 (Boy)", "직접 입력 (Custom)"]
)

custom_species = ""
if char_type == "직접 입력 (Custom)":
    custom_species = st.sidebar.text_input("캐릭터 입력 (예: Alien)", "Hamster")

char_feature = st.sidebar.text_input("외모 특징", "white fur, round eyes, pink cheeks")
char_outfit = st.sidebar.text_input("착용 의상", "yellow hoodie, blue jeans")

st.sidebar.divider()
st.sidebar.header("3️⃣ 스토리 (10 Themes)")
# [UPDATE] 테마 10개로 확장
story_theme = st.sidebar.selectbox(
    "이야기 테마 선택",
    [
        "1. 일상 공감 (Daily Life)", 
        "2. 성장/도전 (Growth)", 
        "3. 꿀팁 정보 (Information)", 
        "4. 감동/힐링 (Healing)",
        "5. ✈️ 여행/휴가 (Travel)",
        "6. 💕 연애/사랑 (Romance)",
        "7. 👻 공포/미스터리 (Horror)",
        "8. 📦 제품 리뷰 (Review)",
        "9. 🍳 요리/먹방 (Cooking)",   # NEW
        "10. 🎨 덕질/취미 (Hobby)"     # NEW
    ]
)

st.sidebar.header("4️⃣ 연출/앵글 (10 Layouts)")
# [UPDATE] 연출 10개로 확장
layout_mode = st.sidebar.selectbox(
    "카메라 연출 방식 선택",
    [
        "1. 안정적 (Standard) - 기본 눈높이",
        "2. 다이내믹 (Dynamic) - 역동적/사선",
        "3. 시네마틱 (Cinematic) - 영화적 깊이감",
        "4. 셀카 모드 (Selfie) - 얼굴 중심",            # NEW
        "5. 1인칭 시점 (POV) - 주인공의 시선",          # NEW
        "6. 아이소메트릭 (Isometric) - 귀여운 3D 뷰",   # NEW
        "7. 항공 샷 (Drone/Top) - 위에서 아래로",       # NEW
        "8. 로우 앵글 (Low Angle) - 웅장하게 올려다봄", # NEW
        "9. 어안 렌즈 (Fish-eye) - 재미있는 왜곡",      # NEW
        "10. 실루엣/역광 (Silhouette) - 감성적 분위기"  # NEW
    ]
)

art_style = st.sidebar.select_slider("그림체 농도", options=["손그림/낙서", "깔끔한 웹툰", "고퀄리티 일러스트"])

st.sidebar.divider()
st.sidebar.header("5️⃣ 대사 언어")
text_lang = st.sidebar.radio("말풍선 언어", ["한국어 (Korean)", "영어 (English)", "없음 (No Text)"])

seed_num = st.sidebar.number_input("일관성 시드(Seed)", value=1234, min_value=0)

# ==========================================
# 4. 핵심 로직
# ==========================================
def get_story_scenario(theme):
    """테마별 10컷 시나리오 데이터베이스"""
    
    # 1~8번 기존 테마 (요약됨)
    if "일상" in theme:
        return [("posing confidently", "월요병", "Monday"), ("waking up", "으아...", "Ugh"), ("looking at calendar", "벌써?", "Already?"), ("sitting at desk", "집 갈래", "Home"), ("spilling coffee", "앗!", "Oops"), ("cleaning up", "망했다", "No"), ("eating food", "맛있다", "Yum"), ("watching TV", "행복", "Happy"), ("thumbs up", "공감?", "Relatable"), ("waving", "내일 봐", "Bye")]
    elif "성장" in theme:
        return [("tying headband", "도전!", "Start"), ("looking at wall", "가능?", "Can I?"), ("training hard", "으랏차!", "Go"), ("falling down", "아야", "Ouch"), ("sitting sad", "포기?", "Give up"), ("friend helping", "괜찮아", "Okay"), ("eyes fire", "다시!", "Again"), ("jumping", "성공!", "Success"), ("trophy", "해냈다", "Win"), ("waving", "화이팅", "Fight")]
    elif "꿀팁" in theme:
        return [("holding book", "오늘의 팁", "Tip"), ("question mark", "뭐지?", "What?"), ("studying", "검색", "Search"), ("pointer stick", "첫째!", "First"), ("chart", "중요", "Key"), ("X sign", "주의", "Warn"), ("O sign", "추천", "Good"), ("writing", "메모", "Memo"), ("winking", "쉽죠?", "Easy"), ("subscribe", "저장", "Save")]
    elif "감동" in theme:
        return [("sunset", "위로", "Rest"), ("walking alone", "지친다", "Tired"), ("sighing", "휴...", "Sigh"), ("flower", "어?", "Oh?"), ("smiling", "예쁘다", "Pretty"), ("sky", "편안", "Peace"), ("stars", "괜찮아", "Okay"), ("tea", "따뜻해", "Warm"), ("smile", "수고했어", "Good job"), ("bed", "잘 자요", "Night")]
    elif "여행" in theme:
        return [("packing", "짐 싸기", "Packing"), ("airport", "공항", "Airport"), ("airplane", "출발", "Go"), ("scenery", "도착!", "Arrive"), ("selfie", "찰칵", "Photo"), ("eating", "냠냠", "Yum"), ("beach", "힐링", "Healing"), ("night view", "야경", "Night"), ("hotel", "피곤", "Tired"), ("souvenir", "선물", "Gift")]
    elif "연애" in theme:
        return [("mirror", "준비", "Ready"), ("phone", "연락", "Msg"), ("meeting", "안녕", "Hi"), ("holding hands", "설렘", "Love"), ("cafe", "데이트", "Date"), ("pouty", "흥!", "Hmph"), ("gift", "선물?", "Gift?"), ("happy", "감동", "Wow"), ("heart hand", "사랑해", "Love you"), ("kiss", "쪽", "Kiss")]
    elif "공포" in theme:
        return [("flashlight", "무서운 얘기", "Scary"), ("noise", "무슨 소리?", "Sound?"), ("walking dark", "누구세요", "Who?"), ("shadow", "히익!", "Eek"), ("shocked face", "깜짝이야", "Shock"), ("running", "도망쳐", "Run"), ("hiding", "덜덜", "Shake"), ("cute monster", "어라?", "Huh?"), ("relief", "휴...", "Phew"), ("ghost costume", "놀랐지?", "Boo")]
    elif "리뷰" in theme:
        return [("box", "택배 왔다", "Delivery"), ("unboxing", "언박싱", "Open"), ("item", "영롱해", "Shiny"), ("detail", "디테일", "Detail"), ("using", "사용 중", "Using"), ("before", "전", "Before"), ("after", "후", "After"), ("thumbs up", "강추", "Best"), ("link", "링크", "Link"), ("product", "득템", "Get it")]
    
    # [NEW] 9. 요리/먹방
    elif "요리" in theme:
        return [
            ("wearing apron and chef hat", "요리사!", "Chef!"),
            ("chopping vegetables, focused", "탁탁탁", "Chop"),
            ("frying pan with fire", "불쇼!", "Fire!"),
            ("smelling aroma, floating hearts", "음~ 스멜", "Smell"),
            ("tasting with spoon", "간 보기", "Taste"),
            ("plating food beautifully", "완성!", "Done!"),
            ("taking photo of food", "인증샷", "Photo"),
            ("eating with big mouth", "와앙!", "Eat"),
            ("holding belly, full", "배불러", "Full"),
            ("washing dishes, piled up", "설거지...", "Dishes")
        ]
    # [NEW] 10. 덕질/취미
    elif "덕질" in theme:
        return [
            ("looking at phone, screaming happiness", "오빠!!", "My Bias!"),
            ("buying tickets on computer, fast typing", "피켓팅", "Ticketing"),
            ("waiting in line, holding fan", "두근두근", "Waiting"),
            ("holding light stick, glowing", "응원봉", "Light stick"),
            ("concert stage view, crying happy tears", "사랑해!", "Love U"),
            ("buying merchandise, empty wallet", "내 돈...", "My money"),
            ("unboxing merchandise albums", "포카깡", "Unboxing"),
            ("decorating diary or wall", "다꾸", "Decor"),
            ("lying in bed looking at photo", "행복했다", "Happy"),
            ("waving with goods", "덕질 최고", "Fan life")
        ]
    return []

def make_prompts(mode, ctype, cspec, cfeat, coutfit, theme, style, layout, lang, seed):
    
    # 1. 캐릭터
    if ctype == "직접 입력 (Custom)":
        species = cspec
    else:
        species = ctype.split("(")[1].replace(")", "")
    
    if species in ["Cat", "Dog", "Rabbit", "Bear", "Hamster", "Tiger"]:
        base_char = f"Cute anthropomorphic {species} character"
    else:
        base_char = f"Cute {species} character"

    full_char_desc = f"{base_char}, {cfeat}, wearing {coutfit}, simple iconic design"

    # 2. 스타일
    if style == "손그림/낙서":
        style_kw = "doodle style, rough pencil lines, crayon texture"
    elif style == "고퀄리티 일러스트":
        style_kw = "high quality 3D render, pixar style, octane render"
    else: 
        style_kw = "flat vector art, thick outlines, webtoon style, cel shading"

    # 3. 레이아웃 (10종 매핑)
    if "다이내믹" in layout:
        angle_kw = "dynamic dutch angle, exaggerated perspective, action lines"
    elif "시네마틱" in layout:
        angle_kw = "cinematic lighting, depth of field, dramatic composition"
    elif "셀카" in layout:
        angle_kw = "holding smartphone camera, selfie angle, extreme close-up, face focus"
    elif "1인칭" in layout:
        angle_kw = "first-person point of view (POV), hands visible in frame, immersive"
    elif "아이소메트릭" in layout:
        angle_kw = "isometric view, 3D cute game style, high angle, miniature effect"
    elif "항공" in layout:
        angle_kw = "bird's-eye view, top-down shot, wide angle, drone shot"
    elif "로우" in layout:
        angle_kw = "low angle shot, worm's-eye view, looking up at character, imposing"
    elif "어안" in layout:
        angle_kw = "fish-eye lens effect, distorted funny face, wide convex view"
    elif "실루엣" in layout:
        angle_kw = "silhouette against light, backlighting, atmospheric, rim light"
    else: # 안정적
        angle_kw = "flat composition, symmetrical balance, eye-level shot"

    # 4. 출력 모드
    if mode == "단일 컷 (1장당 그림 1개)":
        mode_kw = "single panel, independent illustration, full shot, one image"
        negative_kw = "--no comic grid, storyboard, multiple panels, split view"
    else:
        mode_kw = "character sheet, multiple poses, storyboard layout"
        negative_kw = ""

    # 5. 프롬프트 생성
    story_data = get_story_scenario(theme)
    prompts = []
    
    for i, (action, ko_text, en_text) in enumerate(story_data):
        
        if lang == "한국어 (Korean)":
            text_prompt = f'speech bubble with text "{ko_text}", written in Korean Hangul font'
        elif lang == "영어 (English)":
            text_prompt = f'speech bubble with text "{en_text}", written in English'
        else:
            text_prompt = "no text"

        # 최종 프롬프트
        p = f"/imagine prompt: **[Subject]** {full_char_desc} **[Action]** {action} **[Text]** {text_prompt} **[Style]** {style_kw}, {angle_kw}, {mode_kw} --ar 4:5 --niji 6 --seed {seed} {negative_kw}"
        prompts.append(p)
    
    return prompts, full_char_desc, story_data

# ==========================================
# 5. 결과 UI
# ==========================================
if 'generated_prompts' not in st.session_state:
    st.session_state.generated_prompts = []
    st.session_state.story_data = []

if st.button("🚀 10컷 프롬프트 생성 (Click)"):
    with st.spinner("AI가 시나리오와 연출을 계산 중입니다..."):
        prompts, summary, s_data = make_prompts(
            output_mode, char_type, custom_species, char_feature, char_outfit, 
            story_theme, art_style, layout_mode, text_lang, seed_num
        )
        st.session_state.generated_prompts = prompts
        st.session_state.story_data = s_data

if st.session_state.generated_prompts:
    st.divider()
    st.success(f"✅ 생성 완료! 테마: [{story_theme}] / 연출: [{layout_mode}]")
    
    st.subheader("📋 전체 복사하기")
    st.markdown("👇 **오른쪽 위 📄 아이콘**을 누르면 전체 복사됩니다.")
    all_text = "\n\n".join(st.session_state.generated_prompts)
    st.code(all_text, language="markdown")
    
    st.divider()
    
    st.subheader("✂️ 컷별 상세 확인")
    for i, p in enumerate(st.session_state.generated_prompts):
        try:
            action_txt = st.session_state.story_data[i][0]
            dialog_txt = st.session_state.story_data[i][1] if text_lang == "한국어 (Korean)" else st.session_state.story_data[i][2]
        except:
            action_txt = "장면"
            dialog_txt = ""

        col1, col2 = st.columns([0.8, 0.2])
        with col1:
            st.markdown(f"**Cut {i+1}: {dialog_txt}** ({action_txt})")
        st.code(p, language="markdown")
