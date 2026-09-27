# 제주-경남 협력형 에너지인력양성센터 홍보 영상 시나리오 v4

---

## 버전 히스토리

| 버전 | 주요 변경 내용 |
|------|----------------|
| v1 | 최초 시나리오 작성 — 씬 1~3 스토리보드, 프롬프트 초안 |
| v2 | USP 추가, 씬별 프롬프트 수정 기록 추가, 도구 선택 이유 명시, 단계별 실행 가이드 추가 |
| v3 | 프롬프트 v2 확정본 반영, 진행 상황 추적 항목 추가, 다음 세션 시작점 명시, 내레이션 nova/shimmer 비교 방식 정립 |
| v4 | 전 씬 제작 완료 반영, 편집 도구 Vegas 15 Pro 확정, 씬 3 자막 Python 스크립트 방식 추가, 보너스 2 완료 추가 |

---

## 브랜드 아이덴티티

```
브랜드명:    제주-경남 협력형 에너지인력양성센터
타겟:        에너지 분야 취업을 희망하는 청년 / 취준생
톤앤매너:    미래지향적·역동적, 클린에너지, 첨단기술, 모던 블루 계열
USP:         제주(풍력·수소)와 경남(제조·연구)의 지역 협력으로 만든 실전형 에너지 인재 육성
핵심 메시지: "에너지 산업의 미래를 내가 이끈다."
광고 목적:   인지 — 센터의 존재와 비전을 청년층에게 각인
```

---

## 현재 진행 상황 (v4 기준 — 전 작업 완료)

```
[✅] 씬 1 참고 이미지    scene01_ref.png 생성 완료
[✅] 씬 1 영상           scene01_futurecity.mp4 생성 완료 (BGM 포함 — 그대로 사용)
[✅] 씬 2 참고 이미지    scene02_ref.png 생성 완료
[✅] 씬 2 영상           scene02_labstudents.mp4 생성 완료
[✅] 씬 3 배경 이미지    scene03_outro_bg.png 생성 완료
[✅] 씬 3 영상           scene03_outro.mp4 생성 완료 (veo-3.1)
[✅] 씬 3 자막 합성      scene03_outro.mp4 위에 Python 스크립트로 자막 합성 완료
[✅] 내레이션            nova / shimmer 비교 완료 — 최종 선택 후 파일명 확정
[✅] 최종 편집           Vegas 15 Pro로 씬 1~3 + 내레이션 통합 완료
[✅] 보너스 2            sora-2로 씬 1~3 전체 재제작 완료
```

---

## 씬별 스토리보드

### 씬 1 — 미래 에너지 도시 (0~4초)

| 필드 | 내용 |
|------|------|
| 씬 번호 / 길이 | 씬 1 / 4초 |
| 목표 메시지 | "풍력과 수소가 가득한 미래 에너지 도시가 펼쳐진다" |
| 화면 구성 | 부감 항공뷰 / 해상 풍력발전 단지 + 수소 에너지 시설이 있는 미래 스마트시티 / 새벽빛 또는 일출 조명 / 파란 에너지 라인 / 텍스트 없음 |
| 내레이션 | "미래 에너지가 세상을 바꾸고 있습니다." |
| 사용 도구 | 참고 이미지: gemini-2.5-flash-image (codyssey_media.py) / 영상: veo-3.1 (codyssey_media.py) / 내레이션: gpt-4o-mini-tts (codyssey_media.py) |
| 도구 선택 이유 | gemini-2.5-flash-image — 영상 생성 전 화면 구성·색감·분위기 사전 확인용 / veo-3.1 — Codyssey 기관 API 확정 영상 모델, 텍스트 프롬프트에서 4초 영상 직접 생성 / gpt-4o-mini-tts — 기관 API 확정 TTS 모델, 내레이션 MP3 직접 생성 |
| 참고 이미지 프롬프트 (영문) | `futuristic smart coastal city in the foreground with 5 offshore wind turbines neatly aligned in the background, glowing blue energy lines, cinematic aerial drone view, golden hour sunrise lighting, ultra-realistic, clean composition` |
| 영상 프롬프트 (영문) | 이미지 프롬프트와 동일 |
| 내레이션 텍스트 | `미래 에너지가 세상을 바꾸고 있습니다.` |
| 출력 결과 요약 | 참고 이미지 확인 후 → 해상 풍력+수소시설+미래도시 조감이 결합된 4초 영상 + 내레이션 MP3 |
| 결과 파일명 | `media/images/scene01_ref.png` ✅ / `media/videos/scene01_futurecity.mp4` ✅ / `media/audio/scene01_narration.mp3` ✅ |

#### 실행 명령어 (씬 1)

**① 참고 이미지 생성** ✅

```powershell
python codyssey_media.py image "futuristic smart coastal city in the foreground with 5 offshore wind turbines neatly aligned in the background, glowing blue energy lines, cinematic aerial drone view, golden hour sunrise lighting, ultra-realistic, clean composition" --model gemini-2.5-flash-image
```

파일명 변경: `image_YYYYMMDD_HHMMSS.png` → `scene01_ref.png`

**② 영상 생성** ✅

```powershell
python codyssey_media.py video "futuristic smart coastal city in the foreground with 5 offshore wind turbines neatly aligned in the background, glowing blue energy lines, cinematic aerial drone view, golden hour sunrise lighting, ultra-realistic, clean composition" --model veo-3.1 --duration 4 --resolution 720p --image media/images/scene01_ref.png
```

파일명 변경: `video_YYYYMMDD_HHMMSS.mp4` → `scene01_futurecity.mp4`

**③ 내레이션 생성** ✅

> nova / shimmer 두 버전 생성 후 청취 비교 → 최종 선택 (하단 '내레이션 명령어' 섹션 참조)

#### 프롬프트 수정 기록 (씬 1)

| 버전 | 프롬프트 | 변경 사유 |
|------|----------|-----------|
| 초안 | `futuristic city with wind turbines` | 도시와 풍력이 어색하게 분리되어 연결감 없음, 너무 일반적인 SF 도시 느낌 |
| v1 수정 | `futuristic smart coastal city with massive offshore wind turbines and hydrogen energy infrastructure, glowing blue energy lines, cinematic aerial drone view, golden hour sunrise lighting, ultra-realistic` | `coastal` 추가로 제주 해안 느낌 / `hydrogen energy infrastructure`, `glowing blue energy lines` 추가로 수소·에너지 시각화 / `golden hour sunrise`로 희망적 분위기 강조 |
| v2 확정 | `futuristic smart coastal city in the foreground with 5 offshore wind turbines neatly aligned in the background, glowing blue energy lines, cinematic aerial drone view, golden hour sunrise lighting, ultra-realistic, clean composition` | `in the foreground` / `5 offshore wind turbines neatly aligned in the background` — 전경·후경 구도 명확화 / `clean composition` 추가로 깔끔한 화면 구성 |

---

### 씬 2 — 연구실에서 연구하는 학생들 (4~8초)

| 필드 | 내용 |
|------|------|
| 씬 번호 / 길이 | 씬 2 / 4초 |
| 목표 메시지 | "나 역시 이곳에서 미래 에너지를 연구할 수 있다" |
| 화면 구성 | 수평 미디엄샷 / 첨단 에너지 연구실 내부 / 청년 학생 2~3명이 홀로그래픽 디스플레이·실험장비 앞에서 협력 연구 / 파란·흰 조명 / 텍스트 없음 |
| 내레이션 | "당신의 손으로 직접 설계하세요." |
| 사용 도구 | 참고 이미지: gemini-2.5-flash-image (codyssey_media.py) / 영상: veo-3.1 (codyssey_media.py) / 내레이션: gpt-4o-mini-tts (codyssey_media.py) |
| 도구 선택 이유 | gemini-2.5-flash-image — 영상 생성 전 화면 구성·색감·분위기 사전 확인용 / veo-3.1 — 씬 1과 동일 모델로 색감·스타일 일관성 유지 / gpt-4o-mini-tts — 씬 1과 동일 TTS 모델, 목소리 톤 통일 |
| 참고 이미지 프롬프트 (영문) | `young Korean students gathered together around advanced lab equipment and large holographic displays showing wind turbine schematics and hydrogen energy data, all focused on the same experiment, bright professional energy research laboratory, cool blue and white lighting, cinematic composition, ultra-realistic` |
| 영상 프롬프트 (영문) | 이미지 프롬프트와 동일 |
| 내레이션 텍스트 | `당신의 손으로 직접 설계하세요.` |
| 출력 결과 요약 | 참고 이미지 확인 후 → 첨단 랩실에서 협력 연구하는 청년 학생들의 4초 영상 + 내레이션 MP3 |
| 결과 파일명 | `media/images/scene02_ref.png` ✅ / `media/videos/scene02_labstudents.mp4` ✅ / `media/audio/scene02_narration.mp3` ✅ |

#### 실행 명령어 (씬 2)

**① 참고 이미지 생성** ✅

```powershell
python codyssey_media.py image "young Korean students gathered together around advanced lab equipment and large holographic displays showing wind turbine schematics and hydrogen energy data, all focused on the same experiment, bright professional energy research laboratory, cool blue and white lighting, cinematic composition, ultra-realistic" --model gemini-2.5-flash-image
```

파일명 변경: `image_YYYYMMDD_HHMMSS.png` → `scene02_ref.png`

**② 영상 생성** ✅

```powershell
python codyssey_media.py video "young Korean students gathered together around advanced lab equipment and large holographic displays showing wind turbine schematics and hydrogen energy data, all focused on the same experiment, bright professional energy research laboratory, cool blue and white lighting, cinematic composition, ultra-realistic" --model veo-3.1 --duration 4 --resolution 720p --image media/images/scene02_ref.png
```

파일명 변경: `video_YYYYMMDD_HHMMSS.mp4` → `scene02_labstudents.mp4`

**③ 내레이션 생성** ✅

> nova / shimmer 두 버전 생성 후 청취 비교 → 최종 선택 (하단 '내레이션 명령어' 섹션 참조)

#### 프롬프트 수정 기록 (씬 2)

| 버전 | 프롬프트 | 변경 사유 |
|------|----------|-----------|
| 초안 | `students working in a laboratory, scientific equipment` | 일반 화학·생물 실험실처럼 보여 에너지 연구 느낌이 없음 / 학생 얼굴 클로즈업으로 AI 특유의 부자연스러운 얼굴 왜곡 발생 |
| v1 수정 | `young Asian students researching in a futuristic advanced energy laboratory, holographic displays showing wind turbine schematics and hydrogen molecules, modern scientific equipment, teamwork atmosphere, cool blue and white lighting, cinematic composition, ultra-realistic` | `energy laboratory`로 분야 특정 / `holographic displays` 추가로 에너지 연구 시각화 / `teamwork atmosphere`로 협력 분위기 강조 |
| v2 확정 | `young Korean students gathered together around advanced lab equipment and large holographic displays showing wind turbine schematics and hydrogen energy data, all focused on the same experiment, bright professional energy research laboratory, cool blue and white lighting, cinematic composition, ultra-realistic` | `gathered together around` / `all focused on the same experiment` — 학생들이 하나의 실험에 집중하는 구도 명확화 / `bright professional` — 밝고 전문적인 연구실 분위기 강조 |

---

### 씬 3 — 브랜드 타이틀 아웃트로 (8~12초)

| 필드 | 내용 |
|------|------|
| 씬 번호 / 길이 | 씬 3 / 4초 |
| 목표 메시지 | "제주-경남 협력형 에너지인력양성센터가 당신을 기다립니다" |
| 화면 구성 | 밝은 미래 에너지 도시 영상 배경 / 화면 하단부 자막 위치에 센터명 텍스트 페이드인 |
| 내레이션 | "제주-경남 협력형 에너지인력양성센터." |
| 화면 텍스트 | `제주-경남 협력형 에너지인력양성센터` |
| 사용 도구 | 배경 이미지: gemini-2.5-flash-image (codyssey_media.py) / 영상: veo-3.1 (codyssey_media.py) / 자막 합성: Python 스크립트 (OpenCV + Pillow + FFmpeg) / 내레이션: gpt-4o-mini-tts (codyssey_media.py) |
| 도구 선택 이유 | gemini-2.5-flash-image — 텍스트 오버레이용 배경 기준 이미지 생성 / veo-3.1 — 정지 이미지 대신 움직이는 영상으로 씬 통일감 확보 / Python 스크립트 — CapCut 없이 자막·페이드인 효과를 코드로 직접 처리, 재현 가능 / gpt-4o-mini-tts — 씬 1·2와 동일 TTS 모델로 목소리 통일 |
| 이미지 프롬프트 (영문) | `bright futuristic smart city powered by clean energy, solar panels on buildings, 5 offshore wind turbines in the distance, glowing blue energy lines flowing through the city, golden sunlight, cinematic aerial drone view, hopeful and vibrant atmosphere, ultra-realistic, no text` |
| 내레이션 텍스트 | `제주-경남 협력형 에너지인력양성센터.` |
| 출력 결과 요약 | 배경 이미지 → veo-3.1 영상 생성 → Python 스크립트로 자막 합성 → 내레이션 MP3 |
| 결과 파일명 | `media/images/scene03_outro_bg.png` ✅ / `media/videos/scene03_outro.mp4` ✅ (자막 합성 완료) / `media/audio/scene03_narration.mp3` ✅ |

#### 실행 명령어 (씬 3)

**① 배경 이미지 생성** ✅

```powershell
python codyssey_media.py image "bright futuristic smart city powered by clean energy, solar panels on buildings, 5 offshore wind turbines in the distance, glowing blue energy lines flowing through the city, golden sunlight, cinematic aerial drone view, hopeful and vibrant atmosphere, ultra-realistic, no text" --model gemini-2.5-flash-image
```

파일명 변경: `image_YYYYMMDD_HHMMSS.png` → `scene03_outro_bg.png`

**② 영상 생성** ✅

```powershell
python codyssey_media.py video "bright futuristic smart city powered by clean energy, solar panels on buildings, 5 offshore wind turbines in the distance, glowing blue energy lines flowing through the city, golden sunlight, cinematic aerial drone view, hopeful and vibrant atmosphere, ultra-realistic, no text" --model veo-3.1 --duration 4 --resolution 720p --image media/images/scene03_outro_bg.png
```

파일명 변경: `video_YYYYMMDD_HHMMSS.mp4` → (자막 합성 후 `scene03_outro.mp4`로 확정)

**③ 씬 3 자막 합성 — Python 스크립트** ✅

> CapCut 대신 Python 스크립트로 자막을 직접 합성하는 방식을 채택. 코드로 처리하므로 재현 가능하고 외부 편집 앱 없이 동작.

스크립트 파일: `add_text_scene03.py`

```python
# 핵심 파라미터
TEXT      = "제주-경남 협력형 에너지인력양성센터"
FONT_PATH = r"C:\Windows\Fonts\malgunbd.ttf"   # 맑은 고딕 Bold
FONT_SIZE = 60
FADE_SEC  = 1.0   # 0~1초 페이드인
# 위치: 화면 중앙 → 아래 절반 → 다시 아래 절반 (y = H * 7/8)
```

```powershell
python add_text_scene03.py
```

**자막 처리 방식:**
1. Pillow로 투명 배경 RGBA PNG에 흰색 텍스트 생성 (맑은 고딕 Bold, 가운데 정렬, y=7/8 지점)
2. 반투명 검정 배경 박스 + 드롭 섀도 추가로 가독성 확보
3. OpenCV로 프레임별 알파 블렌딩 — 0~1초 동안 선형 페이드인
4. FFmpeg으로 원본 오디오 붙여 최종 MP4 출력

출력 파일: `media/videos/scene03_outro.mp4`

**④ 내레이션 생성** ✅

> nova / shimmer 두 버전 생성 후 청취 비교 → 최종 선택

#### 프롬프트 수정 기록 (씬 3)

| 버전 | 프롬프트 | 변경 사유 |
|------|----------|-----------|
| v1 원안 | `abstract futuristic energy background, flowing blue particle waves, glowing light streams, deep space dark blue background, clean minimal composition, no text, ultra-realistic` | 추상적 어두운 배경 — 브랜드 타이틀 텍스트 오버레이용 |
| v2 확정 | `bright futuristic smart city powered by clean energy, solar panels on buildings, 5 offshore wind turbines in the distance, glowing blue energy lines flowing through the city, golden sunlight, cinematic aerial drone view, hopeful and vibrant atmosphere, ultra-realistic, no text` | 추상 배경 → 밝은 미래 에너지 도시로 변경하여 희망적 분위기 강조 / 씬 1과 시각적 연결감 확보 / `solar panels`, `wind turbines` — 클린에너지 요소 직접 표현 |

---

## 내레이션 명령어

> nova / shimmer 두 버전 생성 후 청취 비교 → 최종 선택

### Nova

```powershell
python codyssey_media.py audio "미래 에너지가 세상을 바꾸고 있습니다." --model gpt-4o-mini-tts --voice nova --output "media/audio/scene01_narration_nova.mp3"
```

```powershell
python codyssey_media.py audio "당신의 손으로 직접 설계하세요." --model gpt-4o-mini-tts --voice nova --output "media/audio/scene02_narration_nova.mp3"
```

```powershell
python codyssey_media.py audio "제주-경남 협력형 에너지인력양성센터." --model gpt-4o-mini-tts --voice nova --output "media/audio/scene03_narration_nova.mp3"
```

### Shimmer

```powershell
python codyssey_media.py audio "미래 에너지가 세상을 바꾸고 있습니다." --model gpt-4o-mini-tts --voice shimmer --output "media/audio/scene01_narration_shimmer.mp3"
```

```powershell
python codyssey_media.py audio "당신의 손으로 직접 설계하세요." --model gpt-4o-mini-tts --voice shimmer --output "media/audio/scene02_narration_shimmer.mp3"
```

```powershell
python codyssey_media.py audio "제주-경남 협력형 에너지인력양성센터." --model gpt-4o-mini-tts --voice shimmer --output "media/audio/scene03_narration_shimmer.mp3"
```

---

## 사용 도구 목록

| 카테고리 | 도구 | 실행 방식 |
|----------|------|------------|
| 이미지 생성 | gemini-2.5-flash-image | VS Code 터미널 `codyssey_media.py image` |
| 영상 생성 | veo-3.1 (4초 / 720p) | VS Code 터미널 `codyssey_media.py video` |
| 내레이션 (TTS) | gpt-4o-mini-tts (nova / shimmer) | VS Code 터미널 `codyssey_media.py audio` |
| 씬 3 자막 합성 | Python 스크립트 (OpenCV + Pillow + FFmpeg) | VS Code 터미널 `python add_text_scene03.py` |
| 최종 영상 편집 | Vegas 15 Pro | Vegas Pro 앱 직접 실행 |

---

## 최종 영상 정보

```
파일명:        energy_center_promo.mp4
길이:          12초 (씬당 4초 × 3씬)
해상도:        1280x720 (720p)
프레임레이트:  30fps
비디오 코덱:   H.264
오디오 코덱:   AAC
```

---

# 단계별 실행 가이드

> 이 순서대로 따라가면 영상 완성까지 막히지 않습니다.

---

## 사전 준비 — API 키 설정

**어디서:** VS Code 터미널 (PowerShell)

```powershell
cd C:\co\codyssey_media_setup
$env:CODYSSEY_API_KEY="발급받은_API_KEY"
```

> API 키는 터미널 세션마다 다시 설정해야 합니다. VS Code를 새로 열거나 터미널을 닫으면 재입력 필요.

---

## STEP 1. gemini-2.5-flash-image — 씬 1 참고 이미지 생성 ✅

```powershell
python codyssey_media.py image "futuristic smart coastal city in the foreground with 5 offshore wind turbines neatly aligned in the background, glowing blue energy lines, cinematic aerial drone view, golden hour sunrise lighting, ultra-realistic, clean composition" --model gemini-2.5-flash-image
```

파일명 변경: `image_YYYYMMDD_HHMMSS.png` → `scene01_ref.png`

---

## STEP 2. veo-3.1 — 씬 1 영상 생성 ✅

```powershell
python codyssey_media.py video "futuristic smart coastal city in the foreground with 5 offshore wind turbines neatly aligned in the background, glowing blue energy lines, cinematic aerial drone view, golden hour sunrise lighting, ultra-realistic, clean composition" --model veo-3.1 --duration 4 --resolution 720p --image media/images/scene01_ref.png
```

파일명 변경: `video_YYYYMMDD_HHMMSS.mp4` → `scene01_futurecity.mp4`

---

## STEP 3. gemini-2.5-flash-image — 씬 2 참고 이미지 생성 ✅

```powershell
python codyssey_media.py image "young Korean students gathered together around advanced lab equipment and large holographic displays showing wind turbine schematics and hydrogen energy data, all focused on the same experiment, bright professional energy research laboratory, cool blue and white lighting, cinematic composition, ultra-realistic" --model gemini-2.5-flash-image
```

파일명 변경: `image_YYYYMMDD_HHMMSS.png` → `scene02_ref.png`

---

## STEP 4. veo-3.1 — 씬 2 영상 생성 ✅

```powershell
python codyssey_media.py video "young Korean students gathered together around advanced lab equipment and large holographic displays showing wind turbine schematics and hydrogen energy data, all focused on the same experiment, bright professional energy research laboratory, cool blue and white lighting, cinematic composition, ultra-realistic" --model veo-3.1 --duration 4 --resolution 720p --image media/images/scene02_ref.png
```

파일명 변경: `video_YYYYMMDD_HHMMSS.mp4` → `scene02_labstudents.mp4`

---

## STEP 5. gemini-2.5-flash-image — 씬 3 배경 이미지 생성 ✅

```powershell
python codyssey_media.py image "bright futuristic smart city powered by clean energy, solar panels on buildings, 5 offshore wind turbines in the distance, glowing blue energy lines flowing through the city, golden sunlight, cinematic aerial drone view, hopeful and vibrant atmosphere, ultra-realistic, no text" --model gemini-2.5-flash-image
```

파일명 변경: `image_YYYYMMDD_HHMMSS.png` → `scene03_outro_bg.png`

---

## STEP 5-2. veo-3.1 — 씬 3 영상 생성 ✅

> v3까지는 정지 이미지 + CapCut Ken Burns 효과 방식이었으나, v4에서 veo-3.1로 움직이는 영상을 직접 생성하는 방식으로 변경.

```powershell
python codyssey_media.py video "bright futuristic smart city powered by clean energy, solar panels on buildings, 5 offshore wind turbines in the distance, glowing blue energy lines flowing through the city, golden sunlight, cinematic aerial drone view, hopeful and vibrant atmosphere, ultra-realistic, no text" --model veo-3.1 --duration 4 --resolution 720p --image media/images/scene03_outro_bg.png
```

---

## STEP 5-3. Python 스크립트 — 씬 3 자막 합성 ✅

> veo-3.1로 생성한 씬 3 영상 위에 센터명 자막을 코드로 직접 합성.

```powershell
python add_text_scene03.py
```

**자막 스펙:**
- 텍스트: `제주-경남 협력형 에너지인력양성센터`
- 폰트: 맑은 고딕 Bold (malgunbd.ttf), 60pt
- 색상: 흰색 + 드롭 섀도 + 반투명 검정 배경 박스
- 위치: 화면 7/8 지점 (하단부), 가로 가운데 정렬
- 효과: 0~1초 선형 페이드인

출력 파일: `media/videos/scene03_outro.mp4`

---

## STEP 6. gpt-4o-mini-tts — 내레이션 생성 ✅

> nova / shimmer 두 버전 생성 후 청취 비교하여 최종 선택.

씬 1 내레이션 (Nova / Shimmer):
```powershell
python codyssey_media.py audio "미래 에너지가 세상을 바꾸고 있습니다." --model gpt-4o-mini-tts --voice nova --output "media/audio/scene01_narration_nova.mp3"
python codyssey_media.py audio "미래 에너지가 세상을 바꾸고 있습니다." --model gpt-4o-mini-tts --voice shimmer --output "media/audio/scene01_narration_shimmer.mp3"
```

씬 2 내레이션 (Nova / Shimmer):
```powershell
python codyssey_media.py audio "당신의 손으로 직접 설계하세요." --model gpt-4o-mini-tts --voice nova --output "media/audio/scene02_narration_nova.mp3"
python codyssey_media.py audio "당신의 손으로 직접 설계하세요." --model gpt-4o-mini-tts --voice shimmer --output "media/audio/scene02_narration_shimmer.mp3"
```

씬 3 내레이션 (Nova / Shimmer):
```powershell
python codyssey_media.py audio "제주-경남 협력형 에너지인력양성센터." --model gpt-4o-mini-tts --voice nova --output "media/audio/scene03_narration_nova.mp3"
python codyssey_media.py audio "제주-경남 협력형 에너지인력양성센터." --model gpt-4o-mini-tts --voice shimmer --output "media/audio/scene03_narration_shimmer.mp3"
```

---

## STEP 7. Vegas 15 Pro — 최종 편집 ✅

> v3까지는 CapCut을 편집 도구로 계획했으나, v4에서 Vegas 15 Pro로 최종 편집 도구 변경.

### 타임라인 구성
```
[씬1: scene01_futurecity.mp4      / 0~4초]
[씬2: scene02_labstudents.mp4     / 4~8초]
[씬3: scene03_outro.mp4           / 8~12초]  ← 자막 이미 합성된 파일
```

### 씬 전환 효과
- 씬 1→2: `Cross Dissolve` 0.3초
- 씬 2→3: `Fade to Black` 후 밝아지기 0.3초

### 내레이션 삽입
- `scene01_narration.mp3` → 씬 1 구간 (0~4초)
- `scene02_narration.mp3` → 씬 2 구간 (4~8초)
- `scene03_narration.mp3` → 씬 3 구간 (8~12초)
- 볼륨: 100% / 각 씬 끝 0.3초 페이드아웃

### 색보정 (선택)
- 전체 씬 밝기 살짝 올리기 (+5~10)
- 채도: 파란 계열 강조 (+10)
- 씬 간 색온도 통일 (쿨톤 유지)

### 내보내기 설정
```
해상도:        1280x720
프레임레이트:  30fps
포맷:          MP4 (H.264)
오디오:        AAC
파일명:        energy_center_promo.mp4
```

---

## 작업 순서 요약 체크리스트

```
[✅] 사전 준비    VS Code 터미널에서 디렉토리 이동 및 API 키 설정
[✅] STEP 1       씬 1 참고 이미지 생성 및 검토 (gemini-2.5-flash-image)
[✅] STEP 2       씬 1 영상 생성 (veo-3.1, 4초/720p)
[✅] STEP 3       씬 2 참고 이미지 생성 및 검토 (gemini-2.5-flash-image)
[✅] STEP 4       씬 2 영상 생성 (veo-3.1, 4초/720p)
[✅] STEP 5       씬 3 배경 이미지 생성 (gemini-2.5-flash-image)
[✅] STEP 5-2     씬 3 영상 생성 (veo-3.1, 4초/720p)
[✅] STEP 5-3     씬 3 자막 합성 (Python 스크립트 — OpenCV + Pillow + FFmpeg)
[✅] STEP 6       씬 1·2·3 내레이션 생성 (gpt-4o-mini-tts, nova/shimmer 비교 후 선택)
[✅] STEP 7       Vegas 15 Pro로 클립 + 내레이션 통합 편집 후 MP4 내보내기
```

---

## 작업 흐름 한눈에 보기

| 순서 | 도구 | 할 일 | 결과물 | 상태 |
|------|------|--------|--------|------|
| 1 | **gemini-2.5-flash-image** | 씬 1 참고 이미지 생성·검토 | `scene01_ref.png` | ✅ |
| 2 | **veo-3.1** | 씬 1 영상 생성 | `scene01_futurecity.mp4` | ✅ |
| 3 | **gemini-2.5-flash-image** | 씬 2 참고 이미지 생성·검토 | `scene02_ref.png` | ✅ |
| 4 | **veo-3.1** | 씬 2 영상 생성 | `scene02_labstudents.mp4` | ✅ |
| 5 | **gemini-2.5-flash-image** | 씬 3 배경 이미지 생성 | `scene03_outro_bg.png` | ✅ |
| 5-2 | **veo-3.1** | 씬 3 영상 생성 | `scene03_outro_raw.mp4` | ✅ |
| 5-3 | **Python (OpenCV+Pillow+FFmpeg)** | 씬 3 자막 합성 | `scene03_outro.mp4` | ✅ |
| 6 | **gpt-4o-mini-tts** | 씬 1·2·3 내레이션 생성 (nova/shimmer) | `scene0X_narration.mp3` × 3 | ✅ |
| 7 | **Vegas 15 Pro** | 클립 + 내레이션 통합 편집 → MP4 | `energy_center_promo.mp4` | ✅ |

---

## 최종 파일 목록

```
media/
├── images/
│   ├── scene01_ref.png                  ✅
│   ├── scene02_ref.png                  ✅
│   ├── scene03_outro_bg.png             ✅
│   └── scene03_text_overlay.png         ✅  (자막 합성용 중간 산출물)
├── videos/
│   ├── scene01_futurecity.mp4           ✅
│   ├── scene02_labstudents.mp4          ✅
│   └── scene03_outro.mp4                ✅  (자막 합성 완료본)
└── audio/
    ├── scene01_narration_nova.mp3        ✅
    ├── scene01_narration_shimmer.mp3     ✅
    ├── scene02_narration_nova.mp3        ✅
    ├── scene02_narration_shimmer.mp3     ✅
    ├── scene03_narration_nova.mp3        ✅
    └── scene03_narration_shimmer.mp3     ✅

scripts/
└── add_text_scene03.py                  ✅  (씬 3 자막 합성 스크립트)

output/
└── energy_center_promo.mp4              ✅  (최종 완성본)
```

---

## 오류 발생 시 대응

| 상황 | 대응 |
|------|------|
| API 키 오류 | `$env:CODYSSEY_API_KEY` 재설정 후 재실행 |
| 영상 생성 타임아웃 | `codyssey_media.py`가 자동 재시도, 완료까지 대기 후 저장 |
| 이미지 품질 불량 | 프롬프트에 `cinematic`, `photorealistic` 키워드 추가 후 재생성 |
| 영상에 인물 왜곡 발생 | `silhouette style` 또는 `blurred face` 키워드 추가 후 재생성 |
| 자막 스크립트 오류 — ffmpeg 없음 | `where.exe ffmpeg`로 경로 확인 후 `add_text_scene03.py`의 FFMPEG 변수 수정 |
| 자막 스크립트 오류 — Pillow 없음 | `pip install Pillow` 설치 후 재실행 |
| 자막이 보이지 않음 | `scene03_text_overlay.png` 열어 텍스트 픽셀 확인, OpenCV 버전 확인 |

---

---

# 보너스 2 — 동일 스토리보드, 다른 도구로 재제작

---

## 개요

```
목적:    동일한 씬 1~3 스토리보드를 다른 영상 생성 도구로 재제작하여 결과물 비교
도구:    코디세이 제공 학습 네이토 sora-2
대상:    씬 1, 씬 2, 씬 3 전체 (3개 씬 모두 재제작)
상태:    ✅ 완료
```

## 재제작 내용

| 씬 | 원본 도구 | 재제작 도구 | 프롬프트 |
|----|-----------|-------------|----------|
| 씬 1 — 미래 에너지 도시 | veo-3.1 | sora-2 | 씬 1 확정 프롬프트 동일 적용 |
| 씬 2 — 연구실 학생들 | veo-3.1 | sora-2 | 씬 2 확정 프롬프트 동일 적용 |
| 씬 3 — 브랜드 아웃트로 | veo-3.1 | sora-2 | 씬 3 확정 프롬프트 동일 적용 |

## 비교 포인트

- 동일 프롬프트에서 veo-3.1과 sora-2의 영상 품질·색감·모션 스타일 차이 확인
- 생성 시간, API 사용 방식, 결과물 해상도 비교
- 최종 편집 적합성 (색보정 용이성, 씬 간 통일감) 비교
