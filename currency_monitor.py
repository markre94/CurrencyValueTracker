import requests
from bs4 import BeautifulSoup
from time import sleep
from twilio.rest import Client
from datetime import datetime
import csv


class PriceTracker:
    @staticmethod
    def make_phone_call():
        auth_token = 'f724b54966b1e70ea3571f5e75c8920e'
        account_sid = 'AC3db5ec02ff2806df335242cef7f07c87'
        client = Client(account_sid, auth_token)

        call = client.calls.create(
            url='http://demo.twilio.com/docs/classic.mp3',
            to='+48668397153',
            from_='+16505499680'
        )

        print(call.sid)

    @staticmethod
    def send_a_report(message: str):
        auth_token = 'f724b54966b1e70ea3571f5e75c8920e'
        account_sid = 'AC3db5ec02ff2806df335242cef7f07c87'
        client = Client(account_sid, auth_token)

        message = client.messages \
            .create(
            body=message,
            to='+48668397153',
            from_='+16505499680'
        )

        print(message.sid)

    @staticmethod
    def track_price():
        r = requests.get('https://finance.yahoo.com/quote/EURPLN=X?p=EURPLN%3DX&.tsrc=fin-srch&guce_referrer'
                         '=aHR0cHM6Ly9maW5hbmNlLnlhaG9vLmNvbS8_Z3VjZV9yZWZlcnJlcj1hSFIwY0hNNkx5OTNkM2N1WjI5dloyeGxMbU52YlM4Jmd1Y2VfcmVmZXJyZXJfc2lnPUFRQUFBRG1vS3ROMkF5bzFpTDRpd29Td0Z4Z0NDTVNXU3M0UkNoa2pBcGl2NmxobmxJcWRab0JIWUF6NVJuNHlZdkN1WTRBNEdwVTRfWjBZQ3JNM1RwX2ZMd05rejg0TkVWdksyUzA3LVNmNXdndUJCUjhieG5sZEN4dGRCRmV6eEZfMnNQdEpQeXJ6UzREeV9WRUF4ZXNUMXNLYzlnTm1pSlFCV3R6LVpLX0hvc2p5Jl9ndWNfY29uc2VudF9za2lwPTE1OTcwODc3MTg&guce_referrer_sig=AQAAAKzjjM2--Diw1M3gykrGHjIn9NdqSch_odxmo6xqtgD4pNoanrEQBgPoZ9xkh8HPYFN1_9mpio4Fg2tEGa4GrsK69bHe4yN9LactTwdKEuBxazZPO751TNSeFH_lltkNoN1k7D6I978v1eXB9WaCp0NUgbRZRmbYEdoZmkmQvUq7&_guc_consent_skip=1597087949')
        soup = BeautifulSoup(r.text, 'html.parser')
        price_elem = soup.find('span', {"class": "Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)"})
        sleep(1)
        return float(price_elem.text)

    @staticmethod
    def check_min_value(tracked_price, min_value: float):
        if tracked_price < 4.399:
            print(f'Warning! Price dropeed under {min_value} pln {tracked_price}')
            PriceTracker.make_phone_call()
        else:
            print(f"Current price for Euro in PLN is {tracked_price}")


    @staticmethod
    def write_to_file():
        with open(f'{datetime.utcnow().date()}_data.csv', 'w', newline='') as file:
            fieldnames = ['date', 'value_in_pln']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

            while True:
                price = PriceTracker.track_price()
                writer.writerow({'date': datetime.utcnow().strftime("%H:%M:%S"), 'value_in_pln': price})

                PriceTracker.check_min_value(tracked_price=price, min_value=4.399)


if __name__ == "__main__":
    PriceTracker().write_to_file()


