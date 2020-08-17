import requests
from bs4 import BeautifulSoup
from time import sleep
from twilio.rest import Client
from datetime import datetime, timedelta, date
from secrets import account_sid, auth_token
import csv
import statistics


class PriceTracker:
    """Initialzes the PriceTracker class. THe min_value attribute indicates as the critical value of the tracked
    currency. Track_to is for the time of when the tracking suppose to end. And warning calls is to track the
    number of an emergency calls"""

    def __init__(self, min_value: float, track_to: datetime, emergency_number: str):
        self.min_value = min_value
        self.track_to = track_to
        self.warning_calls = 0
        self.emergency_number = emergency_number

    def make_phone_call(self):
        """Methods that connects to the API of the Twilio service and make a phone call"""
        client = Client(account_sid, auth_token)

        call = client.calls.create(
            url='http://demo.twilio.com/docs/classic.mp3',
            to=self.emergency_number,
            from_='+16505499680'
        )

        print(call.sid)

    def send_a_message(self, message: str):
        """Connecting to api of the Twilio.com and sends a text message to the provided number"""

        client = Client(account_sid, auth_token)

        message = client.messages \
            .create(
            body=message,
            to=self.emergency_number,
            from_='+16505499680'
        )

        print(message.sid)

    @staticmethod
    def track_price():
        """Method gets and extracts the price for EUR/PLN value from yahoo finance. Extracting the date was possible due
        to use of bs4"""
        r = requests.get('https://finance.yahoo.com/quote/EURPLN=X?p=EURPLN%3DX&.tsrc=fin-srch&guce_referrer'
                         '=aHR0cHM6Ly9maW5hbmNlLnlhaG9vLmNvbS8_Z3VjZV9yZWZlcnJlcj1hSFIwY0hNNkx5OTNkM2N1WjI5d'
                         'loyeGxMbU52YlM4Jmd1Y2VfcmVmZXJyZXJfc2lnPUFRQUFBRG1vS3ROMkF5bzFpTDRpd29Td0Z4Z0NDTVN'
                         'XU3M0UkNoa2pBcGl2NmxobmxJcWRab0JIWUF6NVJuNHlZdkN1WTRBNEdwVTRfWjBZQ3JNM1RwX2ZMd05rej'
                         'g0TkVWdksyUzA3LVNmNXdndUJCUjhieG5sZEN4dGRCRmV6eEZfMnNQdEpQeXJ6UzREeV9WRUF4ZXNUMXNLYz'
                         'lnTm1pSlFCV3R6LVpLX0hvc2p5Jl9ndWNfY29uc2Vud'
                         'F9za2lwPTE1OTcwODc3MTg&guce_referrer_sig=AQAAAKzjjM2--Diw1M3gykrGHjIn9NdqSch_odxmo6xqtgD4pNo'
                         'anrEQBgPoZ9xkh8HPYFN1_9mpio4Fg2tEGa4GrsK69bHe4yN9LactTwdKEuBxazZPO751TNSeFH_lltkNoN1k7D6I978v'
                         '1eXB9WaCp0NUgbRZRmbYEdoZmkmQvUq7&_guc_consent_skip=1597087949')
        if r.status_code != 200:
            raise ConnectionError
        else:
            soup = BeautifulSoup(r.text, 'html.parser')
            price_elem = soup.find('span', {"class": "Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)"})
            return float(price_elem.text)

    def check_min_value(self, tracked_price):
        """Method that check if the currency dropped under critcal value. Make 3 warning calls, after 3 call sents a
        warning message"""
        if tracked_price < self.min_value and self.warning_calls <= 2:
            print(f'Warning! Price dropeed under {self.min_value} pln {tracked_price}')
            self.make_phone_call()
            self.warning_calls += 1
        elif tracked_price < self.min_value and self.warning_calls == 3:
            self.send_a_message(
                f'This is a warning message. Price of EUR/PLN dropped under critical value!'
                f' {self.min_value} pln')
            print(f'Called 3 times! Price dropeed under {self.min_value} pln {tracked_price}')
            self.warning_calls = 0
        else:
            print(f"Current price for Euro in PLN is {tracked_price}")

    def write_to_file(self):
        """Writes a tracked views to to the csv file to generate report"""
        name = datetime.today().date()
        with open(f'{name}.csv', 'w', newline='') as file_create:
            fieldnames = ['date', 'value_in_pln']
            writer = csv.DictWriter(file_create, fieldnames=fieldnames)
            writer.writeheader()
        while datetime.today() < self.track_to:
            value_of_currency = PriceTracker.track_price()
            with open(f'{file_create.name}', 'a', newline='') as file_append:
                fieldnames = ['date', 'value_in_pln']
                writer = csv.DictWriter(file_append, fieldnames=fieldnames)
                writer.writerow({'date': datetime.today().strftime("%H:%M:%S"), 'value_in_pln': value_of_currency})

            self.check_min_value(tracked_price=value_of_currency)
            sleep(1)

        return self.generate_report(file_create.name)

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

            body_of_report = f'The daily report of the Value Tracker. The mean EUR/PLN price for ' \
                             f'{datetime.today().date()} was' \
                             f' {round(statistics.mean(values_of_eur), 3)}. The currency dropped {under_min_value}' \
                             f' times under critical value.'
            return body_of_report

    @staticmethod
    def get_tommorows_noon_time():
        """ Method returns the tommorrows date at noon. The tracking will last till the end of current day"""
        dt = datetime.combine(date.today() + timedelta(days=1), datetime.min.time())
        return dt


if __name__ == "__main__":
    while True:
        print(f'Tracking EUR/VAL for the {date.today()}')
        tracker = PriceTracker(min_value=4.2, track_to=datetime.today() + timedelta(minutes=1),
                               emergency_number='specified_number')
        report = tracker.write_to_file()
        tracker.send_a_message(message=report)
        print('Finished with price tracking for tommorrow. The report has been send.')
        sleep(5)
