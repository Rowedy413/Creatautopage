#!/usr/bin/env python3
# mmg_final_premium.py
# Premium MMG Auto Page Creator — OWNER ROWEDY KIING (RAJASTHAN)
# Requirements: requests, colorama, bs4
# Usage: python mmg_final_premium.py

import os
import sys
import time
import random
import re
import json
from concurrent.futures import ThreadPoolExecutor

# Auto-install missing packages
def ensure(pkg, import_name=None):
    try:
        __import__(import_name or pkg)
    except Exception:
        os.system(f"{sys.executable} -m pip install {pkg}")

for package in ("requests", "colorama", "bs4"):
    ensure(package)

import requests
from time import sleep
from colorama import init as colorama_init, Fore, Style
from bs4 import BeautifulSoup as BS

colorama_init(autoreset=True)

# ---------------- CONFIG ----------------
DEFAULT_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.207 Safari/537.36"
THREADS = 12
OUTPUT_LOG = "created_pages.txt"

# ---------------- Stylers ----------------
COLORS = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.MAGENTA, Fore.BLUE]

def rnd_color(): 
    return random.choice(COLORS)

def owner_badge():
    return f"{Style.BRIGHT}{Fore.WHITE}[{Fore.MAGENTA}OWNER{Style.RESET_ALL}{Style.BRIGHT}{Fore.WHITE} {Fore.CYAN}ROWEDY KIING (RAJASTHAN){Style.RESET_ALL}{Style.BRIGHT}{Fore.WHITE}]"

def cprint(text, color=Fore.WHITE, nl=True, end="\n"):
    if nl:
        print(color + str(text) + Style.RESET_ALL, end=end)
    else:
        print(color + str(text) + Style.RESET_ALL, end=end)

def typewriter(text, delay=0.002):
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        sleep(delay)
    print()

# ---------------- Banner ----------------
BANNER = r"""
███╗   ███╗███╗   ███╗
████╗ ████║████╗ ████║
██╔████╔██║██╔████╔██║
██║╚██╔╝██║██║╚██╔╝██║
██║ ╚═╝ ██║██║ ╚═╝ ██║
╚═╝     ╚═╝╚═╝     ╚═╝
"""

def print_rainbow_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    for line in BANNER.splitlines():
        colored = ""
        for ch in line:
            if ch == " ":
                colored += " "
            else:
                colored += random.choice(COLORS) + ch + Style.RESET_ALL
        typewriter(colored, delay=0.003)
    typewriter(f"{Fore.YELLOW}{Style.BRIGHT}OWNER ROWEDY KIING (RAJASTHAN)\n", delay=0.004)
    typewriter(f"{Fore.CYAN}{Style.BRIGHT}MMG - Auto Page Creator Premium\n", delay=0.003)
    print()

# ---------------- Page creation logic ----------------
names_fast = ["Rowedy kiing", "kiing", "baba tillu", "tera baap", "tusar ki mummy"]
last_names = [str(i) for i in range(1, 101)]
page_total = []

def make_headers(user_agent, cookie_string):
    return {
        'authority': 'www.facebook.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'cache-control': 'max-age=0',
        'user-agent': user_agent,
        'cookie': cookie_string
    }

def parse_cookie_string(cs):
    return cs.strip()

def save_log(entry):
    try:
        with open(OUTPUT_LOG, "a", encoding="utf-8") as f:
            f.write(entry + "\n")
    except Exception:
        pass

def show_box(msg, color=Fore.GREEN):
    """Stylish console box for success/failure."""
    border = "═" * (len(msg) + 4)
    print(color + f"╔{border}╗")
    print(color + f"║  {msg}  ║")
    print(color + f"╚{border}╝" + Style.RESET_ALL)

def create_page_for_cookie(coki, user_agent):
    cookie_str = parse_cookie_string(coki)
    headers = make_headers(user_agent, cookie_str)
    session = requests.Session()
    session.headers.update({'user-agent': user_agent})
    try:
        r = session.get('https://www.facebook.com/pages/creation/?ref_type=launch_point', headers=headers, timeout=20)
    except requests.exceptions.RequestException as e:
        show_box(f"Network error for '{cookie_str[:18]}...': {e}", Fore.RED)
        save_log(f"NETERR|{cookie_str[:18]}|{e}")
        return

    if r.status_code != 200:
        show_box(f"HTTP {r.status_code} loading page (prefix '{cookie_str[:18]}...')", Fore.RED)
        save_log(f"HTTP{r.status_code}|{cookie_str[:18]}")
        return

    html = r.text

    # extract tokens (best-effort)
    try: usr = re.search(r'c_user=(\d+)', cookie_str).group(1)
    except: usr = "0"
    try: dts = re.search(r'fb_dtsg\"\s*:\s*\"([^"]+)\"', html).group(1)
    except: dts = ""
    try: jzt = re.search(r'&jazoest=(.*?)",', html).group(1)
    except: jzt = ""
    try: lsd = re.search(r'"LSD",.*?,{"token":"(.*?)"', html).group(1)
    except: lsd = ""
    try: rev = re.search(r'{"rev":(.*?)}', html).group(1)
    except: rev = "0"

    name_p = f"{random.choice(names_fast)} {random.choice(last_names)}"
    bio_p = "PAGE CREATED BY ROWEDY KIING"

    variables_json = json.dumps({
        "input": {
            "bio": bio_p,
            "categories": ["1350536325044173","200597389954350","123377808095874"],
            "creation_source": "comet",
            "name": name_p,
            "page_referrer": "launch_point",
            "actor_id": usr,
            "client_mutation_id": "3"
        }
    }, separators=(",", ":"))

    data = {
        'av': usr,
        '__user': usr,
        '__a': '1',
        '__req': '1i',
        '__hs': '19666.HYP:comet_pkg.2.1..2.1',
        'dpr': '1',
        '__ccg': 'MODERATE',
        '__rev': rev,
        'fb_dtsg': dts,
        'jazoest': jzt,
        'lsd': lsd,
        '__aaid': '0',
        'variables': variables_json,
        'server_timestamps': 'true',
        'doc_id': '5296879960418435',
    }

    post_headers = headers.copy()
    post_headers.update({'content-type': 'application/x-www-form-urlencoded', 'accept': 'application/json, text/javascript, */*; q=0.01'})

    try:
        resp = session.post('https://www.facebook.com/api/graphql/', headers=post_headers, data=data, timeout=25)
    except requests.exceptions.RequestException as e:
        show_box(f"POST error for uid {usr}: {e}", Fore.RED)
        save_log(f"POSTERR|{usr}|{e}")
        return

    try:
        parsed = resp.json()
    except Exception:
        show_box(f"Invalid JSON response for uid {usr} (status {resp.status_code})", Fore.RED)
        save_log(f"INVALIDJSON|{usr}|HTTP{resp.status_code}")
        return

    try:
        add = parsed.get('data', {}).get('additional_profile_plus_create', {})
        additional_profile_id = add.get('additional_profile', {}).get('id')
        page_id = add.get('page', {}).get('id')
        if additional_profile_id or page_id:
            page_url = f"https://facebook.com/{page_id}" if page_id else f"https://facebook.com/profile.php?id={additional_profile_id}"
            page_total.append(page_id or additional_profile_id)
            show_box(f"SUCCESS! {name_p} | uid={usr} | URL: {page_url}", Fore.GREEN)
            save_log(f"OK|{usr}|{additional_profile_id}|{page_id}|{page_url}|{name_p}")
        else:
            reason = parsed.get('errors') or parsed.get('error_summary') or parsed
            show_box(f"FAIL uid={usr}: {str(reason)[:250]}", Fore.YELLOW)
            save_log(f"FAIL|{usr}|{str(reason)[:250]}")
    except Exception as e:
        show_box(f"Unexpected parse error: {e}", Fore.RED)
        save_log(f"EXC|{usr}|{e}")

# ---------------- Modes ----------------
def run_mode_paste():
    cprint(f"\n{owner_badge()} {Fore.CYAN}Paste cookies (multi-line). Press Enter twice to finish.", Fore.WHITE)
    lines = []
    while True:
        line = input()
        if not line.strip():
            break
        lines.append(line.strip())
    if not lines:
        cprint(f"{owner_badge()} {Fore.RED}No cookies pasted.", Fore.WHITE)
        return
    cookies = []
    for ln in lines:
        if ln.count("c_user=") > 1:
            parts = re.split(r'\s*(?=c_user=)', ln)
            cookies.extend([p.strip() for p in parts if p.strip()])
        else:
            cookies.append(ln)
    cprint(f"{owner_badge()} {Fore.MAGENTA}Processing {len(cookies)} cookies with {THREADS} threads...", Fore.WHITE)
    with ThreadPoolExecutor(max_workers=THREADS) as ex:
        for ck in cookies:
            ex.submit(create_page_for_cookie, ck, DEFAULT_UA)

# ---------------- Main ----------------
def main():
    print_rainbow_banner()
    run_mode_paste()
    cprint(f"\n{owner_badge()} {Fore.GREEN}Run finished. Pages collected: {len(page_total)}", Fore.WHITE)
    for i, pid in enumerate(page_total, start=1):
        cprint(f"{owner_badge()} {Fore.GREEN}{i}. {pid}", Fore.WHITE)
    cprint(f"{owner_badge()} {Fore.YELLOW}Saved log: {OUTPUT_LOG}", Fore.WHITE)
    cprint(f"{owner_badge()} {Fore.CYAN}Exiting in 5 seconds...", Fore.WHITE)
    sleep(5)

if __name__ == "__main__":
    main()
