import tkinter as tk
import pyperclip
import time
from googletrans import Translator
from PIL import Image, ImageTk

class TranslatorCatApp:
    def __init__(self, root):
        self.root = root
        self.root.overrideredirect(True)  # 기본 창의 테두리 제거
        self.root.attributes("-topmost", True)
        self.root.attributes("-transparentcolor", "white")  # 투명한 배경 설정
        
        # 화면의 너비와 높이를 가져와 창의 초기 위치 설정
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"300x180+{screen_width-320}+{screen_height-220}")  # 작업표시줄 시간 위에 배치

        # 클립보드 모니터링
        self.is_running = True
        self.recent_text = ""
        self.translator = Translator()

        self.current_page = 0
        self.pages = []

        # 고양이 창 생성 및 표시
        self.create_cat_window()
        self.monitor_clipboard()

    def create_cat_window(self):
        self.canvas = tk.Canvas(self.root, width=300, height=180, bg="white", highlightthickness=0)
        self.canvas.pack()

        # 고양이 이미지 로드 및 크기 조정
        self.cat_image = Image.open("C:/Users/KIM/Desktop/translatorcat/translator_Cat.png")
        self.cat_image = self.cat_image.resize((80, 80), Image.Resampling.LANCZOS)  # 크기를 80x80으로 조정
        self.cat_photo = ImageTk.PhotoImage(self.cat_image)
        self.canvas.create_image(50, 90, image=self.cat_photo, anchor=tk.CENTER)

        # 텍스트 라벨
        self.text_label = tk.Label(self.root, text="", bg="white", font=("Arial", 10), wraplength=130, justify=tk.LEFT)
        self.text_label.place(x=100, y=30)  # 위쪽 여백을 줄여서 y=30으로 설정

        # 다음 버튼을 오른쪽 위로 이동
        self.next_button = tk.Button(self.root, text="다음", command=self.show_next_page)
        self.next_button.place(x=240, y=10)

        # 이전 버튼을 다음 버튼 바로 아래로 이동
        self.prev_button = tk.Button(self.root, text="이전", command=self.show_prev_page)
        self.prev_button.place(x=240, y=40)

        # 이동 버튼 생성 (사용자 커서로 위치 조정)
        self.move_button = tk.Button(self.root, text="이동", command=self.enable_move_mode)
        self.move_button.place(x=240, y=70)

        # 닫기 버튼 생성
        self.close_button = tk.Button(self.root, text="닫기", command=self.close_app)
        self.close_button.place(x=240, y=100)

        # 색상 변경 버튼 생성
        self.create_color_buttons()

    def create_color_buttons(self):
        # 글자 색상을 변경할 수 있는 4개의 작은 버튼을 2x2로 생성
        colors = ["red", "blue", "green", "black"]
        x_position = 240
        y_position = 130
        for i, color in enumerate(colors):
            button = tk.Button(self.root, bg=color, width=1, height=1, command=lambda c=color: self.change_text_color(c))
            button.place(x=x_position, y=y_position)
            if i % 2 == 0:
                x_position += 20
            else:
                x_position = 240
                y_position += 20

    def change_text_color(self, color):
        self.text_label.config(fg=color)

    def enable_move_mode(self):
        self.root.bind("<B1-Motion>", self.on_move)

    def on_move(self, event):
        x = self.root.winfo_pointerx() - self.root.winfo_width() // 2
        y = self.root.winfo_pointery() - self.root.winfo_height() // 2
        self.root.geometry(f"+{x}+{y}")

    def close_app(self):
        self.is_running = False
        self.root.destroy()

    def monitor_clipboard(self):
        if self.is_running:
            text = pyperclip.paste()
            if text != self.recent_text and text:
                self.recent_text = text
                translated = self.translator.translate(text, src='en', dest='ko')
                self.paginate_translation(translated.text)
                self.show_translation()
            self.root.after(1000, self.monitor_clipboard)

    def paginate_translation(self, text):
        # 텍스트를 페이지 단위로 나누기
        max_length = 70  # 페이지당 최대 글자 수를 줄여 더 많은 텍스트가 보이도록 조정
        self.pages = [text[i:i + max_length] for i in range(0, len(text), max_length)]
        self.current_page = 0

    def show_translation(self):
        if self.pages:
            self.text_label.config(text=self.pages[self.current_page])

    def show_next_page(self):
        if self.current_page < len(self.pages) - 1:
            self.current_page += 1
            self.show_translation()

    def show_prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.show_translation()

if __name__ == "__main__":
    root = tk.Tk()
    app = TranslatorCatApp(root)
    root.mainloop()
