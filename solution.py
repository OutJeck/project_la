import matplotlib.pyplot as plt
import numpy as np
from numpy.linalg.linalg import tensorinv

plt.style.use('dark_background')

n = 20
C = 10

plot_direction = lambda a, ax, r=1: ax.plot([0, r*np.cos(a)], [0, r*np.sin(a)])
plot_polar = lambda a, r, ax, marker='o': ax.scatter(r*np.cos(a), r*np.sin(a), marker='o')

def gen_circle_boundaries(gamma, angular_radius, R=1, r=1, n=n):
	thetas = np.linspace(gamma-angular_radius, gamma+angular_radius+2*angular_radius/n, n)
	cos = np.cos(thetas)
	sin = np.sin(thetas)
	x, y = np.cos(gamma)*R, np.sin(gamma)*R
	further = ((x*cos+y*sin)+np.sqrt(r**2-(x*sin-y*cos)**2))
	closer = ((x*cos+y*sin)-np.sqrt(r**2-(x*sin-y*cos)**2))
	return closer, further, thetas

fig = plt.figure(constrained_layout=True)
gs = fig.add_gridspec(nrows=2, ncols=4)
basicax = fig.add_subplot(gs[:, :2])
ax00, ax01, ax10, ax11 = \
	fig.add_subplot(gs[0, 2]),\
	fig.add_subplot(gs[0, 3]),\
	fig.add_subplot(gs[1, 2]),\
	fig.add_subplot(gs[1, 3])

for i in range(1):
	alpha = np.random.random()*2*np.pi
	beta = np.random.random()*2*np.pi
	circle_center = np.array([np.cos(alpha), np.sin(alpha)])*C
	r = 1
	R = (np.random.random()/1.25+0.1)*C

	angular_radius = np.arcsin(r/R)

	closer, further, thetas = gen_circle_boundaries(beta, angular_radius, R, r)
	angles = -thetas+alpha-2*np.pi

	p = np.array([])
	t = []
	for c, f, d in zip(closer, further, thetas):
		try:
			newpoints = np.arange(c, f+0.1, 0.1)
			p = np.concatenate((p, newpoints))
			t += [d]*len(newpoints)
		except ValueError:
			continue
	t = -np.array(t)+alpha-2*np.pi

	mapped_dots = []
	matrices = []
	for a, c in zip(t, p):
		rotation = np.array([[np.cos(a), -np.sin(a)], [np.sin(a), np.cos(a)]])
		m = rotation*c/C
		mapped_dots.append(circle_center.dot(m))
		matrices.append(m)
	mapped_dots = np.array(mapped_dots).T
	matrices = np.array(matrices)
	x, y = mapped_dots
	ax00.scatter(x, y, c=matrices[:, 0, 0], cmap='plasma', marker='s')
	ax01.scatter(x+0.1, y, c=matrices[:, 0, 1], cmap='plasma', marker='s')
	ax10.scatter(x, y+0.1, c=matrices[:, 1, 0], cmap='plasma', marker='s')
	ax11.scatter(x+0.1, y+0.1, c=matrices[:, 1, 1], cmap='plasma', marker='s')

	basicax.plot([0, R*np.cos(beta)], [0, R*np.sin(beta)], color='gold')
	basicax.plot([0, C*np.cos(alpha)], [0, C*np.sin(alpha)], color='white')
	basicax.plot(np.cos(thetas)*closer, np.sin(thetas)*closer, label='circle inner boundary')
	basicax.plot(np.cos(thetas)*further, np.sin(thetas)*further, label='circle outer boundary')
	basicax.scatter(*circle_center, color='white', marker='x', s=100, label='circle_center')
	basicax.scatter(R*np.cos(beta), R*np.sin(beta), marker='*', s=200, color="gold")
	basicax.grid()
	basicax.legend()

	for axis in [ax00, ax01, ax10, ax11]:
		axis.grid()
		axis.axis("off")
	ax00.set_title(f"matrix[0][0]")
	ax01.set_title(f"matrix[0][1]")
	ax10.set_title(f"matrix[1][0]")
	ax11.set_title(f"matrix[1][1]")
	fig.suptitle("solutions")
	plt.show()

