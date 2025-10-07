#!/usr/bin/env python3

import os
import sys
import time
import random
import re
import json
from concurrent.futures import ThreadPoolExecutor

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

DEFAULT_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.207 Safari/537.36"
THREADS = 12
OUTPUT_LOG = "created_pages.txt"

COLORS = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.MAGENTA, Fore.BLUE]
def rnd_color(): return random.choice(COLORS)

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
██████╗  ██████╗ ██╗    ██╗███████╗██████╗ ██╗   ██╗
██╔══██╗██╔═══██╗██║    ██║██╔════╝██╔══██╗╚██╗ ██╔╝
██████╔╝██║   ██║██║ █╗ ██║█████╗  ██║  ██║ ╚████╔╝ 
██╔══██╗██║   ██║██║███╗██║██╔══╝  ██║  ██║  ╚██╔╝  
██║  ██║╚██████╔╝╚███╔███╔╝███████╗██████╔╝   ██║   
╚═╝  ╚═╝ ╚═════╝  ╚══╝╚══╝ ╚══════╝╚═════╝    ╚═╝   
""" ROWEDY KIING AUTO PAGE CREATED

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
        typewriter(colored, delay=0.001)
    typewriter(f"\n{Fore.YELLOW}{Style.BRIGHT}    Auto Page Creator - Manual Naming Mode\n", delay=0.002)
    print()

def print_box(message, color=Fore.CYAN):
    width = len(message) + 4
    top_border = "╔" + "═" * width + "╗"
    content = f"║  {message}  ║"
    bottom_border = "╚" + "═" * width + "╝"
    
    print(color + top_border + Style.RESET_ALL)
    print(color + content + Style.RESET_ALL)
    print(color + bottom_border + Style.RESET_ALL)

page_total = []
page_names_list = []
profile_pic_url = None

def make_headers(user_agent, cookie_string):
    headers_global = {
        'authority': 'www.facebook.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
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
        'user-agent': user_agent,
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

def set_profile_picture(session, headers, page_id, profile_id, user_id, fb_dtsg, image_url):
    try:
        img_response = session.get(image_url, timeout=15)
        if img_response.status_code != 200:
            print_box(f"Failed to download image from URL", Fore.RED)
            save_log(f"IMG_DL_FAIL|{page_id}|HTTP{img_response.status_code}")
            return False
        
        image_content = img_response.content
        
        upload_headers = headers.copy()
        upload_headers.update({
            'accept': '*/*',
            'content-type': 'image/jpeg',
            'x-entity-length': str(len(image_content)),
            'x-entity-name': f'profile_pic_{page_id}.jpg',
            'x-entity-type': 'image/jpeg',
        })
        
        upload_url = f'https://upload.facebook.com/ajax/profile/picture/upload?profile_id={page_id}&photo_source=57&av={user_id}'
        
        upload_resp = session.post(upload_url, headers=upload_headers, data=image_content, timeout=30)
        
        if upload_resp.status_code == 200:
            try:
                result = upload_resp.json()
                if 'payload' in result or 'success' in str(result):
                    print(f"{Fore.GREEN}✓ Profile picture set successfully!{Style.RESET_ALL}")
                    save_log(f"DP_SET_OK|{page_id}")
                    return True
            except:
                pass
        
        print(f"{Fore.YELLOW}⚠ Profile picture upload attempted (check manually){Style.RESET_ALL}")
        save_log(f"DP_SET_PARTIAL|{page_id}|HTTP{upload_resp.status_code}")
        return False
        
    except Exception as e:
        print(f"{Fore.RED}✗ Profile picture error: {str(e)[:40]}{Style.RESET_ALL}")
        save_log(f"DP_SET_ERR|{page_id}|{e}")
        return False

def create_page_for_cookie(coki, user_agent):
    cookie_str = parse_cookie_string(coki)
    headers = make_headers(user_agent, cookie_str)
    session = requests.Session()
    session.headers.update({'user-agent': user_agent, 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9'})
    
    if not page_names_list:
        print_box(f"ERROR: No page names available!", Fore.RED)
        save_log(f"NONAME|{cookie_str[:18]}")
        return
    
    name_p = page_names_list.pop(0) if page_names_list else "Default Page"
    
    try:
        r = session.get('https://www.facebook.com/pages/creation/?ref_type=launch_point', headers=headers, timeout=20)
    except requests.exceptions.RequestException as e:
        print_box(f"Network Error: {str(e)[:50]}", Fore.RED)
        save_log(f"NETERR|{cookie_str[:18]}|{e}")
        return

    if r.status_code != 200:
        print_box(f"HTTP {r.status_code} Error", Fore.RED)
        save_log(f"HTTP{r.status_code}|{cookie_str[:18]}")
        return

    html = r.text

    try:
        usr = re.search(r'__user=(.*?)&', html).group(1)
    except Exception:
        m = re.search(r'c_user=(\d+)', cookie_str)
        usr = m.group(1) if m else "0"
    try:
        rev = re.search(r'{"rev":(.*?)}', html).group(1)
    except:
        rev = "0"
    try:
        dts = re.search(r'"DTSGInitialData",\[\],{"token":"(.*?)"', html).group(1)
    except:
        m = re.search(r'fb_dtsg\"\s*:\s*\"([^"]+)\"', html)
        dts = m.group(1) if m else ""
    try:
        jzt = re.search(r'&jazoest=(.*?)",', html).group(1)
    except:
        jzt = ""
    try:
        lsd = re.search(r'"LSD",\[\],{"token":"(.*?)"', html).group(1)
    except:
        lsd = ""
    try:
        spr = re.search(r'"__spin_r":(.*?),', html).group(1)
    except:
        spr = "0"
    try:
        spt = re.search(r'"__spin_t":(.*?),', html).group(1)
    except:
        spt = "0"

    bio_p = "PAGE CREATED BY ROWEDY"

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
        'jazoest': jzt,
        'lsd': lsd,
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
        'accept': 'application/json, text/javascript, */*; q=0.01'
    })

    try:
        resp = session.post('https://www.facebook.com/api/graphql/', headers=post_headers, data=data, timeout=25)
    except requests.exceptions.RequestException as e:
        print_box(f"POST Error: {str(e)[:50]}", Fore.RED)
        save_log(f"POSTERR|{usr}|{e}")
        return

    try:
        parsed = resp.json()
    except Exception:
        print_box(f"Invalid JSON Response", Fore.RED)
        save_log(f"INVALIDJSON|{usr}|HTTP{resp.status_code}")
        return

    try:
        add = parsed.get('data', {}).get('additional_profile_plus_create', {})
        additional_profile_id = add.get('additional_profile', {}).get('id')
        page_id = add.get('page', {}).get('id')
        if additional_profile_id or page_id:
            if page_id:
                page_url = f"https://facebook.com/{page_id}"
            else:
                page_url = f"https://facebook.com/profile.php?id={additional_profile_id}"
            page_total.append(page_id or additional_profile_id)
            
            print_box(f"OWNER ROWEDY KIING", Fore.GREEN)
            print(f"{Fore.CYAN}Profile ID: {Fore.YELLOW}{additional_profile_id}")
            print(f"{Fore.CYAN}Page ID: {Fore.YELLOW}{page_id}")
            print(f"{Fore.CYAN}URL: {Fore.YELLOW}{page_url}{Style.RESET_ALL}")
            
            if profile_pic_url:
                print(f"{Fore.MAGENTA}Setting profile picture...{Style.RESET_ALL}")
                set_profile_picture(
                    session, 
                    headers, 
                    page_id or additional_profile_id,
                    additional_profile_id,
                    usr, 
                    dts, 
                    profile_pic_url
                )
            print()
            
            save_log(f"OK|{usr}|{additional_profile_id}|{page_id}|{page_url}|{name_p}")
        else:
            reason = parsed.get('errors') or parsed.get('error_summary') or parsed
            print_box(f"Failed: {str(reason)[:30]}", Fore.YELLOW)
            save_log(f"FAIL|{usr}|{str(reason)[:250]}")
    except Exception as e:
        print_box(f"Parse Error: {str(e)[:50]}", Fore.RED)
        save_log(f"EXC|{usr}|{e}")

def run_mode_paste(user_agent):
    print_box("Paste cookies (multi-line)", Fore.CYAN)
    print(f"{Fore.YELLOW}After pasting, press Enter then type 'END' on a new line{Style.RESET_ALL}\n")
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
        print_box("No cookies pasted!", Fore.RED)
        return
    cookies = []
    for ln in lines:
        if ln.count("c_user=") > 1:
            parts = re.split(r'\s*(?=c_user=)', ln)
            cookies.extend([p.strip() for p in parts if p.strip()])
        else:
            cookies.append(ln)
    
    print_box(f"Enter page names (one per line, total {len(cookies)} needed)", Fore.MAGENTA)
    print(f"{Fore.YELLOW}Press Enter on empty line when done{Style.RESET_ALL}\n")
    
    for i in range(len(cookies)):
        name = input(f"{Fore.CYAN}Page {i+1} name: {Style.RESET_ALL}")
        if name.strip():
            page_names_list.append(name.strip())
        else:
            page_names_list.append(f"Auto Page {i+1}")
    
    print_box(f"Processing {len(cookies)} cookies with {THREADS} threads", Fore.MAGENTA)
    with ThreadPoolExecutor(max_workers=THREADS) as ex:
        for ck in cookies:
            ex.submit(create_page_for_cookie, ck, user_agent)

def run_mode_file(user_agent):
    print_box("Enter cookies filename", Fore.CYAN)
    fn = input(f"{Fore.YELLOW}Filename: {Style.RESET_ALL}").strip()
    if not fn:
        print_box("No filename provided!", Fore.RED)
        return
    if not os.path.isfile(fn):
        print_box(f"File not found: {fn}", Fore.RED)
        return
    with open(fn, 'r', encoding='utf-8', errors='ignore') as f:
        lines = [ln.strip() for ln in f.read().splitlines() if ln.strip()]
    if not lines:
        print_box("No cookies found in file!", Fore.RED)
        return
    
    print_box(f"Enter page names (one per line, total {len(lines)} needed)", Fore.MAGENTA)
    print(f"{Fore.YELLOW}Press Enter on empty line when done{Style.RESET_ALL}\n")
    
    for i in range(len(lines)):
        name = input(f"{Fore.CYAN}Page {i+1} name: {Style.RESET_ALL}")
        if name.strip():
            page_names_list.append(name.strip())
        else:
            page_names_list.append(f"Auto Page {i+1}")
    
    print_box(f"Loaded {len(lines)} cookies. Starting threads", Fore.MAGENTA)
    with ThreadPoolExecutor(max_workers=THREADS) as ex:
        for ck in lines:
            ex.submit(create_page_for_cookie, ck, user_agent)

def run_mode_quick(user_agent):
    print_box("Paste cookies (one per line)", Fore.CYAN)
    print(f"{Fore.YELLOW}Press Enter on empty line to finish{Style.RESET_ALL}\n")
    temp = []
    while True:
        ln = input()
        if not ln.strip():
            break
        temp.append(ln.strip())
    if not temp:
        print_box("No cookies entered!", Fore.RED)
        return
    
    print_box(f"Enter page names (one per line, total {len(temp)} needed)", Fore.MAGENTA)
    print(f"{Fore.YELLOW}Press Enter on empty line when done{Style.RESET_ALL}\n")
    
    for i in range(len(temp)):
        name = input(f"{Fore.CYAN}Page {i+1} name: {Style.RESET_ALL}")
        if name.strip():
            page_names_list.append(name.strip())
        else:
            page_names_list.append(f"Auto Page {i+1}")
    
    print_box(f"Processing {len(temp)} cookies", Fore.MAGENTA)
    with ThreadPoolExecutor(max_workers=THREADS) as ex:
        for ck in temp:
            ex.submit(create_page_for_cookie, ck, user_agent)

def main():
    global profile_pic_url
    
    print_rainbow_banner()
    
    print_box("Profile Picture Setup", Fore.MAGENTA)
    print(f"{Fore.YELLOW}Enter profile picture URL (or press Enter to skip):{Style.RESET_ALL}")
    pic_url = input(f"{Fore.CYAN}URL: {Style.RESET_ALL}").strip()
    
    if pic_url:
        profile_pic_url = pic_url
        print_box(f"✓ Profile picture will be set for all pages", Fore.GREEN)
    else:
        print_box(f"Profile picture setting skipped", Fore.YELLOW)
    
    print()
    
    user_agent = DEFAULT_UA
    print_box(f"Using Default User-Agent", Fore.GREEN)
    print(f"{Fore.CYAN}{user_agent[:80]}...{Style.RESET_ALL}\n")

    print_box("Choose mode", Fore.CYAN)
    print(f"{Fore.YELLOW}1) Paste cookies (multi-line, end with 'END')")
    print(f"2) Load cookies from file")
    print(f"3) Quick multi-line paste (press Enter on blank line){Style.RESET_ALL}\n")
    
    choice = input(f"{Fore.MAGENTA}Select 1, 2 or 3: {Style.RESET_ALL}").strip()
    if choice == "1":
        run_mode_paste(user_agent)
    elif choice == "2":
        run_mode_file(user_agent)
    elif choice == "3":
        run_mode_quick(user_agent)
    else:
        print_box("Invalid choice. Exiting.", Fore.RED)
        return

    print("\n")
    print_box(f"COMPLETED! Total pages created: {len(page_total)}", Fore.GREEN)
    print(f"{Fore.CYAN}Check '{OUTPUT_LOG}' for details{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
