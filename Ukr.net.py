from selenium import webdriver
import time
import random
import string

messages_dict = {}
messages = 15

# Random string
def randomString(stringLength=10):
	lettersDigits = string.ascii_letters + "0123456789"
	return ''.join(random.choice(lettersDigits) for i in range(stringLength))

# count letters and numbers
def numbers_letters(message):
    numbers = 0
    letters = 0
    i=0
    while i < len(message)-1:
        if message[i].isalpha():
            letters += 1
        else:
            numbers += 1
        i += 1
    nl = [letters, numbers]
    return nl

# Login
driver = webdriver.Chrome("C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")
driver.get("https://mail.ukr.net/")

Login_field = driver.find_element_by_id("id-l")
pass_field = driver.find_element_by_id("id-p")
login_button = driver.find_element_by_xpath("/html/body/div/div/main/form/button")

Login_field.send_keys("YourLogin")
pass_field.send_keys("YourPassword")
login_button.click()
time.sleep(3)

# sending messages
i = 0
while i < messages:
    new_message = driver.find_element_by_xpath("//button[@class = 'default compose']")
    new_message.click()
    time.sleep(1)

    adress_field = driver.find_element_by_xpath("//input[@name='toFieldInput']")
    adress_field.send_keys("alexandrtest@ukr.net")

    subject_field = driver.find_element_by_xpath("//input[@name='subject']")
    subject_field.send_keys(randomString())

    message_field_selector = '//*[@id="mce_{}_ifr"]'.format(i)
    message_field = driver.find_element_by_xpath(message_field_selector)
    message_field.send_keys(randomString())

    send_button = driver.find_element_by_xpath("//button[@class='default send']")
    send_button.click()
    time.sleep(2)

    i += 1

# Verify all messages recieved
inbox_counter = driver.find_element_by_xpath("//*[@data-folder='0']/span[2]")
assert str(messages) in inbox_counter.text

# Read all received mail
inbox_link = driver.find_element_by_xpath("//span[contains(text(),'Inbox')]")
inbox_link.click()

i = 0
while i < messages:
    inbox_message_selector = "//tbody/tr[{}]/td[4]/a".format(i+1)
    inbox_message = driver.find_element_by_xpath(inbox_message_selector).text
    message_collection = inbox_message.split("  ")
    messages_dict[message_collection[0]] = message_collection[1]
    i += 1

message_st = ""
for x,y in messages_dict.items():
    nl = numbers_letters(y)
    message_st += "Received mail on theme {} with message: {}. It contains {} letters and {} numbers\n".format(x, y, nl[0], nl[1])

# Delete all messages
inbox_link = driver.find_element_by_xpath("//span[contains(text(),'Inbox')]")
inbox_link.click()

select_all = driver.find_element_by_xpath("//*[@id='msglist']/div[1]/div/div[1]/label")
select_all.click()

delete_all = driver.find_element_by_xpath("//*[contains(text(),'Delete')]")
delete_all.click()

# Report
new_message = driver.find_element_by_xpath("//button[@class = 'default compose']")
new_message.click()
time.sleep(1)

adress_field = driver.find_element_by_xpath("//input[@name='toFieldInput']")
adress_field.send_keys("alexandrtest@ukr.net")

subject_field = driver.find_element_by_xpath("//input[@name='subject']")
subject_field.send_keys("Report")

message_field_selector = '//*[@id="mce_{}_ifr"]'.format(i)
message_field = driver.find_element_by_xpath(message_field_selector)
message_field.send_keys(message_st)

send_button = driver.find_element_by_xpath("//button[@class='default send']")
send_button.click()
time.sleep(1)

inbox_link = driver.find_element_by_xpath("//span[contains(text(),'Inbox')]")
inbox_link.click()