import requests
from bs4 import BeautifulSoup
from time import sleep


class PriceTracker:
    def make_phone_call(self):
        pass

    @staticmethod
    def track_price():
        r = requests.get('https://finance.yahoo.com/quote/EURPLN=X?p=EURPLN%3DX&.tsrc=fin-srch&guce_referrer'
                         '=aHR0cHM6Ly9maW5hbmNlLnlhaG9vLmNvbS8_Z3VjZV9yZWZlcnJlcj1hSFIwY0hNNkx5OTNkM2N1WjI5dloyeGxMbU52YlM4Jmd1Y2VfcmVmZXJyZXJfc2lnPUFRQUFBRG1vS3ROMkF5bzFpTDRpd29Td0Z4Z0NDTVNXU3M0UkNoa2pBcGl2NmxobmxJcWRab0JIWUF6NVJuNHlZdkN1WTRBNEdwVTRfWjBZQ3JNM1RwX2ZMd05rejg0TkVWdksyUzA3LVNmNXdndUJCUjhieG5sZEN4dGRCRmV6eEZfMnNQdEpQeXJ6UzREeV9WRUF4ZXNUMXNLYzlnTm1pSlFCV3R6LVpLX0hvc2p5Jl9ndWNfY29uc2VudF9za2lwPTE1OTcwODc3MTg&guce_referrer_sig=AQAAAKzjjM2--Diw1M3gykrGHjIn9NdqSch_odxmo6xqtgD4pNoanrEQBgPoZ9xkh8HPYFN1_9mpio4Fg2tEGa4GrsK69bHe4yN9LactTwdKEuBxazZPO751TNSeFH_lltkNoN1k7D6I978v1eXB9WaCp0NUgbRZRmbYEdoZmkmQvUq7&_guc_consent_skip=1597087949')
        soup = BeautifulSoup(r.text, 'html.parser')
        elem = soup.find('span', {"class": "Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)"})
        sleep(1)
        return float(elem.text)


if __name__ == "__main__":

    tracker = PriceTracker()
    while True:
        price = tracker.track_price()
        if price < 4.399:
            print(f'Warning! Price dropeed under 4.399 pln {price}')
        else:
            print(f"Current price for Euro in PLN is {price}")


