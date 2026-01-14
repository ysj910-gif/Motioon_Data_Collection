import numpy as np

# 기본 데이터 저장 경로
DATA_DIR = "training_data_v2"
SAVE_NAME = "recording_log.csv"

# 초기 미니맵 ROI (콘솔에서 재설정 가능)
MINIMAP_ROI = {'top': 65, 'left': 30, 'width': 215, 'height': 135}

# 캐릭터 탐지 색상
YELLOW_HSV_LOWER = np.array([25, 150, 150])
YELLOW_HSV_UPPER = np.array([35, 255, 255])

# 기본 액션 매핑 (콘솔에서 재설정됨)
KEY_ACTION_MAP = {}

# 수집 설정
FPS_LIMIT = 10