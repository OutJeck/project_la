from operator import ge
import pygame
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

plt.style.use('dark_background')
pygame.init()

#pygame.display.set_icon(pygame.image.load('icon.png'))
width, height = 600, 600
win = pygame.display.set_mode((width, height))

C = 10
gen_angle = lambda: np.random.random()*2*np.pi
polar_to_plain = lambda a, R: [np.cos(a)*R, np.sin(a)*R]
r = 1

def gen_circle_boundaries(gamma, angular_radius, R=1, r=1, n=20):
	thetas = np.linspace(gamma-angular_radius, gamma+angular_radius+2*angular_radius/n, n)
	cos = np.cos(thetas)
	sin = np.sin(thetas)
	x, y = np.cos(gamma)*R, np.sin(gamma)*R
	closer = ((x*cos+y*sin)+np.sqrt(r**2-(x*sin-y*cos)**2))
	further = ((x*cos+y*sin)-np.sqrt(r**2-(x*sin-y*cos)**2))
	return closer, further, thetas


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
		self.max_val, self.min_val = 10, -10

		fig, ax = plt.subplots(1, 1, figsize=(10, 10))
		min_ax, max_ax = -10, 10
		p = np.linspace(min_ax, max_ax, 20)
		x, y = np.meshgrid(p, p)
		x, y = x.flatten(), y.flatten()
		c = (x+(max_ax-min_ax))*(y+(max_ax-min_ax))
		ax.scatter(x, y, c=c, cmap=cm.plasma, s=50, marker="s")
		self.xx, self.yy = x, y
		ax.set_xlim(min_ax, max_ax)
		ax.set_ylim(min_ax, max_ax)
		ax.axis("off")
		self.fig, self.ax = fig, ax
		self.c = c
		angles = np.linspace(0, np.pi*2, 30)
		self.circle_radius = 1
		self.circle_points = np.array([np.cos(angles), np.sin(angles)])
	
		self.alpha, self.beta = gen_angle(), gen_angle()
		self.C = (np.random.random()/1.25+0.1)*C
		self.R = (np.random.random()/1.25+0.1)*C

		self.star = self.ax.scatter(0, 0)

		self.generate_circle()
		self.generate_star()
		self.update_colors()

	def generate_circle(self):
		self.alpha = gen_angle()

	def generate_star(self):
		self.star.remove()
		self.beta = gen_angle()
		x, y = polar_to_plain(self.beta, self.R)
		self.star = self.ax.scatter(x, y, s=500, marker='*')

	def autosolve(self):
		angular_radius = np.arcsin(r/self.R)
		closer, further, thetas = gen_circle_boundaries(self.beta, angular_radius, self.R, r)
		angles = self.alpha-thetas-2*np.pi

		matrices = np.array([[np.cos(thetas), -np.sin(thetas)], [np.sin(thetas), np.cos(thetas)]])
		matrices_c = matrices
		matrices_f = matrices



	def draw(self, win):
		pygame.draw.rect(win, self.top_left_color, (self.x, self.y, self.w, self.h))
		pygame.draw.rect(win, self.top_right_color, (self.x+self.w, self.y, self.w, self.h))
		pygame.draw.rect(win, self.bottom_left_color, (self.x, self.y+self.h, self.w, self.h))
		pygame.draw.rect(win, self.bottom_right_color, (self.x+self.w, self.y+self.h, self.w, self.h))

	def get_matrix(self):
		return

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
		self.update_canvas(win)

	def get_canvas(self):
		matrix = np.array([[self.top_left_value, self.top_right_value], [self.bottom_left_value, self.bottom_right_value]])/(self.max_val-self.min_val)*2
		xt, yt = matrix.dot(np.array([self.xx, self.yy]))
		collection = self.ax.scatter(xt, yt, c=self.c, cmap=cm.plasma, s=50, marker="s")
		circle_center = np.array(polar_to_plain(self.alpha, self.C))
		circle = self.ax.scatter(*(matrix.dot(circle_center).T+((self.circle_points*self.circle_radius).T)).T, marker='x')
		self.fig.canvas.draw()
		self.fig.savefig("figure.jpg")
		img = plt.imread("figure.jpg")
		collection.remove()
		circle.remove()
		return img, matrix.dot(circle_center)

	def update_canvas(self, win):
		img, (Cx, Cy) = self.get_canvas()
		surface = pygame.surfarray.make_surface(img)
		surface = pygame.transform.scale(surface, (width, height))  # Scaled a bit.
		win.blit(surface, (0, 0))
		x, y = polar_to_plain(self.beta, self.R)
		print(Cx, x, Cy, y)
		if (Cx-x)**2+(Cy-y)**2 < self.circle_radius**2:
			self.generate_star()
			self.generate_circle()

cp = ControlPanel(50, 50, 20, 20)
cp.update_canvas(win)
while True:
	cp.update(win)
	cp.draw(win)

	pygame.display.update()
	pygame.event.pump()
	pygame.time.delay(10)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
