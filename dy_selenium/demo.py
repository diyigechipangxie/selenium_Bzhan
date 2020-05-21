#!/bin/bash/evn python
# encoding=utf-8
"""
@file:demo.py
@time:5/21/20|12:26 PM
"""
import time

from selenium import webdriver


class LoginBD(object):
	def __init__(self):
		self.driver = webdriver.Chrome()
		self.driver.get('https://www.baidu.com')
		self.driver.fullscreen_window()

	def _login(self):
		self.driver.find_element_by_xpath('//*[@id="u1"]/a[2]').click()
		self.driver.implicitly_wait(5)
		self.driver.find_element_by_xpath('//*[@id="TANGRAM__PSP_11__footerULoginBtn"]').click()
		self.driver.find_element_by_xpath('//*[@id="TANGRAM__PSP_11__userName"]').send_keys('红发千本樱')
		self.driver.find_element_by_xpath('//*[@id="TANGRAM__PSP_11__password"]').send_keys('Xxy39881105/*')
		self.driver.find_element_by_xpath('//*[@id="TANGRAM__PSP_11__submit"]').click()
		time.sleep(5)

	def close(self):
		self.driver.quit()


if __name__ == '__main__':
	lb = LoginBD()
	lb._login()
	lb.close()
