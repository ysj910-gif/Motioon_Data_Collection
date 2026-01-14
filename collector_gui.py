import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import time
import os
import pandas as pd
import cv2
import numpy as np
from pynput import keyboard

import config
from vision_engine import VisionEngine
from platform_manager import PlatformManager

class DataCollectorApp:
    def __init__(self, root):
        self.root = root
        # 콘솔에서 설정한 직업과 이동방식을 타이틀에 표시
        self.root.title(f"데이터 수집기 - {getattr(config, 'JOB', '미지정')} ({getattr(config, 'MOVE_TYPE', '??')})")
        self.root.geometry("450x400")

        # 엔진 및 관리자 초기화
        self.vision = VisionEngine()
        self.plat_mgr = PlatformManager()
        
        # 상태 변수
        self.is_recording = False
        self.samples = []
        self.current_actions = set()
        self.map_loaded = False
        self.start_time = 0

        # 레이아웃 설정
        self._setup_layout()

        # 키보드 리스너 시작 (config.KEY_ACTION_MAP 반영)
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()

        # 종료 프로토콜
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def _setup_layout(self):
        """GUI 구성: 맵 업로드 버튼 및 현재 설정 상태 표시"""
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(expand=True, fill="both")

        # 1. 맵 데이터 업로드 (기능 1)
        ttk.Label(main_frame, text="1. 맵 데이터 설정", font=("Arial", 10, "bold")).pack(anchor="w")
        self.map_btn = ttk.Button(main_frame, text="JSON 맵 파일 불러오기", command=self.upload_map)
        self.map_btn.pack(fill="x", pady=5)
        self.map_status = ttk.Label(main_frame, text="맵 파일: 대기 중", foreground="red")
        self.map_status.pack(anchor="w", pady=(0, 10))

        ttk.Separator(main_frame, orient="horizontal").pack(fill="x", pady=10)

        # 2. 현재 설정 정보 표시 (기능 2, 3, 4, 7 반영 확인용)
        ttk.Label(main_frame, text="2. 현재 수집 설정", font=("Arial", 10, "bold")).pack(anchor="w")
        info_text = (
            f"• 직업: {getattr(config, 'JOB', 'N/A')}\n"
            f"• 이동 방식: {getattr(config, 'MOVE_TYPE', 'N/A')}\n"
            f"• 저장 경로: {config.DATA_DIR}\n"
            f"• 파일명: {config.SAVE_NAME}"
        )
        ttk.Label(main_frame, text=info_text, justify="left").pack(anchor="w", pady=5)

        ttk.Separator(main_frame, orient="horizontal").pack(fill="x", pady=10)

        # 3. 제어 버튼
        self.status_label = ttk.Label(main_frame, text="상태: 맵을 먼저 불러와주세요", foreground="blue")
        self.status_label.pack(pady=5)

        self.record_btn = ttk.Button(main_frame, text="녹화 시작", command=self.toggle_recording, state="disabled")
        self.record_btn.pack(fill="x", pady=5)

        self.count_label = ttk.Label(main_frame, text="수집된 프레임: 0")
        self.count_label.pack()

    def upload_map(self):
        """기능 1: 녹화 시작 전 .json 맵 데이터 로드"""
        file_path = filedialog.askopenfilename(
            title="맵 데이터 JSON 선택",
            filetypes=[("JSON files", "*.json")]
        )
        if file_path:
            self.plat_mgr.load_platforms(file_path)
            self.map_loaded = True
            self.map_status.config(text=f"맵 파일: {os.path.basename(file_path)}", foreground="green")
            self.record_btn.config(state="normal")
            self.status_label.config(text="상태: 준비 완료")
            messagebox.showinfo("완료", "맵 데이터를 성공적으로 불러왔습니다.")

    def on_press(self, key):
        """기능 4: 콘솔에서 설정한 조작키 매핑 반영"""
        try:
            if hasattr(key, 'char') and key.char is not None:
                k = key.char
            else:
                k = str(key).replace('Key.', '')

            # config.KEY_ACTION_MAP은 main.py의 wizard에서 생성됨
            action = config.KEY_ACTION_MAP.get(k)
            if action:
                self.current_actions.add(action)
        except: pass

    def on_release(self, key):
        try:
            if hasattr(key, 'char') and key.char is not None:
                k = key.char
            else:
                k = str(key).replace('Key.', '')

            action = config.KEY_ACTION_MAP.get(k)
            if action in self.current_actions:
                self.current_actions.remove(action)
        except: pass

    def toggle_recording(self):
        """녹화 시작/중지 토글"""
        if not self.is_recording:
            self.start_recording()
        else:
            self.stop_recording()

    def start_recording(self):
        self.is_recording = True
        self.samples = []
        self.start_time = time.time()
        self.record_btn.config(text="녹화 중지 및 저장")
        self.status_label.config(text="상태: 녹화 중...", foreground="red")
        self.map_btn.config(state="disabled")
        
        threading.Thread(target=self.record_loop, daemon=True).start()

    def record_loop(self):
        """데이터 수집 핵심 루프"""
        count = 0
        interval = 1.0 / config.FPS_LIMIT
        
        while self.is_recording:
            loop_start = time.time()
            
            # 1. 미니맵 캡처 (기능 6에서 지정한 ROI 사용)
            mini_bgr = self.vision.capture_minimap()
            
            # 2. 이미지 저장 (기능 7에서 지정한 경로 사용)
            img_name = f"{config.JOB}_{int(time.time()*1000)}.jpg"
            img_path = os.path.join(config.DATA_DIR, "images", img_name)
            cv2.imwrite(img_path, mini_bgr)

            # 3. 캐릭터 위치 및 발판 인식
            mask = self.vision.get_character_mask(mini_bgr)
            M = cv2.moments(mask)
            char_x, char_y = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])) if M["m00"] != 0 else (0, 0)
            
            current_plat = self.plat_mgr.get_current_platform(char_x, char_y)
            plat_id = current_plat.get('id', -1) if current_plat else -1

            # 4. 데이터 저장
            action_log = " ".join(list(self.current_actions)) if self.current_actions else "idle"
            
            self.samples.append({
                'timestamp': time.time() - self.start_time,
                'job': config.JOB,
                'move_type': config.MOVE_TYPE,
                'image_path': img_name,
                'char_x': char_x,
                'char_y': char_y,
                'platform_id': plat_id,
                'actions': action_log
            })

            count += 1
            self.count_label.config(text=f"수집된 프레임: {count}")

            # FPS 유지
            elapsed = time.time() - loop_start
            time.sleep(max(0, interval - elapsed))

    def stop_recording(self):
        self.is_recording = False
        self.record_btn.config(text="녹화 시작")
        self.status_label.config(text="상태: 데이터 저장 중...", foreground="orange")
        
        if self.samples:
            df = pd.DataFrame(self.samples)
            csv_path = os.path.join(config.DATA_DIR, config.SAVE_NAME)
            
            # 이어붙이기 모드 (기능 7)
            header = not os.path.exists(csv_path)
            df.to_csv(csv_path, mode='a', index=False, header=header)
            
            messagebox.showinfo("저장 완료", f"{len(self.samples)} 프레임이 {config.SAVE_NAME}에 추가되었습니다.")
        
        self.map_btn.config(state="normal")
        self.status_label.config(text="상태: 준비 완료", foreground="green")

    def on_closing(self):
        self.is_recording = False
        self.listener.stop()
        self.root.destroy()