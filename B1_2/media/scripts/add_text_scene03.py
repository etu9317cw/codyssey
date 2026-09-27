"""
씬 3 텍스트 오버레이 스크립트
- 텍스트: 제주-경남 협력형 에너지인력양성센터
- 위치: 화면 가운데
- 색상: 흰색
- 효과: 0~1초 페이드인
"""
import cv2
import numpy as np
import subprocess
from PIL import Image, ImageDraw, ImageFont

INPUT   = r"media\videos\video_20260830_182712.mp4"
OUTPUT  = r"media\videos\scene03_outro.mp4"
TEMP    = r"media\videos\scene03_temp_noaudio.mp4"
OVERLAY = r"media\images\scene03_text_overlay.png"
FFMPEG  = r"C:\ffmpeg\ffmpeg.exe"

TEXT      = "제주-경남 협력형 에너지인력양성센터"
FONT_PATH = r"C:\Windows\Fonts\malgunbd.ttf"
FONT_SIZE = 60
W, H      = 1280, 720
FADE_SEC  = 1.0  # 페이드인 구간 (초)

# 1. 텍스트 오버레이 PNG 생성
img  = Image.new("RGBA", (W, H), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)
font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
bbox   = draw.textbbox((0, 0), TEXT, font=font)
text_w = bbox[2] - bbox[0]
text_h = bbox[3] - bbox[1]
x = (W - text_w) // 2
y = H * 7 // 8 - text_h // 2  # 화면 중앙 → 아래 절반 → 다시 아래 절반

pad_x, pad_y = 28, 14
bg_x0 = x - pad_x
bg_y0 = y - pad_y
bg_x1 = x + text_w + pad_x
bg_y1 = y + text_h + pad_y

# 반투명 어두운 배경 (가독성 향상)
draw.rounded_rectangle([bg_x0, bg_y0, bg_x1, bg_y1], radius=12, fill=(0, 0, 0, 140))

# 드롭 섀도 (오른쪽 아래 4px 오프셋, 반투명 검정)
draw.text((x + 4, y + 4), TEXT, font=font, fill=(0, 0, 0, 180))

# 흰색 메인 텍스트
draw.text((x, y), TEXT, font=font, fill=(255, 255, 255, 255))
img.save(OVERLAY)
print(f"오버레이 이미지 생성: {OVERLAY}")

# RGBA numpy 배열로 변환
overlay_rgba = np.array(img, dtype=np.float32) / 255.0  # (H, W, 4)

# 2. 영상 프레임별 합성
cap = cv2.VideoCapture(INPUT)
fps   = cap.get(cv2.CAP_PROP_FPS)
total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
w     = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h     = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

fourcc = cv2.VideoWriter_fourcc(*"mp4v")
writer = cv2.VideoWriter(TEMP, fourcc, fps, (w, h))

print(f"프레임 합성 중... (총 {total}프레임, {fps}fps)")

for idx in range(total):
    ret, frame = cap.read()
    if not ret:
        break

    t = idx / fps
    alpha = min(t / FADE_SEC, 1.0)  # 0~1초 동안 0→1

    if alpha > 0:
        frame_f = frame.astype(np.float32) / 255.0          # (H, W, 3) BGR
        text_alpha = overlay_rgba[:, :, 3:4] * alpha         # (H, W, 1)
        text_rgb   = overlay_rgba[:, :, :3][:, :, ::-1]      # RGB→BGR

        frame_f = frame_f * (1 - text_alpha) + text_rgb * text_alpha
        frame = (frame_f * 255).clip(0, 255).astype(np.uint8)

    writer.write(frame)

cap.release()
writer.release()
print("프레임 합성 완료")

# 3. 오디오 붙이기 (ffmpeg)
print("오디오 합성 중...")
cmd = [
    FFMPEG, "-y",
    "-i", TEMP,
    "-i", INPUT,
    "-map", "0:v",
    "-map", "1:a?",
    "-c:v", "libx264",
    "-c:a", "copy",
    OUTPUT
]
subprocess.run(cmd, check=True)

import os
os.remove(TEMP)
print(f"완료: {OUTPUT}")
