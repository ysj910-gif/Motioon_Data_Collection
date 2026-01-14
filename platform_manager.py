# platform_manager.py 파일의 내용으로 아래 코드를 넣으세요
import json

class PlatformManager:
    def __init__(self):
        self.platforms = []

    def load_platforms(self, file_path):
        """맵 에디터에서 만든 JSON 파일을 불러옵니다."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.platforms = data.get('platforms', [])
                print(f"성공적으로 {len(self.platforms)}개의 발판을 불러왔습니다.")
        except Exception as e:
            print(f"발판 로딩 실패: {e}")

    def get_current_platform(self, char_x, char_y):
        """캐릭터 좌표를 기반으로 현재 밟고 있는 발판을 찾습니다."""
        for p in self.platforms:
            if p['x_start'] <= char_x <= p['x_end'] and abs(char_y - p['y']) < 10:
                return p
        return None