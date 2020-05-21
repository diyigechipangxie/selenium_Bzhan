#!/bin/bash/evn python
# encoding=utf-8
"""
@file:dilidili.py
@time:5/21/20|2:39 PM
"""
import time
from io import BytesIO

from PIL import Image

from selenium import webdriver
from selenium.webdriver import ActionChains

input_keys_flag = False


class Bili(object):
	def __init__(self):
		self.driver = webdriver.Chrome()
		url = 'https://passport.bilibili.com/login'
		self.driver.get(url)
		self.driver.fullscreen_window()

	def input_keys(self):
		el_user = self.driver.find_element_by_xpath('//*[@id="login-username"]')
		el_user.send_keys('username')
		el_pwd = self.driver.find_element_by_xpath('//*[@id="login-passwd"]')
		el_pwd.send_keys('password')

		el_login = self.driver.find_element_by_xpath('//*[@id="geetest-wrap"]/div/div[5]/a[1]')
		el_login.click()
		global input_keys_flag
		input_keys_flag = True

	def get_slide_button(self):
		slide_button = self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[6]/div/div[1]/div[2]/div[2]')
		return slide_button

	def get_position(self):
		if input_keys_flag:
			pass
		else:
			self.input_keys()
		self.driver.implicitly_wait(3)
		img = self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[6]/div/div[1]/div[1]/div/a/div[1]')
		time.sleep(3)
		location = img.location
		print(location)
		size = img.size
		print(size)

		left, top, right, bottom = 2 * location['x'], 2 * location['y'], 2 * (location['x'] + size['width']), 2 * (
				location['y'] + size['height'])
		return left, top, right, bottom

	def get_screenshot(self):
		shot = self.driver.get_screenshot_as_png()
		pshot = Image.open(BytesIO(shot))
		return pshot

	def crop_image(self, name='sha_img.png'):
		img_info = self.get_position()
		shot = self.get_screenshot()
		sha_img = shot.crop(img_info)
		with open(name, 'wb') as f:
			sha_img.save(f)
		return sha_img

	def handle_img(self):
		sha_img = self.crop_image()
		# get the original image
		self.ban_style()
		ori_img = self.crop_image(name='ori_img.png')
		return ori_img, sha_img

	def ban_style(self):
		self.driver.execute_script(
			"var x=document.getElementsByClassName('geetest_canvas_fullbg geetest_fade geetest_absolute')[0];"
			"x.style.display='block';"
			"x.style.opacity=1")

	def is_pixel_equal(self, img1, img2, x, y):
		pixel1 = img1.load()[x, y]
		pixel2 = img2.load()[x, y]
		threshold = 60
		if abs(pixel1[0] - pixel2[0]) < threshold and abs(pixel1[1] - pixel2[1]) < threshold and abs(
			pixel1[2] - pixel2[2]) < threshold:
			return True
		else:
			return False

	def counting_offset(self, img1, img2):
		left = 120
		for i in range(left, img1.size[0]):
			for j in range(left, img1.size[1]):
				# 根据像素点的色差 判断阴影部分
				if not self.is_pixel_equal(img1, img2, i, j):
					left = i
					return round(left/2 - 8)
		return left

	def do_slide(self, offset):
		# save step
		steps = []
		# current step
		current = 0
		# mid
		mid = offset * 3 / 5
		t = 1.5
		v = 0
		while current < offset:
			if current < round(mid):
				a = 2
			else:
				a = -3
			v0 = v
			v = v0 + a * t
			move = v0*t + 1/2*a*t*t
			current += move
			steps.append(round(move))
		return steps


	def run(self):
		img1, img2 = self.handle_img()
		offset = self.counting_offset(img1, img2)
		print(offset)
		steps = self.do_slide(offset)
		self.operate_slide_button(steps)
		# self.close()

	def close(self):
		self.driver.quit()

	def operate_slide_button(self, steps):
		btn = self.get_slide_button()
		# press and hold btn
		ActionChains(self.driver).click_and_hold(btn).perform()
		#TODO add chaos avoid login failed
		# ActionChains(self.driver).move_by_offset(xoffset=66, yoffset=0).perform()
		# ActionChains(self.driver).move_by_offset(xoffset=-43, yoffset=0).perform()
		# move btn
		for i in steps:
			ActionChains(self.driver).move_by_offset(xoffset=i,yoffset=0).perform()
		# release btn
		ActionChains(self.driver).release().perform()


if __name__ == '__main__':
	bi = Bili()
	bi.run()
