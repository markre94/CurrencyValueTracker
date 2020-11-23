# Currency Value Tracker

### Functionality

The script provides a legit information about current price of the Euro currency in polish zloty's. The information is being acquired from the yahoo finance in real time.
The tracker also comes with the abilty to notify the user about the sudden drop of the monitored value via phone call and/or text message. This peculiar connection feature
was established with the use of the Twilio Communication API.

Whenever the price drops under the value specified by the user the make_phone_call method makes the phone call to the verifed number as a warning.
After the specifed time of a price monitoring the script sends a message with the summary report containing the mean of tracked price value, 
along with the information of how many times the currency dropped under critical value (specified by the user).


### File structure

The CurrencyValueTracker consist of the following files:
- tracker.py _the main file containing PriceTracker class which enables real time EUR/PLN price tracking_
- requirements.txt _contains the required packages for the project._


- secrets.py _the secret file containing authentication keys needed to connect with Twilio Api._
- conftest.py _contains the fixtures used in texting the script._
- unit_test.py _test file contaning the array of unitests written with pytest - still in development._

The test files are still being developed.  


### Autentication 
The Twilio API provides the phone number used in the script along with other authentication data needed for sending the text messages and making a warning phone calls.
To connect with the Twilio API the personal account must be created. The details of how to connect with the API, make a phone call or receive the personal authetication tokens
are all contined in the Twilio docs. Please visit https://www.twilio.com/docs for further infromations.


### Additinal challenges

- [ ] complete the unit_test.py file and generate the testing html report 
- [ ] improve the current script by adding the features like generating a weekly reports containing line plots that would describe variabilty of the monitored price
      and sending it as a fully generated report in PDF via e-mail. The e-mail address will be specified by the user. 
- [ ] add data science to predict the price of the tracked currency
- [ ] restruct the code. Use SOLID and Python Design Patterns.
