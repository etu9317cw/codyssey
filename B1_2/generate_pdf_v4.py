# -*- coding: utf-8 -*-
"""
시나리오 v4 마크다운 → PDF 변환 스크립트
fpdf2 + 맑은 고딕 폰트 / 씬 이미지 + font.jpg + VEGAS15.jpg 포함
"""

import os
from fpdf import FPDF

# ── 경로 ───────────────────────────────────────────────────
FONT_DIR     = r"C:\Windows\Fonts"
FONT_REGULAR = os.path.join(FONT_DIR, "malgun.ttf")
FONT_BOLD    = os.path.join(FONT_DIR, "malgunbd.ttf")

IMG_SCENE1   = r"C:\co\codyssey_media_setup\media\images\scene01_ref.png"
IMG_SCENE2   = r"C:\co\codyssey_media_setup\media\images\scene02_ref.png"
IMG_SCENE3   = r"C:\co\codyssey_media_setup\media\images\scene03_outro_bg.png"
IMG_FONT     = r"C:\co\Sub_B1_2\codyssey_media\images2\font.jpg"
IMG_VEGAS    = r"C:\co\Sub_B1_2\codyssey_media\images2\VEGAS15.jpg"

# ── 이미지 배치 ────────────────────────────────────────────
IMG_MIN_H      = 60    # 남은 공간이 이보다 작으면 다음 페이지로
IMG_BOTTOM_GAP = 3     # 하단 여백(20mm) 위로 추가로 비워 둘 공간 (mm)

# ── 색상 ───────────────────────────────────────────────────
COLOR_PRIMARY   = (25, 60, 120)
COLOR_SECONDARY = (40, 95, 160)
COLOR_ACCENT    = (0, 120, 200)
COLOR_TEXT      = (40, 40, 40)
COLOR_LIGHT_BG  = (235, 242, 250)
COLOR_CODE_BG   = (245, 245, 245)
COLOR_WHITE     = (255, 255, 255)
COLOR_BORDER    = (180, 200, 220)
COLOR_TH_BG     = (30, 70, 130)
COLOR_DONE      = (34, 139, 34)
COLOR_PENDING   = (200, 130, 0)
COLOR_GRAY      = (120, 120, 120)
COLOR_BONUS     = (15, 90, 60)
COLOR_BONUS_BG  = (220, 242, 232)


class ScenarioPDF(FPDF):
    def __init__(self):
        super().__init__(orientation='P', unit='mm', format='A4')
        self.set_auto_page_break(auto=True, margin=20)
        self.add_font("MG", "",  FONT_REGULAR)
        self.add_font("MG", "B", FONT_BOLD)

    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("MG", "B", 8)
        self.set_text_color(*COLOR_GRAY)
        self.cell(0, 6, "제주-경남 협력형 에너지인력양성센터  |  홍보 영상 시나리오 v4", 0, 1, "L")
        self.set_draw_color(*COLOR_ACCENT)
        self.set_line_width(0.4)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)

    def footer(self):
        if self.page_no() == 1:
            return
        self.set_y(-15)
        self.set_font("MG", "", 8)
        self.set_text_color(*COLOR_GRAY)
        self.cell(0, 10, f"— {self.page_no()} —", 0, 0, "C")

    # ── 유틸 ──────────────────────────────────────────────
    def section_title(self, text, level=1):
        if level == 1:
            self.set_font("MG", "B", 16)
            self.set_text_color(*COLOR_PRIMARY)
            self.ln(4)
            y = self.get_y()
            self.set_fill_color(*COLOR_ACCENT)
            self.rect(10, y, 3, 9, 'F')
            self.set_x(16)
            self.cell(0, 10, text, 0, 1)
            self.ln(2)
        elif level == 2:
            self.set_font("MG", "B", 13)
            self.set_text_color(*COLOR_SECONDARY)
            self.ln(2)
            self.cell(0, 8, text, 0, 1)
            self.ln(1)
        elif level == 3:
            self.set_font("MG", "B", 11)
            self.set_text_color(*COLOR_ACCENT)
            self.ln(1)
            self.cell(0, 7, text, 0, 1)
            self.ln(0.5)

    def bonus_title(self, text):
        self.set_font("MG", "B", 16)
        self.set_text_color(*COLOR_BONUS)
        self.ln(4)
        y = self.get_y()
        self.set_fill_color(*COLOR_BONUS)
        self.rect(10, y, 3, 9, 'F')
        self.set_x(16)
        self.cell(0, 10, text, 0, 1)
        self.ln(2)

    def body_text(self, text, bold=False):
        style = "B" if bold else ""
        self.set_font("MG", style, 10)
        self.set_text_color(*COLOR_TEXT)
        self.multi_cell(0, 6, text)
        self.ln(1)

    def code_block(self, lines):
        self.set_font("MG", "", 8.5)
        self.set_text_color(50, 50, 50)
        x = self.get_x()
        w = 190
        total_h = 6
        line_heights = []
        for line in lines:
            nb = self.multi_cell(w - 8, 5, line, dry_run=True, output="LINES")
            h = len(nb) * 5
            line_heights.append(h)
            total_h += h
        if self.get_y() + total_h + 5 > self.h - self.b_margin:
            self.add_page()
        y_start = self.get_y()
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
        self.set_font("MG", "B", 10)
        self.set_text_color(*COLOR_SECONDARY)
        self.cell(38, 6, label, 0, 0)
        self.set_font("MG", "", 10)
        self.set_text_color(*COLOR_TEXT)
        self.multi_cell(0, 6, value)
        self.ln(0.5)

    def status_line(self, done, text):
        y = self.get_y()
        x = self.get_x()
        cx, cy = x + 4, y + 3
        if done:
            self.set_fill_color(*COLOR_DONE)
            self.set_draw_color(*COLOR_DONE)
        else:
            self.set_fill_color(*COLOR_PENDING)
            self.set_draw_color(*COLOR_PENDING)
        self.ellipse(cx - 2.5, cy - 2.5, 5, 5, 'F')
        self.set_font("MG", "B", 7)
        self.set_text_color(*COLOR_WHITE)
        self.set_xy(cx - 2.5, cy - 2)
        self.cell(5, 4, "V" if done else "...", 0, 0, "C")
        self.set_xy(x + 10, y)
        self.set_text_color(*COLOR_TEXT)
        self.set_font("MG", "", 9.5)
        self.cell(0, 6, text, 0, 1)

    def scene_table(self, rows):
        col_w = [32, 153]
        row_h = 7
        self.set_fill_color(*COLOR_TH_BG)
        self.set_text_color(*COLOR_WHITE)
        self.set_font("MG", "B", 9)
        self.cell(col_w[0], row_h, "항목", 1, 0, "C", True)
        self.cell(col_w[1], row_h, "내용", 1, 1, "C", True)
        self.set_text_color(*COLOR_TEXT)
        self.set_font("MG", "", 9)
        fill = False
        for label, value in rows:
            nb_lines = self.multi_cell(col_w[1], row_h, value, dry_run=True, output="LINES")
            cell_h = max(len(nb_lines), 1) * row_h
            if self.get_y() + cell_h > self.h - self.b_margin:
                self.add_page()
            y_b = self.get_y()
            xs  = self.get_x()
            if fill:
                self.set_fill_color(*COLOR_LIGHT_BG)
            else:
                self.set_fill_color(*COLOR_WHITE)
            self.set_font("MG", "B", 9)
            self.set_draw_color(*COLOR_BORDER)
            self.rect(xs, y_b, col_w[0], cell_h, 'D')
            self.set_xy(xs + 1, y_b + (cell_h - row_h) / 2)
            self.cell(col_w[0] - 2, row_h, label, 0, 0, "C", fill)
            self.set_font("MG", "", 8.5)
            self.rect(xs + col_w[0], y_b, col_w[1], cell_h, 'D')
            if fill:
                self.rect(xs + col_w[0] + 0.3, y_b + 0.3, col_w[1] - 0.6, cell_h - 0.6, 'F')
            self.set_xy(xs + col_w[0] + 2, y_b + 1)
            self.multi_cell(col_w[1] - 4, row_h, value)
            self.set_y(y_b + cell_h)
            fill = not fill
        self.ln(4)

    def flow_table(self, rows):
        """작업 흐름 테이블 (4열)"""
        col_w = [10, 45, 70, 35, 30]
        row_h = 7
        headers = ["순서", "도구", "할 일", "결과물", "상태"]
        self.set_fill_color(*COLOR_TH_BG)
        self.set_text_color(*COLOR_WHITE)
        self.set_font("MG", "B", 8)
        for i, h in enumerate(headers):
            self.cell(col_w[i], row_h, h, 1, 0, "C", True)
        self.ln()
        self.set_text_color(*COLOR_TEXT)
        fill = False
        for row in rows:
            cell_h = row_h
            if fill:
                self.set_fill_color(*COLOR_LIGHT_BG)
            else:
                self.set_fill_color(*COLOR_WHITE)
            self.set_font("MG", "", 8)
            for i, val in enumerate(row):
                self.cell(col_w[i], cell_h, val, 1, 0, "C", fill)
            self.ln()
            fill = not fill
        self.ln(4)

    def image_block(self, path, caption="", w=170):
        """이미지 삽입 (캡션 포함)"""
        if not os.path.exists(path):
            return
        import PIL.Image as PILImage
        try:
            img = PILImage.open(path)
            iw, ih = img.size
            ratio = ih / iw
        except Exception:
            ratio = 0.6
        # 페이지 남은 공간을 채우되 하단 여백 위로 IMG_BOTTOM_GAP 만큼 비워 둠
        caption_h = 7 if caption else 2
        max_h = w * ratio
        avail = self.h - self.b_margin - IMG_BOTTOM_GAP - caption_h - self.get_y()
        if avail < IMG_MIN_H:
            self.add_page()
            avail = self.h - self.b_margin - IMG_BOTTOM_GAP - caption_h - self.get_y()
        img_h_mm = min(max_h, avail)
        w = img_h_mm / ratio
        x = (210 - w) / 2
        self.image(path, x=x, y=self.get_y(), w=w, h=img_h_mm)
        self.set_y(self.get_y() + img_h_mm + 2)
        if caption:
            self.set_font("MG", "", 8)
            self.set_text_color(*COLOR_GRAY)
            self.cell(0, 5, caption, 0, 1, "C")
        # 이미지 뒤에 오는 제목은 다음 페이지에서 시작
        self.add_page()

    def two_images(self, path1, cap1, path2, cap2):
        """두 이미지 위아래 배치 (남은 페이지를 나눠 채움)"""
        import PIL.Image as PILImage
        def img_ratio(path):
            try:
                img = PILImage.open(path)
                iw, ih = img.size
                return ih / iw
            except Exception:
                return 0.6

        max_w = 170
        caption_h = 12   # 이미지 아래 간격 2mm + 캡션 2줄 10mm
        spacing = 4      # 두 이미지 사이 간격
        items = [(path1, cap1, img_ratio(path1)), (path2, cap2, img_ratio(path2))]

        # 페이지 남은 공간을 채우되 하단 여백 위로 IMG_BOTTOM_GAP 만큼 비워 둠
        def avail_each():
            total = self.h - self.b_margin - IMG_BOTTOM_GAP - self.get_y()
            return (total - 2 * caption_h - spacing) / 2
        if avail_each() < IMG_MIN_H * 1.5:
            self.add_page()
        each_h = avail_each()

        for i, (path, cap, ratio) in enumerate(items):
            h = min(each_h, max_w * ratio)
            w = h / ratio
            y = self.get_y()
            if os.path.exists(path):
                self.image(path, x=(210 - w) / 2, y=y, w=w, h=h)
            self.set_y(y + h + 2)
            self.set_font("MG", "", 8)
            self.set_text_color(*COLOR_GRAY)
            self.multi_cell(0, 5, cap, 0, "C")
            if i == 0:
                self.ln(spacing)
        self.ln(3)

    def prompt_history_table(self, rows):
        """프롬프트 수정 기록 테이블 (버전 / 프롬프트 / 변경 사유)"""
        col_w = [18, 95, 77]
        row_h = 6
        self.set_fill_color(*COLOR_TH_BG)
        self.set_text_color(*COLOR_WHITE)
        self.set_font("MG", "B", 8.5)
        for h, w in zip(["버전", "프롬프트 (영문)", "변경 사유"], col_w):
            self.cell(w, row_h, h, 1, 0, "C", True)
        self.ln()
        fill = False
        for ver, prompt, reason in rows:
            # 각 셀 줄 수 계산 → 최대 높이 사용
            nb_p = self.multi_cell(col_w[1] - 4, row_h, prompt, dry_run=True, output="LINES")
            nb_r = self.multi_cell(col_w[2] - 4, row_h, reason, dry_run=True, output="LINES")
            cell_h = max(len(nb_p), len(nb_r), 1) * row_h

            if self.get_y() + cell_h > self.h - self.b_margin:
                self.add_page()

            if fill:
                self.set_fill_color(*COLOR_LIGHT_BG)
            else:
                self.set_fill_color(*COLOR_WHITE)

            y_b = self.get_y()
            xs  = self.get_x()

            # 버전 셀
            self.set_font("MG", "B", 8.5)
            self.set_text_color(*COLOR_TEXT)
            self.set_draw_color(*COLOR_BORDER)
            self.rect(xs, y_b, col_w[0], cell_h, 'D')
            if fill:
                self.set_fill_color(*COLOR_LIGHT_BG)
                self.rect(xs + 0.3, y_b + 0.3, col_w[0] - 0.6, cell_h - 0.6, 'F')
            self.set_xy(xs + 1, y_b + (cell_h - row_h) / 2)
            self.cell(col_w[0] - 2, row_h, ver, 0, 0, "C")

            # 프롬프트 셀
            self.set_font("MG", "", 8)
            self.rect(xs + col_w[0], y_b, col_w[1], cell_h, 'D')
            if fill:
                self.rect(xs + col_w[0] + 0.3, y_b + 0.3, col_w[1] - 0.6, cell_h - 0.6, 'F')
            self.set_xy(xs + col_w[0] + 2, y_b + 1)
            self.multi_cell(col_w[1] - 4, row_h, prompt)

            # 변경 사유 셀
            self.rect(xs + col_w[0] + col_w[1], y_b, col_w[2], cell_h, 'D')
            if fill:
                self.rect(xs + col_w[0] + col_w[1] + 0.3, y_b + 0.3, col_w[2] - 0.6, cell_h - 0.6, 'F')
            self.set_xy(xs + col_w[0] + col_w[1] + 2, y_b + 1)
            self.multi_cell(col_w[2] - 4, row_h, reason)

            self.set_y(y_b + cell_h)
            fill = not fill
        self.ln(4)

    def horizontal_rule(self):
        self.set_draw_color(*COLOR_BORDER)
        self.set_line_width(0.3)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)

    def version_table(self, rows):
        col_w = [18, 172]
        row_h = 7
        self.set_fill_color(*COLOR_TH_BG)
        self.set_text_color(*COLOR_WHITE)
        self.set_font("MG", "B", 9)
        self.cell(col_w[0], row_h, "버전", 1, 0, "C", True)
        self.cell(col_w[1], row_h, "주요 변경 내용", 1, 1, "C", True)
        self.set_text_color(*COLOR_TEXT)
        fill = False
        for ver, desc in rows:
            if fill:
                self.set_fill_color(*COLOR_LIGHT_BG)
            else:
                self.set_fill_color(*COLOR_WHITE)
            self.set_font("MG", "B", 9)
            self.cell(col_w[0], row_h, ver, 1, 0, "C", fill)
            self.set_font("MG", "", 9)
            self.cell(col_w[1], row_h, desc, 1, 1, "L", fill)
            fill = not fill
        self.ln(4)


# ══════════════════════════════════════════════════════════════
def build_pdf(output_path):
    pdf = ScenarioPDF()

    # ─────────────────────────────────────────────────────────
    # 1페이지 — 표지
    # ─────────────────────────────────────────────────────────
    pdf.add_page()
    pdf.set_fill_color(*COLOR_PRIMARY)
    pdf.rect(0, 0, 210, 8, 'F')
    pdf.set_fill_color(*COLOR_ACCENT)
    pdf.rect(0, 8, 210, 3, 'F')

    pdf.ln(50)
    pdf.set_font("MG", "B", 28)
    pdf.set_text_color(*COLOR_PRIMARY)
    pdf.cell(0, 15, "홍보 영상 시나리오", 0, 1, "C")

    pdf.set_font("MG", "", 12)
    pdf.set_text_color(*COLOR_GRAY)
    pdf.cell(0, 8, "Version 4.0  |  최종본", 0, 1, "C")
    pdf.ln(10)

    pdf.set_draw_color(*COLOR_ACCENT)
    pdf.set_line_width(0.5)
    pdf.line(60, pdf.get_y(), 150, pdf.get_y())
    pdf.ln(12)

    pdf.set_font("MG", "B", 16)
    pdf.set_text_color(*COLOR_SECONDARY)
    pdf.cell(0, 10, "제주-경남 협력형", 0, 1, "C")
    pdf.cell(0, 10, "에너지인력양성센터", 0, 1, "C")
    pdf.ln(8)

    # 핵심 메시지 박스
    pdf.set_fill_color(*COLOR_LIGHT_BG)
    pdf.set_draw_color(*COLOR_ACCENT)
    pdf.rect(45, pdf.get_y(), 120, 14, 'DF')
    pdf.set_font("MG", "B", 12)
    pdf.set_text_color(*COLOR_ACCENT)
    pdf.cell(0, 14, '"에너지 산업의 미래를 내가 이끈다."', 0, 1, "C")
    pdf.ln(18)

    pdf.set_font("MG", "", 10)
    pdf.set_text_color(*COLOR_GRAY)
    pdf.cell(0, 7, "작성일: 2026년 8월 30일  |  영상 길이: 12초 (씬당 4초 × 3씬)", 0, 1, "C")
    pdf.cell(0, 7, "해상도: 1280×720 (720p)  |  편집 도구: Vegas 15 Pro", 0, 1, "C")
    pdf.cell(0, 7, "영상 생성: veo-3.1  |  내레이션: gpt-4o-mini-tts", 0, 1, "C")

    pdf.set_fill_color(*COLOR_ACCENT)
    pdf.rect(0, 287, 210, 3, 'F')
    pdf.set_fill_color(*COLOR_PRIMARY)
    pdf.rect(0, 290, 210, 8, 'F')

    # ─────────────────────────────────────────────────────────
    # 2페이지 — 버전 히스토리 + 브랜드 아이덴티티 + 진행 상황
    # ─────────────────────────────────────────────────────────
    pdf.add_page()

    pdf.section_title("버전 히스토리")
    pdf.version_table([
        ("v1", "최초 시나리오 작성 — 씬 1~3 스토리보드, 프롬프트 초안"),
        ("v2", "USP 추가, 씬별 프롬프트 수정 기록 추가, 도구 선택 이유 명시, 단계별 실행 가이드 추가"),
        ("v3", "프롬프트 v2 확정본 반영, 진행 상황 추적 추가, 다음 세션 시작점 명시, 내레이션 비교 방식 정립"),
        ("v4", "전 씬 제작 완료 반영, 편집 도구 Vegas 15 Pro 확정, 씬 3 자막 Python 스크립트 추가, 보너스 2 완료"),
    ])

    pdf.horizontal_rule()

    pdf.section_title("브랜드 아이덴티티")
    y_box = pdf.get_y()
    pdf.set_fill_color(*COLOR_LIGHT_BG)
    pdf.rect(10, y_box, 190, 56, 'F')
    pdf.set_draw_color(*COLOR_ACCENT)
    pdf.rect(10, y_box, 190, 56, 'D')
    pdf.ln(4)
    pdf.set_x(15)
    pdf.info_card("브랜드명", "제주-경남 협력형 에너지인력양성센터")
    pdf.set_x(15)
    pdf.info_card("타겟", "에너지 분야 취업을 희망하는 청년 / 취준생")
    pdf.set_x(15)
    pdf.info_card("톤앤매너", "미래지향적·역동적, 클린에너지, 첨단기술, 모던 블루 계열")
    pdf.set_x(15)
    pdf.info_card("USP", "제주(풍력·수소)와 경남(제조·연구)의 지역 협력으로 만든 실전형 에너지 인재 육성")
    pdf.set_x(15)
    pdf.info_card("핵심 메시지", '"에너지 산업의 미래를 내가 이끈다."')
    pdf.set_x(15)
    pdf.info_card("광고 목적", "인지 — 센터의 존재와 비전을 청년층에게 각인")
    pdf.set_y(y_box + 59)

    pdf.ln(3)
    pdf.horizontal_rule()

    pdf.section_title("전체 진행 상황 (v4 — 완료)")
    pdf.ln(2)
    statuses = [
        (True,  "씬 1 참고 이미지 — scene01_ref.png 생성 완료"),
        (True,  "씬 1 영상 — scene01_futurecity.mp4 생성 완료 (BGM 포함)"),
        (True,  "씬 2 참고 이미지 — scene02_ref.png 생성 완료"),
        (True,  "씬 2 영상 — scene02_labstudents.mp4 생성 완료"),
        (True,  "씬 3 배경 이미지 — scene03_outro_bg.png 생성 완료"),
        (True,  "씬 3 영상 — scene03_outro.mp4 생성 완료 (veo-3.1)"),
        (True,  "씬 3 자막 합성 — Python 스크립트로 자막 합성 완료"),
        (True,  "내레이션 — nova / shimmer 비교 완료, 최종 선택 확정"),
        (True,  "최종 편집 — Vegas 15 Pro로 씬 1~3 + 내레이션 통합 완료"),
        (True,  "보너스 2 — sora-2로 씬 1~3 전체 재제작 완료"),
    ]
    for done, text in statuses:
        pdf.status_line(done, text)

    # ─────────────────────────────────────────────────────────
    # 3페이지 — 씬 1
    # ─────────────────────────────────────────────────────────
    pdf.add_page()
    pdf.section_title("씬별 스토리보드")
    pdf.section_title("씬 1 — 미래 에너지 도시 (0~4초)", level=2)

    pdf.scene_table([
        ("씬 / 길이",    "씬 1 / 4초"),
        ("목표 메시지",  "풍력과 수소가 가득한 미래 에너지 도시가 펼쳐진다"),
        ("화면 구성",    "부감 항공뷰 / 해상 풍력발전 단지 + 수소 에너지 시설 / 새벽빛 일출 조명 / 파란 에너지 라인 / 텍스트 없음"),
        ("내레이션",     "미래 에너지가 세상을 바꾸고 있습니다."),
        ("사용 도구",    "참고 이미지: gemini-2.5-flash-image / 영상: veo-3.1 / 내레이션: gpt-4o-mini-tts"),
        ("이미지 프롬프트", "futuristic smart coastal city in the foreground with 5 offshore wind turbines neatly aligned in the background, glowing blue energy lines, cinematic aerial drone view, golden hour sunrise lighting, ultra-realistic, clean composition"),
        ("영상 프롬프트", "이미지 프롬프트와 동일"),
        ("결과 파일",    "scene01_ref.png  /  scene01_futurecity.mp4  /  scene01_narration.mp3  [모두 완료]"),
    ])

    pdf.section_title("씬 1 참고 이미지", level=3)
    pdf.image_block(IMG_SCENE1, caption="scene01_ref.png  —  gemini-2.5-flash-image 생성 (씬 1 영상 생성 전 구도·색감 확인용)")

    pdf.section_title("씬 1 실행 명령어", level=3)
    pdf.code_block([
        "# ① 참고 이미지 생성",
        'python codyssey_media.py image \\',
        '  "futuristic smart coastal city in the foreground with 5 offshore wind turbines',
        '   neatly aligned in the background, glowing blue energy lines,',
        '   cinematic aerial drone view, golden hour sunrise lighting,',
        '   ultra-realistic, clean composition" \\',
        '  --model gemini-2.5-flash-image',
    ])
    pdf.code_block([
        "# ② 영상 생성 (참고 이미지 확인 후)",
        'python codyssey_media.py video \\',
        '  "futuristic smart coastal city in the foreground with 5 offshore wind turbines',
        '   neatly aligned in the background, glowing blue energy lines,',
        '   cinematic aerial drone view, golden hour sunrise lighting,',
        '   ultra-realistic, clean composition" \\',
        '  --model veo-3.1 --duration 4 --resolution 720p \\',
        '  --image media/images/scene01_ref.png',
    ])

    pdf.section_title("씬 1 프롬프트 수정 기록", level=3)
    pdf.prompt_history_table([
        ("초안",
         "futuristic city with wind turbines",
         "도시와 풍력이 어색하게 분리됨. 일반적인 SF 도시 느낌으로 에너지 연결감 없음"),
        ("v1 수정",
         "futuristic smart coastal city with massive offshore wind turbines and hydrogen energy infrastructure, glowing blue energy lines, cinematic aerial drone view, golden hour sunrise lighting, ultra-realistic",
         "coastal 추가(제주 해안 느낌) / hydrogen energy infrastructure·glowing blue energy lines 추가(수소·에너지 시각화) / golden hour sunrise(희망적 분위기)"),
        ("v2 확정",
         "futuristic smart coastal city in the foreground with 5 offshore wind turbines neatly aligned in the background, glowing blue energy lines, cinematic aerial drone view, golden hour sunrise lighting, ultra-realistic, clean composition",
         "in the foreground / 5 offshore wind turbines neatly aligned in the background — 전경·후경 구도 명확화 / clean composition 추가"),
    ])

    # ─────────────────────────────────────────────────────────
    # 4페이지 — 씬 2
    # ─────────────────────────────────────────────────────────
    pdf.add_page()
    pdf.section_title("씬 2 — 연구실에서 연구하는 학생들 (4~8초)", level=2)

    pdf.scene_table([
        ("씬 / 길이",    "씬 2 / 4초"),
        ("목표 메시지",  "나 역시 이곳에서 미래 에너지를 연구할 수 있다"),
        ("화면 구성",    "수평 미디엄샷 / 첨단 에너지 연구실 / 청년 학생 2~3명이 홀로그래픽 디스플레이·실험장비 앞에서 협력 연구 / 파란·흰 조명"),
        ("내레이션",     "당신의 손으로 직접 설계하세요."),
        ("사용 도구",    "참고 이미지: gemini-2.5-flash-image / 영상: veo-3.1 / 내레이션: gpt-4o-mini-tts"),
        ("이미지 프롬프트", "young Korean students gathered together around advanced lab equipment and large holographic displays showing wind turbine schematics and hydrogen energy data, all focused on the same experiment, bright professional energy research laboratory, cool blue and white lighting, cinematic composition, ultra-realistic"),
        ("영상 프롬프트", "이미지 프롬프트와 동일"),
        ("결과 파일",    "scene02_ref.png  /  scene02_labstudents.mp4  /  scene02_narration.mp3  [모두 완료]"),
    ])

    pdf.section_title("씬 2 참고 이미지", level=3)
    pdf.image_block(IMG_SCENE2, caption="scene02_ref.png  —  gemini-2.5-flash-image 생성 (씬 2 영상 생성 전 구도·색감 확인용)")

    pdf.section_title("씬 2 실행 명령어", level=3)
    pdf.code_block([
        "# ① 참고 이미지 생성",
        'python codyssey_media.py image \\',
        '  "young Korean students gathered together around advanced lab equipment',
        '   and large holographic displays showing wind turbine schematics',
        '   and hydrogen energy data, all focused on the same experiment,',
        '   bright professional energy research laboratory,',
        '   cool blue and white lighting, cinematic composition, ultra-realistic" \\',
        '  --model gemini-2.5-flash-image',
    ])
    pdf.code_block([
        "# ② 영상 생성",
        'python codyssey_media.py video \\',
        '  "young Korean students gathered together around advanced lab equipment',
        '   and large holographic displays showing wind turbine schematics',
        '   and hydrogen energy data, all focused on the same experiment,',
        '   bright professional energy research laboratory,',
        '   cool blue and white lighting, cinematic composition, ultra-realistic" \\',
        '  --model veo-3.1 --duration 4 --resolution 720p \\',
        '  --image media/images/scene02_ref.png',
    ])

    pdf.section_title("씬 2 프롬프트 수정 기록", level=3)
    pdf.prompt_history_table([
        ("초안",
         "students working in a laboratory, scientific equipment",
         "일반 화학·생물 실험실처럼 보여 에너지 연구 느낌 없음. 얼굴 클로즈업으로 AI 특유의 부자연스러운 왜곡 발생"),
        ("v1 수정",
         "young Asian students researching in a futuristic advanced energy laboratory, holographic displays showing wind turbine schematics and hydrogen molecules, modern scientific equipment, teamwork atmosphere, cool blue and white lighting, cinematic composition, ultra-realistic",
         "energy laboratory로 분야 특정 / holographic displays 추가(에너지 연구 시각화) / teamwork atmosphere(협력 분위기 강조)"),
        ("v2 확정",
         "young Korean students gathered together around advanced lab equipment and large holographic displays showing wind turbine schematics and hydrogen energy data, all focused on the same experiment, bright professional energy research laboratory, cool blue and white lighting, cinematic composition, ultra-realistic",
         "gathered together around / all focused on the same experiment — 하나의 실험에 집중하는 구도 명확화 / bright professional — 밝고 전문적인 연구실 분위기 강조"),
    ])

    # ─────────────────────────────────────────────────────────
    # 5페이지 — 씬 3
    # ─────────────────────────────────────────────────────────
    pdf.add_page()
    pdf.section_title("씬 3 — 브랜드 타이틀 아웃트로 (8~12초)", level=2)

    pdf.scene_table([
        ("씬 / 길이",    "씬 3 / 4초"),
        ("목표 메시지",  "제주-경남 협력형 에너지인력양성센터가 당신을 기다립니다"),
        ("화면 구성",    "밝은 미래 에너지 도시 영상 / 화면 하단부에 센터명 텍스트 페이드인"),
        ("화면 텍스트",  "제주-경남 협력형 에너지인력양성센터"),
        ("내레이션",     "제주-경남 협력형 에너지인력양성센터."),
        ("사용 도구",    "배경 이미지: gemini-2.5-flash-image / 영상: veo-3.1 / 자막: Python 스크립트 / 내레이션: gpt-4o-mini-tts"),
        ("이미지 프롬프트", "bright futuristic smart city powered by clean energy, solar panels on buildings, 5 offshore wind turbines in the distance, glowing blue energy lines flowing through the city, golden sunlight, cinematic aerial drone view, hopeful and vibrant atmosphere, ultra-realistic, no text"),
        ("결과 파일",    "scene03_outro_bg.png  /  scene03_outro.mp4 (자막 합성 완료)  /  scene03_narration.mp3  [모두 완료]"),
    ])

    pdf.section_title("씬 3 참고 이미지", level=3)
    pdf.image_block(IMG_SCENE3, caption="scene03_outro_bg.png  —  gemini-2.5-flash-image 생성 (씬 3 영상 생성 전 배경 확인용)")

    pdf.section_title("씬 3 영상 생성 명령어", level=3)
    pdf.code_block([
        "# ① 배경 이미지 생성",
        'python codyssey_media.py image \\',
        '  "bright futuristic smart city powered by clean energy,',
        '   solar panels on buildings, 5 offshore wind turbines in the distance,',
        '   glowing blue energy lines flowing through the city,',
        '   golden sunlight, cinematic aerial drone view,',
        '   hopeful and vibrant atmosphere, ultra-realistic, no text" \\',
        '  --model gemini-2.5-flash-image',
    ])
    pdf.code_block([
        "# ② 영상 생성",
        'python codyssey_media.py video \\',
        '  "bright futuristic smart city powered by clean energy, ...(동일 프롬프트)" \\',
        '  --model veo-3.1 --duration 4 --resolution 720p \\',
        '  --image media/images/scene03_outro_bg.png',
    ])

    pdf.section_title("씬 3 프롬프트 수정 기록", level=3)
    pdf.prompt_history_table([
        ("v1 원안",
         "abstract futuristic energy background, flowing blue particle waves, glowing light streams, deep space dark blue background, clean minimal composition, no text, ultra-realistic",
         "추상적·어두운 배경 — 브랜드 타이틀 텍스트 오버레이용으로 계획했으나 영상 톤이 무거움"),
        ("v2 확정",
         "bright futuristic smart city powered by clean energy, solar panels on buildings, 5 offshore wind turbines in the distance, glowing blue energy lines flowing through the city, golden sunlight, cinematic aerial drone view, hopeful and vibrant atmosphere, ultra-realistic, no text",
         "추상 배경 → 밝은 미래 에너지 도시로 변경 / 씬 1과 시각적 연결감 확보 / solar panels·wind turbines — 클린에너지 요소 직접 표현 / hopeful and vibrant atmosphere — 희망적 분위기 강조"),
    ])

    # ─────────────────────────────────────────────────────────
    # 6페이지 — 씬 3 자막 합성 + font.jpg + Vegas15.jpg
    # ─────────────────────────────────────────────────────────
    pdf.add_page()
    pdf.section_title("씬 3 자막 합성 — Python 스크립트", level=2)

    pdf.body_text(
        "veo-3.1로 생성한 씬 3 영상 위에 센터명 자막을 Python 스크립트(add_text_scene03.py)로 직접 합성했습니다. "
        "외부 편집 앱 없이 OpenCV + Pillow + FFmpeg으로 처리하여 재현 가능한 방식입니다."
    )

    pdf.scene_table([
        ("텍스트",   "제주-경남 협력형 에너지인력양성센터"),
        ("폰트",     "맑은 고딕 Bold (malgunbd.ttf) / 60pt"),
        ("색상",     "흰색 + 드롭 섀도 (4px 오프셋) + 반투명 검정 배경 박스"),
        ("위치",     "화면 7/8 지점 (하단부 중앙) — 수평 가운데 정렬"),
        ("효과",     "0~1초 선형 페이드인 (OpenCV 프레임별 알파 블렌딩)"),
        ("처리 도구", "Pillow (텍스트 PNG 생성) → OpenCV (프레임 합성) → FFmpeg (오디오 재결합)"),
        ("출력 파일", "media/videos/scene03_outro.mp4"),
    ])

    pdf.code_block([
        "# 자막 합성 실행",
        "python add_text_scene03.py",
        "",
        "# 핵심 파라미터",
        'TEXT      = "제주-경남 협력형 에너지인력양성센터"',
        'FONT_PATH = r"C:\\Windows\\Fonts\\malgunbd.ttf"',
        "FONT_SIZE = 60",
        "FADE_SEC  = 1.0   # 0~1초 페이드인",
        "y         = H * 7 // 8 - text_h // 2   # 화면 7/8 위치",
    ])

    pdf.section_title("씬 3 자막 적용 결과 및 Vegas 15 Pro 편집", level=3)
    pdf.ln(2)
    pdf.two_images(
        IMG_FONT,    "자막 합성 결과 (font.jpg)\n맑은 고딕 Bold + 드롭 섀도 + 반투명 배경",
        IMG_VEGAS,   "Vegas 15 Pro 최종 편집 (VEGAS15.jpg)\n씬 1~3 타임라인 + 내레이션 통합"
    )

    # ─────────────────────────────────────────────────────────
    # 7페이지 — 내레이션 + 도구 목록
    # ─────────────────────────────────────────────────────────
    pdf.add_page()
    pdf.section_title("내레이션 명령어")
    pdf.body_text("nova / shimmer 두 버전을 생성 후 청취 비교하여 최종 선택합니다.")
    pdf.ln(1)

    pdf.section_title("Nova 음성", level=2)
    pdf.code_block([
        '# 씬 1',
        'python codyssey_media.py audio "미래 에너지가 세상을 바꾸고 있습니다."',
        '  --model gpt-4o-mini-tts --voice nova --output "media/audio/scene01_narration_nova.mp3"',
        '# 씬 2',
        'python codyssey_media.py audio "당신의 손으로 직접 설계하세요."',
        '  --model gpt-4o-mini-tts --voice nova --output "media/audio/scene02_narration_nova.mp3"',
        '# 씬 3',
        'python codyssey_media.py audio "제주-경남 협력형 에너지인력양성센터."',
        '  --model gpt-4o-mini-tts --voice nova --output "media/audio/scene03_narration_nova.mp3"',
    ])

    pdf.section_title("Shimmer 음성", level=2)
    pdf.code_block([
        '# 씬 1',
        'python codyssey_media.py audio "미래 에너지가 세상을 바꾸고 있습니다."',
        '  --model gpt-4o-mini-tts --voice shimmer --output "media/audio/scene01_narration_shimmer.mp3"',
        '# 씬 2',
        'python codyssey_media.py audio "당신의 손으로 직접 설계하세요."',
        '  --model gpt-4o-mini-tts --voice shimmer --output "media/audio/scene02_narration_shimmer.mp3"',
        '# 씬 3',
        'python codyssey_media.py audio "제주-경남 협력형 에너지인력양성센터."',
        '  --model gpt-4o-mini-tts --voice shimmer --output "media/audio/scene03_narration_shimmer.mp3"',
    ])

    pdf.horizontal_rule()
    pdf.section_title("사용 도구 목록")
    pdf.scene_table([
        ("이미지 생성",     "gemini-2.5-flash-image  —  VS Code 터미널 codyssey_media.py image"),
        ("영상 생성",       "veo-3.1 (4초 / 720p)  —  VS Code 터미널 codyssey_media.py video"),
        ("내레이션 (TTS)",  "gpt-4o-mini-tts (nova / shimmer)  —  codyssey_media.py audio"),
        ("씬 3 자막 합성",  "Python 스크립트 (OpenCV + Pillow + FFmpeg)  —  add_text_scene03.py"),
        ("최종 영상 편집",  "Vegas 15 Pro  —  씬 1~3 클립 + 내레이션 통합 편집"),
    ])

    # ─────────────────────────────────────────────────────────
    # 8페이지 — 체크리스트 + 파일 목록 + 최종 스펙
    # ─────────────────────────────────────────────────────────
    pdf.add_page()
    pdf.section_title("작업 순서 체크리스트")
    pdf.ln(2)
    checklist = [
        (True, "사전 준비 — API 키 설정 및 디렉토리 이동"),
        (True, "STEP 1 — 씬 1 참고 이미지 생성 (gemini-2.5-flash-image)"),
        (True, "STEP 2 — 씬 1 영상 생성 (veo-3.1, 4초/720p)"),
        (True, "STEP 3 — 씬 2 참고 이미지 생성 (gemini-2.5-flash-image)"),
        (True, "STEP 4 — 씬 2 영상 생성 (veo-3.1, 4초/720p)"),
        (True, "STEP 5 — 씬 3 배경 이미지 생성 (gemini-2.5-flash-image)"),
        (True, "STEP 5-2 — 씬 3 영상 생성 (veo-3.1, 4초/720p)"),
        (True, "STEP 5-3 — 씬 3 자막 합성 (Python 스크립트)"),
        (True, "STEP 6 — 씬 1·2·3 내레이션 생성 (nova/shimmer 비교 후 선택)"),
        (True, "STEP 7 — Vegas 15 Pro로 최종 편집 및 MP4 내보내기"),
    ]
    for done, text in checklist:
        pdf.status_line(done, text)
    pdf.ln(4)

    pdf.horizontal_rule()
    pdf.section_title("최종 파일 목록")
    pdf.code_block([
        "media/",
        "+-- images/",
        "|   +-- scene01_ref.png                  [완료]",
        "|   +-- scene02_ref.png                  [완료]",
        "|   +-- scene03_outro_bg.png             [완료]",
        "|   +-- scene03_text_overlay.png         [완료] (자막 합성용 중간 산출물)",
        "+-- videos/",
        "|   +-- scene01_futurecity.mp4           [완료]",
        "|   +-- scene02_labstudents.mp4          [완료]",
        "|   +-- scene03_outro.mp4                [완료] (자막 합성 완료본)",
        "+-- audio/",
        "    +-- scene01_narration_nova.mp3        [완료]",
        "    +-- scene01_narration_shimmer.mp3     [완료]",
        "    +-- scene02_narration_nova.mp3        [완료]",
        "    +-- scene02_narration_shimmer.mp3     [완료]",
        "    +-- scene03_narration_nova.mp3        [완료]",
        "    +-- scene03_narration_shimmer.mp3     [완료]",
        "",
        "scripts/",
        "    +-- add_text_scene03.py              [완료] (씬 3 자막 합성 스크립트)",
        "",
        "output/",
        "    +-- energy_center_promo.mp4          [완료] (최종 완성본)",
    ])

    pdf.add_page()
    pdf.section_title("영상 최종 스펙")
    y_box = pdf.get_y()
    pdf.set_fill_color(*COLOR_LIGHT_BG)
    pdf.rect(10, y_box, 190, 46, 'F')
    pdf.set_draw_color(*COLOR_ACCENT)
    pdf.rect(10, y_box, 190, 46, 'D')
    pdf.ln(4)
    pdf.set_x(15); pdf.info_card("파일명",       "energy_center_promo.mp4")
    pdf.set_x(15); pdf.info_card("길이",         "12초 (씬당 4초 × 3씬)")
    pdf.set_x(15); pdf.info_card("해상도",       "1280×720 (720p) / 30fps")
    pdf.set_x(15); pdf.info_card("비디오 코덱",  "H.264")
    pdf.set_x(15); pdf.info_card("오디오 코덱",  "AAC")

    # ─────────────────────────────────────────────────────────
    # 9페이지 — 보너스 2
    # ─────────────────────────────────────────────────────────
    pdf.add_page()

    # 보너스 헤더 배경
    pdf.set_fill_color(*COLOR_BONUS)
    pdf.rect(0, 0, 210, 8, 'F')
    pdf.set_fill_color(100, 180, 140)
    pdf.rect(0, 8, 210, 3, 'F')
    pdf.ln(3)

    pdf.bonus_title("보너스 2 — 동일 스토리보드, 다른 도구로 재제작")

    # 개요 박스
    y_box = pdf.get_y()
    pdf.set_fill_color(*COLOR_BONUS_BG)
    pdf.set_draw_color(*COLOR_BONUS)
    pdf.rect(10, y_box, 190, 34, 'DF')
    pdf.ln(4)
    pdf.set_x(15); pdf.info_card("목적",  "동일한 씬 1~3 스토리보드를 다른 영상 생성 도구로 재제작하여 결과물 비교")
    pdf.set_x(15); pdf.info_card("도구",  "코디세이 제공 학습 네이토 sora-2")
    pdf.set_x(15); pdf.info_card("대상",  "씬 1, 씬 2, 씬 3 전체 (3개 씬 모두 재제작)")
    pdf.set_x(15); pdf.info_card("상태",  "완료")
    pdf.set_y(y_box + 37)

    pdf.ln(4)
    pdf.horizontal_rule()

    pdf.section_title("재제작 내용", level=2)
    # 재제작 테이블
    col_w = [18, 40, 40, 97]
    row_h = 7
    pdf.set_fill_color(*COLOR_TH_BG)
    pdf.set_text_color(*COLOR_WHITE)
    pdf.set_font("MG", "B", 9)
    for h, w in zip(["씬", "원본 도구", "재제작 도구", "프롬프트"], col_w):
        pdf.cell(w, row_h, h, 1, 0, "C", True)
    pdf.ln()
    rows_bonus = [
        ("씬 1", "veo-3.1", "sora-2", "씬 1 확정 프롬프트 동일 적용"),
        ("씬 2", "veo-3.1", "sora-2", "씬 2 확정 프롬프트 동일 적용"),
        ("씬 3", "veo-3.1", "sora-2", "씬 3 확정 프롬프트 동일 적용"),
    ]
    fill = False
    pdf.set_text_color(*COLOR_TEXT)
    for row in rows_bonus:
        if fill:
            pdf.set_fill_color(*COLOR_BONUS_BG)
        else:
            pdf.set_fill_color(*COLOR_WHITE)
        pdf.set_font("MG", "", 9)
        for val, w in zip(row, col_w):
            pdf.cell(w, row_h, val, 1, 0, "C", fill)
        pdf.ln()
        fill = not fill
    pdf.ln(6)

    pdf.horizontal_rule()
    pdf.section_title("비교 포인트", level=2)
    compare_items = [
        "동일 프롬프트에서 veo-3.1과 sora-2의 영상 품질·색감·모션 스타일 차이 확인",
        "생성 시간, API 사용 방식, 결과물 해상도 비교",
        "최종 편집 적합성 (색보정 용이성, 씬 간 통일감) 비교",
    ]
    for item in compare_items:
        pdf.set_font("MG", "", 10)
        pdf.set_text_color(*COLOR_TEXT)
        pdf.set_x(14)
        pdf.cell(4, 7, "-", 0, 0)
        pdf.multi_cell(0, 7, item)

    # ── 출력 ──────────────────────────────────────────────
    pdf.output(output_path)
    print(f"PDF 생성 완료: {output_path}")


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "02scenario_v4.pdf")
    build_pdf(out)
