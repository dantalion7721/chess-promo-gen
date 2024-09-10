import fake_useragent,random_strings
from colorama import Fore
from assets.formatt import GetFormattedProxy
import yaml,concurrent.futures,os
from tls_client import Session




class Chess:
    def __init__(self, proxy=None):
        self.session = Session(client_identifier="chrome_103")

        if proxy:
            self.session.proxies = GetFormattedProxy(proxy)

        self.name = random_strings.random_string(3)

        self.session.headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "en-US,en;q=0.9",
            "user-agent": fake_useragent.UserAgent().random,
        }
        

    def Gen(self):


        res = self.session.get(
            "https://www.chess.com/member/"+self.name
        )

        if res.status_code != 200:
            return False

        uuid = res.text.split('data-user-uuid="')[1].split('"')[0]



        res = self.session.post(
            "https://www.chess.com/rpc/chesscom.partnership_offer_codes.v1.PartnershipOfferCodesService/RetrieveOfferCode",
            json={"userUuid": uuid, "campaignId": "4daf403e-66eb-11ef-96ab-ad0a069940ce"}
        )

        try:


            code = 'https://promos.discord.gg/'+res.json()["codeValue"]

            print(f"{Fore.GREEN}{code}{Fore.RESET}")

            with open('output/codes.txt','a') as f:
                f.write(code+'\n')

        except Exception as e:

            print(f"{Fore.RED}Failed to fetch promo code! {e}{Fore.RESET}")




def main():
    with open('config.yml', 'r') as f:
        config = yaml.safe_load(f)
        proxy = config.get('proxy', '').strip()

    os.system('cls' if os.name == 'nt' else 'clear')  

    workers = int(input(f"{Fore.YELLOW}Workers: {Fore.RESET}"))

    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        while True:
            futures = [executor.submit(Chess(proxy).Gen) for _ in range(workers)]
            concurrent.futures.wait(futures)


if __name__ == "__main__":
    main()
