import shutil
import requests
from bs4 import BeautifulSoup
import os
import re


def get_titles(soup):
    """fetches all the titles from the given link"""
    titles = soup.findAll("h2")
    titles_lst = []
    for i in titles:
        titles_lst.append(i.text)
    return titles_lst


def get_desc(soup):
    """fetches all the descriptions from the given link"""
    desc = soup.find_all("p")
    desc_lst = []
    for i in desc:
        if "#" in i.text or "$" in i.text or "Disclosure:" in i.text or len(i.text)<2:
            continue
        desc_lst.append(i.text)
    return desc_lst


def get_image_links(soup):
    """fetches all the image links that direct to amazon"""
    images = soup.find_all('a', attrs={'href': re.compile("^https://")})
    images_lst = []
    for i in images:
        if "amazon" in i.get("href") and i.get("href") not in images_lst:
            if "//aax-us-east.amazon-adsystem.com" in i.get("href"):
                continue
            images_lst.append(i.get("href"))
    return images_lst


def get_images(driver, images_lst):
    """from amazon link fetches all the necessary .jpg links"""
    image_links = []
    for url in images_lst:
        driver.get(url)
        soup_ = BeautifulSoup(driver.page_source, 'html.parser')
        image = soup_.find_all("img", class_='a-dynamic-image a-stretch-vertical')
        image = str(image[0])
        image = image.split(',')
        image = image[0][image[0].index("https"):-6]

        image_links.append(image)

    return image_links


def retrieve_img(url, name):
    """takes a url and name and downloads the image from there"""
    filename = name+".jpg"

    # Open the url image, set stream to True, this will return the stream content.
    r = requests.get(url, stream=True)

    # Check if the image was retrieved successfully
    if r.status_code == 200:
        # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
        r.raw.decode_content = True

        # Open a local file with wb ( write binary ) permission.
        with open(filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

        print('Image successfully Downloaded: ', filename)
    else:
        print('Image Couldn\'t be retrieved')


def downloading_img(image_links):
    """downloads all the images and renames them"""
    count = 20
    for i in image_links:
        retrieve_img(i, str(count))
        count -= 1


def delete_images():
    """after the images have been uploaded it deletes all of them"""
    for i in range(1, 21):
        os.remove(os.getcwd() + '\\' + str(i)+".jpg")
    print("all currently downloaded images were deleted")

