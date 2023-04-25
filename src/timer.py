from datetime import datetime
from typing import Union


class Timer:

    def __init__(self) -> None:
        self.name = 'timer'
        self.detail = None
        self.second = 0

    def set_name(self, name: str):
        """設置名稱

        Args:
            name (str): 名稱
        """
        self.name = name

    def set_detail(self, detail: str):
        """設置描述

        Args:
            detail (str): 描述
        """
        self.detail = detail

    def start(self):
        self.second = datetime.now().timestamp()

    def stop(self):
        self.second = datetime.now().timestamp() - self.second

    def get_time_str(self, total_secends: Union[int, float]) -> str:
        """依照秒數 回傳中文時間

        Args:
            total_secends (int): 總秒數

        Returns:
            str: 回傳時間
        """
        msg = ''
        seconds = total_secends % 60
        minutes = (total_secends // 60) % 60
        hours = ((total_secends // 60) // 60) % 24
        days = ((total_secends // 60) // 60) // 24
        if days != 0:
            msg += f"{days}天"
        if hours != 0:
            msg += f"{hours}時"
        if minutes != 0:
            msg += f"{minutes}分"
        if seconds != 0:
            msg += f"{seconds}秒"
        return msg

    def get_result(self) -> str:
        """回傳 結果

        Returns:
            str: 結果訊息
        """
        if self.detail:
            return f'{self.name}\n{self.detail}\n經過時間: {self.get_time_str(self.second)}'
        else:
            return f'{self.name}\n經過時間: {self.get_time_str(self.second)}'
