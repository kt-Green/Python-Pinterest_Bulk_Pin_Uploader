# Created by Karthik on 10/03/2020
import os
import glob
import time
from selenium import webdriver
from random import randint

# Your Pinterest account details
user_mail = "e-mail / username"
user_password = "password"

# Selenium predefined xpaths and href's do not mess with these predefinition update them if they have expired
pinterest_home = "https://pinterest.com/"
pin_builder = "https://in.pinterest.com/pin-builder/"
flex_pre_login = '//*[@id="__PWS_ROOT__"]/div[1]/div/div/div/div[3]/div[1]/div[1]/div[2]/div[1]/button/div'
mail_box = '//*[@id="email"]'
pass_box = '//*[@id="password"]'
login_button = '//*[@id="__PWS_ROOT__"]/div[1]/div[2]/div/div/div[3]/div[1]/div/div/div[1]/div/div/div/div[3]/form/div[5]/button/div'
pin_name = "//*[starts-with(@id, 'pin-draft-title-')]"
pin_description = "//*[starts-with(@id, 'pin-draft-description-')]"
image_input = "media-upload-input"
drop_down_menu = "//button[@data-test-id='board-dropdown-select-button']"
publish_button = "//button[@data-test-id='board-dropdown-save-button']"


# Defining your Pinterest boards
board_names = []
boards = []
ind = 0

# Creating a txt file to store the name of the boards
os.chdir('G:\Python')

# To add your board names to the list by reading them from the txt file
def addBoardList():
    file = open('Boards.txt','r')
    for itr in file:
        board_names.append(itr.rstrip())
    file.close()

# Add your board to the txt file if not shown in the list
def addBoard():
    file = open('Boards.txt', 'a')
    file.write('\n' + input("Enter your desired board name **attention this name is case sensitive**: "))
    file.close()
    confirmation()

# Show the availabele boards in the list
def boardChoice():
    global ind
    file = open('Boards.txt', 'r')
    print(file.read())
    file.close()
    decision = input("Do you have your board listed Y/N?: ")
    if decision.casefold() == 'y':
        addBoardList()
        bname = input("Enter the board of your choice from the list shown **attention this name case sensitive**: ")
        for itr in range (len(board_names)):
            if bname == board_names[itr]:
                ind = itr
        boardFormat()
    else:
        addBoard()

# A chance to correct the txt file if last entry is wrong
def correctBoard():
    file = open("Boards.txt", "r")
    fromTxt_file = file.read()
    file.close()
    To_duplicate_list = fromTxt_file.split("\n")
    Remove_last_element = "\n".join(To_duplicate_list[:-1])
    file = open("Boards.txt", "w+")
    for itr in range(len(Remove_last_element)):
        file.write(Remove_last_element[itr])
    file.close()
    addBoard()

# To confirm if the entry is correct
def confirmation():
    global ind
    print("Make sure you have entered the name correctly")
    decision = input("Do you want to make any changes Y/N?: ")
    if decision.casefold() == 'y':
        correctBoard()
    else:
        addBoardList()
        time.sleep(2)
        print(board_names)
        ind = (len(board_names)-1)
        boardFormat()

# To append the board names to the required format for the selenium
def boardFormat():
    for itr in board_names:
        boards.append("//*[@title='{0}']".format(itr))

# Choosing your board to pin the images
boardChoice()

# Definitions about pins
image_file = 'D:\My album\PinBulk\\'
description = input("Enter a description for your pins **attention this goes for each every pin in the folder**: ")

#changing directory to the images folder
os.chdir('D:\My album\PinBulk')

#Getting images from file
image_list = []
for filename in glob.glob('*.jpg'):
    image_list.append(filename)

# Defining chrome driver
driver = webdriver.Chrome('C:\WebDrivers\chromedriver')

# Slicing the image name
def pre_name():
    ind = img.find(".")
    product = img[:(ind)]
    pre_name = product.replace("_", " ")
    pre_name = pre_name.upper()
    return pre_name

# Login to your account
def login():
    # Open pinterest on Chrome driver
    driver.get(pinterest_home)
    driver.find_element_by_xpath(flex_pre_login).click()

    # Enter the mail and password and login..
    driver.find_element_by_xpath(mail_box).send_keys(user_mail)
    driver.find_element_by_xpath(pass_box).send_keys(user_password)
    time.sleep(2)
    driver.find_element_by_xpath(login_button).click()
    time.sleep(5)

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
    driver.find_element_by_xpath(board).click()
    time.sleep(3)

    # Click publish button
    driver.find_element_by_xpath(publish_button).click()
    time.sleep(5)

# Login to your pinterest account
login()
i = 0

# when ther are files in the folder the image_list will be > 1
while i < len(image_list):
    for img in image_list:
        name = pre_name()
        board = boards[ind]  # choose your board from the list
        b_ind = -2
        pin()
        i += 1
        print(name.title(), "pinned on", board[12:(b_ind)])
        print("{} image(s) are pinned.".format(i))
        t = randint(0,5)
        print("Waiting next session...{} seconds".format(t))
        print("")
        time.sleep(t)
print("All done! Finally {} images have been pinned!".format(i))
driver.quit()
