import csv
import re

import requests
from tqdm import tqdm

EMAIL = ''
PASSWORD = ''

URL = 'http://front.partysponsors.be/nl/sessions'


def main():
    # Start a session so we can have persistant cookies
    session = requests.session()

    # This is the form data that the page sends when logging in
    login_data = {
        'login': EMAIL,
        'password': PASSWORD,
        'remember_me': '1',
    }

    # Authenticate
    session.post(URL, data=login_data)

    # Try accessing a page that requires you to be logged in

    p = re.compile("<h5>Uw contactgegevens</h5>.*<div class=\"edit\">")
    p_li = re.compile("<li>.*</li>")
    p_gsm = re.compile("<li>.*<span>gsm</span>")
    p_fax = re.compile("<li>.*<span>fax</span>")
    p_tel = re.compile("<li>.*<span>tel</span>")
    p_email = re.compile("<li>.*<span>email</span>")

    fp = csv.writer(open("data.csv", 'w', encoding='utf8', newline=''))
    fp.writerow(["Naam", "Straat", "Gemeente", "Telefoon", "GSM", "Fax", "E-Mail"])

    for i in tqdm(range(0, 70000)):
        r = session.get('http://front.partysponsors.be/nl/organisers/' + str(i))
        if r.status_code == 200:
            m = p.search(str(r.content))
            if m:
                text = m.group(0)
                a = text.split("\\n")
                naam = a[1]
                straat = a[2]
                gemeente = a[3]

                m = p_li.search(text)

                fax = ""
                email = ""
                tel = ""
                gsm = ""
                if m:
                    b = m.group(0).split("</li>")
                    for string in b:
                        c = p_gsm.search(string)
                        if c:
                            gsm = c.group(0)
                            continue
                        c = p_fax.search(string)
                        if c:
                            fax = c.group(0)
                            continue
                        c = p_email.search(string)
                        if c:
                            email = c.group(0)
                            continue
                        c = p_tel.search(string)
                        if c:
                            tel = c.group(0)
                            continue
                naam = clean(naam)
                straat = clean(straat)
                gemeente = clean(gemeente)
                tel = clean(tel)
                gsm = clean(gsm)
                fax = clean(fax)
                email = clean(email)
                # print(naam, straat, gemeente, tel, gsm, fax, email)
                fp.writerow([naam, straat, gemeente, tel, gsm, fax, email])
            else:
                raise Exception('wrong page?')


def clean(string):
    result = re.sub("<span>.*</span>", "", string)
    result = re.sub("<\w{0,2}>", "", result)
    result = result.strip()
    return str(result)


if __name__ == '__main__':
    main()
