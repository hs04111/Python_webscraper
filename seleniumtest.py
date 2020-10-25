from selenium import webdriver
from selenium.webdriver.common.keys import Keys

browser = webdriver.Chrome("./chromedriver.exe")  # 같은 경로에 있으면 괄호 안 생략가능
browser.get("https://zum.com")
search = browser.find_element_by_name("query")
search.send_keys("ㄱ")
