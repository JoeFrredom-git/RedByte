#!/usr/bin/env python3

import socket
import urllib.request
import urllib.parse
import json
import sys
import platform
import random
import ipaddress


# ============================================================
# RED BYTE
# OSINT / NETWORK TOOLKIT
# ============================================================

VERSION = "1.0"


# ============================================================
# COLORS
# ============================================================

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
WHITE = "\033[97m"
GRAY = "\033[90m"
RESET = "\033[0m"


# ============================================================
# SCREEN
# ============================================================

def clear_screen():
    print("\033[2J\033[H", end="")


def pause():
    input(
        "\n" +
        GRAY +
        "Press Enter to return to the menu..." +
        RESET
    )


# ============================================================
# BANNER
# ============================================================

def banner():
    print(
        CYAN +
        r"""
 ______     _   ____        _
|  _ \ ___| | | __ ) _   _| |_ ___
| |_) / _ \ | |  _ \| | | | __/ _ \
|  _ <  __/ | | |_) | |_| | ||  __/
|_| \_\___|_| |____/ \__, |\__\___|
                     |___/

        OSINT / NETWORK TOOLKIT
""" +
        RESET
    )


# ============================================================
# MENU
# ============================================================

def show_menu():
    clear_screen()
    banner()

    print(
        CYAN +
        "+--------------------------------------+\n"
        "|              RED BYTE                |\n"
        "+--------------------------------------+\n"
        "|                                      |\n"
        "| [1] Public IP                        |\n"
        "| [2] Domain -> IP                     |\n"
        "| [3] Reverse DNS                      |\n"
        "| [4] IP Information                   |\n"
        "| [5] HTTP Headers                     |\n"
        "| [6] Port Scanner                     |\n"
        "| [7] Local Network                    |\n"
        "| [8] OSINT Search                     |\n"
        "| [9] IP Generator                     |\n"
        "| [00] Exit                            |\n"
        "|            joefrredom-tech           |\n"
        "+--------------------------------------+\n" +
        RESET
    )


# ============================================================
# 1 - PUBLIC IP
# ============================================================

def public_ip():
    clear_screen()
    banner()

    print(CYAN + "[ PUBLIC IP ]\n" + RESET)

    try:
        request = urllib.request.Request(
            "https://api.ipify.org?format=json",
            headers={
                "User-Agent": "RedByte/1.0"
            }
        )

        with urllib.request.urlopen(
            request,
            timeout=5
        ) as response:

            data = json.loads(
                response.read().decode("utf-8")
            )

        print(GREEN + "[+] Public IP:" + RESET)
        print("    " + data["ip"])

    except Exception as error:
        print(
            RED +
            "[!] Could not retrieve public IP." +
            RESET
        )
        print(GRAY + str(error) + RESET)

    pause()


# ============================================================
# 2 - DOMAIN -> IP
# ============================================================

def domain_to_ip():
    clear_screen()
    banner()

    print(CYAN + "[ DOMAIN -> IP ]\n" + RESET)

    target = input(
        WHITE +
        "Domain: " +
        RESET
    ).strip()

    if not target:
        pause()
        return

    try:
        addresses = socket.getaddrinfo(
            target,
            None,
            socket.AF_INET
        )

        ips = sorted(
            set(
                result[4][0]
                for result in addresses
            )
        )

        if ips:
            print(
                GREEN +
                "\n[+] IPv4 addresses:" +
                RESET
            )

            for ip in ips:
                print("    " + ip)

        else:
            print(
                YELLOW +
                "\n[!] No IPv4 addresses found." +
                RESET
            )

    except socket.gaierror:
        print(
            RED +
            "\n[!] Could not resolve domain." +
            RESET
        )

    pause()


# ============================================================
# 3 - REVERSE DNS
# ============================================================

def reverse_dns():
    clear_screen()
    banner()

    print(CYAN + "[ REVERSE DNS ]\n" + RESET)

    ip = input(
        WHITE +
        "IP address: " +
        RESET
    ).strip()

    try:
        ipaddress.ip_address(ip)

    except ValueError:
        print(
            RED +
            "[!] Invalid IP address." +
            RESET
        )
        pause()
        return

    try:
        hostname, aliases, addresses = socket.gethostbyaddr(ip)

        print(
            GREEN +
            "\n[+] Hostname:" +
            RESET
        )

        print("    " + hostname)

        if aliases:
            print(
                GREEN +
                "\n[+] Aliases:" +
                RESET
            )

            for alias in aliases:
                print("    " + alias)

    except socket.herror:
        print(
            YELLOW +
            "\n[!] No reverse DNS record found." +
            RESET
        )

    pause()


# ============================================================
# 4 - IP INFORMATION
# ============================================================

def ip_information():
    clear_screen()
    banner()

    print(CYAN + "[ IP INFORMATION ]\n" + RESET)

    ip = input(
        WHITE +
        "IP address: " +
        RESET
    ).strip()

    try:
        ipaddress.ip_address(ip)

    except ValueError:
        print(
            RED +
            "[!] Invalid IP address." +
            RESET
        )
        pause()
        return

    try:
        url = (
            "https://ipinfo.io/" +
            urllib.parse.quote(ip) +
            "/json"
        )

        request = urllib.request.Request(
            url,
            headers={
                "User-Agent": "RedByte/1.0"
            }
        )

        with urllib.request.urlopen(
            request,
            timeout=8
        ) as response:

            data = json.loads(
                response.read().decode("utf-8")
            )

        fields = [
            ("IP", "ip"),
            ("Hostname", "hostname"),
            ("City", "city"),
            ("Region", "region"),
            ("Country", "country"),
            ("Location", "loc"),
            ("Organization", "org"),
            ("Postal", "postal"),
            ("Timezone", "timezone")
        ]

        print()

        for label, key in fields:

            value = data.get(key)

            if value:
                print(
                    f"{GREEN}{label:<15}{RESET}: {value}"
                )

    except Exception as error:

        print(
            RED +
            "[!] Could not retrieve IP information." +
            RESET
        )

        print(
            GRAY +
            str(error) +
            RESET
        )

    pause()


# ============================================================
# 5 - HTTP HEADERS
# ============================================================

def http_headers():
    clear_screen()
    banner()

    print(CYAN + "[ HTTP HEADERS ]\n" + RESET)

    url = input(
        WHITE +
        "Website: " +
        RESET
    ).strip()

    if not url:
        pause()
        return

    if not url.startswith(
        ("http://", "https://")
    ):
        url = "https://" + url

    try:

        request = urllib.request.Request(
            url,
            method="HEAD",
            headers={
                "User-Agent": "RedByte/1.0"
            }
        )

        with urllib.request.urlopen(
            request,
            timeout=8
        ) as response:

            print(
                GREEN +
                f"\n[+] Status: {response.status}" +
                RESET
            )

            print(
                CYAN +
                "\n[+] Headers:\n" +
                RESET
            )

            for key, value in response.headers.items():

                print(
                    f"{WHITE}{key}{RESET}: {value}"
                )

    except Exception as error:

        print(
            RED +
            "[!] Could not connect to website." +
            RESET
        )

        print(
            GRAY +
            str(error) +
            RESET
        )

    pause()


# ============================================================
# 6 - PORT SCANNER
# ============================================================

def port_scanner():
    clear_screen()
    banner()

    print(CYAN + "[ PORT SCANNER ]\n" + RESET)

    print(
        YELLOW +
        "Only scan systems you own or have permission to test." +
        RESET
    )

    target = input(
        WHITE +
        "\nTarget IP/domain: " +
        RESET
    ).strip()

    if not target:
        pause()
        return

    start_input = input(
        WHITE +
        "Start port [1]: " +
        RESET
    ).strip()

    end_input = input(
        WHITE +
        "End port [1024]: " +
        RESET
    ).strip()

    try:

        start_port = (
            int(start_input)
            if start_input
            else 1
        )

        end_port = (
            int(end_input)
            if end_input
            else 1024
        )

    except ValueError:

        print(
            RED +
            "[!] Invalid port number." +
            RESET
        )

        pause()
        return

    if (
        start_port < 1
        or end_port > 65535
        or start_port > end_port
    ):

        print(
            RED +
            "[!] Invalid port range." +
            RESET
        )

        pause()
        return

    try:
        ip = socket.gethostbyname(target)

    except socket.gaierror:

        print(
            RED +
            "[!] Could not resolve target." +
            RESET
        )

        pause()
        return

    print(
        CYAN +
        f"\n[+] Target: {target}" +
        RESET
    )

    print(
        CYAN +
        f"[+] IP: {ip}" +
        RESET
    )

    print(
        CYAN +
        f"[+] Ports: {start_port}-{end_port}\n" +
        RESET
    )

    open_ports = []

    try:

        for port in range(
            start_port,
            end_port + 1
        ):

            sock = socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM
            )

            sock.settimeout(0.25)

            try:

                result = sock.connect_ex(
                    (ip, port)
                )

                if result == 0:

                    try:
                        service = socket.getservbyport(
                            port
                        )

                    except OSError:
                        service = "unknown"

                    open_ports.append(
                        (port, service)
                    )

                    print(
                        GREEN +
                        f"[OPEN] {port:<5} {service}" +
                        RESET
                    )

            finally:
                sock.close()

    except KeyboardInterrupt:

        print(
            YELLOW +
            "\n[!] Scan stopped." +
            RESET
        )

    print(
        CYAN +
        f"\n[+] Open ports found: {len(open_ports)}" +
        RESET
    )

    pause()


# ============================================================
# 7 - LOCAL NETWORK
# ============================================================

def local_network():
    clear_screen()
    banner()

    print(CYAN + "[ LOCAL NETWORK ]\n" + RESET)

    hostname = socket.gethostname()

    print(
        GREEN +
        f"Hostname        : {hostname}" +
        RESET
    )

    print(
        WHITE +
        f"Operating System : {platform.system()}" +
        RESET
    )

    print(
        WHITE +
        f"OS Version       : {platform.release()}" +
        RESET
    )

    print(
        WHITE +
        f"Machine          : {platform.machine()}" +
        RESET
    )

    try:

        local_ip = socket.gethostbyname(
            hostname
        )

        print(
            GREEN +
            f"Local IPv4       : {local_ip}" +
            RESET
        )

    except Exception:

        print(
            YELLOW +
            "Local IPv4       : unavailable" +
            RESET
        )

    pause()


# ============================================================
# 8 - OSINT SEARCH
# ============================================================

def osint_search():
    clear_screen()
    banner()

    print(CYAN + "[ OSINT SEARCH ]\n" + RESET)

    target = input(
        WHITE +
        "Search target: " +
        RESET
    ).strip()

    if not target:
        pause()
        return

    encoded = urllib.parse.quote(target)

    searches = {
        "Google":
            f"https://www.google.com/search?q={encoded}",

        "Bing":
            f"https://www.bing.com/search?q={encoded}",

        "DuckDuckGo":
            f"https://duckduckgo.com/?q={encoded}",

        "Google News":
            f"https://www.google.com/search?tbm=nws&q={encoded}"
    }

    print(
        GREEN +
        "\n[+] Search URLs:\n" +
        RESET
    )

    for name, url in searches.items():

        print(
            f"{CYAN}{name:<15}{RESET}{url}"
        )

    pause()


# ============================================================
# 9 - IP GENERATOR
# ============================================================

def ip_generator():

    while True:

        clear_screen()
        banner()

        print(CYAN + "[ IP GENERATOR ]\n" + RESET)

        print("[01] Private/test IP")
        print("[02] Random IPv4")
        print("[03] Generate multiple")
        print("[00] Back")

        choice = input(
            CYAN +
            "\nRedByte > " +
            RESET
        ).strip().lower()

        # ----------------------------------------------------
        # PRIVATE IP
        # ----------------------------------------------------

        if choice == "01":

            networks = [
                ipaddress.ip_network(
                    "10.0.0.0/8"
                ),
                ipaddress.ip_network(
                    "172.16.0.0/12"
                ),
                ipaddress.ip_network(
                    "192.168.0.0/16"
                )
            ]

            network = random.choice(
                networks
            )

            ip = random.choice(
                list(network.hosts())
            )

            print(
                GREEN +
                f"\nGenerated private IP: {ip}" +
                RESET
            )

            input("\nPress Enter...")

        # ----------------------------------------------------
        # RANDOM IPv4
        # ----------------------------------------------------

        elif choice == "02":

            ip = ipaddress.IPv4Address(
                random.randint(
                    1,
                    4294967294
                )
            )

            print(
                GREEN +
                f"\nGenerated IPv4: {ip}" +
                RESET
            )

            print(
                YELLOW +
                "\nThis is randomly generated data; "
                "it does not indicate ownership." +
                RESET
            )

            input("\nPress Enter...")

        # ----------------------------------------------------
        # MULTIPLE IPs
        # ----------------------------------------------------

        elif choice == "03":

            amount_input = input(
                WHITE +
                "\nNumber of IPs [10]: " +
                RESET
            ).strip()

            try:

                amount = (
                    int(amount_input)
                    if amount_input
                    else 10
                )

            except ValueError:

                print(
                    RED +
                    "Invalid number." +
                    RESET
                )

                input("\nPress Enter...")
                continue

            if amount < 1 or amount > 1000:

                print(
                    RED +
                    "Choose between 1 and 1000." +
                    RESET
                )

                input("\nPress Enter...")
                continue

            print(
                GREEN +
                "\nGenerated IPs:\n" +
                RESET
            )

            for _ in range(amount):

                ip = ipaddress.IPv4Address(
                    random.randint(
                        1,
                        4294967294
                    )
                )

                print(ip)

            input("\nPress Enter...")

        # ----------------------------------------------------
        # BACK
        # ----------------------------------------------------

        elif choice in ("00", "0", "q"):

            return

        else:

            print(
                RED +
                "\nInvalid selection." +
                RESET
            )

            input("\nPress Enter...")


# ============================================================
# MAIN
# ============================================================

def main():

    while True:

        show_menu()

        choice = input(
            CYAN +
            "RedByte > " +
            RESET
        ).strip().lower()

        if choice in ("01", "1"):
            public_ip()

        elif choice in ("02", "2"):
            domain_to_ip()

        elif choice in ("03", "3"):
            reverse_dns()

        elif choice in ("04", "4"):
            ip_information()

        elif choice in ("05", "5"):
            http_headers()

        elif choice in ("06", "6"):
            port_scanner()

        elif choice in ("07", "7"):
            local_network()

        elif choice in ("08", "8"):
            osint_search()

        elif choice in ("09", "9"):
            ip_generator()

        elif choice in ("00", "0", "q"):

            clear_screen()

            print(
                GREEN +
                "\nRed Byte shutting down...\n" +
                RESET
            )

            sys.exit(0)

        else:

            print(
                RED +
                "\n[!] Invalid option." +
                RESET
            )

            input(
                "\nPress Enter to continue..."
            )


# ============================================================
# START
# ============================================================

if __name__ == "__main__":

    try:
        main()

    except KeyboardInterrupt:

        print(
            YELLOW +
            "\n\nRed Byte terminated." +
            RESET
        )

        sys.exit(0)