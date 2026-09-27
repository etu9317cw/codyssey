# -*- coding: utf-8 -*-
"""
시나리오 마크다운 → PDF 변환 스크립트
fpdf2 + 나눔고딕 폰트 사용
"""

import os
import sys
from fpdf import FPDF

# ── 폰트 경로 ──────────────────────────────────────────────
FONT_DIR = r"C:\Windows\Fonts"
FONT_REGULAR = os.path.join(FONT_DIR, "malgun.ttf")     # 맑은 고딕
FONT_BOLD = os.path.join(FONT_DIR, "malgunbd.ttf")      # 맑은 고딕 Bold

# ── 색상 정의 ──────────────────────────────────────────────
COLOR_PRIMARY   = (25, 60, 120)    # 딥 블루 (제목)
COLOR_SECONDARY = (40, 95, 160)    # 미디엄 블루 (소제목)
COLOR_ACCENT    = (0, 120, 200)    # 포인트 블루
COLOR_TEXT      = (40, 40, 40)     # 본문 텍스트
COLOR_LIGHT_BG  = (235, 242, 250)  # 연한 파란 배경
COLOR_CODE_BG   = (245, 245, 245)  # 코드 배경
COLOR_WHITE     = (255, 255, 255)
COLOR_BORDER    = (180, 200, 220)  # 테이블 테두리
COLOR_TH_BG     = (30, 70, 130)    # 테이블 헤더 배경
COLOR_DONE      = (34, 139, 34)    # 완료 (초록)
COLOR_PENDING   = (200, 130, 0)    # 진행중 (주황)
COLOR_GRAY      = (120, 120, 120)  # 회색


class ScenarioPDF(FPDF):
    def __init__(self):
        super().__init__(orientation='P', unit='mm', format='A4')
        self.set_auto_page_break(auto=True, margin=20)

        # 폰트 등록
        self.add_font("MalgunGothic", "", FONT_REGULAR)
        self.add_font("MalgunGothic", "B", FONT_BOLD)

        self.page_count_total = 0

    def header(self):
        if self.page_no() == 1:
            return  # 첫 페이지(표지)에는 헤더 없음
        self.set_font("MalgunGothic", "B", 8)
        self.set_text_color(*COLOR_GRAY)
        self.cell(0, 6, "제주-경남 협력형 에너지인력양성센터 │ 홍보 영상 시나리오 v2", 0, 1, "L")
        # 헤더 밑줄
        self.set_draw_color(*COLOR_ACCENT)
        self.set_line_width(0.4)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)

    def footer(self):
        if self.page_no() == 1:
            return
        self.set_y(-15)
        self.set_font("MalgunGothic", "", 8)
        self.set_text_color(*COLOR_GRAY)
        self.cell(0, 10, f"— {self.page_no()} —", 0, 0, "C")

    # ── 유틸리티 ─────────────────────────────────────────
    def section_title(self, text, level=1):
        """섹션 제목 출력"""
        if level == 1:
            self.set_font("MalgunGothic", "B", 16)
            self.set_text_color(*COLOR_PRIMARY)
            self.ln(4)
            # 왼쪽 파란 바
            y = self.get_y()
            self.set_fill_color(*COLOR_ACCENT)
            self.rect(10, y, 3, 9, 'F')
            self.set_x(16)
            self.cell(0, 10, text, 0, 1)
            self.ln(2)
        elif level == 2:
            self.set_font("MalgunGothic", "B", 13)
            self.set_text_color(*COLOR_SECONDARY)
            self.ln(2)
            self.cell(0, 8, text, 0, 1)
            self.ln(1)

    def body_text(self, text, bold=False):
        """본문 텍스트 출력"""
        style = "B" if bold else ""
        self.set_font("MalgunGothic", style, 10)
        self.set_text_color(*COLOR_TEXT)
        self.multi_cell(0, 6, text)
        self.ln(1)

    def code_block(self, lines, lang=""):
        """코드 블록 출력 (배경색 포함)"""
        self.set_font("MalgunGothic", "", 8.5)
        self.set_text_color(50, 50, 50)

        x = self.get_x()
        w = 190

        # 전체 높이 계산
        total_h = 0
        line_heights = []
        for line in lines:
            nb = self.multi_cell(w - 8, 5, line, dry_run=True, output="LINES")
            h = len(nb) * 5
            line_heights.append(h)
            total_h += h
        total_h += 6  # 패딩

        # 페이지 넘김 체크
        if self.get_y() + total_h + 5 > self.h - self.b_margin:
            self.add_page()

        y_start = self.get_y()

        # 배경
        self.set_fill_color(*COLOR_CODE_BG)
        self.set_draw_color(*COLOR_BORDER)
        self.rect(x, y_start, w, total_h, 'DF')

        self.set_y(y_start + 3)
        for line in lines:
            self.set_x(x + 4)
            self.multi_cell(w - 8, 5, line)

        self.set_y(y_start + total_h)
        self.ln(3)

    def info_card(self, label, value):
        """라벨: 값 형태의 정보 카드"""
        self.set_font("MalgunGothic", "B", 10)
        self.set_text_color(*COLOR_SECONDARY)
        self.cell(35, 6, label, 0, 0)
        self.set_font("MalgunGothic", "", 10)
        self.set_text_color(*COLOR_TEXT)
        self.multi_cell(0, 6, value)
        self.ln(0.5)

    def status_line(self, status_icon, text):
        """상태 표시 줄 (동그라미 아이콘)"""
        is_done = ("DONE" in status_icon or "완료" in status_icon)
        y = self.get_y()
        x = self.get_x()

        # 동그라미 아이콘 그리기
        cx, cy = x + 4, y + 3
        if is_done:
            self.set_fill_color(*COLOR_DONE)
            self.set_draw_color(*COLOR_DONE)
        else:
            self.set_fill_color(*COLOR_PENDING)
            self.set_draw_color(*COLOR_PENDING)
        self.ellipse(cx - 2.5, cy - 2.5, 5, 5, 'F')

        # 체크/시계 텍스트
        self.set_font("MalgunGothic", "B", 7)
        self.set_text_color(*COLOR_WHITE)
        label = "V" if is_done else "..."
        self.set_xy(cx - 2.5, cy - 2)
        self.cell(5, 4, label, 0, 0, "C")

        # 본문 텍스트
        self.set_xy(x + 10, y)
        self.set_text_color(*COLOR_TEXT)
        self.set_font("MalgunGothic", "", 9.5)
        self.cell(0, 6, text, 0, 1)

    def scene_table(self, rows):
        """씬 정보 테이블"""
        col_w = [28, 157]
        row_h = 7

        # 헤더
        self.set_fill_color(*COLOR_TH_BG)
        self.set_text_color(*COLOR_WHITE)
        self.set_font("MalgunGothic", "B", 9)
        self.cell(col_w[0], row_h, "항목", 1, 0, "C", True)
        self.cell(col_w[1], row_h, "내용", 1, 1, "C", True)

        # 데이터
        self.set_text_color(*COLOR_TEXT)
        self.set_font("MalgunGothic", "", 9)
        fill = False
        for label, value in rows:
            if fill:
                self.set_fill_color(*COLOR_LIGHT_BG)
            else:
                self.set_fill_color(*COLOR_WHITE)

            # 값 길이에 따라 줄 수 계산
            nb_lines = self.multi_cell(col_w[1], row_h, value, dry_run=True, output="LINES")
            cell_h = max(len(nb_lines), 1) * row_h

            # 페이지 넘침 체크
            if self.get_y() + cell_h > self.h - self.b_margin:
                self.add_page()

            y_before = self.get_y()
            x_start = self.get_x()

            # 라벨 셀
            self.set_font("MalgunGothic", "B", 9)
            self.set_draw_color(*COLOR_BORDER)
            self.rect(x_start, y_before, col_w[0], cell_h, 'D')
            self.set_xy(x_start + 1, y_before + (cell_h - row_h) / 2)
            self.cell(col_w[0] - 2, row_h, label, 0, 0, "C", fill)

            # 값 셀
            self.set_font("MalgunGothic", "", 8.5)
            self.rect(x_start + col_w[0], y_before, col_w[1], cell_h, 'D')
            if fill:
                self.set_fill_color(*COLOR_LIGHT_BG)
                self.rect(x_start + col_w[0] + 0.3, y_before + 0.3,
                          col_w[1] - 0.6, cell_h - 0.6, 'F')
            self.set_xy(x_start + col_w[0] + 2, y_before + 1)
            self.multi_cell(col_w[1] - 4, row_h, value)

            self.set_y(y_before + cell_h)
            fill = not fill

        self.ln(4)

    def horizontal_rule(self):
        """구분선"""
        self.set_draw_color(*COLOR_BORDER)
        self.set_line_width(0.3)
        y = self.get_y()
        self.line(10, y, 200, y)
        self.ln(4)


def build_pdf(output_path):
    pdf = ScenarioPDF()

    # ═══════════════════════════════════════════════════════
    # 표지 (1페이지)
    # ═══════════════════════════════════════════════════════
    pdf.add_page()

    # 상단 장식 바
    pdf.set_fill_color(*COLOR_PRIMARY)
    pdf.rect(0, 0, 210, 8, 'F')
    pdf.set_fill_color(*COLOR_ACCENT)
    pdf.rect(0, 8, 210, 3, 'F')

    # 제목
    pdf.ln(55)
    pdf.set_font("MalgunGothic", "B", 28)
    pdf.set_text_color(*COLOR_PRIMARY)
    pdf.cell(0, 15, "홍보 영상 시나리오", 0, 1, "C")

    pdf.set_font("MalgunGothic", "", 12)
    pdf.set_text_color(*COLOR_GRAY)
    pdf.cell(0, 8, "Version 2.0", 0, 1, "C")

    pdf.ln(10)

    # 중앙 장식 라인
    pdf.set_draw_color(*COLOR_ACCENT)
    pdf.set_line_width(0.5)
    pdf.line(60, pdf.get_y(), 150, pdf.get_y())
    pdf.ln(12)

    # 센터명
    pdf.set_font("MalgunGothic", "B", 16)
    pdf.set_text_color(*COLOR_SECONDARY)
    pdf.cell(0, 10, "제주-경남 협력형", 0, 1, "C")
    pdf.cell(0, 10, "에너지인력양성센터", 0, 1, "C")

    pdf.ln(25)

    # 하단 정보
    pdf.set_font("MalgunGothic", "", 10)
    pdf.set_text_color(*COLOR_GRAY)
    pdf.cell(0, 7, "작성일: 2026년 8월 30일", 0, 1, "C")
    pdf.cell(0, 7, "영상 길이: 12초 (씬당 4초 × 3씬) │ 해상도: 720p", 0, 1, "C")

    # 하단 장식 바
    pdf.set_fill_color(*COLOR_ACCENT)
    pdf.rect(0, 287, 210, 3, 'F')
    pdf.set_fill_color(*COLOR_PRIMARY)
    pdf.rect(0, 290, 210, 8, 'F')

    # ═══════════════════════════════════════════════════════
    # 2페이지 — 브랜드 아이덴티티 + 현재 진행 상황
    # ═══════════════════════════════════════════════════════
    pdf.add_page()

    pdf.section_title("브랜드 아이덴티티")

    # 정보 카드 박스
    y_box_start = pdf.get_y()
    pdf.set_fill_color(*COLOR_LIGHT_BG)
    pdf.rect(10, y_box_start, 190, 52, 'F')
    pdf.set_draw_color(*COLOR_ACCENT)
    pdf.rect(10, y_box_start, 190, 52, 'D')
    pdf.ln(4)
    pdf.set_x(15)
    pdf.info_card("브랜드명", "제주-경남 협력형 에너지인력양성센터")
    pdf.set_x(15)
    pdf.info_card("타겟", "에너지 분야 취업을 희망하는 청년 / 취준생")
    pdf.set_x(15)
    pdf.info_card("톤앤매너", "미래지향적·역동적, 클린에너지, 첨단기술, 모던 블루 계열")
    pdf.set_x(15)
    pdf.info_card("핵심 메시지", '"에너지 산업의 미래를 내가 이끈다."')
    pdf.set_x(15)
    pdf.info_card("광고 목적", "인지 — 센터의 존재와 비전을 청년층에게 각인")
    pdf.set_y(y_box_start + 55)

    pdf.ln(3)
    pdf.horizontal_rule()

    pdf.section_title("현재 진행 상황")
    pdf.ln(2)

    statuses = [
        ("DONE 완료", "씬 1 참고 이미지 — scene01_ref.png 생성 완료"),
        ("DONE 완료", "씬 1 영상 — scene01_futurecity.mp4 생성 완료 (BGM 포함)"),
        ("DONE 완료", "씬 2 참고 이미지 — scene02_ref.png 생성 완료"),
        ("PENDING", "씬 2 영상 — 토큰 리필 후 진행 예정"),
        ("DONE 완료", "씬 3 배경 이미지 — scene03_outro_bg.png 생성 완료"),
        ("PENDING", "내레이션 — nova / shimmer 테스트 중"),
    ]
    for icon, text in statuses:
        pdf.status_line(icon, text)
    pdf.ln(4)

    pdf.horizontal_rule()

    pdf.section_title("다음 세션 시작점")
    pdf.body_text("토큰 리필 확인 후 씬 2 영상 생성 명령어를 실행합니다.")
    pdf.code_block([
        'python codyssey_media.py video \\',
        '  "young Korean students gathered together around',
        '   advanced lab equipment and large holographic displays',
        '   showing wind turbine schematics and hydrogen energy data,',
        '   all focused on the same experiment, bright professional',
        '   energy research laboratory, cool blue and white lighting,',
        '   cinematic composition, ultra-realistic"  \\',
        '  --model veo-3.1 --duration 4 --resolution 720p \\',
        '  --image media/images/scene02_ref.png',
    ])

    pdf.body_text("완료 후 파일명 변경:")
    pdf.code_block([
        'Rename-Item "media\\videos\\video_YYYYMMDD_HHMMSS.mp4"',
        '            "media\\videos\\scene02_labstudents.mp4"',
    ])

    # ═══════════════════════════════════════════════════════
    # 3페이지 — 씬별 프롬프트
    # ═══════════════════════════════════════════════════════
    pdf.add_page()

    pdf.section_title("씬별 확정 프롬프트")

    # ── 씬 1 ──
    pdf.section_title("씬 1 — 미래 에너지 도시 (0~4초)", level=2)
    pdf.scene_table([
        ("내레이션", "미래 에너지가 세상을 바꾸고 있습니다."),
        ("이미지 프롬프트",
         "futuristic smart coastal city in the foreground with 5 offshore wind turbines neatly aligned in the background, glowing blue energy lines, cinematic aerial drone view, golden hour sunrise lighting, ultra-realistic, clean composition"),
        ("영상 프롬프트", "이미지 프롬프트와 동일"),
        ("참고 이미지", "media/images/scene01_ref.png"),
        ("결과 파일", "media/videos/scene01_futurecity.mp4"),
    ])

    # ── 씬 2 ──
    pdf.section_title("씬 2 — 연구실 학생들 (4~8초)", level=2)
    pdf.scene_table([
        ("내레이션", "당신의 손으로 직접 설계하세요."),
        ("이미지 프롬프트",
         "young Korean students gathered together around advanced lab equipment and large holographic displays showing wind turbine schematics and hydrogen energy data, all focused on the same experiment, bright professional energy research laboratory, cool blue and white lighting, cinematic composition, ultra-realistic"),
        ("영상 프롬프트", "이미지 프롬프트와 동일"),
        ("참고 이미지", "media/images/scene02_ref.png"),
        ("결과 파일", "media/videos/scene02_labstudents.mp4 ← 생성 예정"),
    ])

    # ── 씬 3 ──
    pdf.section_title("씬 3 — 브랜드 타이틀 아웃트로 (8~12초)", level=2)
    pdf.scene_table([
        ("내레이션", "제주-경남 협력형 에너지인력양성센터."),
        ("이미지 프롬프트",
         "bright futuristic smart city powered by clean energy, solar panels on buildings, 5 offshore wind turbines in the distance, glowing blue energy lines flowing through the city, golden sunlight, cinematic aerial drone view, hopeful and vibrant atmosphere, ultra-realistic, no text"),
        ("결과 파일", "media/images/scene03_outro_bg.png"),
    ])

    # ═══════════════════════════════════════════════════════
    # 4페이지 — 내레이션 명령어
    # ═══════════════════════════════════════════════════════
    pdf.add_page()

    pdf.section_title("내레이션 명령어")
    pdf.body_text("nova / shimmer 두 버전을 생성 후 청취 비교하여 최종 선택합니다.")
    pdf.ln(2)

    pdf.section_title("Nova 음성", level=2)
    pdf.code_block([
        '# 씬 1',
        'python codyssey_media.py audio "미래 에너지가 세상을 바꾸고 있습니다."',
        '  --model gpt-4o-mini-tts --voice nova',
        '  --output "media/audio/scene01_narration_nova.mp3"',
    ])
    pdf.code_block([
        '# 씬 2',
        'python codyssey_media.py audio "당신의 손으로 직접 설계하세요."',
        '  --model gpt-4o-mini-tts --voice nova',
        '  --output "media/audio/scene02_narration_nova.mp3"',
    ])
    pdf.code_block([
        '# 씬 3',
        'python codyssey_media.py audio "제주-경남 협력형 에너지인력양성센터."',
        '  --model gpt-4o-mini-tts --voice nova',
        '  --output "media/audio/scene03_narration_nova.mp3"',
    ])

    pdf.section_title("Shimmer 음성", level=2)
    pdf.code_block([
        '# 씬 1',
        'python codyssey_media.py audio "미래 에너지가 세상을 바꾸고 있습니다."',
        '  --model gpt-4o-mini-tts --voice shimmer',
        '  --output "media/audio/scene01_narration_shimmer.mp3"',
    ])
    pdf.code_block([
        '# 씬 2',
        'python codyssey_media.py audio "당신의 손으로 직접 설계하세요."',
        '  --model gpt-4o-mini-tts --voice shimmer',
        '  --output "media/audio/scene02_narration_shimmer.mp3"',
    ])
    pdf.code_block([
        '# 씬 3',
        'python codyssey_media.py audio "제주-경남 협력형 에너지인력양성센터."',
        '  --model gpt-4o-mini-tts --voice shimmer',
        '  --output "media/audio/scene03_narration_shimmer.mp3"',
    ])

    # ═══════════════════════════════════════════════════════
    # 5페이지 — 체크리스트 + 파일 목록 + 최종 스펙
    # ═══════════════════════════════════════════════════════
    pdf.add_page()

    pdf.section_title("남은 작업 체크리스트")
    pdf.ln(2)
    checklist = [
        ("PENDING", "씬 2 영상 생성 (토큰 리필 후)"),
        ("PENDING", "nova / shimmer 청취 후 최종 음성 선택"),
        ("PENDING", "선택한 음성으로 파일명 확정 (scene0X_narration.mp3)"),
        ("PENDING", "최종 영상 편집 및 내보내기"),
    ]
    for icon, text in checklist:
        pdf.status_line(icon, text)
    pdf.ln(6)

    pdf.horizontal_rule()

    pdf.section_title("최종 파일 목록")
    pdf.ln(2)

    file_tree = [
        "media/",
        "+-- images/",
        "|   +-- scene01_ref.png              [완료]",
        "|   +-- scene02_ref.png              [완료]",
        "|   +-- scene03_outro_bg.png         [완료]",
        "+-- videos/",
        "|   +-- scene01_futurecity.mp4       [완료]",
        "|   +-- scene02_labstudents.mp4      [대기]",
        "+-- audio/",
        "    +-- scene01_narration_nova.mp3    [대기]",
        "    +-- scene01_narration_shimmer.mp3 [대기]",
        "    +-- scene02_narration_nova.mp3    [대기]",
        "    +-- scene02_narration_shimmer.mp3 [대기]",
        "    +-- scene03_narration_nova.mp3    [대기]",
        "    +-- scene03_narration_shimmer.mp3 [대기]",
    ]
    pdf.code_block(file_tree)

    pdf.horizontal_rule()

    pdf.section_title("영상 최종 스펙")
    pdf.ln(2)

    y_box = pdf.get_y()
    pdf.set_fill_color(*COLOR_LIGHT_BG)
    pdf.rect(10, y_box, 190, 38, 'F')
    pdf.set_draw_color(*COLOR_ACCENT)
    pdf.rect(10, y_box, 190, 38, 'D')
    pdf.ln(4)
    pdf.set_x(15)
    pdf.info_card("파일명", "energy_center_promo.mp4")
    pdf.set_x(15)
    pdf.info_card("길이", "12초 (씬당 4초 × 3씬)")
    pdf.set_x(15)
    pdf.info_card("해상도", "1280×720 (720p)")
    pdf.set_x(15)
    pdf.info_card("프레임레이트", "30fps")

    # ── 출력 ──
    pdf.output(output_path)
    print(f"PDF 생성 완료: {output_path}")


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__),
                       "02scenario_v2.pdf")
    build_pdf(out)
