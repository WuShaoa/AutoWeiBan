# -*- coding: UTF-8 -*-
from time import sleep

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import json
import re

driver = webdriver.Chrome()

HOST='https://weiban.mycourse.cn/#/'
HAS_UNKNOWN_QUESTION = False
# login
driver.get(HOST)
driver.implicitly_wait(5)
WebDriverWait(driver, 600, 0.5).until(EC.visibility_of_element_located((By.CLASS_NAME, 'task-block-new')))
WebDriverWait(driver, 600, 0.5).until_not(EC.visibility_of_element_located((By.CLASS_NAME, 'enforcePop')))
WebDriverWait(driver, 600, 0.5).until(EC.visibility_of_element_located((By.CLASS_NAME, 'task-block-new')))
driver.implicitly_wait(3)

# in menu
driver.find_element(by=By.CLASS_NAME, value='task-block-new').click()
driver.implicitly_wait(5)

WebDriverWait(driver, 600, 0.5).until(EC.visibility_of_element_located((By.CLASS_NAME, 'mint-navbar')))
driver.find_elements(by=By.CLASS_NAME, value='mint-tab-item')[1].click()
driver.implicitly_wait(5)

folderlists = driver.find_elements(by=By.CLASS_NAME, value='folder-list')
folderitems = folderlists[1].find_elements(by=By.CLASS_NAME, value='folder-item')

print("NUMMM: ", 30)
###################
# part1 答题
###################
for k, folder in enumerate(folderitems):
    i = k + 10
    WebDriverWait(driver, 600, 0.5).until(EC.presence_of_element_located(
        (By.CLASS_NAME, 'folder-item')
    ))
    state = folder.find_elements(by=By.CLASS_NAME, value='state')[0].text.split('/') #剩余课时
    print("STATTT: ", folder.find_elements(by=By.CLASS_NAME, value='state')[0].text)
    if len(state) >= 2 and state[0] != state[1]:
        sleep(3)
        driver.implicitly_wait(3)
        folder.find_elements(by=By.LINK_TEXT,value="去学习>")[0].click()
        
        courseNum = len(driver.find_elements(by=By.CLASS_NAME, value='course'))
        for j in range(courseNum):
            try:
                print('start:第',i,'组，第',j,'个课程')
                sleep(3)
                WebDriverWait(driver, 600, 0.5).until(EC.presence_of_element_located(
                    (By.CLASS_NAME, 'course')
                ))
                course = driver.find_elements(by=By.CLASS_NAME, value='course')[0]
                course.click()
                WebDriverWait(driver, 60, 0.5).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'page-iframe')))
                myframe = driver.find_elements(by=By.CLASS_NAME, value='page-iframe')[0]
                driver.switch_to.frame(myframe)
                sleep(10)
                res = driver.execute_script(
                    'finishWxCourse();'
                )
                sleep(3)
                driver.switch_to.alert.accept();
                print('finish:第',i,'组，第',j,'个课程')
                driver.back()
                sleep(3)
            except Exception as e:
                print(e)
                driver.back()
                sleep(3)
        driver.back()
