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
        "https://cdn.jsdelivr.net/gh/proxifly/free-proxy-list@main/proxies/protocols/socks5/data.json"
)

SITES = [
    "https://www.facebook.com",
]


TIMEOUT = 3


NEEDED_COUNTRIES = {

}

def check(proxy: str) -> dict | None:
    p = {"http": proxy, "https": proxy}
    try:
        d = requests.get("http://ip-api.com/json?fields=status,countryCode", proxies=p, timeout=TIMEOUT).json()
        if d.get("status") != "success":
            return None

        t0 = time.perf_counter()
        if not all(requests.get(s, proxies=p, timeout=TIMEOUT, verify=True).ok for s in SITES):
            return None

        if d.get("countryCode") in NEEDED_COUNTRIES or not NEEDED_COUNTRIES:
            return {"server": proxy, "cc": d.get("countryCode"), "sec": round(time.perf_counter() - t0, 2) / len(SITES)}
    except Exception:
        return None


def main():
    print(f"downloading proxies...")

    try:
        json = requests.get(URL, timeout=60).json()

    except requests.exceptions.RequestException as e:
        print(f"download error: {type(e).__name__}")
        return []

    proxies = [item["proxy"] for item in json if item["geolocation"]["country"] in NEEDED_COUNTRIES or not NEEDED_COUNTRIES]


    print(f"{len(proxies)} proxies received")

    found = []
    with cf.ThreadPoolExecutor(80) as ex:
        for r in ex.map(check, proxies):
            if r:
                found.append(r)

    found.sort(key=itemgetter("sec"))

    for f in found:
        print(f"{f["sec"]}  {f['server']}  {f['cc']}")


if __name__ == "__main__":
    main()