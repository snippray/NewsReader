#!/bin/python

import time
import datetime
import notify2
from playsound import playsound
import multiprocessing
from gtts import gTTS
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

def send_notification(number_of_posts):
    notify2.init("New Article")
        
    n = notify2.Notification(f"{number_of_posts} new Threatpost article(s).")
    n.show()

def create_mp3():
    language = 'en'
    f = open(file_name_with_path, "r")
    article_text=f.read()
    voice_obj = gTTS(text=article_text, lang=language, slow=False)
    voice_obj.save(file_name_with_path+'.mp3')

def get_inside_links_content(url,number):
    try:
            wait = WebDriverWait(driver, 30)
            driver.get(url)
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'c-article__main')))
            driver.execute_script("window.stop();")
            inside_content=driver.find_element(By.CLASS_NAME, 'c-article__main').text
            file_name_temp=final_article[number].replace(" ", "_").replace("?" , "_").replace(":", "_").replace("/", "_")
            file_name=file_name_temp + '.txt'
            save_path='./ThreatPost_News'
            global file_name_with_path
            file_name_with_path = os.path.join(save_path, file_name)
            path_exist = os.path.exists(save_path)
            if not path_exist: 
                print("[*] The output will be saved in './ThreatPost_News'")
                os.makedirs(save_path)
            f1= open(file_name_with_path,"w+")
            f1.write(inside_content)
            f1.close()
            driver.quit()                                            
    except Exception as e: 
            print(e)      
            driver.quit()   

emrooz = datetime.datetime.now()
current_date= str(emrooz.strftime("%B") + " " + str(emrooz.day) + ', ' + str(emrooz.year))
print (current_date)
final_article=[]
final_published_dates=[]
final_links=[]
capa = DesiredCapabilities.CHROME
capa["pageLoadStrategy"] = "none"
driver = webdriver.Chrome(desired_capabilities=capa)
wait = WebDriverWait(driver, 30)
driver.get('https://www.threatpost.com')
wait.until(EC.presence_of_element_located((By.TAG_NAME, 'article')))
driver.execute_script("window.stop();")

all_articles = driver.find_elements(By.TAG_NAME,"article")
counter=0
for every in all_articles:
  if counter <4:
    if str(current_date) in str(every.find_element(By.CLASS_NAME, 'c-card__time').text):
        final_article.append(every.find_element(By.CLASS_NAME, 'c-card__title').text)
        find_link=every.find_element(By.TAG_NAME, 'a')
        final_links.append(find_link.get_attribute('href'))
    counter=counter+1
if len(final_article)>0: 
    send_notification(len(final_article))
    for article in range(len(final_article)):
        print(f'{article+1}. ' +final_article[article])
    which_article= input('\nWhich article are you interested in:' )
    if 0 < int(which_article) <= int(len(final_article)):
        selected_article_link=final_links[int(which_article)-1]
        print("[*] I am trying to get the article...")
        get_inside_links_content(selected_article_link,int(which_article)-1)
        create_mp3()
        while True: 
            yes_or_no=input("[*] The article that you have selected is ready. Would you like to hear it now? (Y/N): ")
            if yes_or_no.lower() == 'y':
                playsound(file_name_with_path+'.mp3')
                break                
            elif yes_or_no.lower() == 'n':
                asking_again=input("[+] How long to wait before asking again? (in minutes).\nType 'exit' if you dont want to listen to the article at all: ")
                if asking_again == 'exit':
                    break
                else:    
                    print (f'[*] Alright. I will wait for about {asking_again} minute(s).')
                    time.sleep(int(asking_again)*60)         
            else:
                print ('Wrong input')
    else:
        print('[-] The input is out of range.')  
        driver.quit()  
else:
    print('[-] There is no news today.')
    driver.quit()