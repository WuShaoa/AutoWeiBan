# -*- coding: UTF-8 -*-
from time import sleep

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import json
import re

driver = webdriver.Chrome() #driver = webdriver.Edge() #https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/

HOST = 'https://weiban.mycourse.cn/#/'
HAS_UNKNOWN_QUESTION = False
# login
driver.get(HOST)
driver.implicitly_wait(5)
WebDriverWait(driver, 600, 0.5).until(
    EC.visibility_of_element_located((By.CLASS_NAME, 'task-block-new')))
WebDriverWait(driver, 600, 0.5).until_not(
    EC.visibility_of_element_located((By.CLASS_NAME, 'enforcePop')))
WebDriverWait(driver, 600, 0.5).until(
    EC.visibility_of_element_located((By.CLASS_NAME, 'task-block-new')))
driver.implicitly_wait(3)

# in menu
driver.find_element(by=By.CLASS_NAME, value='task-block-new').click()
driver.implicitly_wait(5)

folderlists = driver.find_elements(by=By.CLASS_NAME, value='folder-list')

folderNum = len(driver.find_elements(by=By.CLASS_NAME, value='folder-item'))
print("NUMMM: ", folderNum)
###################
# part1 答题
###################
flag = True
for i in range(folderNum):
    if i >= 10 and flag:
        WebDriverWait(driver, 600, 0.5).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'mint-navbar')))
        driver.find_elements(by=By.CLASS_NAME, value='mint-tab-item')[1].click()
        driver.implicitly_wait(5)
        flag = False
    WebDriverWait(driver, 600, 0.5).until(EC.presence_of_element_located(
        (By.CLASS_NAME, 'folder-item')
    ))
    folder = driver.find_elements(by=By.CLASS_NAME, value='folder-item')[i]

    state = folder.find_elements(by=By.CLASS_NAME, value='state')[0].text.split('/')  # 剩余课时
    print("STATTT: ", folder.find_elements(
        by=By.CLASS_NAME, value='state')[0].text)
    if len(state) >= 2 and state[0] != state[1]:
        sleep(3)
        driver.implicitly_wait(3)
        folder.find_elements(by=By.LINK_TEXT, value="去学习>")[0].click()

        courseNum = len(driver.find_elements(by=By.CLASS_NAME, value='course'))
        for j in range(courseNum):
            try:
                print('start:第', i, '组，第', j, '个课程')
                sleep(3)
                WebDriverWait(driver, 600, 0.5).until(EC.presence_of_element_located(
                    (By.CLASS_NAME, 'course')
                ))
                course = driver.find_elements(
                    by=By.CLASS_NAME, value='course')[0]
                course.click()

                WebDriverWait(driver, 60, 0.5).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'page-iframe')))

                myframe = driver.find_elements(
                    by=By.CLASS_NAME, value='page-iframe')[0]
                driver.switch_to.frame(myframe)
                sleep(10)
                res = driver.execute_script(
                    'finishWxCourse();'
                )
                sleep(3)
                driver.switch_to.alert.accept()
                print('finish:第', i, '组，第', j, '个课程')
                driver.back()
                sleep(3)

            except Exception as e:
                print(e)
                driver.back()
                sleep(3)
        driver.back()

###################
# part2 考试 （题目过时）
###################
# with open("db.json", 'r', encoding='utf8') as f:
#     db = json.load(f)

#     WebDriverWait(driver, 600, 0.5).until(EC.presence_of_element_located(
#         (By.CLASS_NAME, 'mint-tab-item')
#     ))
#     driver.find_elements(by=By.CLASS_NAME, value='mint-tab-item')[1].click()

#     WebDriverWait(driver, 600, 0.5).until(EC.presence_of_element_located(
#         (By.CLASS_NAME, 'exam-btn-group')
#     ))
#     btn_group = driver.find_elements(by=By.CLASS_NAME, value='exam-btn-group')[
#         0].find_elements(by=By.CLASS_NAME, value='exam-block')
#     btn_group[len(btn_group)-1].click()

#     WebDriverWait(driver, 600, 0.5).until(EC.presence_of_element_located(
#         (By.CLASS_NAME, 'popup-btn')
#     ))
#     driver.find_elements(by=By.CLASS_NAME, value='popup-btn')[1].click()

#     while(1):
#         try:
#             sleep(1)
#             question = driver.find_element(
#                 by=By.CLASS_NAME, value='quest-stem').text
#             if HAS_UNKNOWN_QUESTION:
#                 WebDriverWait(driver, 600, 0.5).until_not(
#                     EC.text_to_be_present_in_element(
#                         (By.CLASS_NAME, 'quest-stem'),
#                         question
#                     )
#                 )
#                 question = driver.find_element(
#                     by=By.CLASS_NAME, value='quest-stem').text
#                 HAS_UNKNOWN_QUESTION = False
#             question = re.sub('\d+\.', '', question, 1)
#             theQ = db['questions'].get(question)
#             if theQ is None:
#                 HAS_UNKNOWN_QUESTION = True
#                 continue
#             for i in range(len(theQ['optionList'])):
#                 if theQ['optionList'][i]['isCorrect'] == 1:
#                     driver.find_elements(
#                         by=By.CLASS_NAME, value='quest-option-item')[i].click()

#             # 下一题
#             sleep(1)
#             driver.find_elements(by=By.CLASS_NAME, value='bottom-ctrls')[0].find_elements(
#                 by=By.CLASS_NAME, value='mint-button--default')[1].click()

#             # 判断是否可以提交
#             sleep(1)
#             confirm_window_style = driver.find_elements(
#                 by=By.CLASS_NAME, value='confirm-sheet')[0].get_property('style')
#             if (confirm_window_style.count('display') == 0):
#                 sleep(3)
#                 driver.find_elements(by=By.CLASS_NAME, value='confirm-sheet')[0].find_elements(
#                     by=By.CLASS_NAME, value='mint-button--danger')[0].click()
#                 break
#         except Exception as e:
#             print(e)
# print('完成了')
# driver.__exit__()
