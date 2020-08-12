import requests
from bs4 import BeautifulSoup
from time import sleep
from twilio.rest import Client
from datetime import datetime
from datetime import timedelta
from datetime import date
import csv
import statistics


class PriceTracker:
    def __init__(self, min_value: float, track_to: datetime):
        self.min_value = min_value
        self.track_to = track_to
        self.warnings = 0

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
                         '=aHR0cHM6Ly9maW5hbmNlLnlhaG9vLmNvbS8_Z3VjZV9yZWZlcnJlcj1hSFIwY0hNNkx5OTNkM2N1WjI5d'
                         'loyeGxMbU52YlM4Jmd1Y2VfcmVmZXJyZXJfc2lnPUFRQUFBRG1vS3ROMkF5bzFpTDRpd29Td0Z4Z0NDTVN'
                         'XU3M0UkNoa2pBcGl2NmxobmxJcWRab0JIWUF6NVJuNHlZdkN1WTRBNEdwVTRfWjBZQ3JNM1RwX2ZMd05rej'
                         'g0TkVWdksyUzA3LVNmNXdndUJCUjhieG5sZEN4dGRCRmV6eEZfMnNQdEpQeXJ6UzREeV9WRUF4ZXNUMXNLYz'
                         'lnTm1pSlFCV3R6LVpLX0hvc2p5Jl9ndWNfY29uc2Vud'
                         'F9za2lwPTE1OTcwODc3MTg&guce_referrer_sig=AQAAAKzjjM2--Diw1M3gykrGHjIn9NdqSch_odxmo6xqtgD4pNo'
                         'anrEQBgPoZ9xkh8HPYFN1_9mpio4Fg2tEGa4GrsK69bHe4yN9LactTwdKEuBxazZPO751TNSeFH_lltkNoN1k7D6I978v'
                         '1eXB9WaCp0NUgbRZRmbYEdoZmkmQvUq7&_guc_consent_skip=1597087949')

        soup = BeautifulSoup(r.text, 'html.parser')
        price_elem = soup.find('span', {"class": "Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)"})
        sleep(10)
        return float(price_elem.text)

    def check_min_value(self, tracked_price):
        if tracked_price < self.min_value and self.warnings <= 2:
            print(f'Warning! Price dropeed under {self.min_value} pln {tracked_price}')
            # PriceTracker.make_phone_call()
            self.warnings += 1
        elif tracked_price < self.min_value and self.warnings == 3:
            # PriceTracker.send_a_report(
            #     f'This is a warning message. Called 3 times already. Price of EUR/PLN dropped under critical value'
            # f' {self.min_value} pln')
            print(f'Called 3 times! Price dropeed under {self.min_value} pln {tracked_price}')
        else:
            print(f"Current price for Euro in PLN is {tracked_price}")

    def write_to_file(self):
        name = datetime.today().date()
        with open(f'{name}.csv', 'w', newline='') as file:
            fieldnames = ['date', 'value_in_pln']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            while datetime.today() < self.track_to:
                value_of_currency = PriceTracker.track_price()
                writer.writerow({'date': datetime.today().strftime("%H:%M:%S"), 'value_in_pln': value_of_currency})

                self.check_min_value(tracked_price=value_of_currency)

        return self.generate_report(file.name)

    def generate_report(self, file_name: str):
        """Generates a daily report that will be send with SMS message"""
        with open(f'{file_name}', 'r') as file:
            csv_reader = csv.DictReader(file)
            values_of_eur = []
            under_min_value = 0
            for value in csv_reader:
                values_of_eur.append(float(value ['value_in_pln']))
                if float(value ['value_in_pln']) < self.min_value:
                    under_min_value += 1

            body_of_report = f'The daily report of the Value Tracker. The mean EUR/PLN price for {datetime.today().date()} was' \
                             f' {round(statistics.mean(values_of_eur), 3)}. The currency dropped {under_min_value} times under critical value.'
            return body_of_report

    @staticmethod
    def get_tommorows_date():
        """ Method returns the tommorrows date at noon. The tracking will last till the end of current day"""
        # y = datetime.today().date() + timedelta(days=1)
        # min = datetime.min.time(0,0)
        dt = datetime.combine(date.today() + timedelta(days=1), datetime.min.time())
        return dt


if __name__ == "__main__":
    while True:
        bot = PriceTracker(min_value=4.402, track_to=PriceTracker.get_tommorows_date())

        report = bot.write_to_file()

        bot.send_a_report(message=report)

        print('Finished with price tracking for tommorrow. The report has been send.')
