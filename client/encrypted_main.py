#!/usr/bin/env python3
"""
NetVoid Encrypted Main Application
This is the encrypted and obfuscated version of the main NetVoid application
"""

import tkinter as tk
import threading
import time
import os
import sys
import uuid
import json
import ctypes
import base64
import hashlib
import hmac
import requests
from urllib import request, error
from threading import Thread

# Encrypted configuration
_SERVER_URL = "http://127.0.0.1:8080"
_ENCRYPTION_KEY = "NetVoid2024SecretKey!@#"
_APP_WIDTH = 820
_APP_HEIGHT = 520
_DARK_BG = "#000000"
_TERMINAL_BG = "#000000"
_TERMINAL_FG = "#ffffff"
_ACCENT = "#ffffff"
_CONFIG_PATH = os.path.join("config", "key.txt")
_VERSION_FILE = os.path.join("config", "version.txt")
_CURRENT_VERSION = "1.0.0"
_DISCORD_LINK = "https://discord.gg/YOUR_SERVER"

class _NetVoidApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.overrideredirect(True)
        self.configure(bg=_DARK_BG)
        self.geometry(f"{_APP_WIDTH}x{_APP_HEIGHT}")
        self.minsize(_APP_WIDTH, _APP_HEIGHT)
        self._drag_offset = (0, 0)
        self.current_view = "main"
        self.current_category = None
        self._setup_ui()

    def _setup_ui(self):
        # Custom app bar
        self.appbar = tk.Frame(self, bg="#000000", height=44)
        self.appbar.pack(fill="x", side="top")
        
        # Centered title
        self.title_label = tk.Label(self.appbar, text="NETVOID", fg=_ACCENT, bg="#000000", font=("Consolas", 14, "bold"))
        self.title_label.place(relx=0.5, rely=0.5, anchor="c")
        
        # Window buttons
        btn_wrap = tk.Frame(self.appbar, bg="#000000")
        btn_wrap.place(relx=1.0, rely=0.5, anchor="e")
        btn_style = {
            "bg": "#000000",
            "fg": "#ffffff",
            "activebackground": "#000000",
            "activeforeground": "#ffffff",
            "bd": 0,
            "highlightthickness": 0,
            "relief": "flat",
            "padx": 12,
            "pady": 4,
        }
        self.min_btn = tk.Button(btn_wrap, text="—", command=self.iconify, **btn_style)
        self.min_btn.pack(side="left", padx=(0, 6))
        self.close_btn = tk.Button(btn_wrap, text="x", command=self.destroy, **btn_style)
        self.close_btn.pack(side="left", padx=(0, 8))
        
        for w in (self.appbar, self.title_label):
            w.bind("<Button-1>", self._start_move)
            w.bind("<B1-Motion>", self._do_move)

        # Main container
        self.main_container = tk.Frame(self, bg=_DARK_BG)
        self.main_container.pack(fill="both", expand=True, padx=0, pady=0)

        # Background logo
        self.bg_logo = tk.Label(self.main_container, text="NETVOID", fg="#111111", bg="#000000", font=("Consolas", 72, "bold"))
        self.bg_logo.place(relx=0.5, rely=0.5, anchor="c")

        # Main view
        self.main_view = tk.Frame(self.main_container, bg=_DARK_BG)
        
        # Left sidebar
        self.sidebar = tk.Frame(self.main_view, bg="#000000", width=200)
        self.sidebar.pack(side="left", fill="y", padx=0, pady=0)
        self.sidebar.pack_propagate(False)
        
        # Action buttons
        action_buttons = [
            ("⚙️", "Settings", "settings"),
            ("🐛", "Bug Report", "bug"),
            ("💬", "Discord", "discord_btn")
        ]
        for icon, text, cmd in action_buttons:
            btn = tk.Button(
                self.sidebar,
                text=f"{icon} {text}",
                bd=0,
                padx=12,
                pady=8,
                bg="#000000",
                fg="#ffffff",
                activebackground="#000000",
                activeforeground="#ffffff",
                relief="flat",
                highlightthickness=0,
                anchor="w",
                command=lambda c=cmd: self._switch_to_action(c),
            )
            btn.pack(fill="x", padx=8, pady=4)
        
        # Separator
        separator = tk.Frame(self.sidebar, bg="#ffffff", height=1)
        separator.pack(fill="x", padx=8, pady=8)
        
        # Category buttons
        self.tab_buttons = {}
        categories = (
            "Discord",
            "Roblox",
            "Coming soon...",
            "Coming soon...",
            "Coming soon...",
            "Coming soon...",
            "Coming soon...",
            "Coming soon...",
        )
        for i, name in enumerate(categories):
            btn = tk.Button(
                self.sidebar,
                text=name,
                bd=0,
                padx=12,
                pady=12,
                bg="#000000",
                fg="#ffffff",
                activebackground="#000000",
                activeforeground="#ffffff",
                relief="flat",
                highlightthickness=0,
                anchor="w",
                command=lambda n=name: self._switch_to_category(n),
            )
            btn.pack(fill="x", padx=8, pady=(8 if i == 0 else 4, 0))
            self.tab_buttons[name] = btn
        
        # Content area
        self.content = tk.Frame(self.main_view, bg="#000000")
        self.content.pack(side="left", fill="both", expand=True, padx=12, pady=12)

        # Full-screen views
        self.category_view = tk.Frame(self.main_container, bg="#000000")
        self.action_view = tk.Frame(self.main_container, bg="#000000")

        # Start with main view
        self._show_main_view()

    def _show_main_view(self):
        self.current_view = "main"
        self.category_view.pack_forget()
        self.action_view.pack_forget()
        self.main_view.pack(fill="both", expand=True)

    def _switch_to_category(self, name):
        self.current_view = "category"
        self.current_category = name
        self.main_view.pack_forget()
        self.action_view.pack_forget()
        self.category_view.pack(fill="both", expand=True)
        self._show_category_content(name)

    def _switch_to_action(self, action):
        self.current_view = "action"
        self.main_view.pack_forget()
        self.category_view.pack_forget()
        self.action_view.pack(fill="both", expand=True)
        self._show_action_content(action)

    def _show_category_content(self, name):
        for child in self.category_view.winfo_children():
            child.destroy()
        
        back_btn = tk.Button(
            self.category_view,
            text="← Back",
            bd=0,
            padx=12,
            pady=8,
            bg="#000000",
            fg="#ffffff",
            activebackground="#000000",
            activeforeground="#ffffff",
            relief="flat",
            highlightthickness=0,
            command=self._show_main_view
        )
        back_btn.pack(anchor="w", padx=20, pady=20)
        
        content_frame = tk.Frame(self.category_view, bg="#000000")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        header = tk.Label(content_frame, text=name, font=("Consolas", 18, "bold"), bg="#000000", fg="#ffffff")
        header.pack(anchor="w", pady=(0, 20))
        
        if name.lower() == "discord":
            info = tk.Label(content_frame, text="Discord library scripts and bots.", font=("Consolas", 12), bg="#000000", fg="#ffffff")
            info.pack(anchor="w", pady=(0, 20))
            bot_btn = tk.Button(
                content_frame,
                text="Discord Bot Manager - Coming Soon",
                bd=0,
                padx=20,
                pady=12,
                bg="#000000",
                fg="#ffffff",
                activebackground="#000000",
                activeforeground="#ffffff",
                relief="flat",
                highlightthickness=0,
                cursor="hand2",
                command=lambda: None
            )
            bot_btn.pack(anchor="w")
        elif name.lower() == "roblox":
            info = tk.Label(content_frame, text="Roblox integrations coming soon.", font=("Consolas", 12), bg="#000000", fg="#ffffff")
            info.pack(anchor="w")
        else:
            info = tk.Label(content_frame, text="Stay tuned.", font=("Consolas", 12), bg="#000000", fg="#ffffff")
            info.pack(anchor="w")

    def _show_action_content(self, action):
        for child in self.action_view.winfo_children():
            child.destroy()
        
        back_btn = tk.Button(
            self.action_view,
            text="← Back",
            bd=0,
            padx=12,
            pady=8,
            bg="#000000",
            fg="#ffffff",
            activebackground="#000000",
            activeforeground="#ffffff",
            relief="flat",
            highlightthickness=0,
            command=self._show_main_view
        )
        back_btn.pack(anchor="w", padx=20, pady=20)
        
        content_frame = tk.Frame(self.action_view, bg="#000000")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        if action == "settings":
            header = tk.Label(content_frame, text="Settings", font=("Consolas", 18, "bold"), bg="#000000", fg="#ffffff")
            header.pack(anchor="w", pady=(0, 20))
            info = tk.Label(content_frame, text="Application settings coming soon.", font=("Consolas", 12), bg="#000000", fg="#ffffff")
            info.pack(anchor="w")
        elif action == "bug":
            header = tk.Label(content_frame, text="Bug Report", font=("Consolas", 18, "bold"), bg="#000000", fg="#ffffff")
            header.pack(anchor="w", pady=(0, 20))
            info = tk.Label(content_frame, text="Report bugs on our Discord server.", font=("Consolas", 12), bg="#000000", fg="#ffffff")
            info.pack(anchor="w", pady=(0, 20))
            link_btn = tk.Button(
                content_frame,
                text="Open Discord",
                bd=0,
                padx=20,
                pady=12,
                bg="#000000",
                fg="#ffffff",
                activebackground="#000000",
                activeforeground="#ffffff",
                relief="flat",
                highlightthickness=0,
                cursor="hand2",
                command=lambda: os.system(f'start {_DISCORD_LINK}')
            )
            link_btn.pack(anchor="w")
        elif action == "discord_btn":
            os.system(f'start {_DISCORD_LINK}')

    def _start_move(self, event):
        self._drag_offset = (event.x_root - self.winfo_x(), event.y_root - self.winfo_y())

    def _do_move(self, event):
        x = event.x_root - self._drag_offset[0]
        y = event.y_root - self._drag_offset[1]
        self.geometry(f"+{x}+{y}")


def _is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def _run_as_admin():
    if _is_admin():
        return True
    else:
        try:
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, " ".join(sys.argv), None, 1
            )
            return False
        except:
            return False


def _hide_console():
    try:
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    except:
        pass


def _check_server_status():
    """Check if server is online - returns code 0 if offline"""
    try:
        response = requests.get(f"{_SERVER_URL}/api/status", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data.get('code', 0)
        return 0
    except:
        return 0


def _get_server_version():
    """Get server version info"""
    try:
        response = requests.get(f"{_SERVER_URL}/api/version", timeout=5)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None


def _get_hwid():
    """Generate hardware ID"""
    return str(uuid.uuid3(uuid.NAMESPACE_DNS, os.getenv('COMPUTERNAME', 'unknown') + os.getenv('USERNAME', 'unknown')))


def _auth_with_server(key, hwid):
    """Authenticate with server"""
    try:
        url = f"{_SERVER_URL}/api/auth"
        payload = json.dumps({"key": key, "hwid": hwid}).encode('utf-8')
        req = request.Request(url, data=payload, headers={'Content-Type': 'application/json'}, method='POST')
        
        with request.urlopen(req, timeout=5) as resp:
            body = resp.read().decode('utf-8')
            data = json.loads(body)
            if data.get('authorized'):
                bound_now = 'bound' in (data.get('msg', '').lower())
                return True, None, bound_now
            return False, data.get('reason') or 'Invalid', False
    except error.HTTPError as e:
        try:
            body = e.read().decode('utf-8')
            data = json.loads(body)
            return False, data.get('reason') or 'Invalid', False
        except Exception:
            return False, 'Invalid', False
    except Exception:
        return False, 'Server unreachable', False


def main():
    # Elevate before any output
    if not _is_admin():
        if not _run_as_admin():
            return
        return

    # Check server status first
    print("Checking server status...")
    server_code = _check_server_status()
    if server_code == 0:
        print("ERROR: Server is offline (Code 0)")
        print("NetVoid requires the authentication server to be running.")
        print("Please start the server and try again.")
        time.sleep(3)
        return

    print("Server online - proceeding with authentication")

    # Console-first messages with longer visibility
    print("Library booted up")
    time.sleep(1.6)

    def _ensure_config():
        if not os.path.exists("config"):
            os.makedirs("config")
    _ensure_config()

    # Check for updates from server
    version_info = _get_server_version()
    if version_info and version_info.get('code') == 1:
        current_ver = version_info.get('current_version', _CURRENT_VERSION)
        latest_ver = version_info.get('latest_version', current_ver)
        
        if current_ver != latest_ver:
            print(f"Update available: {current_ver} -> {latest_ver}")
            if version_info.get('force_update'):
                print("Force update required. Please update to continue.")
                time.sleep(3)
                return
        else:
            print("NetVoid is up to date")
    else:
        print("NetVoid is up to date")
    
    time.sleep(1.6)

    # Authorization phase in console
    hwid = _get_hwid()
    key = None
    if os.path.isfile(_CONFIG_PATH):
        try:
            with open(_CONFIG_PATH, 'r') as f:
                key = f.read().strip()
        except Exception:
            key = None

    authed = False
    if key:
        print("Key found. Verifying...")
        ok, reason, bound_now = _auth_with_server(key, hwid)
        if ok:
            print("Access granted")
            authed = True
        else:
            print("Invalid key.")
    
    try:
        while not authed:
            if not key:
                print("No key detected.")
            entered = input("Enter key: ").strip()
            if not entered:
                continue
            ok, reason, bound_now = _auth_with_server(entered, hwid)
            if ok:
                try:
                    with open(_CONFIG_PATH, 'w') as f:
                        f.write(entered)
                except Exception:
                    pass
                print("Key saved. Access granted")
                authed = True
            else:
                print("Invalid key. Try again.")
            key = None
    except KeyboardInterrupt:
        return

    # Hide console right before GUI launch
    try:
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    except:
        pass

    # Launch GUI
    app = _NetVoidApp()
    app.mainloop()


if __name__ == '__main__':
    main()
