import sys
import concurrent.futures as cf
import time
from operator import itemgetter

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

URL = (
        "https://cdn.jsdelivr.net/gh/proxifly/free-proxy-list@main/proxies/all/data.json"
)

SITES = [
    "https://www.facebook.com",
]


TIMEOUT = 5


NEEDED_COUNTRIES = {

}

ECHO = "https://httpbin.org/get"


def leaks(proxy: str, real_ip: str) -> bool:
    p = {"http": proxy, "https": proxy}
    try:
        r = requests.get(ECHO, proxies=p, timeout=TIMEOUT, verify=True).json()
        exit_ip = r.get("origin", "").split(",")[0].strip()
        if exit_ip == real_ip:
            return True

        h = {k.lower(): v for k, v in r.get("headers", "").items()}

        leak_headers = [k for k in h if k in {
            "x-forwarded-for", "x-real-ip", "via", "forwarded",
            "proxy-connection", "x-proxy-id", "x-proxy-ip", "x-forwarded-host"} or k.startswith("x-proxy")]
        if leak_headers:
            return True

        return False
    except Exception:
        return True


def check(proxy: str, real_ip: str) -> dict | None:
    p = {"http": proxy, "https": proxy}
    try:
        d = requests.get("http://ip-api.com/json?fields=status,countryCode", proxies=p, timeout=TIMEOUT).json()
        if d.get("status") != "success":
            return None

        t0 = time.perf_counter()
        if not all(requests.get(s, proxies=p, timeout=TIMEOUT, verify=True).ok for s in SITES):
            return None
        sec = round(time.perf_counter() - t0, 2) / len(SITES)

        if d.get("countryCode") in NEEDED_COUNTRIES or not NEEDED_COUNTRIES:
            prox = {"server": proxy, "cc": d.get("countryCode"), "sec": sec}
        else:
            return None

        if not leaks(prox["server"], real_ip):
            return prox

        return None
    except Exception:
        return None


def main():
    print(f"downloading proxies...")

    real_ip = requests.get("http://ip-api.com/json?fields=query", timeout=TIMEOUT).json()["query"]

    try:
        json = requests.get(URL, timeout=60).json()

    except requests.exceptions.RequestException as e:
        print(f"download error: {type(e).__name__}")
        return []

    proxies = [item["proxy"] for item in json if item["geolocation"]["country"] in NEEDED_COUNTRIES or not NEEDED_COUNTRIES]


    print(f"{len(proxies)} proxies received")

    found = []
    with cf.ThreadPoolExecutor(80) as ex:
        for r in ex.map(lambda p: check(p, real_ip), proxies):
            if r:
                found.append(r)

    found.sort(key=itemgetter("sec"))

    for f in found:
        print(f"{f["sec"]}  {f['server']}  {f['cc']}")


if __name__ == "__main__":
    main()