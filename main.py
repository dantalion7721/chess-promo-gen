import aiohttp
import asyncio
import fake_useragent
import random_strings
from colorama import Fore
from assets.formatt import GetFormattedProxy
import yaml
import os


class Chess:
    def __init__(self, proxy=None):
        self.proxy = proxy
        self.name = random_strings.random_string(3)
        self.headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "en-US,en;q=0.9",
            "user-agent": fake_useragent.UserAgent().random,
        }

    async def gen(self):

        try:


            async with aiohttp.ClientSession(headers=self.headers) as session:
                proxy = self.proxy if self.proxy else None

                
                async with session.get(
                    f"https://www.chess.com/member/{self.name}",
                    proxy=proxy
                ) as res:
                    
                    if res.status != 200:
                        print(f"{Fore.RED}Failed to get uuid{Fore.RESET}")
                        return False

                    text = await res.text()
                    uuid = text.split('data-user-uuid="')[1].split('"')[0]

                async with session.post(
                    "https://www.chess.com/rpc/chesscom.partnership_offer_codes.v1.PartnershipOfferCodesService/RetrieveOfferCode",
                    json={"userUuid": uuid, "campaignId": "4daf403e-66eb-11ef-96ab-ad0a069940ce"},
                    proxy=proxy
                ) as res:
                    

                    res.raise_for_status()


                    code = f'https://promos.discord.gg/{(await res.json())["codeValue"]}'
                    print(f"{Fore.GREEN}{code}{Fore.RESET}")

                    with open('output/codes.txt', 'a') as f:
                        f.write(code + '\n')

        except Exception as e:

            print(f"{Fore.RED}Failed to fetch promo code! {e}{Fore.RESET}")

async def main():
    with open('config.yml', 'r') as f:
        config = yaml.safe_load(f)
        proxy = config.get('proxy', '').strip()
        proxy = GetFormattedProxy(proxy)

    os.system('cls' if os.name == 'nt' else 'clear')

    workers = int(input(f"{Fore.YELLOW}Workers: {Fore.RESET}"))

    while True:
        tasks = [Chess(proxy).gen() for _ in range(workers)]
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())