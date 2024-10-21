import asyncio
import re
import flet as ft
from flet_timer.flet_timer import Timer
from datetime import datetime
from .controls.clock import Clock, Calender
from .controls.csv_utils import referenceEntryLog

class Index(ft.View):
    def __init__(self):
        self.data = None
        self.running = False
        controls = self.get_controls()
        super().__init__("/", controls=controls)

    def did_mount(self):
        self.running = True
        return super().did_mount()

    def on_button_click(self, e):
        self.number_field.value = ""

    def on_field_update(self, e):
        entered_number = e.data
        print(f"enterd: {entered_number}")
        isStudent = r"^[1-48]20\d{4}0$"
        isTeacherOrStaff = r"^00[1-59]0\d{3}0$"
        verified = re.match(f"({isStudent})|({isTeacherOrStaff})", entered_number)
        if verified:
            self.data = {"studentNo": entered_number}
            history = referenceEntryLog(entered_number)
            self.number_field.value = ""
            if history == 0:
                self.page.go("/entered")
            elif history == 1:
                self.page.go("/leave")


    def focus_field(self, e):
        if self.page.route=="/":
            self.number_field.focus()

    def get_controls(self):
        date_text = Calender(size=48, text_align=ft.TextAlign.LEFT)
        time_text = Clock(size=160, text_align=ft.TextAlign.LEFT)

        appbar = ft.AppBar( 
            title=ft.Text("IWスクエア入退室管理", size=48),
            center_title=False,
            bgcolor=ft.colors.SURFACE_VARIANT,
            toolbar_height=80,
            actions=[date_text]
        )

        order_text = ft.Text("学生証を読み込んでください", size=90, text_align=ft.TextAlign.CENTER)

        self.number_field = ft.TextField(
            autofocus=True,
            text_size=60, 
            text_align=ft.TextAlign.CENTER,
            on_submit=self.on_field_update,
            on_blur=self.focus_field
        )
        
        clear_button = ft.Container(
            content=ft.Text("入力をクリア", size=40), 
            margin=10, 
            padding=ft.padding.symmetric(20,15),
            alignment=ft.alignment.center,
            border=ft.border.all(1, ft.colors.PRIMARY),
            border_radius=15,
            on_click=self.on_button_click
        )
        
        table_content = ft.Container(ft.Column([
            ft.Container(
                content=content,
                margin=10,
                padding=10,
                alignment=ft.alignment.center,)
            for content in[
                time_text,
                order_text]
            ]+[
                ft.Row([
                    ft.Container(
                        content=self.number_field,
                        padding=ft.padding.symmetric(20, 40),
                        expand=True ),
                    clear_button
                    ], 
                    alignment=ft.MainAxisAlignment.SPACE_AROUND,)
            ]),
            padding=ft.padding.only(10, 80, 10, 120),
            alignment=ft.alignment.center
        )

        return [appbar, table_content]
