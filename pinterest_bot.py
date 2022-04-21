from selenium import webdriver
import time
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import csv
import spintax
import sys
import subprocess
import os
import random
import scrape_20 as scrape


def install_packages():
    packages_used = ["selenium", "bs4", "pandas", "spintax"]
    for package in packages_used:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])


def get_url(item):
    """" returns the url of the item to be searched on pinterest"""

    var = item
    url = f"https://www.pinterest.com/search/pins/?q={var}&rs=typed&term_meta[]={var}%7Ctyped"
    return url


def fetching_links(driver, url, num):
    """ Returns a list of links saved in an str format
    Since, it's a dynamic website therefore some loading is done by the program
    for acquiring the desired amount of links"""

    driver.maximize_window()
    list_of_resulting_links = []

    scroll_number = 4  # The depth we wish to load
    sleep_timer = 1  # Waiting 4 second for page to load

    driver.get(url)

    for _ in range(1, scroll_number):
        driver.execute_script("window.scrollTo(1,100000)")  # scrolling in order to receive more data
        print("scrolling")
        time.sleep(sleep_timer)

    soup = BeautifulSoup(driver.page_source, 'lxml')

    for link in soup.find_all('a'):
        temp = link.get("href")
        if "/pin/" not in temp:
            pass
        list_of_resulting_links.append(str(temp))

    # the last 5 results are regarding the privacy policy
    # and the first 2 are unrelated
    for i in range(5):
        if i < 2:
            list_of_resulting_links.pop(0)
        list_of_resulting_links.pop()

    list_of_resulting_links = list_of_resulting_links[:num]

    return list_of_resulting_links


def save_to_csv(data):
    """ saves the links into Links.csv file"""

    file = open("Links.csv")
    csv_reader = csv.reader(file)
    rows = []
    for row in csv_reader:
        if row == '0':
            pass
        else:
            rows.extend(row)
    file.close()

    if not rows:
        df = pd.DataFrame(data)
        df.to_csv("Links.csv", index=False)
    else:
        data.extend(rows)
        df = pd.DataFrame(data)
        df.to_csv("Links.csv", index=False)


def load_previous_links():
    """loads the links from Links.csv to a flattened list"""

    file = open("Links.csv")
    csv_reader = csv.reader(file)
    rows = []
    csv_reader = [element for sublist in csv_reader for element in sublist]
    for row in csv_reader:
        if row != "0":
            rows.append(row)
    return rows


def load_current_link():
    """loads the currently saved links from Links.csv to a flattened list"""

    file = open("Links.csv")
    csv_reader = csv.reader(file)
    rows = []
    csv_reader = [element for sublist in csv_reader for element in sublist]
    csv_reader.pop(0)
    for row in csv_reader:
        if row == "0":
            return rows
        rows.append(row)
    return rows


def post_pin(driver):
    sites = ["https://www.jeansmeta.com/"]  # your sites here
    for site in sites:
        driver.get(site)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        titles = scrape.get_titles(soup)
        descriptions = scrape.get_desc(soup)
        image_links = scrape.get_images(driver, scrape.get_image_links(soup))
        scrape.downloading_img(image_links)
        driver.maximize_window()

        for i in range(20, 0, -1):
            driver.get("https://pinterest.com/pin-builder/")

            driver.execute_script("window.scrollTo(1,350)")

            title_input = driver.find_element(By.XPATH, "//textarea[@class = 'TextArea__textArea TextArea__bold"
                                                        " TextArea__enabled TextArea__large TextArea__wrap']")
            title_input.click()
            title_input.send_keys(titles[-i + 20])

            about_input = driver.find_element(By.XPATH, "//div[@class = 'public-DraftStyleDefault-block"
                                                        " public-DraftStyleDefault-ltr']")
            about_input.click()
            about_input.send_keys(descriptions[-i + 20])

            # link_input = driver.find_element(By.XPATH, "//textarea[@class ='TextArea__textArea TextArea__dark"
            #                                            " TextArea__hide_scrollbars TextArea__enabled TextArea__medium"
            #                                            " TextArea__nowrap TextArea__sm']")
            # link_input.click()
            # link_input.send_keys(link)

            image_input = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[2]/div/div/div/"
                                                        "div[2]/div[2]/div/div/div/div[2]/div/div/div/"
                                                        "div/div/div[2]/div/div[1]/div/div/div/div/div/div/input")
            path_to_image = os.getcwd() + "\\" + str(i) + ".jpg"
            image_input.send_keys(path_to_image)

            # save button
            driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[2]/div/div/div/div[2]"
                                          "/div[2]/div/div/div/div[2]/div/div/div/div/div/div[1]"
                                          "/div/div[2]/div/div/div/button[1]").click()
            time.sleep(2)

            try:
                # selecting an already created board
                driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[2]/div/div/div/div[2]/div[2]"
                                              "/div/div/div/div[2]/div/div/div/div/div/div[1]/div/div[2]/"
                                              "div/div/div[2]/div/div/div/div/div/div/div/div/div/div[2]/"
                                              "div[2]/div/div/div/div[2]/div").click()

            except NoSuchElementException:
                # create board button
                driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[2]/div/div/div/div[2]/div[2]/"
                                              "div/div/div/div[2]/div/div/div/div/div/div[1]/div/div[2]/div/"
                                              "div/div[2]/div/div/div/div/div/div/div/div/div/div[3]/div/div/"
                                              "div/div[2]").click()
                time.sleep(2)

                try:
                    driver.find_element(By.XPATH, "/html/body/div[4]/div/div/div/div[2]"
                                                  "/div/div[2]/div/form/div/div[1]/span/div/input").send_keys(
                        "Articles to buy"
                    )
                except NoSuchElementException:
                    driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div/div[2]"
                                                  "/div/div[2]/div/form/div/div[1]/span/div/input").send_keys(
                        "Articles to buy"
                    )

                driver.find_element(By.XPATH, "/html/body/div[4]/div/div/div/div[2]"
                                              "/div/div[3]/div/div/div/div/div/button").click()
                time.sleep(2)

            driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[2]/div/div"
                                          "/div/div[2]/div[2]/div/div/div/div[2]/div"
                                          "/div/div/div/div/div[1]/div/div[2]/div/div/div/button[2]").click()
            print(i, "pin uploaded")
            # time.sleep(1075)
            time.sleep(5)
        print(f"\nall posts covered form the url {site}")
        scrape.delete_images()


def comment(driver, list_of_links):
    """ for logging in the specified account"""

    driver.maximize_window()
    try:

        # lag for the login time
        time.sleep(7)
        count = 0
        for link in list_of_links:
            # will randomly select an integer from 1-13 and the delay will be randomised
            time.sleep(random.randint(1, 3))
            count += 1
            try:
                driver.get("https://www.pinterest.com" + link)
                time.sleep(2)

                # finding the comment box
                driver.execute_script("window.scrollTo(1,350)")
                comment_box = driver.find_element(By.XPATH, "//textarea[@data-test-id='communityItemTextBox']")
                comment_box.click()

                # Sending data to the comment box
                time.sleep(1)
                comment_text = driver.find_element(By.XPATH, "//div[@data-test-id='add-comment']"
                                                             "/div/div/div/div[2]/div/div/div/div/div/div/div/div/span")
                # add your comments here inside the curly braces, in between the pipes
                comment_text.send_keys(spintax.spin("{Amazing|Awesome|Marvellous|Creative|"
                                                    "incredible|wonderful|lovely|superb} "
                                                    "{piece|work|effort|accomplishment|"
                                                    "creation|work of art|achievement}"))

                # confirming the comment
                done_btn = driver.find_element(By.XPATH, "//div[@data-test-id='activity-item-create-submit']/button")
                done_btn.click()

            except Exception:
                print(f"Could not comment on link {count}, comments were disabled")
                continue

        time.sleep(3)

    except Exception as e:
        print("There was an error in the connection, please try again.", e)


if __name__ == '__main__':

    install_packages()

    # insert your accounts here
    your_accounts = [["quora@andblinds.com", "asdjkl"]]
    selected_acc = random.choice(your_accounts)

    options = Options()
    options.add_experimental_option("detach", True)
    s = Service(os.getcwd() + "\\chromedriver.exe")
    driver = webdriver.Chrome(service=s, options=options)
    driver.maximize_window()
    driver.get("https://www.pinterest.com/")

    # finding the login button
    login_btn = driver.find_element(By.XPATH,
                                    "//div[@id= '__PWS_ROOT__']/div/div/div/main/div/div/div[2]/div[2]/button")
    login_btn.click()

    # finding the email input box
    email = driver.find_element(By.ID, "email")
    email.click()
    email.send_keys(selected_acc[0])  # email used

    # finding the email input box
    pwd = driver.find_element(By.ID, "password")
    pwd.click()
    pwd.send_keys(selected_acc[1])  # password used

    # finding the submit button
    submit = driver.find_element(By.XPATH,
                                 "//div[@data-test-id= 'registerFormSubmitButton']/button")
    submit.click()

    print("\nHello there, this is your Pinterest bot.")
    while True:
        print("""\nYou can perform the following actions:
1) Enter a new Search term
2) Use the previous Links
3) Start posting
4) Close the browser
5) Exit""")

        opt = input("\nYour option : ")

        if opt == "1":
            item = input("\nEnter the item that you desire to search: ")
            try:
                print("Enter the number of links you wish to fetch or "
                      "press any non-numeric key to exit")

                no_of_links = int(input())
                print("\nFetching links\n")
                links = fetching_links(driver, get_url(item), no_of_links)

                save_to_csv(links)
                print("\nAll links saved to links.csv")

                print("\nNow commenting.\n")
                comment(driver, load_current_link())
                break

            except ValueError:
                print("Have a good day!")
                break

        elif opt == "2":
            print("\nCommenting on the previously stored links")
            comment(driver, load_previous_links())

        elif opt == "3":

            try:
                post_pin(driver)

            except Exception as e:
                print("There was an error with the connection", e)

        elif opt == "4":
            driver.close()

        elif opt == "5":
            print("Have a good day!")
            exit()
        else:
            print("Please enter a valid option and try again")
            continue
