import tkinter as tk
from collector_gui import DataCollectorApp

# main.py의 __init__ 부분을 다음과 같이 수정하세요
def __init__(self):
    self.root = tk.Tk()
    self.root.title(Config.TITLE)
    self.root.geometry(Config.WINDOW_SIZE)

    # --- 1. 변수들을 먼저 초기화 (순서 중요!) ---
    self.mode = "PAN"
    self.platforms = []
    self.portals = [] 
    self.selected_platform_idx = None
    
    # 지형 인식용 변수들 추가
    self.thresh_val = tk.IntVar(value=150)
    self.min_len_val = tk.IntVar(value=15)
    self.hsv_lower = [tk.IntVar(value=0), tk.IntVar(value=0), tk.IntVar(value=0)]
    self.hsv_upper = [tk.IntVar(value=180), tk.IntVar(value=255), tk.IntVar(value=255)]
    
    self.zoom_scale = 1.0
    self.pan_x, self.pan_y = 0, 0
    self.orig_img = None
    # ... (기타 변수들)

    # --- 2. 변수 선언이 끝난 후 레이아웃 호출 ---
    self._setup_layout() 
    
    if self.load_initial_image():
        self.run_main_loop()

if __name__ == "__main__":
    root = tk.Tk()
    app = DataCollectorApp(root)
    root.mainloop()