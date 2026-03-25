import tkinter as tk
from collections import deque
import csv
import os

CSV_FILE = "moosault.csv"
MAX_QUEUE_SIZE = 10


def load_csv_data(filename):
    data = []

    if not os.path.exists(filename):
        raise FileNotFoundError(f"{filename} 파일을 찾을 수 없습니다.")

    with open(filename, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        next(reader, None)

        for row in reader:
            if not row or len(row) < 5:
                continue

            sid = row[0].strip()
            name = row[1].strip()
            menus = [x.strip() for x in row[2:5]]

            data.append((name, sid, menus))

    return data


def build_operations_from_csv(csv_data):
    all_menus = []
    for name, sid, menus in csv_data:
        for menu in menus:
            if menu:
                all_menus.append(menu)

    unique_menus = []
    seen = set()
    for menu in all_menus:
        if menu not in seen:
            seen.add(menu)
            unique_menus.append(menu)

    ops = [
        ("declare", None),
        ("isEmpty", None),
    ]

    first_batch = unique_menus[:10]
    rest_batch = unique_menus[10:]

    for menu in first_batch:
        ops.append(("enqueue", menu))

    ops.append(("front", None))

    for _ in range(min(4, len(first_batch))):
        ops.append(("dequeue", None))

    for menu in rest_batch:
        ops.append(("enqueue", menu))

    ops.append(("front", None))
    ops.append(("clear", None))
    ops.append(("isEmpty", None))

    return ops


class QueueVisualizer:
    def __init__(self, root, csv_filename):
        self.root = root
        self.root.title("큐 과제 - 카페무슬트")
        self.root.geometry("1300x930")
        self.root.configure(bg="white")

        self.csv_filename = csv_filename
        self.csv_data = load_csv_data(csv_filename)
        self.operations = build_operations_from_csv(self.csv_data)

        self.step = 0
        self.history = []
        self.auto_play = False

        self.make_history()
        self.build_ui()
        self.show_step(0)

    def make_history(self):
        q = deque()

        for idx, (op, value) in enumerate(self.operations):
            code_text = ""
            message = ""
            result = ""

            if op == "declare":
                code_text = "cafeMoosault = Queue()"
                message = "빈 큐를 선언합니다."
                result = "큐 생성 완료"

            elif op == "isEmpty":
                code_text = "cafeMoosault.isEmpty()"
                empty = len(q) == 0
                message = "큐가 비어있는지 확인합니다."
                result = f"결과: {empty}"

            elif op == "enqueue":
                code_text = f'cafeMoosault.enqueue("{value}")'
                if len(q) < MAX_QUEUE_SIZE:
                    q.append(value)
                    message = f'"{value}" 를 큐의 뒤(rear)에 삽입합니다.'
                    result = "enqueue 성공"
                else:
                    message = f'큐의 최대 크기(10)를 초과하여 "{value}" 를 삽입할 수 없습니다.'
                    result = "enqueue 실패"

            elif op == "dequeue":
                code_text = "cafeMoosault.dequeue()"
                if q:
                    removed = q.popleft()
                    message = f'큐의 앞(front)에서 "{removed}" 를 삭제합니다.'
                    result = f"삭제된 값: {removed}"
                else:
                    message = "큐가 비어 있어 dequeue 할 수 없습니다."
                    result = "dequeue 실패"

            elif op == "front":
                code_text = "cafeMoosault.front()"
                if q:
                    message = "큐의 맨 앞(front) 데이터를 확인합니다."
                    result = f"front 값: {q[0]}"
                else:
                    message = "큐가 비어 있어 front 를 확인할 수 없습니다."
                    result = "front 확인 실패"

            elif op == "clear":
                code_text = "cafeMoosault.clear()"
                q.clear()
                message = "큐의 모든 데이터를 삭제합니다."
                result = "큐 비움 완료"

            self.history.append({
                "step": idx,
                "op": op,
                "value": value,
                "queue": list(q),
                "code": code_text,
                "message": message,
                "result": result,
            })

    def build_ui(self):
        title = tk.Label(
            self.root,
            text="카페무슬트 큐 연산 애니메이션",
            font=("맑은 고딕", 25, "bold"),
            bg="white"
        )
        title.pack(pady=10)

        top_frame = tk.Frame(self.root, bg="white")
        top_frame.pack(fill="x", padx=20, pady=5)

        left_frame = tk.LabelFrame(
            top_frame,
            text=f"팀 CSV 정보 ({self.csv_filename}, 전은빈 제외)",
            font=("맑은 고딕", 13, "bold"),
            bg="white",
            padx=10,
            pady=10
        )
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 12))

        self.csv_text = tk.Text(
            left_frame,
            width=55,
            height=10,
            font=("Consolas", 12),
            bg="#f8f8f8"
        )
        self.csv_text.pack(fill="both", expand=True)

        csv_string = "name,id,1,2,3\n"
        for name, sid, menus in self.csv_data:
            csv_string += f"{name},{sid},{menus[0]},{menus[1]},{menus[2]}\n"
        self.csv_text.insert("1.0", csv_string)
        self.csv_text.config(state="disabled")

        right_frame = tk.LabelFrame(
            top_frame,
            text="현재 수행 중인 연산",
            font=("맑은 고딕", 13, "bold"),
            bg="white",
            padx=10,
            pady=10
        )
        right_frame.pack(side="right", fill="both", expand=True)

        self.code_label = tk.Label(
            right_frame,
            text="",
            font=("Consolas", 20, "bold"),
            bg="#eef6ff",
            fg="#003b73",
            anchor="w",
            justify="left",
            padx=15,
            pady=15
        )
        self.code_label.pack(fill="x", pady=(0, 10))

        self.message_label = tk.Label(
            right_frame,
            text="",
            font=("맑은 고딕", 13),
            bg="white",
            anchor="w",
            justify="left",
            wraplength=500
        )
        self.message_label.pack(fill="x", pady=4)

        self.result_label = tk.Label(
            right_frame,
            text="",
            font=("맑은 고딕", 15, "bold"),
            bg="white",
            fg="#c00000",
            anchor="w",
            justify="left"
        )
        self.result_label.pack(fill="x", pady=4)

        center_frame = tk.LabelFrame(
            self.root,
            text="예시 형태와 유사한 큐 시각화",
            font=("맑은 고딕", 13, "bold"),
            bg="white",
            padx=10,
            pady=10
        )
        center_frame.pack(fill="x", expand=False, padx=20, pady=10)

        self.canvas = tk.Canvas(center_frame, bg="white", height=360)
        self.canvas.pack(fill="both", expand=True)

        bottom_frame = tk.Frame(self.root, bg="white")
        bottom_frame.pack(fill="x", padx=20, pady=10)

        self.step_label = tk.Label(
            bottom_frame,
            text="",
            font=("맑은 고딕", 13, "bold"),
            bg="white"
        )
        self.step_label.pack(pady=5)

        btn_frame = tk.Frame(bottom_frame, bg="white")
        btn_frame.pack()

        tk.Button(btn_frame, text="<< 처음", font=("맑은 고딕", 12), width=10,
                  command=self.go_first).pack(side="left", padx=5)
        tk.Button(btn_frame, text="< 이전", font=("맑은 고딕", 12), width=10,
                  command=self.prev_step).pack(side="left", padx=5)
        tk.Button(btn_frame, text="다음 >", font=("맑은 고딕", 12), width=10,
                  command=self.next_step).pack(side="left", padx=5)

        self.play_btn = tk.Button(
            btn_frame, text="자동재생", font=("맑은 고딕", 12), width=10,
            command=self.toggle_play
        )
        self.play_btn.pack(side="left", padx=5)

        tk.Button(btn_frame, text="마지막 >>", font=("맑은 고딕", 12), width=10,
                  command=self.go_last).pack(side="left", padx=5)

    def draw_queue(self, queue_items):
        self.canvas.delete("all")

        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        if canvas_width < 200:
            canvas_width = 1240
        if canvas_height < 200:
            canvas_height = 360

        self.canvas.create_rectangle(
            15, 15, canvas_width - 15, canvas_height - 15,
            outline="#14a6dc", width=3
        )

        title_x1 = canvas_width - 520
        title_y1 = 15
        title_x2 = canvas_width - 15
        title_y2 = 75

        self.canvas.create_rectangle(
            title_x1, title_y1, title_x2, title_y2,
            outline="#444444", width=1
        )
        self.canvas.create_text(
            (title_x1 + title_x2) // 2,
            (title_y1 + title_y2) // 2,
            text="카페무슬트",
            font=("맑은 고딕", 18, "bold")
        )

        current_code = self.history[self.step]["code"]
        current_result = self.history[self.step]["result"]

        self.canvas.create_text(
            90, 130,
            text=current_code,
            font=("맑은 고딕", 18, "bold"),
            anchor="w"
        )

        self.canvas.create_text(
            90, 175,
            text=current_result,
            font=("맑은 고딕", 14, "bold"),
            fill="#666666",
            anchor="w"
        )

        box_w = 290
        box_h = 22
        x1 = canvas_width - 360
        bottom_y = canvas_height - 20

        visible_count = min(MAX_QUEUE_SIZE, len(queue_items))

        if visible_count == 0:
            self.canvas.create_text(
                canvas_width - 210, 190,
                text="현재 큐는 비어 있음",
                font=("맑은 고딕", 15, "bold"),
                fill="gray"
            )
        else:
            display_items = queue_items[:visible_count]

            for i, item in enumerate(display_items):
                rect_y2 = bottom_y - i * box_h
                rect_y1 = rect_y2 - box_h

                self.canvas.create_rectangle(
                    x1, rect_y1, x1 + box_w, rect_y2,
                    outline="#444444", width=1
                )

                self.canvas.create_text(
                    x1 + box_w // 2,
                    (rect_y1 + rect_y2) // 2,
                    text=item,
                    font=("맑은 고딕", 10, "bold"),
                    width=box_w - 18
                )

            self.canvas.create_text(
                x1 - 55,
                bottom_y - box_h // 2,
                text="front",
                font=("맑은 고딕", 10, "bold"),
                fill="blue"
            )

            top_center_y = bottom_y - (visible_count - 1) * box_h - box_h // 2
            self.canvas.create_text(
                x1 - 50,
                top_center_y,
                text="rear",
                font=("맑은 고딕", 10, "bold"),
                fill="green"
            )

        self.canvas.create_text(
            canvas_width // 2,
            canvas_height - 28,
            text=f"현재 큐 크기: {len(queue_items)} / {MAX_QUEUE_SIZE}",
            font=("맑은 고딕", 13, "bold"),
            fill="#444444"
        )

    def show_step(self, idx):
        data = self.history[idx]
        self.step_label.config(text=f"Step {idx + 1} / {len(self.history)}")
        self.code_label.config(text=data["code"])
        self.message_label.config(text=data["message"])
        self.result_label.config(text=data["result"])
        self.draw_queue(data["queue"])

    def next_step(self):
        if self.step < len(self.history) - 1:
            self.step += 1
            self.show_step(self.step)
        else:
            self.auto_play = False
            self.play_btn.config(text="자동재생")

    def prev_step(self):
        if self.step > 0:
            self.step -= 1
            self.show_step(self.step)

    def go_first(self):
        self.step = 0
        self.show_step(self.step)

    def go_last(self):
        self.step = len(self.history) - 1
        self.show_step(self.step)

    def toggle_play(self):
        self.auto_play = not self.auto_play
        self.play_btn.config(text="정지" if self.auto_play else "자동재생")
        if self.auto_play:
            self.play_steps()

    def play_steps(self):
        if self.auto_play:
            if self.step < len(self.history) - 1:
                self.next_step()
                self.root.after(1200, self.play_steps)
            else:
                self.auto_play = False
                self.play_btn.config(text="자동재생")


if __name__ == "__main__":
    root = tk.Tk()
    app = QueueVisualizer(root, CSV_FILE)
    root.mainloop()