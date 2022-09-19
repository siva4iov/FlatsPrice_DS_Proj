import requests
import ssl
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager
from urllib3.util import ssl_
from random import randint, choice
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
import json
import time

MULTI_T = False # if false, then 1 pool 1 thread, works very slowly. if true, then ThreadPoolExecutor is used,
#  the speed increases several times, but the chance of a ban increases, it is worth using a lot of quality proxies

data = []

# ciphers for adapter creating
CIPHERS = """ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-SHA256:AES256-SHA"""


base_url = "https://www.avito.ru"
url = "https://www.avito.ru/kazan/kvartiry/sdam/na_dlitelnyy_srok-ASgBAgICAkSSA8gQ8AeQUg?context=H4sIAAAAAAAA_0q0MrSqLraysFJKK8rPDUhMT1WyLrYyNLNSKk5NLErOcMsvyg3PTElPLVGyrgUEAAD__xf8iH4tAAAA"

# list of proxies
proxy = [
    
]

proxy = dict(enumerate(proxy)) # for safety deleting elements

# my personal headers
headers = { 'authority': 'www.avito.ru',
'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7' ,
'cache-control': 'max-age=0' ,
'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
"cookie": """u=2thj82n6.1dkvuw0.slmtxzl7jk00; buyer_laas_location=650400; buyer_location_id=650400; abp=1; _ym_uid=1663282989487925154; _ym_d=1663282989; _gcl_au=1.1.319638285.1663282990; SL_G_WPT_TO=ru; tmr_lvid=e6e7134058aaa32d1d447cbd87960569; tmr_lvidTS=1663282990055; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1; isCriteoSetNew=true; buyer_popup_location=0; uxs_uid=9bacf990-354a-11ed-a1ff-dd0d24566ac9; SEARCH_HISTORY_IDS=1; redirectMav=1; luri=kazan; _gid=GA1.2.1396410634.1663424013; f=5.10a94bb89dd075604b5abdd419952845a68643d4d8df96e9a68643d4d8df96e9a68643d4d8df96e9a68643d4d8df96e94f9572e6986d0c624f9572e6986d0c624f9572e6986d0c62ba029cd346349f36c1e8912fd5a48d02c1e8912fd5a48d0246b8ae4e81acb9fa143114829cf33ca746b8ae4e81acb9fa46b8ae4e81acb9fae992ad2cc54b8aa8fbcd99d4b9f4cbdabcc8809df8ce07f640e3fb81381f359178ba5f931b08c66a59b49948619279110df103df0c26013a2ebf3cb6fd35a0ac91e52da22a560f550df103df0c26013a7b0d53c7afc06d0bba0ac8037e2b74f92da10fb74cac1eab71e7cb57bbcb8e0f71e7cb57bbcb8e0f268a7bf63aa148d20df103df0c26013a037e1fbb3ea05095de87ad3b397f946b4c41e97fe93686adecc9ea1e406218ca9538c5b98199aa035d3d12014bda85a476c0626ba176b1517632864d7d4d094f29aa4cecca288d6b3c29848cab14088f8edb85158dee9a660df103df0c26013a0df103df0c26013aafbc9dcfc006bed9d7fb59d404eae758fba29dd198e9981c3de19da9ed218fe23de19da9ed218fe2d6fdecb021a45a31b3d22f8710f7c4ed78a492ecab7d2b7f; ft="xgqzMgy9cUOSjZkmRFWxGoba/gbQkxCLYvaNBfSZdTBKWj9USwi53m/JtmvjFDvrWequpJbKqtCGZQ3ytIBivaUmCxBPPWxQqil6F1dIKVPA2uC6x9lx3xXjiwl9uO9Bk38ZSflB6/GjylvKRis23k0jjl3kVgvjOXYM94M3qzmPyNdn0pjVqfHMr+ZsLRT3"; v=1663503462; tmr_detect=0%7C1663503514136; sx=H4sIAAAAAAAC%2F5yVUZKrOg6G98JzHmRbtuWzGxAgiJsYcMAJt7L3KXqqZ%2Fo%2BHjbwlazv1%2B9%2FKtX3vsfe9%2BC0dR5AccusaoVda1Hr6s8%2F1V79qXKftkNn1fE4Ts%2Bv%2BWnCMM%2FYWdPO3f6oblVX%2FVHOGauQgvvcKiVfjW8fb1F74phACsdSUPAH%2BRrxaGeXZlDrVERaY7kP4b0spRGcfyFRKwcnMnZJNXoNJYoQJkApsTClH6SXh6g7vt6rfsixgvPHiHm8vxYZx9D9Qmqv9DdyX4e%2BKw96IEAUyVkwZ0pXkKiN%2Ftwq3bsa64771jvbWDQGtA5gO69a78P%2F3v%2F0%2Fa7nI4VX54fJmvC0L%2BnmdV%2FV3izL7%2Fd7MP4kvxfvvqZxsyMzSoScOeeS%2BMKwjvBEmt4x9p3i0AXXdB41u2B0WyttQYH%2FIU9dXo5olT%2Ba4d2U%2FhVf2G2jtuPCc7v%2B2z%2BZz62yJkJ56Ps6lkLAcoqizJIv%2Bf%2BOlLU0PuJu9kBCGFPhwsyQ6RLS0ImU2j6L3aaEkUGAOAOmLHzBEll1%2BnfOOW6964ML1qELnW86E1pvgdm34Yf89V6PwyzTsjy7dkez%2BVhGn%2BrjcJsX%2BUUOCtF%2BbpWH6Vji19A0CAgUQQoUAZRL79enJa9nRcO%2Bvm3OESITROGYEl3Pv5dD5XHvtoVyghgJUsySmC9dqcMTOa55eJV1yzGKxFTOPGGCi%2BK%2Fd3k%2FdDi4NoiREwilTOdGL3bJmSW%2FPFcid%2B9MhLNCgJlLROJLU%2FrvXS6vVUzcnEkRi5SCiRITxktT%2FvfhL7gfj7T5wBALnWL4XCr8feIpUAifW0XNo0g9BC%2BFikgWTJxiyldC5AKevUyT8L7uR5yg0FlyJIUYc7m2y7PqQnNsNe9mHhgSRcoSRTjFeK2QzuupFaG6p1FK4gQ5QUqS0q%2BO%2B6tdutN4bfe6hXXbdEESAREsHDNcMm7gNN4Mrmv18XAzJsg5IXICLv%2B%2F8b%2F43K32p%2FFmGaDUWnDABAkBCkmmFC8dpFbqc6sYdfPcTD%2BtXCQRMSIxcIFLUfcnsn3Fp85TW9dEEiMxCHFkidfK%2FQxRp8JwlDEsDeYcM2JGyiVDuTAlaHNOuSzH9JAc6jpjAiDMVDjRpbrUwXw%2B%2FwkAAP%2F%2F0fvqZdYJAAA%3D; dfp_group=68; _dc_gtm_UA-2546784-1=1; _ga_9E363E7BES=GS1.1.1663503473.11.1.1663505048.58.0.0; _ga=GA1.1.1537657974.1663282990; _ga_M29JC28873=GS1.1.1663503475.11.1.1663505049.57.0.0; tmr_reqNum=191""",
'referer': 'https://www.google.com/',
'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"' ,
'sec-ch-ua-mobile': '?0' ,
'sec-ch-ua-platform': '"Windows"' ,
'sec-fetch-dest': 'document' ,
'sec-fetch-mode': 'navigate' ,
'sec-fetch-site': 'same-origin' ,
'sec-fetch-user': '?1' ,
'upgrade-insecure-requests': '1' ,
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36' \
    }

# adapter for requests, avito bans for default(in requests) adapter
class TlsAdapter(HTTPAdapter):

    def __init__(self, ssl_options=0, **kwargs):
        self.ssl_options = ssl_options
        super(TlsAdapter, self).__init__(**kwargs)

    def init_poolmanager(self, *pool_args, **pool_kwargs):
        ctx = ssl_.create_urllib3_context(ciphers=CIPHERS, cert_reqs=ssl.CERT_REQUIRED, options=self.ssl_options)
        self.poolmanager = PoolManager(*pool_args, ssl_context=ctx, **pool_kwargs)

session = requests.session()
session.headers.update(headers)
adapter = TlsAdapter(ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1)
session.mount("https://", adapter)

# function to establish a connection and collect html code of page
def try_connect(url):
    try:
        
        src = ""
        if MULTI_T:
            prox_id = choice(list(proxy.keys()))
            proxies = {"socks4": proxy[prox_id]}
            r = session.request('GET', url, proxies=proxies,  timeout=10)
        else:
            r = session.request('GET', url,  timeout=10)
        if r.status_code == 403:
            raise Exception("403Error")
        src = r.text
        if BeautifulSoup(src, "lxml").title.string == u"Доступ временно заблокирован": # this page appears if ip is banned
            raise Exception("IsBanned")
    except Exception as e:
        print(e)
        if MULTI_T:
            print("trying another proxy...") # if proxy is not available
            del proxy[prox_id]
            if len(proxy) == 0:
                print("ALL PROXY ARE BANNED")
            else:
                src = try_connect(url) # recurse until success
    finally:
        return src


def get_pages_url(url):
    """
    Finds the pagination element on the page and gets the number of pages, then generates a list of urls for each page
    """
    try:
        url_list = []
        src = try_connect(url)
        if not src:
            raise Exception("ConnectionProblem")
        bs = BeautifulSoup(src, "lxml")
        pagination_button = bs.find("div", attrs={"data-marker": "pagination-button"})
        num = pagination_button.find_all('span')[-2]
        num_of_pages = int(num.text)
        url_list = [url + f"&p={page}" for page in range(1, num_of_pages+1)]
    except Exception as e:
        print(e)
    finally:
        time.sleep(5) # user imitation

        return url_list




def get_data_from_page(url):
    """
    Collects information from the ad page. Casts declaration parameters from a string to a dict
    """
    try:
        params = {}
        src = try_connect(url)
        if not src:
            raise Exception("Blank_page")
        bs = BeautifulSoup(src, 'lxml')
        price = bs.find('span', itemprop="price").text
        params = bs.find("div", {"data-marker": "item-view/item-params"}).find_all("li")
        new_params = [param.text.split(":") for param in params]
        params = new_params
        params = {param[0] : param[1] for param in params}
        address = bs.find("div", itemprop="address").find("span").text
        params["Адрес"] = address
        params["Цена"] = price
        
        
    except Exception as e:
        print(e)

    finally:
        data.append(params)
        num = len(data)
        if num % 10 ==0:
            print(f'{num} собрано') # progress status
        time.sleep(5) # user imitation




def parse_adts_from_page(url):

    """
    Collects links to ads from the page, runs a function to collect data from pages
    """
    try:
        src = try_connect(url)
        if not src:
            raise Exception("Blank_page")
        bs = BeautifulSoup(src, 'lxml')
        adts = bs.find_all("a", attrs={"data-marker": 'item-title'})
        adts = [base_url + adt["href"] for adt in adts]
        print(f'Набор ссылок: {len(adts)} ссылок')

        if not len(adts): # in case of error during collecting list of urls
            parse_adts_from_page(url) # recursion for another try
            return 0 # to stop execution
        if MULTI_T:
            with ThreadPoolExecutor() as executor:
                executor.map(get_data_from_page, adts)
                executor.shutdown(wait=True)
        else:
            for adt in map(get_data_from_page, adts):
                adt # execution of collecting function
    except Exception as e:
        print(e)
    finally:
        time.sleep(5) # user imitation


def main():
    url_list = get_pages_url(url)
    for cur_url in url_list:
        parse_adts_from_page(cur_url)
        if len(data) > 10:
            if not any(data[-10:]): # saving the result in case of problems(if ten last dicts is empty). 
                                    # also saving the last page number in case you continue
                with open("log.txt", "w") as file:
                    file.write(f"Last page:{cur_url}\nCollected:{len(data)}")
                break


    dataset = json.dumps(data, indent=2, ensure_ascii=False) # saving to json
    with open("dataset.json", "w", encoding="utf-8") as file:
        file.write(dataset)

if __name__ == "__main__":
    main()
