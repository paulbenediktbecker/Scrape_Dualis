import codecs
import os
import shutil
import smtplib
import ssl
import time
import json 
import argparse
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
'''
There has to be a file called secret.json :

{
    "1":{
        "passwort_g":"", //password of sender mail
        "recipent": "['test@gmail.com']",
        "sender_email": "testdev@gmail.com",
        "username":"wi12345@lehre.dhbw-stuttgart.de",
        "password":"" //password of dualis 
    },
    "2":{
        "passwort_g":"", //password of sender mail
        "recipent": "['test@gmail.com']",
        "sender_email": "testdev@gmail.com",
        "username":"wi12345@lehre.dhbw-stuttgart.de",
        "password":"" //password of dualis 
    }
}   


'''


# Scraping the current grades for the DHBW Ravensburg
class scrape_Grades():
    def Scrape(self, personal_data):
        username = personal_data["username"]
        password = personal_data["password"]

        # Open chrome with a few options so that it's harder for sites to detect a bot
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        #driver = webdriver.Chrome(options=options, executable_path=r'C:\Users\paulb\git\Dualis_Scrape_Notes\chromedriver.exe')
        driver = webdriver.Chrome(ChromeDriverManager().install(), options= options)
        driver.execute_cdp_cmd("Network.setExtraHTTPHeaders", {"headers": {"User-Agent": "browserClientA"}})
        print('Open Chrome')
        driver.get(
            "https://dualis.dhbw.de/scripts/mgrqispi.dll?APPNAME=CampusNet&PRGNAME=EXTERNALPAGES&ARGUMENTS=-N000000000000001,-N000324,-Awelcome")
        driver.find_element_by_xpath('//*[@id="field_user"]').send_keys(username)
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="field_pass"]').send_keys(password)
        driver.find_element_by_xpath('//*[@id="logIn_btn"]').click()
        print('Logged in')
        time.sleep(2)
        #driver.find_element_by_xpath('//*[@id="link000310"]/a').click()
        driver.find_element_by_xpath('//*[@id="link000307"]/a').click()
        time.sleep(2)
        Noten = driver.find_element_by_xpath('//*[@id="contentSpacer_IE"]/div').text


        ##### start my part
        all_noten = []
        select = Select(driver.find_element_by_id("semester"))
        options = select.options
        for index in range(0, len(options) - 1):
            print(f"SCRAPING SEMESTER {index}")
            select = Select(driver.find_element_by_id("semester"))
            options = select.options
            select.select_by_index(index)
            time.sleep(2)
            # do stuff

            new_noten = []
            for count, link in enumerate(driver.find_elements_by_tag_name("tr")):
                try:
                    current_link = link.find_element_by_xpath(f'//*[@id="Popup_details000{count + 1}"]')
                except NoSuchElementException: 
                    break 
            
                old_window = driver.current_window_handle
                current_link = current_link.click()
                time.sleep(2)
                # changing the handles to access login page
                for handle in driver.window_handles:
                    if handle != old_window:
                        login_page = handle
                        
                # change the control to signin page       
                driver.switch_to.window(login_page)

                

                noten_ret = []
                for note in driver.find_elements_by_tag_name("tr"):
                    noten_ret.append(note.text)

                new_noten.append(noten_ret)
                driver.close()
                time.sleep(2)
                driver.switch_to.window(old_window)
            all_noten.append(new_noten)

        ### end my part 



        driver.quit()
        print('Close Chrome')
        
        return all_noten 

    
    def send_mail(self, diffs, personal_data):
        passwort_g = personal_data["passwort_g"]
        recipent = personal_data["recipent"]
        sender_email = personal_data["sender_email"]
      

        message_content = ""
        for diff in diffs:
            message_content = message_content + "\n"
            message_content = message_content + "Change detected from: " + "\n"
            message_content = message_content + str(diff[0])  + "\n"
            message_content = message_content + "To " + "\n"
            message_content = message_content + str(diff[1])  + "\n"+ "\n"+ "\n"+ "\n"+ "\n"+ "\n"
        port = 465  # For SSL
        context = ssl.create_default_context()
        msg = MIMEMultipart()
        msg.attach(MIMEText(
            message_content))
        msg['Subject'] = 'Dualis'
        msg['From'] = sender_email
        msg['To'] = ", ".join(recipent)  # Therefore you can achieve mutliple recipents

        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login(sender_email, passwort_g)
            print("Login for E-Mail")
            server.sendmail(sender_email, recipent, msg.as_bytes())
            print("Email send")

    def parse_json(self,index):
        with open("secret.json") as f:
            data = json.load(f)

        return data[str(index)]

        
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument("secret_index", type=int)
    args = parser.parse_args()
    secrect_index = args.secret_index



    o = scrape_Grades()
    personal_data = o.parse_json(secrect_index)
    scrape_base = o.Scrape(personal_data)
    print("SCRAPED FIRST")
    minutes_to_wait = 30
    seconds_to_wait = 60 * minutes_to_wait
    
    while True:
        print("SCRAPING NEW ENTRY")
        print("#########################################################################################################")
        scrape_new = o.Scrape(personal_data)

        differences = []

        for x, y in zip(scrape_base,scrape_new):
            for x_2, y_2 in zip(x,y):
                if x_2 != y_2: 
                    differences.append([x_2,y_2])

        if len(differences) != 0 :
            print("#########################################################################################################")
            print("FOUND NEW GRADES. WILL SEND MAIL. WILL WAIT FOR {minutes_to_wait} MINUTES.")
            o.send_mail(differences, personal_data)
        else:
            print("#########################################################################################################")
            print(f"NO NEW GRADES FOUND. WILL WAIT FOR {minutes_to_wait} MINUTES.")
     
        scrape_base = scrape_new
    

        time.sleep(seconds_to_wait)
        
