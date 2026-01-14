import tkinter as tk
import cv2
import mss
import numpy as np
import os
import config
from collector_gui import DataCollectorApp

def setup_wizard():
    print("=== 메이플 데이터 수집기 설정 마법사 ===")
    
    # 7. 저장 경로 및 이름 지정
    config.DATA_DIR = input(f"저장 경로 입력 (기본: {config.DATA_DIR}): ") or config.DATA_DIR
    config.SAVE_NAME = input(f"파일 이름 입력 (기본: recording.csv): ") or "recording.csv"
    os.makedirs(os.path.join(config.DATA_DIR, "images"), exist_ok=True)

    # 2. 직업 설정
    jobs = ["전사", "마법사", "궁수", "도적", "소울마스터", "플레임위자드", "윈드브레이커", "나이트워커", "스트라이커", "미하일", "아란", "에반", "루미너스", "메르세데스", "팬텀", "은월", "데몬슬레이어", "데몬어벤저", "블래스터", "배틀메이지", "와일드헌터", "메카닉", "제논", "카이저", "카인", "카데나", "엔젤릭버스터", "제로", "키네시스", "아델", "일리움", "칼리", "아크", "렌", "라라", "호영"]
    print(f"\n[직업 선택]\n{', '.join(jobs)}")
    config.JOB = input("직업명을 입력하세요: ")

    # 3. 이동방식 분류
    config.MOVE_TYPE = input("\n이동 방식 선택 (DJ: 더블점프, TP: 텔레포트): ").upper()

    # 4. 조작키 설정
    print("\n[조작키 설정] (키보드의 실제 키 이름을 입력하세요. 예: alt, space, q, w)")
    jump_key = input("점프 키: ")
    special_key = input(f"{'더블점프' if config.MOVE_TYPE == 'DJ' else '텔레포트'} 키: ")
    
    config.KEY_ACTION_MAP = {
        jump_key: 'jump',
        special_key: 'move_special',
        'left': 'move_left',
        'right': 'move_right',
        'up': 'move_up',
        'down': 'move_down'
    }

    # 6. 미니맵 영역 지정
    print("\n[미니맵 영역 지정] 화면에서 미니맵 영역을 드래그한 후 ENTER를 누르세요.")
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        screen = np.array(sct.grab(monitor))
        screen_bgr = cv2.cvtColor(screen, cv2.COLOR_BGRA2BGR)
        roi = cv2.selectROI("Select Minimap ROI", screen_bgr, False)
        cv2.destroyWindow("Select Minimap ROI")
        
        if roi != (0, 0, 0, 0):
            config.MINIMAP_ROI = {'left': int(roi[0]), 'top': int(roi[1]), 'width': int(roi[2]), 'height': int(roi[3])}

    # 5. 인식 화면 재생 확인
    print("\n[인식 확인] 설정된 영역이 올바른지 확인하세요. (창을 닫으려면 'q' 입력)")
    while True:
        with mss.mss() as sct:
            img = np.array(sct.grab(config.MINIMAP_ROI))
            cv2.imshow("Minimap Preview", cv2.cvtColor(img, cv2.COLOR_BGRA2BGR))
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    cv2.destroyAllWindows()

if __name__ == "__main__":
    setup_wizard()
    root = tk.Tk()
    app = DataCollectorApp(root)
    root.mainloop()