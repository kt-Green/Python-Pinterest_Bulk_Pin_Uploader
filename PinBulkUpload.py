# Created by karth on 6/14/2020
import os
import glob
import time
from selenium import webdriver
from random import randint

# Your Pinterest account details
user_mail = input("Enter your username/email: ") 
user_password = input("Enter your password: ")

# Selenium predefined xpaths and href's do not mess with these predefinition update them if they have expired
pinterest_home = "https://pinterest.ca/"
pin_builder = "https://www.pinterest.ca/pin-builder/"
flex_pre_login = '//*[@id="__PWS_ROOT__"]/div[1]/div/div/div/div[3]/div[1]/div[1]/div[2]/div[1]/button/div'
mail_box = '//*[@id="email"]'
pass_box = '//*[@id="password"]'
login_button = '//*[@id="__PWS_ROOT__"]/div[1]/div/div/div/div[3]/div[1]/div/div/div[1]/div/div/div/div[3]/form/div[5]/button'
pin_name = "//*[starts-with(@id, 'pin-draft-title-')]"
pin_description = "//*[starts-with(@id, 'pin-draft-description-')]"
image_input = "media-upload-input"
drop_down_menu = "//button[@data-test-id='board-dropdown-select-button']"
save_button = "//button[@data-test-id='board-dropdown-save-button']"

# Defining your Pinterest boards
board_names = []
boards = []
index = 0

# Definitions about pins
image_file = 'D:\My album\PinBulk\\'
description = input("Enter a description for your pins **attention this goes for each and every pin in the folder**: ")

#changing directory to the images folder
os.chdir('D:\My album\PinBulk')

#Getting images from file
image_list = []
Extension = ['*.png','*.jpg']
for i in Extension:
    for filename in glob.glob(i):
        image_list.append(filename)

# Defining chrome driver
driver = webdriver.Chrome('C:\WebDrivers\chromedriver')

# Creating a list of available boards
def boardList():
    boards_webelement_list = driver.find_elements_by_xpath('//div[@class="tBJ dyH iFc yTZ pBj DrD IZT mWe z-6"]')
    for board in boards_webelement_list:
        board_names.append(board.get_attribute("innerHTML"))

# Prompting the selection of board from the user
def boardChoice():
    global index
    boardList()
    for num in range(len(board_names)):
        print(str(num)+"-"+board_names[num])
    choice = int(input("Enter the number associated with your selected board: "))
    if choice>=0 and choice<=(len(board_names))-1:
        index = choice
    else:
        boardChoice()
    boardFormat()

# Converting the board_name to a xpath format
def boardFormat():
    for itr in board_names:
        boards.append("//*[@title='{0}']".format(itr))

# Slicing the image name
def pre_name():
    ind = img.find(".")
    find_ind = img[:(ind)]
    pre_name = find_ind.replace("_", " ")
    pre_name = pre_name.upper()
    return pre_name

# To get the boards
def getBoards():
    # Go pin builder page
    driver.get(pin_builder)
    time.sleep(5)

    # Open board drop-down menu
    driver.find_element_by_xpath(drop_down_menu).click()
    time.sleep(3)

    # Choosing your board to pin the images
    boardChoice()

# To pin the image to board
def pin() :
    note = f'{description}'

    # Go pin builder page
    driver.get(pin_builder)
    time.sleep(5)

    # Click the upload button
    driver.find_element_by_id(image_input).send_keys(image_file + img)
    time.sleep(2)

    # Enter pin name
    driver.find_element_by_xpath(pin_name).send_keys(name.title())
    time.sleep(2)

    # Enter description
    driver.find_element_by_xpath(pin_description).send_keys(note)
    time.sleep(2)

    # Open board drop-down menu
    driver.find_element_by_xpath(drop_down_menu).click()
    time.sleep(3)

    # Select board
    driver.find_element_by_xpath(boards[index]).click()
    time.sleep(3)

    # Click publish button
    driver.find_element_by_xpath(save_button).click()
    time.sleep(5)

# Login to your account
def login():
    # Open pinterest on Chrome driver
    driver.get(pinterest_home)
    driver.find_element_by_xpath(flex_pre_login).click()

    # Enter the mail and password to login..
    driver.find_element_by_xpath(mail_box).send_keys(user_mail)
    driver.find_element_by_xpath(pass_box).send_keys(user_password)
    time.sleep(2)
    driver.find_element_by_xpath(login_button).click()
    time.sleep(5)

# Login to your pinterest account
login()
getBoards()
image_count = 0

# when there are files in the folder the image_list will be > 1
while image_count < len(image_list):
    for img in image_list:
        name = pre_name()
        print("Processing", name.title(), "....")
        pin()
        image_count += 1
        time.sleep(randint(0,5))
print("Task Completed! Totally {} images have been pinned!".format(image_count))
driver.quit()
