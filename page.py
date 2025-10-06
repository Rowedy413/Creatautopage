#!/usr/bin/env python3
# mmg_final_with_url.py
# MMG final — OWNER badge, multi-paste, file mode, direct URL on success, stylish UI
# Requirements: requests, colorama, bs4
# Usage: python mmg_final_with_url.py

import os
import sys
import time
import random
import re
import json
from concurrent.futures import ThreadPoolExecutor

# --- Auto-install missing packages if necessary ---
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

# --- small stylers ---
COLORS = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.MAGENTA, Fore.BLUE]
def rnd_color(): return random.choice(COLORS)
def owner_badge():
    return f"{Style.BRIGHT}{Fore.WHITE}[{Fore.MAGENTA}OWNER{Style.RESET_ALL}{Style.BRIGHT}{Fore.WHITE} {Fore.CYAN}MMG{Style.RESET_ALL}{Style.BRIGHT}{Fore.WHITE}]"

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
    lines = BANNER.splitlines()
    for line in lines:
        colored = ""
        for ch in line:
            if ch == " ":
                colored += " "
            else:
                colored += random.choice(COLORS) + ch + Style.RESET_ALL
        typewriter(colored, delay=0.003)
    typewriter(f"\n    {Fore.YELLOW}{Style.BRIGHT}MMG - Auto Page Creator\n", delay=0.003)
    print()

# ---------------- Page creation logic ----------------
names_fast = ["Rowedy kiing", "kiing", "baba tillu", "tera baap", "tusar ki mummy"]
last_names = [str(i) for i in range(1, 101)]
page_total = []

def make_headers(cookie_string):
    headers_global = {
        'authority': 'www.facebook.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,/;q=0.8',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'cache-control': 'max-age=0',
        'dpr': '0.9',
        'sec-ch-prefers-color-scheme': 'light',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-full-version-list': '"Not_A Brand";v="8.0.0.0", "Chromium";v="120.0.6099.109", "Google Chrome";v="120.0.6099.109"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"10.0.0"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': DEFAULT_UA,
        'viewport-width': '983',
        'cookie': cookie_string
    }
    return headers_global

def parse_cookie_string(cs):
    return cs.strip()

def save_log(entry):
    try:
        with open(OUTPUT_LOG, "a", encoding="utf-8") as f:
            f.write(entry + "\n")
    except Exception:
        pass

def create_page_for_cookie(coki):
    cookie_str = parse_cookie_string(coki)
    headers = make_headers(cookie_str)
    session = requests.Session()
    session.headers.update({'user-agent': DEFAULT_UA, 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9'})
    try:
        r = session.get('https://www.facebook.com/pages/creation/?ref_type=launch_point', headers=headers, timeout=20)
    except requests.exceptions.RequestException as e:
        cprint(f"{owner_badge()} {Fore.RED}Network error for cookie prefix '{cookie_str[:18]}...': {e}")
        save_log(f"NETERR|{cookie_str[:18]}|{e}")
        return

    if r.status_code != 200:
        cprint(f"{owner_badge()} {Fore.RED}HTTP {r.status_code} loading creation page (prefix '{cookie_str[:18]}...').")
        save_log(f"HTTP{r.status_code}|{cookie_str[:18]}")
        return

    html = r.text

    # --- extract tokens (best-effort) ---
    try:
        usr = re.search(r'__user=(.?)&', html).group(1)
    except Exception:
        m = re.search(r'c_user=(\d+)', cookie_str)
        usr = m.group(1) if m else "0"
    try:
        rev = re.search(r'{"rev":(.?)}', html).group(1)
    except:
        rev = "0"
    try:
        dts = re.search(r'"DTSGInitialData",,{"token":"(.?)"', html).group(1)
    except:
        dts = ""
    try:
        spr = re.search(r'"__spin_r":(.?),', html).group(1)
    except:
        spr = "0"
    try:
        spt = re.search(r'"__spin_t":(.*?),', html).group(1)
    except:
        spt = "0"

    name_p = f"{random.choice(names_fast)} {random.choice(last_names)}"
    bio_p = "PAGE CREATED BY MMG OWNER"

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
        '__s': 'qvdp97:zb23lw:givv21',
        '__comet_req': '15',
        'fb_dtsg': dts,
        'jazoest': '0',
        'lsd': '',
        '__aaid': '0',
        '__spin_r': spr,
        '__spin_b': 'trunk',
        '__spin_t': spt,
        'fb_api_caller_class': 'RelayModern',
        'fb_api_req_friendly_name': 'AdditionalProfilePlusCreationMutation',
        'variables': variables_json,
        'server_timestamps': 'true',
        'doc_id': '5296879960418435',
    }

    post_headers = headers.copy()
    post_headers.update({
        'content-type': 'application/x-www-form-urlencoded',
        'accept': 'application/json, text/javascript, /; q=0.01'
    })

    try:
        resp = session.post('https://www.facebook.com/api/graphql/', headers=post_headers, data=data, timeout=25)
    except requests.exceptions.RequestException as e:
        cprint(f"{owner_badge()} {Fore.RED}POST error for uid {usr}: {e}")
        save_log(f"POSTERR|{usr}|{e}")
        return

    try:
        parsed = resp.json()
    except Exception:
        cprint(f"{owner_badge()} {Fore.RED}Invalid JSON response for uid {usr} (status {resp.status_code})")
        save_log(f"INVALIDJSON|{usr}|HTTP{resp.status_code}")
        return

    try:
        add = parsed.get('data', {}).get('additional_profile_plus_create', {})
        additional_profile_id = add.get('additional_profile', {}).get('id')
        page_id = add.get('page', {}).get('id')
        if additional_profile_id or page_id:
            page_url = f"https://facebook.com/{page_id}" if page_id else f"https://facebook.com/profile.php?id={additional_profile_id}"
            page_total.append(page_id or additional_profile_id)
            msg = f"Created Page: {name_p} | profile_id={additional_profile_id} | page_id={page_id} | uid={usr}"
            cprint(f"{owner_badge()} {Fore.GREEN}{msg}")
            cprint(f"{owner_badge()} {Fore.CYAN}Direct URL → {Fore.YELLOW}{page_url}")
            save_log(f"OK|{usr}|{additional_profile_id}|{page_id}|{page_url}|{name_p}")
        else:
            reason = parsed.get('errors') or parsed.get('error_summary') or parsed
            cprint(f"{owner_badge()} {Fore.YELLOW}Could not create page for uid={usr}. Info: {str(reason)[:250]}")
            save_log(f"FAIL|{usr}|{str(reason)[:250]}")
    except Exception as e:
        cprint(f"{owner_badge()} {Fore.RED}Unexpected parse error: {e}")
        save_log(f"EXC|{usr}|{e}")

# ---------------- Modes ----------------
def run_mode_paste():
    cprint(f"\n{owner_badge()} {Fore.CYAN}Paste cookies (multi-line). After pasting press Enter then type '{Fore.YELLOW}END{Fore.CYAN}' on a new line to finish.", Fore.WHITE)
    lines = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line.strip().upper() == "END":
            break
        if line.strip():
            lines.append(line.strip())
    if not lines:
        cprint(f"{owner_badge()} {Fore.RED}No cookies pasted. Returning to main.", Fore.WHITE)
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
            ex.submit(create_page_for_cookie, ck)

def run_mode_file():
    cprint(f"\n{owner_badge()} {Fore.CYAN}Enter cookies filename (each line = one cookie):", Fore.WHITE, nl=False)
    fn = input(" ").strip()
    if not fn or not os.path.isfile(fn):
        cprint(f"{owner_badge()} {Fore.RED}File not found or empty: {fn}")
        return
    with open(fn, 'r', encoding='utf-8', errors='ignore') as f:
        lines = [ln.strip() for ln in f.read().splitlines() if ln.strip()]
    if not lines:
        cprint(f"{owner_badge()} {Fore.RED}No cookies found in file.", Fore.WHITE)
        return
    cprint(f"{owner_badge()} {Fore.MAGENTA}Loaded {len(lines)} cookies. Starting threads...", Fore.WHITE)
    with ThreadPoolExecutor(max_workers=THREADS) as ex:
        for ck in lines:
            ex.submit(create_page_for_cookie, ck)

def run_mode_quick():
    cprint(f"{owner_badge()} {Fore.CYAN}Paste many cookies quickly (one per line). Press Enter on empty line to finish:", Fore.WHITE)
    temp = []
    while True:
        ln = input()
        if not ln.strip():
            break
        temp.append(ln.strip())
    if not temp:
        cprint(f"{owner_badge()} {Fore.RED}No cookies entered.")
        return
    cprint(f"{owner_badge()} {Fore.MAGENTA}Processing {len(temp)} cookies...", Fore.WHITE)
    with ThreadPoolExecutor(max_workers=THREADS) as ex:
        for ck in temp:
            ex.submit(create_page_for_cookie, ck)

# ---------------- Main ----------------
def main():
    print_rainbow_banner()
    cprint(f"{owner_badge()} {Fore.GREEN}Welcome! Stylish inputs will show OWNER MMG badge.", Fore.WHITE)
    cprint(f"{owner_badge()} {Fore.CYAN}Using default User-Agent internally.", Fore.WHITE)

    cprint(f"\n{owner_badge()} {Fore.CYAN}Choose mode:\n  1) Paste cookies (multi-line, end with 'END')\n  2) Load cookies from file\n  3) Quick multi-line paste (press Enter on blank line to finish)\n", Fore.WHITE)
    choice = input(f"{owner_badge()} Select 1, 2 or 3: ").strip()
    if choice == "1":
        run_mode_paste()
    elif choice == "2":
        run_mode_file()
    elif choice == "3":
        run_mode_quick()
    else:
        cprint(f"{owner_badge()} {Fore.RED}Invalid choice. Exiting.")
        return

    # --- Finish ---
    cprint(f"\n{owner_badge()} {Fore.GREEN}Run finished. Pages collected: {len(page_total)}", Fore.WHITE)
    for i, pid in enumerate(page_total, start=1):
        cprint(f"{owner_badge()} {Fore.GREEN}{i}. {pid}", Fore.WHITE)
    cprint(f"{owner_badge()} {Fore.YELLOW}Saved log: {OUTPUT_LOG}", Fore.WHITE)
    cprint(f"{owner_badge()} {Fore.CYAN}Exiting in 5 seconds...", Fore.WHITE)
    sleep(5)

if __name__ == "__main__":
    main()
