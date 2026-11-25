<h1>FREE PROXIES</h1>

This is a python script, that gets proxies from proxifly/free-proxies list (I am so thankful to its author)\
checks its anonymity\
and print for you the list of all **WORKING PROXIES** from fastest to slowest

<h2>INSTALLATION</h2>
You need Python 3.12+ for the script to work
Also you need to write this command in terminal:

```bash
 pip install requests[socks]
 ```
<h2>Few settings</h2>

URL --- **leave as is** this is the source of proxies if you will change parsing may work incorrect

ECHO --- **leave as is** this is url for checking proxies anonymity

SITES --- this is the list of sites that script will check with every proxy now there is only facebook\
but you can paste your site or sites (structure: "https://site.com", "https://site.com") and script will route\
proxies through them. And will not show you proxies that can not open any site

TIMEOUT --- it means "if proxy will not connect to sites in TIMEOUT value it will not be shown"

**!!!DESCRIPTION!!!**

It's not about whether the proxy OPENS the site in time — it's about whether it CONNECTS in time\
Proxy can connect to the site in 1 second and open it in 5

NEEDED_COUNTRIES --- you will see proxies from countries mentioned in this list.\
If list is empty, you will see proxies from every country.\
(example: "US", "NL")


<h2>Good luck!</h2>
