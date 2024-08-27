"""
코드 제가 짠거 아니고 어디서 긁어온거라 좀 더러울 수 있습니다 ㅜㅜ
나중에 한번 리팩토링 하고 원본 링크도 추가하겠습니다
"""

from dotenv import load_dotenv

import time, win32con, win32api, win32gui
import os

load_dotenv()
kakao_opentalk_name = os.environ.get("GROUP_NAME")


def sendText(chatroom_name, text):
    # # 핸들 _ 채팅방
    hwndMain = win32gui.FindWindow(None, chatroom_name)
    hwndEdit = win32gui.FindWindowEx(hwndMain, None, "RichEdit50W", None)

    win32api.SendMessage(hwndEdit, win32con.WM_SETTEXT, 0, text)
    sendReturn(hwndEdit)


def sendReturn(hwnd):
    win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
    time.sleep(0.01)
    win32api.PostMessage(hwnd, win32con.WM_KEYUP, win32con.VK_RETURN, 0)


def openChatroom(chatroom_name):
    hwndkakao = win32gui.FindWindow(None, "카카오톡")
    hwndkakao_edit1 = win32gui.FindWindowEx(hwndkakao, None, "EVA_ChildWindow", None)
    hwndkakao_edit2_1 = win32gui.FindWindowEx(hwndkakao_edit1, None, "EVA_Window", None)
    hwndkakao_edit2_2 = win32gui.FindWindowEx(hwndkakao_edit1, hwndkakao_edit2_1, "EVA_Window", None)
    hwndkakao_edit3 = win32gui.FindWindowEx(hwndkakao_edit2_2, None, "Edit", None)

    win32api.SendMessage(hwndkakao_edit3, win32con.WM_SETTEXT, 0, chatroom_name)
    time.sleep(1)   # 안정성 위해 필요
    sendReturn(hwndkakao_edit3)
    time.sleep(1)


if __name__ == '__main__':
    openChatroom(kakao_opentalk_name)
    sendText(kakao_opentalk_name, "테스트")
