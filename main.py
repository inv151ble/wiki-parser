from bs4 import BeautifulSoup
import requests
import re
import time
words_in_wiki = 0

def parse_page(page_url):
    global words_in_wiki
    counter=0
    page_request = requests.get("https://en.wikipedia.org/wiki/"+page_url)
    page_soup = BeautifulSoup(page_request.content, "lxml")
    div_p = page_soup.find('div', attrs={'id':"mw-content-text"}).findAll(text=True)
    rg = re.compile('[A-Za-z]{2,}')     #regular expression to brush off 1-worded words and punctuation marks
    for text in div_p:
        temp = []
        temp.extend(text.split())
        for word in temp:
            if rg.match(word):
                counter += 1
    words_in_wiki += counter
    print(str(counter)+" on "+page_url)


def page_from_list(page):
    url_list = 'https://en.wikipedia.org/wiki/Special:AllPages?from='+page+'&to=&namespace=0&hideredirects=1'
    r = requests.get(url_list)
    soup = BeautifulSoup(r.content, "lxml")
    div = soup.find('div', attrs={'class': "mw-allpages-body"}).find_all('a')
    for link in div:
        new_page=link.get("href")[6:] #[6:] to crop "/wiki"
        parse_page(new_page)
        if list.pop(div) is link:
            page_from_list(new_page)

print ("Ready to parse?")
raw_input("Press ENTER to start, press Ctrl+C to stop")
try:
    while 1:
        page_from_list('')
except KeyboardInterrupt: print ("Total words counted: " + str(words_in_wiki))