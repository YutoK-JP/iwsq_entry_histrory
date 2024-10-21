import flet as ft
from datetime import datetime
import asyncio

DayOfWeek = ["月", "火", "水", "木", "金", "土", "日"]

class Clock(ft.Text):
    def __init__(self, **args):
        super().__init__(**args)
        self.value = datetime.now().strftime("%H:%M:%S")

    def before_update(self):
        dt = datetime.now()
        self.value = datetime.now().strftime("%H:%M:%S")

class Calender(ft.Text):
    def __init__(self, **args):
        super().__init__(**args)
        dt = datetime.now()
        self.value = dt.strftime("%Y年%m月%d日") + f"（{DayOfWeek[dt.weekday()]}）"

    def before_update(self):
        dt = datetime.now()
        self.value = dt.strftime("%Y年%m月%d日") + f"（{DayOfWeek[dt.weekday()]}）"
