from bs4 import BeautifulSoup
import requests
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

URL = "https://fibalivestats.dcd.shared.geniussports.com/u/ABE/2310604/bs.html#ASFSK"
page = requests.get(URL)
soup = BeautifulSoup(page.text, "html")

def flatten_and_append(data, new_list=None):
  if new_list is None:
    new_list = []
  
  for item in data:
    if isinstance(item, list):
      new_list = flatten_and_append(item, new_list)
    else:
      new_list.append(item)

  return new_list

def selenium_extractor_bench(URL):
    
    options = Options()
    options.add_argument("--headless") 
    driver = webdriver.Chrome(options=options)
    driver.get(URL)
    
    element_bench = driver.find_elements(By.CLASS_NAME, "bench")
    player_stats_bench = element_bench[0].text
    
    return player_stats_bench

def selenium_extractor_starters(URL):
    
    options = Options()
    options.add_argument("--headless") 
    driver = webdriver.Chrome(options=options)
    driver.get(URL)
    
    element_starters = driver.find_elements(By.TAG_NAME, "tbody")
    player_stats_starters = element_starters[1].text
    
    return player_stats_starters

def dictionary_creator(boxscore_section):

  player_stats_splitted = boxscore_section.split("\n")

  for i in range(0, len(player_stats_splitted), 3):
    player_stats_splitted[i+2] = player_stats_splitted[i+2].split(" ")
      
  flattened_list = flatten_and_append(player_stats_splitted)
  starters = {f"starter_{i + 1}": flattened_list[i:i+24] for i in range(0, len(flattened_list), 24)}

  return starters

boxscore = soup.find_all("table")[1]
column_names = []
headers = boxscore.find("thead").findAll("th")

for th in headers:
    column_names.append(th.text.strip())
column_names = column_names[:24]

player_stats_starters = dictionary_creator(selenium_extractor_starters("https://fibalivestats.dcd.shared.geniussports.com/u/ABE/2310604/bs.html#ASFSK"))
player_stats_bench = dictionary_creator(selenium_extractor_bench("https://fibalivestats.dcd.shared.geniussports.com/u/ABE/2310604/bs.html#ASFSK"))

import pandas as pd
df = pd.DataFrame(columns= column_names)

for key, value in player_stats_starters.items():
    df.loc[len(df)] = value
    
for key, value in player_stats_bench.items():
    df.loc[len(df)] = value
    
print(df)