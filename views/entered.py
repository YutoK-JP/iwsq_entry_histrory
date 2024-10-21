import asyncio
import flet as ft
from flet_timer.flet_timer import Timer
from datetime import datetime
from .controls.clock import Clock, Calender
import time

class Entered(ft.View):
    def __init__(self):
        self.data = None
        controls = self.get_controls()
        super().__init__("/entered", controls=controls)

    def get_controls(self):
        date_text = Calender(size=48, text_align=ft.TextAlign.LEFT)

        appbar = ft.AppBar(
            title=ft.Text("IWスクエア入退室管理", size=48),
            center_title=False,
            bgcolor=ft.colors.SURFACE_VARIANT,
            toolbar_height=80,
            actions=[date_text]
        )

        main_content = ft.Container(ft.Column([
            ft.Container(
                content=ft.Text(content, size=80, text_align=ft.TextAlign.CENTER),
                margin=10,
                padding=10,
                alignment=ft.alignment.center,)
            for content in[
                "入室を受け付けました",
                "怪我に気をつけてご利用ください"]
            ]),
            padding=ft.padding.only(10, 200, 10, 120),
            alignment=ft.alignment.center
        )

        return [appbar, main_content]