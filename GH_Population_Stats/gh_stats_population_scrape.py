
from bs4 import BeautifulSoup as BS
import requests
import pandas as pd
import os
import re

def gather_page_all(url,element):
  r = requests.get(url)
  c = r.content
  soup = BS(c, "html.parser")
# check code of loaded page
  all = soup.find_all(element) #.get('href')
  return all

def gather_region_name(reg_url):
  r = requests.get(reg_url)
  c = r.content
  soup = BS(c, "html.parser")
# check source code of loaded page
  region_name = soup.find('div',{'class' :'graphWrap'}).find('h2').text
  return region_name

# extract all regional links
def extract_links(all):
  region_links = []
  for item in all:
    # extract link and clean
    href = item.find('a').get('href').replace("®","&reg")
    link = base_url + href
    # print (link)
    region_links.append(link)
  return region_links

# collect page contents / data for each region
def collect_page_details():
  GH_pop = pd.DataFrame()
  for reg_url in extract_links(all):
      # return regional titles for reference
      region_name = gather_region_name(reg_url)

      # grab table and details
      region_data = pd.read_html(reg_url, attrs = {'class':'TDownloadDoc'})
      K = region_data[0][('Year', 'District Name')]
      V = region_data[0][('Population',    'Population')]
      reg_df = pd.DataFrame(zip(K, V)).dropna()
      reg_df.columns = ['district','population']
      reg_df['district'][0] = region_name + str(' REGION')
      # # clean up
      reg_df = reg_df.drop(2,axis=0)
      # print(reg_df)
      GH_pop = pd.concat([GH_pop,reg_df],ignore_index=True)
  GH_pop.to_csv('gh_pop.csv')
  return GH_pop


def main():
  gather_page_all(base_url,"g")
  extract_links(all)
  collect_page_details()

if __name__ == '__main__':
  base_url = "https://www.statsghana.gov.gh/"
  main()
