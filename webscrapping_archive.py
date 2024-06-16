from bs4 import BeautifulSoup
import requests
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd

def team_checker(driver):
    home_team = driver.find_elements(By.TAG_NAME, "tr")
    home_team_finder = home_team[0].text
    
    if home_team_finder.split(" ")[0] == "ITS":
        return True
    return False

def soup_initializer(URL): 
    page = requests.get(URL)
    soup = BeautifulSoup(page.text, "html")
    return soup
  
def initialize_driver(URL):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get(URL)
    return driver

def flatten_and_append(data, new_list=None):
  if new_list is None:
    new_list = []
  
  for item in data:
    if isinstance(item, list):
      new_list = flatten_and_append(item, new_list)
    else:
      new_list.append(item)

  return new_list

def selenium_extractor_bench(driver):
    element_bench = driver.find_elements(By.CLASS_NAME, "bench")
    player_stats_bench = element_bench[0].text
    
    return player_stats_bench
  
def selenium_extractor_starters(driver):
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

def dataframe_inserter(dictionary, dataframe):
    for key, value in dictionary.items():
        dataframe.loc[len(dataframe)] = value
    return dataframe
  
def column_extractor(soup):    
    boxscore = soup.find_all("table")[1]
    column_names = []
    headers = boxscore.find("thead").findAll("th")

    for th in headers:
        column_names.append(th.text.strip())
    column_names = column_names[:24]
    
    return column_names
  
def main():
    URL = "https://fibalivestats.dcd.shared.geniussports.com/u/ABE/2310539/bs.html#ASFSK"
    
    soup = soup_initializer(URL)
    driver = initialize_driver(URL)
    
    column_names = column_extractor(soup)
    df = pd.DataFrame(columns= column_names)
    
    if team_checker(driver) == True:
    
        try:
            starter_stats = selenium_extractor_starters(driver)
            player_stats_starters = dictionary_creator(starter_stats)
            
            
            bench_stats = selenium_extractor_bench(driver)
            player_stats_bench = dictionary_creator(bench_stats)
            
            df = dataframe_inserter(player_stats_starters, df)
            df = dataframe_inserter(player_stats_bench, df)
            
        finally:
            driver.quit()
        
    return df

print(main())