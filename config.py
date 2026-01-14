import numpy as np

# 데이터 저장 경로
DATA_DIR = "training_data_v2"

# 미니맵 ROI (이 영역만 저장하여 효율 극대화)
MINIMAP_ROI = {'top': 65, 'left': 30, 'width': 215, 'height': 135}

# 캐릭터 탐지 색상
YELLOW_HSV_LOWER = np.array([25, 150, 150])
YELLOW_HSV_UPPER = np.array([35, 255, 255])

# --- [추가] 액션 매핑 시스템 ---
# 공격 스킬은 제외하고, 이동과 관련된 키만 등록합니다.
KEY_ACTION_MAP = {
    'alt': 'jump',
    'left': 'move_left',
    'right': 'move_right',
    'up': 'move_up',
    'down': 'move_down',
    'shift': 'dash',    # 이동 관련 스킬 예시
    'space': 'double_jump'
}

# 수집 설정
FPS_LIMIT = 10