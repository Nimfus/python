import http.client
from bs4 import BeautifulSoup
import re
import smtplib
from email.mime.text import MIMEText
import time
import subprocess

subLinks = [2, 11]
payload = ""
headers = {
    'cache-control': "no-cache"
}

def parseMainPage(i):
    conn.request("GET", "" + str(i), payload, headers)
    response = conn.getresponse()
    data = response.read().decode('windows-1250')
    conn.close()
    soup = BeautifulSoup(data, 'html.parser')
    result = soup.find_all(bgcolor="#0d73d7")
    getInnerLink(result)


def getInnerLink(pageData):
    for node in pageData:
        soup = BeautifulSoup(str(node), "html.parser")
        result = soup.a
        try:
            if (parseLinkContent(result.contents[0])):
                notifyByEmail('/a039/obj/' + result.get('href'))
                print(result.get('href'))
        except AttributeError:
            print('Something went wrong')


def parseLinkContent(linkContent):
    return bool(re.search("\d", linkContent))


def notifyByEmail(link):
    msg = MIMEText('test')

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("nimfus@gmail.com", "oreeines")
    msg['Subject'] = 'Link: ' + link
    msg['From'] = ''
    msg['To'] = ''
    s.send_message(msg)
    s.quit()


def run(sub_links):
    for i in sub_links:
        parseMainPage(i)


conn = http.client.HTTPConnection("ke.customer.decent.cz")

while True:
    run(subLinks)
    time.sleep(60)
