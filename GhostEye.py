import os
import sys
import time
import ctypes
import requests
import socket
from colorama import init, Fore, Style

init(autoreset=True)

# ====================== Blue Gradient ======================
def print_gradient_ascii():
    ascii_art = r"""
  ____ _               _   _____           
 / ___| |__   ___  ___| |_| ____|   _  ___ 
| |  _| '_ \ / _ \/ __| __|  _|| | | |/ _ \
| |_| | | | | (_) \__ \ |_| |__| |_| |  __/
 \____|_| |_|\___/|___/\__|_____\__, |\___|
                                |___/      
    """
    gradient_colors = [
        Fore.BLUE,
        Fore.BLUE,
        Fore.LIGHTBLUE_EX,
        Fore.LIGHTBLUE_EX,
        Fore.CYAN,
        Fore.CYAN,
        Fore.LIGHTCYAN_EX
    ]
  
    lines = ascii_art.split('\n')
    for i, line in enumerate(lines):
        if line.strip():
            color = gradient_colors[i % len(gradient_colors)]
            print(color + line + Style.RESET_ALL)
        else:
            print()


# ====================== Windows API ======================
def center_console_window():
    try:
        hwnd = ctypes.windll.kernel32.GetConsoleWindow()
        if not hwnd:
            return
        
        os.system("mode con: cols=150 lines=48")
        time.sleep(0.1)
        
        screen_width = ctypes.windll.user32.GetSystemMetrics(0)
        screen_height = ctypes.windll.user32.GetSystemMetrics(1)
        
        rect = ctypes.wintypes.RECT()
        ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(rect))
        
        w = rect.right - rect.left
        h = rect.bottom - rect.top
        
        x = (screen_width - w) // 2
        y = (screen_height - h) // 2 - 35
        
        ctypes.windll.user32.MoveWindow(hwnd, x, y, w, h, True)
        
    except:
        pass


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def slow_print(text, delay=0.03, color=Fore.WHITE):
    for char in text:
        print(color + char, end='', flush=True)
        time.sleep(delay)
    print(Style.RESET_ALL)


def loading_animation(text="Анализ информации"):
    print(Fore.WHITE)
    for _ in range(3):
        for dots in ["", ".", "..", "..."]:
            print(f"\r{text}{dots}   ", end="")
            time.sleep(0.25)
    print(Style.RESET_ALL)


def startup_animation():
    clear()
    center_console_window()
    
    slow_print("Инициализация GhostEye...", 0.04, Fore.BLUE)
    time.sleep(0.5)
    
    modules = ["colorama", "socket", "requests", "ctypes", "core modules"]
    for module in modules:
        print(f"[{Fore.GREEN}ОК{Style.RESET_ALL}] Загрузка {module}...")
        time.sleep(0.35)
    
    print(f"[{Fore.GREEN}ОК{Style.RESET_ALL}] Инициализация интерфейса...")
    time.sleep(0.6)
    
    print(f"[{Fore.GREEN}ОК{Style.RESET_ALL}] Подключение к системным ресурсам...")
    time.sleep(0.5)
    
    print()
    slow_print("GhostEye успешно запущен.", 0.03, Fore.CYAN)
    time.sleep(0.8)
    
    print(f"\n{Fore.LIGHTCYAN_EX}Добро пожаловать в GhostEye !{Style.RESET_ALL}")
    time.sleep(1.0)
    print()


def port_scan(ip):
    common_ports = [21, 22, 23, 25, 53, 79, 80, 110, 113, 135, 137, 138, 139, 143, 
                   194, 443, 445, 500, 1080, 1243, 1433, 3306, 5000, 12345, 
                   12348, 21544, 27374, 30003, 31337]
    
    open_ports = []
   
    slow_print(f"\nЗапуск анализа портов на {ip}...", 0.04)
    print(f"Всего портов для проверки: {len(common_ports)}\n")
   
    for port in common_ports:
        clear()
        print(Fore.WHITE, end="")
        for _ in range(3):
            for dots in ["", ".", "..", "..."]:
                print(f"\rПроверка порта {port}{dots}   ", end="")
                time.sleep(0.25)
        print(Style.RESET_ALL)
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1.0)
        result = sock.connect_ex((ip, port))
        sock.close()
        
        if result == 0:
            status = f"{Fore.GREEN}Открыт{Style.RESET_ALL}"
            open_ports.append(port)
        else:
            status = f"{Fore.RED}Закрыт{Style.RESET_ALL}"
        
        print(f"[{Fore.GREEN}+{Style.RESET_ALL}] Порт {port} — {status}")
        time.sleep(0.65)
    
    clear()
    slow_print(f"Результат анализа портов для {ip}", 0.04)
    print(f"Проверено портов: {len(common_ports)}\n")
   
    if open_ports:
        print(f"Открытых портов найдено: {len(open_ports)}\n")
        for p in open_ports:
            print(f"[{Fore.GREEN}+{Style.RESET_ALL}] Порт {p} — {Fore.GREEN}Открыт{Style.RESET_ALL}")
    else:
        print(f"{Fore.GREEN}Все порты закрыты.{Style.RESET_ALL}")
   
    print()
    input("Нажмите Enter для возврата в меню...")


def get_ip_info(ip):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
      
        response = requests.get(f"http://ip-api.com/json/{ip}?fields=status,message,query,continent,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as,mobile,proxy,hosting",
                              headers=headers, timeout=10)
     
        if response.status_code == 200:
            data = response.json()
         
            if data.get("status") == "fail":
                return None, data.get("message", "Не удалось получить данные")
         
            try:
                hostname = socket.gethostbyaddr(ip)[0]
            except:
                hostname = "Не удалось определить"
               
            info = {
                "ip": data.get("query"),
                "version": "IPv6" if ":" in ip else "IPv4",
                "hostname": hostname,
                "country": data.get("country"),
                "city": data.get("city"),
                "region": data.get("regionName"),
                "timezone": data.get("timezone"),
                "org": data.get("isp") or data.get("org"),
                "latitude": data.get("lat"),
                "longitude": data.get("lon"),
                "postal": data.get("zip"),
                "proxy": data.get("proxy"),
                "hosting": data.get("hosting"),
                "mobile": data.get("mobile"),
                "maps_link": f"https://www.google.com/maps?q={data.get('lat')},{data.get('lon')}" if data.get("lat") else None
            }
            return info, None
        else:
            return None, f"HTTP Error: {response.status_code}"
    except Exception as e:
        return None, "Не удалось подключиться к серверу. Проверьте интернет."


def show_ip_info(info):
    clear()
    slow_print("Результат анализа:", 0.04)
    print()
 
    print(f"[{Fore.GREEN}+{Style.RESET_ALL}] IP: {info['ip']} ({info['version']})")
    print(f"[{Fore.GREEN}+{Style.RESET_ALL}] Hostname: {info['hostname']}")
    print(f"[{Fore.GREEN}+{Style.RESET_ALL}] Страна: {info['country'] or 'Не найдено'}")
    print(f"[{Fore.GREEN}+{Style.RESET_ALL}] Город: {info['city'] or 'Не найдено'}")
    print(f"[{Fore.GREEN}+{Style.RESET_ALL}] Регион: {info['region'] or 'Не найдено'}")
    print(f"[{Fore.GREEN}+{Style.RESET_ALL}] Часовой пояс: {info['timezone'] or 'Не найдено'}")
    print(f"[{Fore.GREEN}+{Style.RESET_ALL}] Провайдер: {info['org'] or 'Не найдено'}")
    print(f"[{Fore.GREEN}+{Style.RESET_ALL}] Координаты: {info['latitude']}, {info['longitude']}")
    print(f"[{Fore.GREEN}+{Style.RESET_ALL}] Индекс: {info['postal'] or 'Не найдено'}")
  
    risk = []
    if info.get("proxy"): risk.append("Proxy")
    if info.get("hosting"): risk.append("Hosting / Datacenter")
    if info.get("mobile"): risk.append("Mobile")
    print(f"[{Fore.GREEN}+{Style.RESET_ALL}] VPN/Proxy: {' | '.join(risk) if risk else 'Не обнаружено'}")
  
    if info.get("maps_link"):
        print(f"[{Fore.GREEN}+{Style.RESET_ALL}] Google Maps: {info['maps_link']}")
  
    print()
    input("Нажмите Enter для возврата в меню...")


# ====================== Анализ по whois ======================
def whois_lookup(query):
    """Простой whois через socket (работает для доменов и IP)"""
    try:
        if ":" in query or query.replace(".", "").isdigit():  # IP
            server = "whois.iana.org"
        else:
            server = "whois.iana.org"
        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10)
        s.connect((server, 43))
        s.sendall(f"{query}\r\n".encode())
        
        response = b""
        while True:
            data = s.recv(4096)
            if not data:
                break
            response += data
        s.close()
        
        return response.decode('utf-8', errors='ignore')
    except Exception as e:
        return f"Ошибка whois: {str(e)}"


def show_whois_info(result, query):
    clear()
    slow_print("Результат анализа whois", 0.04, Fore.CYAN)
    print(f"для запроса: {Fore.YELLOW}{query}{Style.RESET_ALL}")
    print("=" * 80)
    print()
    
    if "Ошибка" in result:
        print(f"{Fore.RED}{result}{Style.RESET_ALL}")
    else:
        lines = result.split('\n')[:70]
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('%') or line.startswith('#'):
                continue
                
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()
                
                important_keys = ['domain', 'organisation', 'registrar', 'registrant', 
                                'creation', 'changed', 'expiry', 'status', 'nameserver', 
                                'email', 'phone', 'org', 'address', 'admin', 'tech']
                
                key_lower = key.lower()
                
                if any(imp in key_lower for imp in important_keys):
                    key_display = key[0].upper() + key[1:] if key else key
                    print(f"[{Fore.GREEN}+{Style.RESET_ALL}] {Fore.CYAN}{key_display}{Style.RESET_ALL}: {value}")
                else:
                    key_display = key[0].upper() + key[1:] if key else key
                    print(f"[{Fore.GREEN}+{Style.RESET_ALL}] {key_display}: {value}")
            else:
                print(f"[{Fore.GREEN}+{Style.RESET_ALL}] {line}")
    
    print()
    print("=" * 80)
    input("Нажмите Enter для возврата в меню...")


# ====================== DNS анализ ======================
def get_dns_info(dns_server):
    try:
        info = {
            "dns": dns_server,
            "hostname": "Не удалось определить",
            "org": "Неизвестно",
            "country": "Неизвестно",
            "city": "Неизвестно",
            "isp": "Неизвестно"
        }
        
        # Reverse DNS (PTR)
        try:
            hostname = socket.gethostbyaddr(dns_server)[0]
            info["hostname"] = hostname
        except:
            pass
        
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(f"http://ip-api.com/json/{dns_server}?fields=status,message,country,city,isp,org,as", 
                                  headers=headers, timeout=8)
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "success":
                    info["country"] = data.get("country", "Неизвестно")
                    info["city"] = data.get("city", "Неизвестно")
                    info["isp"] = data.get("isp", "Неизвестно")
                    info["org"] = data.get("org", data.get("isp", "Неизвестно"))
        except:
            pass
        
        try:
            whois_data = whois_lookup(dns_server)
            if whois_data and "Ошибка" not in whois_data:
                for line in whois_data.split('\n'):
                    if any(x in line.lower() for x in ["orgname", "organisation", "org:"]):
                        if ':' in line:
                            value = line.split(':', 1)[1].strip()
                            if value and len(value) > 3:
                                info["org"] = value
                                break
        except:
            pass
        
        return info
    except:
        return None


def show_dns_info(info, dns):
    clear()
    slow_print("Результат анализа DNS", 0.04, Fore.CYAN)
    print(f"для сервера: {Fore.YELLOW}{dns}{Style.RESET_ALL}")
    print()
    
    if not info:
        print(f"{Fore.RED}Не удалось получить информацию о DNS сервере.{Style.RESET_ALL}")
    else:
        print(f"[{Fore.GREEN}+{Style.RESET_ALL}] DNS Сервер: {info['dns']}")
        print(f"[{Fore.GREEN}+{Style.RESET_ALL}] Hostname: {info['hostname']}")
        print(f"[{Fore.GREEN}+{Style.RESET_ALL}] Организация: {info['org']}")
        print(f"[{Fore.GREEN}+{Style.RESET_ALL}] Страна: {info['country']}")
        print(f"[{Fore.GREEN}+{Style.RESET_ALL}] Город: {info['city']}")
        print(f"[{Fore.GREEN}+{Style.RESET_ALL}] Провайдер: {info['isp']}")
    
    print()
    input("Нажмите Enter для возврата в меню...")


def exit_animation():
    clear()
    slow_print("GhostEye завершил свою работу.", 0.05, Fore.GREEN)
    time.sleep(1.8)


def main_menu():
    BLUE = "\033[38;2;66;170;255m"
    RESET = Style.RESET_ALL
    
    while True:
        clear()
     
        print_gradient_ascii()
     
        print(f"{BLUE}[1]{RESET}{BLUE} • Информация об утилите")
        print(f"{BLUE}[2]{RESET}{BLUE} • Мануал по анонимности")
        print(f"{BLUE}[3]{RESET}{BLUE} • Анализ по IP-адресу")
        print(f"{BLUE}[4]{RESET}{BLUE} • Анализ портов")
        print(f"{BLUE}[5]{RESET}{BLUE} • Анализ по whois")
        print(f"{BLUE}[6]{RESET}{BLUE} • Анализ по DNS")
        print(f"{BLUE}[7]{RESET}{BLUE} • Выход\n")
     
        print(f"{BLUE}Выберите пункт в меню: {RESET}", end="")
        choice = input().strip()
      
        if choice == "1":
            clear()
            slow_print("Разработчик утилиты: @drugserenity", 0.04)
            slow_print("Дата создания: 10.05.2026", 0.04)
            slow_print("Версия: 2.2", 0.04)
            print()
            slow_print("ПРЕДУПРЕЖДЕНИЕ: Разработчик не несёт ответственности за неправомерное использование утилиты.", 0.04, Fore.RED)
            slow_print("ВАЖНО: Утилита предназначена исключительно для легального использования. ", 0.04, Fore.RED)
            slow_print("Неправомерное применение влечёт уголовную/административную ответственность. ", 0.04, Fore.RED)
            slow_print("Потенциальные нарушения при неправомерном использовании: ", 0.04, Fore.RED)
            slow_print("1. Ст. 137 УК РФ — нарушение неприкосновенности частной жизни сбор/распространение данных без согласия.", 0.04, Fore.RED)
            slow_print("2. Ст. 272 УК РФ — неправомерный доступ к информации наказание — ДО 2 ЛЕТ ЛИШЕНИЯ СВОБОДЫ.", 0.04, Fore.RED)
            slow_print("3. Ст. 273 УК РФ — создание/использование вредоносных программ (при модификации утилиты).", 0.04, Fore.RED)
            slow_print("4. Ст. 274 УК РФ — нарушение правил эксплуатации средств хранения информации.", 0.04, Fore.RED)
            slow_print("5. ФЗ-152 «О персональных данных» — обработка ПД без согласия субъекта.", 0.04, Fore.RED)
            slow_print("6. Ст. 152.2 ГК РФ — защита частной жизни и персональных данных.", 0.04, Fore.RED)
            slow_print("7. ФЗ «Об информации…» (ст. 6) — несанкционированный доступ к информации.", 0.04, Fore.RED)
            slow_print("8. КоАП РФ (ст. 13.11) — административная ответственность за нарушение обработки ПД.", 0.04, Fore.RED)
            print()
            slow_print("GhostEye — утилита для поиска информации по IP-адресу. С её помощью можно быстро узнать:", 0.04)
            slow_print("где физически находится IP (страна, город, регион, часовой пояс, провайдер, координаты, индекс).", 0.04)
            slow_print("какие порты на целевом IP открыты и какие сервисы работают на этих портах (анализ портов с помощью встроенного сканера).", 0.04)
            slow_print("также с помощью функции «Анализ по whois» можно узнать владельца IP/домена, сроки регистрации и контактные данные.", 0.04)
            slow_print("с помощью функции «Анализ по DNS» можно найти реальную информацию о DNS-сервере.", 0.04)
            print()
            input("Нажмите Enter для возврата в меню...")

        elif choice == "2":
            clear()
            slow_print("Мануал по анонимности и OPSEC", 0.04, Fore.CYAN)
            print()
            
            manual = [
                "1. Используй отдельную среду",
                "• Виртуальная машина",
                "• Отдельный браузер / профиль",
                "",
                "2. Никогда не работай со своего реального IP",
                "• Используй VPN с Kill Switch",
                "• Избегай бесплатных VPN",
                "• Tor Browser для максимальной анонимности",
                "",
                "3. Разделяй личности",
                "• Отдельные почты, ники, аккаунты",
                "",
                "4. Отключай лишние данные в браузере",
                "• WebRTC, геолокацию, автосохранение",
                "",
                "5. Осторожно открывай файлы",
                "• PDF, DOCX, изображения могут содержать трекеры",
                "",
                "6. Не доверяй случайным ссылкам",
                "",
                "7. Следи за OPSEC",
                "• Не смешивай личное и рабочее",
                "• Думай, что может тебя деанонимизировать",
                "",
                "8. Обновляй систему и зависимости",
                "",
                "9. Минимизируй цифровой след",
                "",
                "10. Соблюдай закон"
            ]
            
            for line in manual:
                if line.strip() == "":
                    print()
                elif line.startswith(("1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.", "9.", "10.")):
                    slow_print(line, 0.02, Fore.YELLOW)
                else:
                    slow_print("   " + line, 0.02)
            
            print()
            input("Нажмите Enter для возврата в меню...")

        elif choice == "3":
            clear()
            slow_print("Введите IP-адрес для анализа", 0.03)
            ip = input("> ").strip()
         
            if not ip:
                continue
             
            loading_animation()
            info, error = get_ip_info(ip)
         
            if info:
                show_ip_info(info)
            else:
                clear()
                print(f"\nОшибка: {error}")
                time.sleep(2.5)
                
        elif choice == "4":
            clear()
            slow_print("Вставьте IP-адрес для анализа открытых портов", 0.04)
            ip = input("> ").strip()
           
            if not ip:
                continue
               
            port_scan(ip)

        elif choice == "5":
            clear()
            slow_print("Введите домен или IP для whois", 0.04)
            query = input("> ").strip()
           
            if not query:
                continue
               
            loading_animation("Выполняется whois-запрос")
            result = whois_lookup(query)
            show_whois_info(result, query)
            
        elif choice == "6":
            clear()
            slow_print("Введите DNS сервер для анализа", 0.04)
            dns = input("> ").strip()
           
            if not dns:
                continue
               
            loading_animation("Выполняется анализ DNS")
            dns_info = get_dns_info(dns)
            show_dns_info(dns_info, dns)
            
        elif choice == "7":
            exit_animation()
            sys.exit(0)
         
        else:
            print(f"\n{Fore.RED}Вы выбрали неверный пункт !{Style.RESET_ALL}")
            time.sleep(1.7)


if __name__ == "__main__":
    startup_animation()        
    main_menu()