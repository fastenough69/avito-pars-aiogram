from bs4 import BeautifulSoup as bs
import aiohttp
from datetime import datetime
from random import choice
import asyncio

class Selector:
    headers = {"User-Agent": '',
               "Accept-Language": "en-US,en;q=0.9",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                "Referer": "https://www.avito.ru/",}
    
    link = 'https://www.avito.ru/yaroslavl/mototsikly_i_mototehnika/mototsikly-ASgBAgICAUQ80k0?cd=1&radius=200&s=104&searchRadius=200'
    coockie = {'srv_id': 'G8CKFP_Ats-HPpvi.sFfTCj8ZPQl9JIuKWeFHCqWFpzTY3A4Btf3SnsLItB4rkKfa7EBtOaVp7zTl5aQ=.slUOeVX5EzcmFiL-nb1IeAmU6m4GPuL1xRpr9GiidoY=.web', 'u': '32q5yws5.qdxrez.zw2hsnytb8g0', 'v': '1730148245', 'luri': 'all', 'buyer_location_id': '621540', 'sx': 'H4sIAAAAAAAC%2FwTAUQ6DIAwG4Lv8z3vQlurkNq3YZSRLdMkIjHB3vw6VZL7s9AxqSior7TJtiXlzIUszYkdBxF8uP%2B17fCg0sVryWdu7%2FLL69cq14YEDcV55Ig6L8Bh3AAAA%2F%2F820YglWwAAAA%3D%3D', 'dfp_group': '15'}
    
    # def get_coockies():
    #     session = requests.Session()
    #     response = session.get(Selector.link, headers=Selector.headers)
    #     with open('log.txt', 'a+') as logfile:
    #         print(f'request status code: {response.status_code}, date: {datetime.now()}, discription: get coockies', file=logfile)
    #     return session.cookies.get_dict()
    
    # def get_headers():
    #     session = requests.Session()
    #     response = session.get(Selector.link)
    #     sleep(7)
    #     return response.headers

async def data_collection(min_price=None, max_price=None):
        try:
            with open('user_agent_pc.txt', 'r') as user_file:
                temp = user_file.readlines()
                user = choice(temp).strip()

            # link = f'https://www.avito.ru/yaroslavl/mototsikly_i_mototehnika/mototsikly-ASgBAgICAUQ80k0?cd=1&s=104&priceMin={min_price}&priceMax={max_price}'
            headers = Selector.headers
            headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 YaBrowser/24.10.0.0 Safari/537.36'
            # coockie = Selector.coockie
            
            async with aiohttp.ClientSession() as session:
                async with session.get(Selector.link, headers=headers, ssl=False) as response:
            
                    print(f'request status code: {response.status}, date: {datetime.now()}')
                    soup = bs(await response.text(), 'lxml')
                    await asyncio.sleep(5)

            block = soup.find('div', attrs={'data-marker': 'catalog-serp'})
            # items = block.find_all('p', attrs={'data-marker': 'item-date'})
            urls = block.find_all('a',  attrs={'data-marker': 'item-title'})
            # prises = block.find_all('strong', class_ = 'styles-module-root-bLKnd')

            data = []
            for i in range(len(urls)):
                url = 'https://www.avito.ru'+urls[i]['href']
                data.append(url)
            return data
        
        except Exception as error:
            print(f'ERROR "In func module": {error}, date: {datetime.now()}')
            await asyncio.sleep(10)
            return

async def main():
    last = await data_collection(100000, 1000000)
                
    while True:
            await asyncio.sleep(15)
            current = await data_collection(100000, 1000000)
            for i in range(len(current[:10])):
                if current[i] not in last:
                    print(f'{i + 1}: {current[i]}')
                
                
            last = current

if __name__ == '__main__':
    asyncio.run(main())
