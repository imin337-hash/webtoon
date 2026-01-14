# -*- coding: utf-8 -*-
import streamlit as st

# 1. 페이지 설정
st.set_page_config(page_title="나이툰: 나만의 인스타툰 메이커", page_icon="🎨", layout="wide")

# 2. 헤더 및 소개
st.title("🎨 MyToon : AI 인스타툰 생성기 (8가지 테마)")
st.markdown("""
**캐릭터, 스토리, 연출**을 조합하여 **10컷의 인스타툰 프롬프트**를 만드세요.
이제 **여행, 연애, 공포, 제품 리뷰** 등 더 다양한 상황을 연출할 수 있습니다.
""")

# ==========================================
# 3. 사이드바: 옵션 설정
# ==========================================
st.sidebar.header("1️⃣ 캐릭터 (Character)")

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
st.sidebar.header("2️⃣ 스토리 & 연출")

# [업데이트] 테마 목록 8개로 확장
story_theme = st.sidebar.radio(
    "이야기 테마 (시나리오가 변경됨)",
    [
        "일상 공감 (Daily Life)", 
        "성장/도전 (Growth)", 
        "꿀팁 정보 (Information)", 
        "감동/힐링 (Healing)",
        "✈️ 여행/휴가 (Travel)",       # NEW
        "💕 연애/사랑 (Romance)",      # NEW
        "👻 공포/미스터리 (Horror)",   # NEW
        "📦 제품 리뷰 (Review)"        # NEW
    ]
)

art_style = st.sidebar.select_slider("그림체", options=["손그림/낙서", "깔끔한 웹툰", "고퀄리티 일러스트"])
layout_mode = st.sidebar.selectbox("연출 방식", ["안정적 (기본)", "다이내믹 (액션)", "시네마틱 (영화)"])

st.sidebar.divider()
st.sidebar.header("3️⃣ 대사 언어 (Language)")
text_lang = st.sidebar.radio("말풍선 언어", ["한국어 (Korean)", "영어 (English)", "없음 (No Text)"])

seed_num = st.sidebar.number_input("일관성 시드(Seed)", value=1234, min_value=0)

# ==========================================
# 4. 핵심 로직: 테마별 시나리오 DB (확장됨)
# ==========================================
def get_story_scenario(theme, char_desc):
    """
    테마에 따라 10컷의 (장면설명, 한국어대사, 영어대사) 리스트를 반환
    """
    # 1. 일상 공감
    if "일상" in theme:
        return [
            ("posing with title text, bored face", "월요병", "Monday Blues"),
            ("waking up in bed, messy hair", "으아...", "Ugh..."),
            ("looking at calendar, shocked expression", "벌써?!", "Already?!"),
            ("sitting at desk, pile of work, soul leaving body", "집 가고 싶다", "Go home..."),
            ("spilling coffee on desk, disaster moment", "앗!!", "Oops!!"),
            ("cleaning up mess, crying funny tears", "망했다", "Oh no"),
            ("eating delicious food, suddenly happy", "역시 맛있는 게 최고", "Yummy!"),
            ("lying on sofa watching TV, relaxed", "이게 행복이지", "Happiness"),
            ("thumbs up to camera, relatable face", "공감?", "Relatable?"),
            ("waving goodbye in pajamas", "내일 봐요", "See ya")
        ]
    # 2. 성장/도전
    elif "성장" in theme:
        return [
            ("posing confidently with headband", "도전 시작!", "Challenge Start!"),
            ("looking at a high wall or big obstacle", "할 수 있을까?", "Can I do it?"),
            ("trying hard, sweating, working out", "으라차차!", "Let's go!"),
            ("failing and falling down, scrape on knee", "아야!", "Ouch!"),
            ("sitting on ground, looking sad and tired", "포기할까...", "Give up?"),
            ("friend or light spirit helping character up", "괜찮아!", "It's okay!"),
            ("eyes burning with fire, determination", "다시 한번!", "Try again!"),
            ("overcoming the obstacle, jumping high", "해냈다!", "I did it!"),
            ("flexing muscles or holding trophy", "나도 할 수 있다", "Success!"),
            ("waving goodbye with confidence", "도전하세요!", "You can do it")
        ]
    # 3. 꿀팁 정보
    elif "꿀팁" in theme:
        return [
            ("wearing glasses, holding a book, title card", "오늘의 꿀팁", "Today's Tip"),
            ("pointing at a question mark, confused face", "이게 뭘까?", "What is this?"),
            ("opening a book or laptop, studying", "알아보자", "Let's check"),
            ("holding a pointer stick, teacher pose", "첫 번째!", "First!"),
            ("showing a chart or diagram, serious face", "중요해요", "Important"),
            ("holding an X sign with arms, warning", "주의!", "Warning!"),
            ("holding an O sign, smiling", "이건 좋아요", "Good!"),
            ("writing notes, sparkling background", "메모 메모", "Memo this"),
            ("winking and pointing finger", "참 쉽죠?", "Easy right?"),
            ("waving goodbye with a subscribe button icon", "저장하세요!", "Save this!")
        ]
    # 4. 감동/힐링
    elif "감동" in theme:
        return [
            ("looking at sunset, sentimental vibe", "위로가 필요해", "Need rest"),
            ("walking alone with head down, lonely", "힘든 하루", "Hard day"),
            ("sitting on a park bench, sighing", "휴...", "Sigh..."),
            ("seeing a small flower or butterfly", "어?", "Oh?"),
            ("crouching down to look at nature, soft smile", "예쁘다", "Beautiful"),
            ("lying on grass looking at clouds", "편안해", "Peaceful"),
            ("watching stars in the night sky", "괜찮아", "It's okay"),
            ("hugging a pillow or warm tea", "따뜻해", "Warmth"),
            ("smiling gently at camera, healing atmosphere", "수고했어", "Good job"),
            ("waving goodbye with soft lighting", "잘 자요", "Good night")
        ]
    # 5. 여행/휴가 (NEW)
    elif "여행" in theme:
        return [
            ("packing a suitcase with excitement, messy room", "여행 가자!", "Let's Travel!"),
            ("holding a passport and ticket at airport", "공항 도착", "At Airport"),
            ("looking out of airplane window, clouds", "설렌다", "Excited"),
            ("arriving at destination, wide scenic view", "우와!!", "Wow!!"),
            ("taking a selfie with a landmark", "인생샷", "Selfie time"),
            ("eating exotic local food, drooling", "진짜 맛있다", "So tasty"),
            ("walking on beach or street, sunglasses", "힐링 중", "Healing"),
            ("looking at night view, sparkling city", "예쁜 밤", "Beautiful night"),
            ("lying in hotel bed, tired but happy", "피곤해", "Tired"),
            ("waving goodbye with souvenir bags", "다음에 또 봐", "See you again")
        ]
    # 6. 연애/사랑 (NEW)
    elif "연애" in theme:
        return [
            ("getting ready in front of mirror, blushing", "두근두근", "Heart beat"),
            ("checking phone message, shy smile", "연락 왔다!", "Message!"),
            ("meeting someone(shadow or hand), happy face", "안녕?", "Hi?"),
            ("walking side by side, hands touching", "설레...", "Flutter"),
            ("sitting in a cafe, drinking coffee together", "좋다", "So good"),
            ("minor misunderstanding, looking sad/pouty", "흥!", "Hmph!"),
            ("receiving a flower or gift, surprised", "어? 선물?", "A gift?"),
            ("smiling widely, hearts floating around", "고마워", "Thank you"),
            ("making a heart shape with hands", "사랑해", "Love you"),
            ("waving goodbye, blowing a kiss", "행복하세요", "Be happy")
        ]
    # 7. 공포/미스터리 (NEW)
    elif "공포" in theme:
        return [
            ("dark room, holding a candle/flashlight", "무서운 이야기", "Scary Story"),
            ("hearing a strange noise, looking back", "무슨 소리지?", "What's that?"),
            ("walking slowly in a dark hallway, sweating", "누구세요?", "Who's there?"),
            ("shadow appearing behind the character", "히익!", "Eek!"),
            ("extreme close-up on scared eyes, shocked", "깜짝이야!", "Shocked!"),
            ("running away, speed lines", "도망쳐!", "Run!"),
            ("hiding under blanket or desk, shaking", "살려줘...", "Help me..."),
            ("revealing the monster is actually cute/small", "어라?", "Huh?"),
            ("sigh of relief, wiping sweat", "다행이다", "Relief"),
            ("waving goodbye with a ghost costume", "오싹했죠?", "Spooky?")
        ]
    # 8. 제품 리뷰 (NEW)
    elif "리뷰" in theme:
        return [
            ("holding a delivery box, excited face", "택배 왔다!", "Delivery!"),
            ("opening the box (unboxing), sparkles", "언박싱", "Unboxing"),
            ("holding the product (glowing item)", "짜잔!", "Ta-da!"),
            ("examining product closely, magnifying glass", "디테일 봐", "Details"),
            ("using the product, looking amazed", "대박인데?", "Amazing!"),
            ("showing 'Before' state (bad)", "전에는...", "Before..."),
            ("showing 'After' state (good)", "확 달라짐!", "Changed!"),
            ("giving a big thumbs up, winking", "강추!", "Recommend!"),
            ("pointing to bio/link text", "링크 확인", "Check Link"),
            ("waving goodbye holding the product", "득템하세요", "Get it!")
        ]
    
    return []

def make_prompts(ctype, cspec, cfeat, coutfit, theme, style, layout, lang, seed):
    
    # 1. 캐릭터 조립
    if ctype == "직접 입력 (Custom)":
        species = cspec
    else:
        species = ctype.split("(")[1].replace(")", "")
    
    # 동물형은 의인화 추가
    if species in ["Cat", "Dog", "Rabbit", "Bear", "Hamster", "Tiger"]:
        base_char = f"Cute anthropomorphic {species} character"
    else:
        base_char = f"Cute {species} character"

    full_char_desc = f"{base_char}, {cfeat}, wearing {coutfit}, simple iconic design"

    # 2. 스타일 설정
    if style == "손그림/낙서":
        style_kw = "doodle style, rough pencil lines, crayon texture, loose and cute"
    elif style == "고퀄리티 일러스트":
        style_kw = "high quality 3D render style, pixar style, octane render, detailed lighting"
    else: 
        style_kw = "flat vector art, thick outlines, webtoon style, cel shading, clean colors"

    # 3. 레이아웃 설정
    if layout == "다이내믹":
        angle_kw = "dynamic dutch angle, exaggerated perspective, speed lines"
    elif layout == "시네마틱":
        angle_kw = "cinematic lighting, depth of field, dramatic angles"
    else:
        angle_kw = "flat composition, symmetrical balance, clear eye-level shot"

    # 4. 시나리오 데이터 가져오기
    story_data = get_story_scenario(theme, full_char_desc)
    
    prompts = []
    
    for i, (action, ko_text, en_text) in enumerate(story_data):
        
        # 언어별 텍스트 처리
        text_prompt = ""
        if lang == "한국어 (Korean)":
            text_prompt = f'speech bubble with text "{ko_text}", written in Korean Hangul font, bold text'
        elif lang == "영어 (English)":
            text_prompt = f'speech bubble with text "{en_text}", written in English, comic font'
        else:
            text_prompt = "no text, no speech bubbles"

        # 최종 프롬프트 조합
        p = f"/imagine prompt: **[Cut {i+1}]** {full_char_desc} **[Action]** {action} **[Text]** {text_prompt} **[Style]** {style_kw}, {angle_kw} --ar 4:5 --niji 6 --seed {seed}"
        prompts.append(p)
    
    return prompts, full_char_desc

# ==========================================
# 5. 결과 출력 및 복사 (UI)
# ==========================================

# 세션 상태 초기화
if 'generated_prompts' not in st.session_state:
    st.session_state.generated_prompts = []
    st.session_state.char_summary = ""

# 버튼 클릭
if st.button("🚀 인스타툰 시나리오 & 프롬프트 생성"):
    with st.spinner("AI가 이야기와 대사를 쓰고 있습니다..."):
        prompts, summary = make_prompts(
            char_type, custom_species, char_feature, char_outfit, 
            story_theme, art_style, layout_mode, text_lang, seed_num
        )
        st.session_state.generated_prompts = prompts
        st.session_state.char_summary = summary

# 결과 표시
if st.session_state.generated_prompts:
    st.divider()
    st.success(f"✅ 생성 완료! 테마: {story_theme}")
    
    # [1] 전체 복사
    st.subheader("📋 전체 프롬프트 복사")
    st.caption("오른쪽 위의 📄 아이콘을 누르세요.")
    all_text = "\n\n".join(st.session_state.generated_prompts)
    st.code(all_text, language="markdown")
    
    st.divider()
    
    # [2] 개별 컷 확인
    st.subheader("✂️ 컷별 상세 확인 (대사 포함)")
    
    for i, p in enumerate(st.session_state.generated_prompts):
        # 보기 좋게 파싱
        try:
            action_part = p.split("**[Action]**")[1].split("**[Text]**")[0].strip()
            text_part = p.split('text "')[1].split('"')[0] if 'text "' in p else "대사 없음"
        except:
            action_part = "장면 설명"
            text_part = ""

        with st.expander(f"Cut {i+1}: {text_part} ({action_part})", expanded=True):
            st.code(p, language="markdown")
