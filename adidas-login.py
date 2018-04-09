import requests
from bs4 import BeautifulSoup as soup
import re

#Necessary headers
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"
}
headersForData = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"
}

def acountlogin(locale, username, password):
    session = requests.session()
    try:
        if locale == "US":
            #Grab first login page to obtain CSRF Token
            Request1 = session.get("https://cp.adidas.com/web/eCom/en_US/loadsignin?target=account", headers=headers)
            #parsing and finding CSRF token
            html = soup(Request1.text, "html.parser")
            CSRF = html.find("input", {"name": "CSRFToken"})["value"]
            #payload required for Request2
            payload = {
                "username": username,
                "password": password,
                "signinSubmit": "Sign in",
                "IdpAdapterId": "adidasIdP10",
                "SpSessionAuthnAdapterId": "https://cp.adidas.com/web/",
                "PartnerSpId": "sp:demandware",
                "remembermeParam": "",
                "validator_id": "adieComDWus",
                "TargetResource": "https://www.adidas.com/on/demandware.store/Sites-adidas-US-Site/en_US/MyAccount-ResumeLogin?target=account&target=account",
                "InErrorResource": "https://www.adidas.com/on/demandware.store/Sites-adidas-US-Site/en_US/null",
                "loginUrl": "https://cp.adidas.com/web/eCom/en_US/loadsignin",
                "cd": "eCom|en_US|cp.adidas.com|null",
                "app": "eCom",
                "locale": "en_US",
                "domain": "cp.adidas.com",
                "email": "",
                "pfRedirectBaseURL_test": "https://cp.adidas.com",
                "pfStartSSOURL_test": "https://cp.adidas.com/idp/startSSO.ping",
                "resumeURL_test": "",
                "FromFinishRegistraion": "",
                "CSRFToken": CSRF
            }
            #Request link below to obtain JS redirect link
            Request2 = session.post("https://cp.adidas.com/idp/startSSO.ping", data=payload, headers=headers)
            #Finding and requesting the redirection link
            Request3 = session.get(
                re.search("(?P<url>https?://[^\s]+)", soup(Request2.text, "html.parser").find_all("script")[2].text).group(
                    "url").replace("';", ""), headers=headers)
            #Grabbing necessary values from redirected link
            RelayState = soup(Request3.text, "html.parser").find("input", {"name": "RelayState"})["value"]
            SAMLResponse = soup(Request3.text, "html.parser").find("input", {"name": "SAMLResponse"})["value"]
            #Payload required for Request4
            payload69 = {
                "RelayState": RelayState,
                "SAMLResponse": SAMLResponse
            }
            #
            Request4 = session.post("https://cp.adidas.com/sp/ACS.saml2", data=payload69, headers=headers)
            #Grabbing required REF value and TargetResource value for next request
            REF = soup(Request4.text, "html.parser").find("input", {"name": "REF"})["value"]
            TargetResource = soup(Request4.text, "html.parser").find("input", {"name": "TargetResource"})["value"]
            #Payload for Request5
            data89 = {
                "REF": REF,
                "TargetResource": TargetResource
            }
            #Posting final anti-bot info to adidas to resume login
            Request5 = session.post(
                "https://www.adidas.com/on/demandware.store/Sites-adidas-US-Site/en_US/MyAccount-ResumeLogin",
                data=data89, headers=headers)
            #Checking if login was successfull
            CheckIfLoginSuccess = session.get("https://www.adidas.com/us/myaccount-show?fromlogin=true", headers=headers)
            if CheckIfLoginSuccess.url == "https://www.adidas.com/us/myaccount-show?fromlogin=true":
                print("Logged in.")
                print("Cookies are below:")
                print(session.cookies)
            else:
                print("Login failed.")
        if locale == "UK":
            #Same general idea for UK...
            Request1 = session.get("https://cp.adidas.co.uk/web/eCom/en_GB/loadsignin?target=account", headers=headers)
            html = soup(Request1.text, "html.parser")
            CSRF = html.find("input", {"name": "CSRFToken"})["value"]
            payload = {
                "username": username,
                "password": password,
                "signinSubmit": "Sign in",
                "IdpAdapterId": "adidasIdP10",
                "SpSessionAuthnAdapterId": "https://cp.adidas.com/web/",
                "PartnerSpId": "sp:demandware",
                "validator_id": "adieComDWgb",
                "TargetResource": "https://www.adidas.co.uk/on/demandware.store/Sites-adidas-GB-Site/en_GB/MyAccount-ResumeLogin?target=account&target=account",
                "InErrorResource": "https://www.adidas.co.uk/on/demandware.store/Sites-adidas-GB-Site/en_GB/null",
                "loginUrl": "https://cp.adidas.co.uk/web/eCom/en_GB/loadsignin",
                "cd": "eCom|en_GB|cp.adidas.co.uk|null",
                "remembermeParam": "",
                "app": "eCom",
                "locale": "en_GB",
                "domain": "cp.adidas.co.uk",
                "email": "",
                "pfRedirectBaseURL_test": "https://cp.adidas.co.uk",
                "pfStartSSOURL_test": "https://cp.adidas.co.uk/idp/startSSO.ping",
                "resumeURL_test": "",
                "FromFinishRegistraion": "",
                "CSRFToken": CSRF
            }
            Request2 = session.post("https://cp.adidas.co.uk/idp/startSSO.ping", data=payload, headers=headers)

            Request3 = session.get(
                re.search("(?P<url>https?://[^\s]+)", soup(Request2.text, "html.parser").find_all("script")[2].text).group(
                    "url").replace("';", ""), headers=headers)

            RelayState = soup(Request3.text, "html.parser").find("input", {"name": "RelayState"})["value"]
            SAMLResponse = soup(Request3.text, "html.parser").find("input", {"name": "SAMLResponse"})["value"]
            payload69 = {
                "RelayState": RelayState,
                "SAMLResponse": SAMLResponse
            }
            Request4 = session.post("https://cp.adidas.co.uk/sp/ACS.saml2", data=payload69, headers=headers)

            REF = soup(Request4.text, "html.parser").find("input", {"name": "REF"})["value"]
            TargetResource = soup(Request4.text, "html.parser").find("input", {"name": "TargetResource"})["value"]
            data89 = {
                "REF": REF,
                "TargetResource": TargetResource
            }
            Request5 = session.post(
                "https://www.adidas.co.uk/on/demandware.store/Sites-adidas-GB-Site/en_GB/MyAccount-ResumeLogin",
                data=data89, headers=headers)
            checkifsuccess = session.get(
                "https://www.adidas.co.uk/on/demandware.store/Sites-adidas-GB-Site/en_GB/MyAccount-Show?fromlogin=true",
                headers=headers)
            if checkifsuccess.url == "https://www.adidas.co.uk/on/demandware.store/Sites-adidas-GB-Site/en_GB/MyAccount-Show?fromlogin=true":
                print("Logged in.")
                print("Cookies are below:")
                print(session.cookies)
            else:
                print("Login failed.")
    except Exception as e:
        print("Login code error occured: [ERROR] " + str(e))

print("----------------------------")
print("Adidas login through requests")
print("By @TMCKCM on twitter")
print("----------------------------")
a=input("Locale (UK or US): ")
b=input("Username: ")
c=input("Password: ")
acountlogin(a,b,c)