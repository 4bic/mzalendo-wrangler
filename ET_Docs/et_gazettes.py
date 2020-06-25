# -*- coding: utf-8 -*-

from google.colab import drive , files
import os, os.path
import requests
from bs4 import BeautifulSoup as BS
from urllib.parse import urljoin
from pathlib import Path

# Commented out IPython magic to ensure Python compatibility.
# %cd "/content/drive/My Drive/Colab_Notebooks/ET"

"""## Regulations"""

pdf_links = []

def get_page(base_url):
  response = requests.get(base_url)
  c = response.content
  soup = BS(c,"html.parser")
  section = soup.find('section',{'class':'entry'})
  elements = section.find_all('a')
  # all = soup.find_all('p',{'style':'text-align: center;'})
  return elements

# period_links = []

def clean_links(page):
  links = []
  for row in page:
      link  = row.get("href")
      link_name = row.text.title()
      try:
        if link[-4:] != '.jpg':
          links.append(link)
      except Exception as e:
          print(e,"Doc not found or File doesn't Exist")

  return links

def gather_docs(period):
  doc_links  = []
  for link in period:
    doc_link = get_page(link)
    cleaned_link = clean_links(doc_link)
    if cleaned_link['href'][-4:]=='.pdf':
      doc_links.append(cleaned_link)
  return doc_links


def grab_pdf(links_list):
  for link in links_list:
    # url = link.get("href")
    try:
      if link.endswith('pdf'):
        pdf_links.append(link)
    except Exception as e:
       pass
  # return pdf_links


def download_pdf():
  # pdf_links = grab_pdf(links_list)
  try:
    for doc in pdf_links:
      if not os.path.exists(folder_location):
          os.makedirs(folder_location)
          
          metadata = {
            'title': doc.split("/")[-1],
            'country': 'Ethiopia'
            }
          file_name = doc.split("/")[-1]
          file_path = Path(os.path.join(folder_location,file_name))

          ####  make Downloads
          content= requests.get(doc)
          try:
              if not file_path.is_file():
                if content.status_code==200 and content.headers['content-type']=='application/pdf':
                  with open(file_name, 'wb') as pdf:
                    pdf.write(content.content)
          except Exception as e:
            print(e,"Doc hasn't been posted or File Exists")
  except Exception as e:
      pass

def scrape_ET():
  base_page = get_page(base_url)
  _period = clean_links(base_page)
  for time in _period:
    doc_links = get_page(time)
    time_pdf = clean_links(doc_links)
    download_pdf()



if __name__=='__main__': 

  base_url = "https://chilot.me/council-of-ministers-regulations/"
  folder_location = '/content/drive/My Drive/Colab_Notebooks/ET/regulations'
  scrape_ET()

