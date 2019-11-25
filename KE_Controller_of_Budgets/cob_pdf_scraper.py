# -*- coding: utf-8 -*-
from google.colab import drive , files
import os
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

base_url = "https://cob.go.ke/publications/?cp_consolidated-county-review="

headers = {
    'Content-Type': 'application/pdf',
}

# Commented out IPython magic to ensure Python compatibility.
# %cd /content/drive/'My Drive'/Colab_Notebooks/COB

#If there is no such folder, the script will create one automatically
folder_location = "./cob_pdf"

if not os.path.exists(folder_location):os.mkdir(folder_location)

for page in range(1,3,1)
  url = base_url + str(page)
  response = requests.get(url)
  soup= BeautifulSoup(response.text, "html.parser")
  all = soup.find_all("a",{"class" :"wpdm-download-link [btnclass]"})

  for link in all:
      #Name the pdf files using the last portion of each link which are unique in this case
      filename = os.path.join(folder_location,link['onclick'].split("/")[4]+".pdf")
      with open(filename, 'wb') as f:
          doc_file = requests.get(urljoin(url,link['onclick'])).content
          f.write(doc_file)
