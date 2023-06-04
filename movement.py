"""Change position"""
vx = v * np.cos(theta)
vy = v * np.sin(theta)
x += vx * dt  # relative coordinates
y += vy * dt
xs = int(x * yMax)  # surface coordinates
ys = yMax - int(y * yMax)

"""Steer depending on location of mouse pointer"""
alpha = np.arctan2(ys - ym, xm - xs)  # get angle of pointer wrt V
if alpha < 0:  # convert -pi pi range of atan2 to 0 2pi
    alpha += 2 * np.pi
if 2 * np.pi - theta + alpha < abs(alpha - theta):  # if angle has to go from under to above x axis
    deltaTheta = 2 * np.pi - theta + alpha
elif 2 * np.pi + theta - alpha < abs(alpha - theta):  # if angle has to go from above to under the x axis
    deltaTheta = - (2 * np.pi + theta - alpha)
else:
    deltaTheta = alpha - theta  # if neither are needed
if abs(deltaTheta) > deltaThetaMax:  # limit rate of turn per time step
    deltaTheta = np.sign(deltaTheta) * deltaThetaMax
theta += deltaTheta  # adjust angle by rate of turn

"""Correct angle if out of bound"""
if theta >= 2 * np.pi:
    theta -= 2 * np.pi
elif theta < 0:
    theta += 2 * np.pi