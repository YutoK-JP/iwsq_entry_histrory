import flet as ft
from flet_timer.flet_timer import Timer
from datetime import datetime
from views import index, entered, used_equipment, left
from views.controls.csv_utils import *
import time
import asyncio  
import requests
import json
import threading
from setting import *


def enter_request(number):
    data = {
        "type": "enter",
        "studentNo": number,
        "numberOfPeople": 1,
        "time":datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    }
    json_data = json.dumps(data)
    response = requests.post(
        GAS_URL,
        data=json_data, 
        headers={"Content-Type": "application/json"}
    )


def leave_request(number, equipments):
    data = {
        "type": "leave",
        "studentNo": number,
        "equipments": ", ".join(equipments),
        "time":datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    }
    json_data = json.dumps(data)
    response = requests.post(
        GAS_URL,
        data=json_data, 
        headers={"Content-Type": "application/json"}
    )
    

def main(page: ft.Page):
    #ページ全体のテーマの設定
    page.vertical_alignment = ft. MainAxisAlignment.CENTER
    page.fonts = {"m1":"fonts/m1plus.ttf"}
    page.theme = ft.Theme(font_family="m1")
    page.theme_mode = ft.ThemeMode.LIGHT

    # キーボード入力の受付
    def on_keyboard(e: ft.KeyboardEvent):
        if page.route == "/" and e.shift and e.ctrl and e.key == "C":
            page.views[-1].on_button_click()
        if page.route == "/leave" and e.shift and e.ctrl:
            if e.key == "C": page.views[-1].on_clear_button_click()
            if e.key == "B": page.views[-1].on_back_button_click()
            if e.key == "N": page.views[-1].on_send_button_click()

    page.on_keyboard_event = on_keyboard

    #ルーティング変更時の処理
    def route_change(e):
        if page.route == "/":
            page.views.clear()
            page.views.append( index.Index() )
        elif page.route == "/entered":
            # 入室のリクエスト処理(非同期処理)
            addEntryLog(page.views[-1].data["studentNo"])
            asyncio.new_event_loop().run_in_executor(None, enter_request, page.views[-1].data["studentNo"])
            ##################
            page.views.append( entered.Entered(data=page.views[-1].data["studentNo"]))
            time.sleep(4)
            page.views.pop()
            top_view = page.views[-1]
            page.go("/")

        elif page.route == "/leave":
            # 退室時の使用設備選択　
            page.views.append( used_equipment.UsedEquipment(data=page.views[-1].data))

        elif page.route == "/left":
            # 退室のリクエスト処理（非同期）
            removeEntryLog(page.views[-1].data["studentNo"])
            asyncio.new_event_loop().run_in_executor(None, leave_request, page.views[-1].data["studentNo"], page.views[-1].data["equipments"])
            ##################
            page.views.append( left.Left() )
            time.sleep(2.5)
            page.views.pop()
            top_view = page.views[-1]
            page.go("/")
            

    #ルート変更時の処理を指定
    page.on_route_change = route_change
    
    # 時計用のティック処理（１秒毎）
    def on_tick (page: ft.Page):
        while page.th.running is True:
            page.update()
            time.sleep(1)

    # ティック処理の開始
    def start_tick(page):
        page.th = threading.Thread( target=on_tick, args=[page], daemon=True)
        page.th.running = True
        page.th.start() 

    # ビューとルートのリセット
    page.views.clear()
    page.go("/")

    page.window.full_screen = True  # フルスクリーンをON
    start_tick(page)                # ページのティックを開始
    page.update()                   # 再描画

checkCsv()

ft.app(main)