import asyncio
import re
import flet as ft
from flet_timer.flet_timer import Timer
from datetime import datetime
from .controls.clock import Clock, Calender

class UsedEquipment(ft.View):
    def __init__(self, data):
        self.studentNo = data["studentNo"]
        self.running = False
        super().__init__("/leave", controls=self.get_controls())

    def did_mount(self):
        self.running = True
        self.equipment_fields[0].focus()
        return super().did_mount()

    def on_clear_button_click(self, e):
        for field in self.equipment_fields:
            field.value = ""
        self.equipment_fields[0].focus()

    def on_back_button_click(self, e):
        self.page.go("/")

    def on_send_button_click(self, e):
        data = {"studentNo": self.studentNo}
        equipments =[field.value for field in self.equipment_fields if field.value != '']
        data["equipments"] =  equipments
        self.data = data
        self.page.go("/left")


    def focus_field(self, e):
        self.number_field.focus()

    def get_controls(self):
        date_text = Calender(size=48, text_align=ft.TextAlign.LEFT)

        appbar = ft.AppBar( 
            title=ft.Text("IWスクエア入退室管理", size=48),
            center_title=False,
            bgcolor=ft.colors.SURFACE_VARIANT,
            toolbar_height=80,
            actions=[date_text]
        )

        order_text = ft.Column ([
            ft.Container(ft.Text(f"学生番号: {self.studentNo}", size=40, text_align=ft.TextAlign.CENTER),
                        margin=ft.margin.only(0,0,0,5),
                        alignment=ft.alignment.center),
            ft.Text("使った設備のバーコードを", size=50, text_align=ft.TextAlign.CENTER),
            ft.Text("QRコードリーダーで読み込んでください。", size=50, text_align=ft.TextAlign.CENTER)
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        
        self.equipment_fields = [ft.TextField(text_size=32, data=i) for i in range(8)]

        for field in self.equipment_fields:
            field.on_submit = lambda _, data=field.data: self.equipment_fields[data+1 if data < 7 else 0].focus()


        self.field_grid = ft.Column([
            ft.Row([
                ft.Container(
                    content=ft.Row([
                        ft.Container(
                            ft.Text(f"設備{(c+1) + 4*r: >3}", size=40),
                            width=130
                        ),
                        ft.Container(
                            self.equipment_fields[c+4*r],
                            expand=True,
                            padding=ft.padding.symmetric(0, 20))
                    ]),
                    expand=True
                )
            for r in range(2)])
        for c in range(4)],
        alignment=ft.MainAxisAlignment.CENTER)
        
        back_button = ft.Container(
            content=ft.Text("戻る", size=40), 
            margin=10, 
            padding=ft.padding.symmetric(10,0),
            width=200,
            alignment=ft.alignment.center,
            border=ft.border.all(1, ft.colors.PRIMARY),
            border_radius=15,
            on_click=self.on_back_button_click
        )
        
        clear_button = ft.Container(
            content=ft.Text("クリア", size=40), 
            margin=10, 
            padding=ft.padding.symmetric(10,0),
            width=200,
            alignment=ft.alignment.center,
            border=ft.border.all(1, ft.colors.PRIMARY),
            border_radius=15,
            on_click=self.on_clear_button_click
        )

        send_button = ft.Container(
            content=ft.Text("送信", size=40), 
            margin=10, 
            padding=ft.padding.symmetric(10,0),
            width=480,
            alignment=ft.alignment.center,
            border=ft.border.all(1, ft.colors.PRIMARY),
            border_radius=15,
            on_click=self.on_send_button_click
        )
        
        button_row = ft.Row([back_button, clear_button, send_button], alignment=ft.MainAxisAlignment.CENTER)

        table_content = ft.Container(ft.Column([
                    ft.Container(
                        content=order_text,
                        margin=10,
                        padding=10,
                        alignment=ft.alignment.center,),
                    ft.Container(
                        content=self.field_grid,
                        padding=ft.padding.symmetric(20, 40),
                        expand=True ),
                    ft.Container(
                        content=button_row,
                        padding=ft.padding.symmetric(20, 10),
                        expand=True,
                        alignment=ft.alignment.center
                    )
                ], 
                horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=ft.padding.only(10, 10, 10, 20),
            alignment=ft.alignment.center
        )

        return [appbar, table_content]
