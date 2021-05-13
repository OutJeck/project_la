#import cv2
import matplotlib.pyplot as plt
#from mpl_toolkits.mplot3d.axes3d import Axes3D
import numpy as np
from matplotlib import cm
import pygame

plt.style.use('dark_background')
pygame.init()
width, height = 600, 600
win = pygame.display.set_mode((width, height))

fig, ax = plt.subplots(2, 3, figsize=(8, 8))
for a in ax.flatten():
	a.axis("off")
n = 40
p = np.linspace(0, np.pi*2, n)
v, theta = np.meshgrid(p, p)
v, theta = v.flatten(), theta.flatten()

function = lambda theta, v: np.array([np.cos(theta/2)*np.cos(v) - np.sin(theta/2)*np.sin(2*v),\
np.sin(theta/2)*np.cos(v) + np.cos(theta/2)*np.sin(2*v), np.cos(theta)*(1+np.sin(v)),\
np.sin(theta)*(1+np.sin(v))])
x, y, z, w = function(theta, v)

class ControlPanel:
	def __init__(self, x, y, w, h):
		self.top_left_value = 1
		self.top_right_value = 0
		self.bottom_left_value = 0
		self.bottom_right_value = 1
		self.top_left_color = np.array([0, 0, 0])
		self.top_right_color = np.array([0, 0, 0])
		self.bottom_left_color = np.array([0, 0, 0])
		self.bottom_right_color = np.array([0, 0, 0])
		self.x, self.y = x, y
		self.w, self.h = w, h
		self.max_val, self.min_val = 20, -20
		self.update_colors()

	def draw(self, win):
		pygame.draw.rect(win, self.top_left_color, (self.x, self.y, self.w, self.h))
		pygame.draw.rect(win, self.top_right_color, (self.x+self.w, self.y, self.w, self.h))
		pygame.draw.rect(win, self.bottom_left_color, (self.x, self.y+self.h, self.w, self.h))
		pygame.draw.rect(win, self.bottom_right_color, (self.x+self.w, self.y+self.h, self.w, self.h))

	def get_matrix(self):
		return np.array([[self.top_left_value, self.top_right_value], [self.bottom_left_value, self.bottom_right_value]])/(self.max_val-self.min_val)*8

	def update_colors(self):
		delta = 200//(self.max_val-self.min_val)
		red = np.array([200//2, 0, 200//2])
		dred = np.array([delta, 0, 0])
		dblue = np.array([0, 0, delta])
		self.top_left_color = red+dred*self.top_left_value-dblue*self.top_left_value
		self.top_right_color = red+dred*self.top_right_value-dblue*self.top_right_value
		self.bottom_left_color = red+dred*self.bottom_left_value-dblue*self.bottom_left_value
		self.bottom_right_color = red+dred*self.bottom_right_value-dblue*self.bottom_right_value

	def update(self, win):
		button1, button2, button3 = pygame.mouse.get_pressed(3)
		if not button1 and not button3:
			return
		x, y = pygame.mouse.get_pos()
		if not (self.x < x < self.x+self.w*2 and self.y < y < self.y+self.h*2):
			return
		if x < self.x+self.w:
			if y < self.y+self.h: # top left
				if button1:
					self.top_left_value = min(self.top_left_value+1, self.max_val)
				else:
					self.top_left_value = max(self.top_left_value-1, self.min_val)
			else: # bottom left
				if button1:
					self.bottom_left_value = min(self.bottom_left_value+1, self.max_val)
				else:
					self.bottom_left_value = max(self.bottom_left_value-1,self.min_val)
		else:
			if y < self.y+self.h: # top right
				if button1:
					self.top_right_value = min(self.top_right_value+1, self.max_val)
				else:
					self.top_right_value = max(self.top_right_value-1, self.min_val)
			else: # bottom right
				if button1:
					self.bottom_right_value = min(self.bottom_right_value+1, self.max_val)
				else:
					self.bottom_right_value = max(self.bottom_right_value-1, self.min_val)
		self.update_colors()
		print(self.get_matrix())
		self.update_canvas(win)
		self.draw(win)

	def update_canvas(self, win):
		transformation = self.get_matrix()
		transformed = function(*transformation.dot(np.array([theta, v])))
		cs = []
		for a, (i, j) in zip(ax.flatten(), [[0, 1], [0, 2], [0, 3], [1, 2], [1, 3], [2, 3]]):
			c = a.scatter(transformed[i], transformed[j], s=3, c=theta*v*2, cmap='Spectral_r')
			cs.append(c)
		
		fig.canvas.draw()
		img = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
		img  = img.reshape(fig.canvas.get_width_height()[::-1] + (3,))
		surface = pygame.surfarray.make_surface(img)
		surface = pygame.transform.scale(surface, (width, height))  # Scaled a bit.
		win.blit(surface, (0, 0))
		for c in cs:
			c.remove()





cp = ControlPanel(50, 50, 20, 20)
cp.update_canvas(win)
cp.draw(win)
while True:
	cp.update(win)
	pygame.display.update()
	pygame.event.pump()
	pygame.time.delay(10)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()

