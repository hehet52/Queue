import tkinter as tk

# ──────────────────────────────────────────────
#  큐(Queue) 클래스 선언
# ──────────────────────────────────────────────
class Queue:
    def __init__(self, max_size=10):
        self.items = []
        self.max_size = max_size

    def enqueue(self, item):
        if len(self.items) < self.max_size:
            self.items.append(item)
            return True
        return False

    def dequeue(self):
        if not self.isEmpty():
            return self.items.pop(0)
        return None

    def front(self):
        if not self.isEmpty():
            return self.items[0]
        return None

    def isEmpty(self):
        return len(self.items) == 0

    def clear(self):
        self.items = []

    def size(self):
        return len(self.items)


# ──────────────────────────────────────────────
#  팀원별 단어 (무솔트 메뉴 엑셀)
# ──────────────────────────────────────────────
ALL_WORDS = [
    ("오정현", "말차라떼1"),
    ("오정현", "초코 스콘"),
    ("오정현", "플레인 휘낭시에1"),
    ("김태연", "카페라떼1"),
    ("김태연", "청포도에이드"),
    ("김태연", "레몬에이드"),
    ("김효린", "피넛라떼1"),
    ("김효린", "매실티"),
    ("김효린", "플레인 휘낭시에2"),
    ("이예지", "카페라떼2"),
    ("이예지", "레몬티1"),
    ("이예지", "스콘1"),
    ("장채은", "카페라떼3"),
    ("장채은", "초코라떼"),
    ("장채은", "레몬티2"),
    ("전은빈", "스콘2"),
    ("전은빈", "레몬티3"),
    ("전은빈", "카페모카1"),
    ("조은서", "카페라떼4"),
    ("조은서", "카페모카2"),
    ("조은서", "피넛라떼2"),
    ("정희원", "초코 휘낭시에"),
    ("정희원", "말차라떼2"),
    ("정희원", "산과 아메리카노"),
]


# ──────────────────────────────────────────────
#  시나리오 생성
#  - enqueue / dequeue / front / isEmpty / clear 모두 포함
#  - 모든 팀원 단어 1번 이상 사용
#  - 큐 크기 10 이하 유지
# ──────────────────────────────────────────────
def build_scenario():
    steps = []

    # 1) 큐 선언
    steps.append(("init",    None, None, "Queue 선언  (최대 크기: 10)"))

    # 2) isEmpty — 처음은 비어있음 확인
    steps.append(("isEmpty", None, None, "isEmpty()  →  큐가 비어있는지 확인"))

    # 3) 첫 번째 묶음: 10개 enqueue
    for name, word in ALL_WORDS[:10]:
        steps.append(("enqueue", word, name, f'enqueue("{word}")  —  {name}'))

    # 4) front 확인
    steps.append(("front", None, None, "front()  →  맨 앞 항목 확인"))

    # 5) dequeue 4번 → 공간 확보 (10 → 6)
    for i in range(4):
        steps.append(("dequeue", None, None, f"dequeue()  →  앞에서 꺼내기  ({i+1}/4)"))

    # 6) 두 번째 묶음: 나머지 14개 (중간에 dequeue 끼워 10 이하 유지)
    #    현재 큐: 6개  /  남은 단어: 14개
    #    enqueue 4개(→10) → dequeue 2개(→8) → enqueue 4개(→12 초과 방지: 2개만) ...
    #    실제로 실행 시 큐 상태를 추적하여 안전하게 구성
    remaining = ALL_WORDS[10:]  # 14개
    queue_sim = 6  # 현재 시뮬레이션 상 큐 크기

    for name, word in remaining:
        if queue_sim >= 10:
            steps.append(("dequeue", None, None, "dequeue()  →  공간 확보"))
            queue_sim -= 1
        steps.append(("enqueue", word, name, f'enqueue("{word}")  —  {name}'))
        queue_sim += 1

    # 7) front 재확인
    steps.append(("front", None, None, "front()  →  현재 맨 앞 항목 확인"))

    # 8) clear
    steps.append(("clear", None, None, "clear()  →  큐 전체 비우기"))

    # 9) isEmpty — clear 후 확인
    steps.append(("isEmpty", None, None, "isEmpty()  →  clear 후 비어있는지 확인"))

    return steps


# ──────────────────────────────────────────────
#  색상 팔레트
# ──────────────────────────────────────────────
BG          = "#F0F4FF"
HEADER_BG   = "#2B6CB0"
WHITE       = "#FFFFFF"
DARK        = "#1A202C"
CARD_COLORS = [
    "#63B3ED", "#68D391", "#F6AD55", "#FC8181",
    "#B794F4", "#76E4F7", "#F687B3", "#9AE6B4",
    "#FAF089", "#E9D8FD",
]
OP_COLOR = {
    "enqueue": "#276749",
    "dequeue": "#C53030",
    "front":   "#744210",
    "isEmpty": "#2B6CB0",
    "clear":   "#702459",
    "init":    "#1A202C",
}


# ──────────────────────────────────────────────
#  GUI 애니메이션
# ──────────────────────────────────────────────
class QueueApp:
    def __init__(self, root):
        self.root = root
        self.root.title("카페무솔트  큐(Queue) 애니메이션")
        self.root.configure(bg=BG)
        self.root.geometry("960x660")
        self.root.resizable(False, False)

        self.queue    = Queue(max_size=10)
        self.scenario = build_scenario()
        self.step_idx = 0
        self.auto_on  = False

        self._build_ui()
        self._refresh()
        self._log("Queue 선언 완료  (최대 크기: 10)", "init")

    # ── UI 구성 ──────────────────────────────
    def _build_ui(self):
        # 헤더
        hdr = tk.Frame(self.root, bg=HEADER_BG, height=56)
        hdr.pack(fill="x")
        tk.Label(hdr, text="☕  카페무솔트  Queue  애니메이션",
                 bg=HEADER_BG, fg=WHITE,
                 font=("맑은 고딕", 15, "bold")).pack(pady=14)

        # 본문
        body = tk.Frame(self.root, bg=BG)
        body.pack(fill="both", expand=True, padx=18, pady=10)

        # ── 왼쪽 패널 ──
        left = tk.Frame(body, bg=BG)
        left.pack(side="left", fill="both", expand=True)

        # 현재 연산 레이블
        self.op_var = tk.StringVar(value="큐를 초기화합니다…")
        op_box = tk.Frame(left, bg="#EBF8FF", relief="groove", bd=2)
        op_box.pack(fill="x", pady=(0, 8))
        tk.Label(op_box, textvariable=self.op_var,
                 bg="#EBF8FF", fg="#1A365D",
                 font=("맑은 고딕", 11, "bold"), wraplength=500).pack(pady=8, padx=10)

        # 큐 캔버스
        q_frame = tk.LabelFrame(left, text="  Queue  (최대 크기: 10)",
                                bg=BG, fg=DARK,
                                font=("맑은 고딕", 9, "bold"),
                                relief="ridge", bd=2)
        q_frame.pack(fill="x", pady=(0, 8))
        self.canvas = tk.Canvas(q_frame, bg=BG, height=120,
                                highlightthickness=0)
        self.canvas.pack(fill="x", padx=10, pady=10)

        # 상태 정보
        info = tk.Frame(left, bg=BG)
        info.pack(fill="x", pady=(0, 8))
        self.front_var = tk.StringVar(value="front: —")
        self.size_var  = tk.StringVar(value="size: 0 / 10")
        self.empty_var = tk.StringVar(value="isEmpty: True")
        for var, color in [
            (self.front_var, "#744210"),
            (self.size_var,  "#2B6CB0"),
            (self.empty_var, "#276749"),
        ]:
            tk.Label(info, textvariable=var, bg=BG, fg=color,
                     font=("맑은 고딕", 10, "bold")).pack(side="left", padx=14)

        # 버튼
        btn_row = tk.Frame(left, bg=BG)
        btn_row.pack(fill="x", pady=4)

        self.next_btn = tk.Button(
            btn_row, text="▶  다음 단계",
            bg="#3182CE", fg=WHITE,
            font=("맑은 고딕", 10, "bold"),
            relief="flat", padx=14, pady=6, cursor="hand2",
            command=self._step)
        self.next_btn.pack(side="left", padx=4)

        self.auto_btn = tk.Button(
            btn_row, text="⏩  자동 재생",
            bg="#38A169", fg=WHITE,
            font=("맑은 고딕", 10, "bold"),
            relief="flat", padx=14, pady=6, cursor="hand2",
            command=self._toggle_auto)
        self.auto_btn.pack(side="left", padx=4)

        tk.Button(
            btn_row, text="🔄  처음부터",
            bg="#718096", fg=WHITE,
            font=("맑은 고딕", 10, "bold"),
            relief="flat", padx=14, pady=6, cursor="hand2",
            command=self._reset).pack(side="left", padx=4)

        # 진행 바
        prog_row = tk.Frame(left, bg=BG)
        prog_row.pack(fill="x", pady=4)
        tk.Label(prog_row, text="진행:", bg=BG,
                 font=("맑은 고딕", 9)).pack(side="left")
        self.prog_cv = tk.Canvas(prog_row, bg="#CBD5E0", height=10,
                                 highlightthickness=0)
        self.prog_cv.pack(side="left", fill="x", expand=True, padx=6)
        self.step_lbl = tk.Label(prog_row, text="0 / 0", bg=BG,
                                 font=("맑은 고딕", 9))
        self.step_lbl.pack(side="left")

        # ── 오른쪽: 로그 ──
        right = tk.Frame(body, bg=BG, width=230)
        right.pack(side="right", fill="y", padx=(12, 0))
        right.pack_propagate(False)

        tk.Label(right, text="📋  실행 로그", bg=BG, fg=DARK,
                 font=("맑은 고딕", 10, "bold")).pack(anchor="w", pady=(0, 4))

        sb = tk.Scrollbar(right)
        sb.pack(side="right", fill="y")
        self.log = tk.Text(right, bg="#EBF8FF", fg=DARK,
                           font=("맑은 고딕", 8),
                           relief="flat", bd=2,
                           yscrollcommand=sb.set,
                           state="disabled", wrap="word")
        self.log.pack(fill="both", expand=True)
        sb.config(command=self.log.yview)

        for op, clr in OP_COLOR.items():
            self.log.tag_config(op, foreground=clr,
                                font=("맑은 고딕", 8, "bold"))

    # ── 큐 시각화 ─────────────────────────────
    def _refresh(self, hi=None, hi_color=None):
        c = self.canvas
        c.delete("all")
        items = self.queue.items
        W  = int(c.winfo_width()) or 640
        sw = max(50, (W - 20) / 10)
        bh = 54
        y0 = 18

        # 빈 슬롯
        for i in range(10):
            x0, x1 = 10 + i * sw, 10 + i * sw + sw - 4
            c.create_rectangle(x0, y0, x1, y0 + bh,
                               fill="#DBEAFE", outline="#93C5FD",
                               width=1, dash=(4, 3))

        # 채워진 항목
        for i, item in enumerate(items):
            x0, x1 = 10 + i * sw, 10 + i * sw + sw - 4
            color = hi_color if hi == i else CARD_COLORS[i % len(CARD_COLORS)]
            c.create_rectangle(x0, y0, x1, y0 + bh,
                               fill=color, outline="#2C5282", width=2)
            c.create_text(x0 + (sw - 4) / 2, y0 + bh / 2,
                          text=item,
                          font=("맑은 고딕", 7, "bold"),
                          fill=DARK, width=sw - 8, justify="center")

        # front / rear 화살표
        if items:
            fx = 10 + 0 * sw + (sw - 4) / 2
            c.create_text(fx, y0 + bh + 14,
                          text="▲ front", fill="#C53030",
                          font=("맑은 고딕", 7, "bold"))
            rx = 10 + (len(items) - 1) * sw + (sw - 4) / 2
            c.create_text(rx, y0 - 12,
                          text="rear ▼", fill="#276749",
                          font=("맑은 고딕", 7, "bold"))

        # 상태 레이블 업데이트
        f = self.queue.front()
        self.front_var.set(f"front: {f or '—'}")
        self.size_var.set(f"size: {self.queue.size()} / 10")
        self.empty_var.set(f"isEmpty: {self.queue.isEmpty()}")

        # 진행 바
        total = len(self.scenario)
        ratio = self.step_idx / total if total else 0
        pw = int(self.prog_cv.winfo_width()) or 300
        self.prog_cv.delete("all")
        self.prog_cv.create_rectangle(0, 0, int(pw * ratio), 10,
                                      fill="#3182CE", outline="")
        self.step_lbl.config(text=f"{self.step_idx} / {total}")

    # ── 로그 출력 ─────────────────────────────
    def _log(self, msg, op="init"):
        self.log.config(state="normal")
        self.log.insert("end", msg + "\n", op)
        self.log.see("end")
        self.log.config(state="disabled")

    # ── 한 단계 실행 ──────────────────────────
    def _step(self):
        if self.step_idx >= len(self.scenario):
            return

        op, item, name, desc = self.scenario[self.step_idx]
        self.step_idx += 1
        self.op_var.set(desc)

        hi, hi_color = None, None

        if op == "init":
            self._log(f"[INIT]     {desc}", "init")

        elif op == "isEmpty":
            result = self.queue.isEmpty()
            self._log(f"[isEmpty]  → {result}", "isEmpty")

        elif op == "enqueue":
            ok = self.queue.enqueue(item)
            if ok:
                hi       = self.queue.size() - 1
                hi_color = "#F6E05E"
                self._log(f"[enqueue]  {item}  ({name})", "enqueue")
            else:
                self._log(f"[enqueue]  FAIL — 큐 가득 참: {item}", "enqueue")

        elif op == "dequeue":
            removed = self.queue.dequeue()
            self._log(f"[dequeue]  꺼낸 값 → {removed or '없음'}", "dequeue")

        elif op == "front":
            f        = self.queue.front()
            hi       = 0 if not self.queue.isEmpty() else None
            hi_color = "#FED7E2"
            self._log(f"[front]    맨 앞 → {f or '없음'}", "front")

        elif op == "clear":
            self.queue.clear()
            self._log("[clear]    큐를 전부 비웠습니다.", "clear")

        self._refresh(hi, hi_color)

        if self.step_idx >= len(self.scenario):
            self.next_btn.config(state="disabled")
            self._log("✅  모든 단계 완료!", "init")

    # ── 자동 재생 ─────────────────────────────
    def _toggle_auto(self):
        self.auto_on = not self.auto_on
        if self.auto_on:
            self.auto_btn.config(text="⏸  일시정지", bg="#C05621")
            self._auto_run()
        else:
            self.auto_btn.config(text="⏩  자동 재생", bg="#38A169")

    def _auto_run(self):
        if not self.auto_on:
            return
        if self.step_idx >= len(self.scenario):
            self.auto_on = False
            self.auto_btn.config(text="⏩  자동 재생", bg="#38A169")
            return
        self._step()
        self.root.after(800, self._auto_run)

    # ── 초기화 ────────────────────────────────
    def _reset(self):
        self.auto_on  = False
        self.auto_btn.config(text="⏩  자동 재생", bg="#38A169")
        self.queue    = Queue(max_size=10)
        self.scenario = build_scenario()
        self.step_idx = 0
        self.next_btn.config(state="normal")
        self.log.config(state="normal")
        self.log.delete("1.0", "end")
        self.log.config(state="disabled")
        self.op_var.set("큐를 초기화합니다…")
        self._refresh()
        self._log("Queue 선언 완료  (최대 크기: 10)", "init")


# ──────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    try:
        root.tk.call("tk", "scaling", 1.25)
    except Exception:
        pass
    QueueApp(root)
    root.mainloop()

