import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import time
import os
import pandas as pd
import cv2
from pynput import keyboard
import config
from vision_engine import VisionEngine
from platform_manager import PlatformManager

class DataCollectorApp:
    def __init__(self, root):
        self.root = root
        self.vision = VisionEngine()
        self.plat_mgr = PlatformManager()
        self.is_recording = False
        self.samples = []
        self.current_keys = set()
        # ... (GUI 및 키보드 리스너 초기화 로직 v2.1과 동일) ...

    def on_press(self, key):
        try:
            # 1. 입력된 물리 키 확인
            k = key.char if hasattr(key, 'char') else str(key).replace('Key.', '')
            
            # 2. 매핑 테이블에 있는 '이동 액션'인 경우에만 저장
            action = config.KEY_ACTION_MAP.get(k)
            if action:
                self.current_actions.add(action)
        except: pass

    def on_release(self, key):
        try:
            k = key.char if hasattr(key, 'char') else str(key).replace('Key.', '')
            action = config.KEY_ACTION_MAP.get(k)
            if action in self.current_actions:
                self.current_actions.remove(action)
        except: pass

    def record_frame(self, count):
        """프레임 기록 루프 내부"""
        # 1. 미니맵만 가져와서 저장 (효율화)
        mini_bgr = self.vision.capture_minimap()
        
        img_name = f"mini_{count:06d}.jpg"
        img_path = os.path.join(config.DATA_DIR, "images", img_name)
        cv2.imwrite(img_path, mini_bgr) # 혹은 mask 저장

        # 2. 현재 활성화된 이동 액션들만 로그 생성
        action_log = " ".join(list(self.current_actions))
        
        return {
            'image_path': img_name,
            'actions': action_log if action_log else "idle"
        }