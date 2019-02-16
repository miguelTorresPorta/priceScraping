#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from requests import get
import pandas as pd
import itertools
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

headers = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})
    
webPage = "https://www.pisos.com/alquiler/pisos-madrid_capital/"
response = get(webPage, headers=headers)
response
html_soup = BeautifulSoup(response.text, 'html.parser')


house_containers = html_soup.find_all('div', class_="price")

first = house_containers[0]
first = first.replace(" ","")
first = first.replace("\r","")
first = first.replace("\n","")

    
dataframe = pd.DataFrame({'prices':house_containers})

dataframe.to_csv(path_or_buf = "./test.csv", index=False)
