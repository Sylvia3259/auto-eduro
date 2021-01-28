from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from chromedriver_autoinstaller import install as chromedriver
from time import sleep

class Macro:
    def __init__(self):
        def load_userdata():
            try:
                file = open('eduro_userdata', 'r')
            except FileNotFoundError:
                driver = webdriver.Chrome(executable_path=chromedriver())
                driver.get('https://hcs.eduro.go.kr/')
                while True:
                    self.users = driver.execute_script('''return localStorage.getItem('users');''')
                    self.password = driver.execute_script('''return document.querySelector('input[type="password"]')?.value;''')
                    if self.users:
                        file = open('eduro_userdata', 'w')
                        file.write('\n'.join([self.users, self.password]))
                        file.close()
                        break
                    sleep(0.1)
                driver.close()
            else:
                self.users, self.password = file.read().split('\n')
                file.close()

        load_userdata()

        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument('disable-gpu')
        options.add_argument('disable-infobars')
        options.add_argument('--disable-extensions')

        self.driver = webdriver.Chrome(executable_path=chromedriver(), options=options)
        self.driver.get('https://hcs.eduro.go.kr/')
        self.driver.execute_script(f'''localStorage.setItem('users', '{self.users}');''')
        self.driver.refresh()

        self.wait = WebDriverWait(self.driver, 10)

    def self_check(self):
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="password"]'))).send_keys(self.password)
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#btnConfirm'))).click()

        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.btn'))).click()

        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[id$="a1"]')))
        answers = self.driver.find_elements(By.CSS_SELECTOR, 'input[id$="a1"]')
        for answer in answers:
            answer.click()
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[type="submit"]'))).click()

    def __del__(self):
        self.driver.close()

macro = Macro()
macro.self_check()
