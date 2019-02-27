"""
The usual steps to do web scrapping are the following :
1. Perform a HTTP request in order to get the content of the page. It can be
   done very easily with the package `requests` (there is a way to do it with
   builtin packages but it is a lot more difficult). Most of the time, a GET
   request without any configuration is ok but sometimes a more advanced request
   is needed. To get the exact the same request as in the browser, you can
   inspect the request sent by the browser (open Developer Tools in Chrome, go
   to Network tab and find the request with the same URL as the current URL; you
   can filtrate all the requests to get only Doc requests)). Then you can copy
   the request as curl and use a converter (like this one :
   https://curl.trillworks.com/) to convert a curl request into a request made
   with `requests`.
2. If the request is successfull (response code between 200 and 299), you have
   to convert the HTML content of the response into an object you can parse to
   extract information. You can use several different package for that like
   Beautiful Soup but I prefer using `lxml.html` (there are some advanced
   features like XPath in this package (a XPath tutorial:
   https://doc.scrapy.org/en/xpath-tutorial/topics/xpath-tutorial.html)).
3. Extract any information in the page you want by using the right selector. In
   order to get the selector, you have to inspect the code source of the HTML
   page (right click on the element you want to inspect, click on Inspect and
   find the selector which allow you to get all the wanted elements and nothing
   more). Most of the time, these steps are sufficient to perform scrapping
   but sometime, you need to perform additional steps in order to avoid limits
   and bypass anti scrapping systems.

If you want to get information from multiple HTML pages, you have to perform for
loops in order to build a system which can follow links and then parse each page
in the right way.

NB: Scrapy is a good framework if you want to extract information from multiple
pages because it is built in such a way it can follow links for you and perform
the request for you and so you just have to tell him how to extract information
from the HTML content. But in order to master it, you have to know some basics
of web scrapping and then follow the tutorial for Scrapy.
(https://docs.scrapy.org/en/latest/intro/tutorial.html).
"""

import requests
from lxml import html

base_url = 'https://www.idealista.com'
search_path = '/en/buscar/venta-viviendas/madrid/'

# headers dictionary got thanks to https://curl.trillworks.com/.
headers = {
    'authority': 'www.idealista.com',
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
    'user-agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) '
                   'AppleWebKit/537.36 (KHTML, like Gecko) '
                   'Chrome/72.0.3626.109 Safari/537.36'),
    'accept': ('text/html,application/xhtml+xml,application/xml;'
               'q=0.9,image/webp,image/apng,*/*;q=0.8'),
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
    '$cookie': (
        'userUUID=a109f54f-4080-4716-aea8-c1a10b5f4721;'
        '_pxhd=5b3b63f7f9669cd11b8ab0f3de3208a258166d30f5b95d91068b9a8e1df2336f:2f9a2201-32c4-11e9-9118-771865a7de33;'
        'xtvrn=$352991$; xtan352991=2-anonymous; xtant352991=1;'
        'cookieDirectiveClosed=true; pxvid=2f9a2201-32c4-11e9-9118-771865a7de33;'
        '_pxvid=2f9a2201-32c4-11e9-9118-771865a7de33;'
        'atuserid=%7B%22name%22%3A%22atuserid%22%2C%22val%22%3A%223417aa01-068b-4b8c-b502-caee4986164b%22%2C%22options%22%3A%7B%22end%22%3A%222020-03-20T14%3A56%3A22.191Z%22%2C%22path%22%3A%22%2F%22%7D%7D;'
        'atidvisitor=%7B%22name%22%3A%22atidvisitor%22%2C%22val%22%3A%7B%22vrn%22%3A%22-582065-%22%7D%2C%22options%22%3A%7B%22path%22%3A%22%2F%22%2C%22session%22%3A15724800%2C%22end%22%3A15724800%7D%7D;'
        'optimizelyEndUserId=oeu1550415382298r0.5018661705843128;'
        'send5852f4e8-421a-48ab-940b-20c0ffb7f6f1="{\'friendsEmail\':null,\'email\':null,\'message\':null}";'
        'contact0871f9e5-787d-45df-add4-bbcbcf0b2c26="{\'email\':null,\'phone\':null,\'phonePrefix\':null,\'friendEmails\':null,\'name\':null,\'message\':null,\'message2Friends\':null,\'maxNumberContactsAllow\':10,\'defaultMessage\':true}";'
        'SESSION=0871f9e5-787d-45df-add4-bbcbcf0b2c26;'
        'WID=d43ec4496401211f|XGvjF|XGvjF;'
        'utag_main=v_id:0168fbf543bf000eb1a21cd898cd03078001d0700093c$_sn:3$_ss:1$_st:1550576155937$ses_id:1550574355937%3Bexp-session$_pn:1%3Bexp-session;'
        '_px2=eyJ1IjoiNTU3NGIxMjAtMzQzNi0xMWU5LTllOGMtNDM5MmM4MTJkZDQ1IiwidiI6IjJmOWEyMjAxLTMyYzQtMTFlOS05MTE4LTc3MTg2NWE3ZGUzMyIsInQiOjE1NTA1NzQ2NTg5MDIsImgiOiI3MDM1MmQ2ZWE5ZWM0ZDg0MjRlMThjZGVlZjdhYWU2NzYyMjYwZGVlNzM2MTEwYmQ2Y2Q3N2UzOTlkYzI1OTk4In0='
    ),
}

# Cookies have a special treatment in `requests` we have to transform the value
# associated `$cookie` in the header to a dictionary which can be sent with the
# HTTP request. First we get the `$cookie` from `headers` (and we delete it from
# the dictionary at the same time) and then we build the dictionary by splitting
# the string.
cookies = headers.pop('$cookie')
cookies = [cookie.split('=', maxsplit=1) for cookie in cookies.split('; ')]
cookies = dict(cookies)

# Performing the request with the right headers and cookies. Then we transform
# the content of the response thanks to the function `lxml.html.fromstring`.
response = requests.get(base_url + search_path,
                        headers=headers, cookies=cookies)
document = html.fromstring(response.content)

# We can now parse the HTML content to get information we want. Let's build a
# list of dictionary containing all the following information for each result :
# - title
# - price
# - surface
# - phone number
# - garage included
# - url (link to follow to get more information about a result)
# - number of rooms
items = document.cssselect('div.items-container article')
results = []
for item in items:
    phone_number = item.cssselect('span.item-not-clickable-phone')
    if phone_number:
        phone_number = phone_number[0].text
    else:
        phone_number = None

    n_room, surface = [
        int(detail.text.strip())
        for detail in item.cssselect('span.item-detail')[:2]
    ]
    print(dict(
        title=item.cssselect('a.item-link')[0].text,
        url=base_url + item.cssselect('a.item-link')[0].get('href'),
        price=int(item.cssselect('span.item-price')[0].text.replace(',', '')),
        with_garage=bool(item.cssselect('span.item-parking')),
        phone_number=phone_number,
        n_room=n_room,
        surface=surface,
    ))
    print("\n")
    results.append(dict(
        title=item.cssselect('a.item-link')[0].text,
        url=base_url + item.cssselect('a.item-link')[0].get('href'),
        price=int(item.cssselect('span.item-price')[0].text.replace(',', '')),
        with_garage=bool(item.cssselect('span.item-parking')),
        phone_number=phone_number,
        n_room=n_room,
        surface=surface,
    ))
