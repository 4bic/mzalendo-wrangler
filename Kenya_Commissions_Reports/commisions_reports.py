import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from urllib.parse import urljoin

url = "http://kenyalaw.org/kl/fileadmin/CommissionReports/"

""" Find PDF files and download  
*   create folder
*   collect document links
*   Download from the 2$nd$ link
"""

folder_location = "./commisions_reports"

if not os.path.exists(folder_location):os.mkdir(folder_location)

response = requests.get(url)
soup= BeautifulSoup(response.text, "html.parser")  
# extract `a` tags
all = soup.find_all("a")

for link in all[1:]:
    filename = link.get('href')
    full_name = os.path.join(folder_location,filename)
    with open(full_name, 'wb') as f:
        doc_file = requests.get(urljoin(url,filename)).content
        f.write(doc_file)