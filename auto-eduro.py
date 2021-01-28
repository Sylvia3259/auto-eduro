from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from chromedriver_autoinstaller import install as chromedriver
from time import sleep

class Macro:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument('disable-gpu')
        options.add_argument('disable-infobars')
        options.add_argument('--disable-extensions')

        self.driver = webdriver.Chrome(executable_path=chromedriver(), options=options)
        self.driver.get('https://hcs.eduro.go.kr/')

        self.wait = WebDriverWait(self.driver, 10)

    def load_userdata(self):
        try:
            file = open('eduro_userdata', 'r')
        except FileNotFoundError:
            temp_driver = webdriver.Chrome(executable_path=chromedriver())
            temp_driver.get('https://hcs.eduro.go.kr/')
            while True:
                self.users = temp_driver.execute_script('''return localStorage.getItem('users');''')
                self.cookies = temp_driver.execute_script('''return document.cookie;''')
                self.password = temp_driver.execute_script('''return document.querySelector('input[type="password"]')?.value;''')
                if self.users:
                    file = open('eduro_userdata', 'w')
                    file.write('\n'.join([self.users, self.cookies, self.password]))
                    file.close()
                    break
            temp_driver.quit()
        else:
            self.users, self.cookies, self.password = file.read().split('\n')
            file.close()

        self.driver.execute_script(f'''localStorage.setItem('users', '{self.users}');''')
        self.driver.execute_script(f'''document.cookie = '{self.cookies}';''')
        self.driver.refresh()

    def self_check(self):
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="password"]'))).send_keys(self.password)
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#btnConfirm'))).click()

        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.btn'))).click()

        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[id$="a1"]')))
        answers = self.driver.find_elements(By.CSS_SELECTOR, 'input[id$="a1"]')
        for answer in answers:
            answer.click()
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[type="submit"]'))).click()

        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'img[alt="정상"]')))

    def update_userdata(self):
        self.users = self.driver.execute_script('''return localStorage.getItem('users');''')
        self.cookies = self.driver.execute_script('''return document.cookie;''')
        file = open('eduro_userdata', 'w')
        file.write('\n'.join([self.users, self.cookies, self.password]))
        file.close()

    def __del__(self):
        self.driver.quit()

macro = Macro()
macro.load_userdata()
macro.self_check()
macro.update_userdata()
