#!/usr/bin/python3


import tkinter
import random
import time

class Window:

	def __init__(self, root):
		self.root = root

		frame = tkinter.Frame(root) # use frame to make go and stop
		frame.pack(side=tkinter.TOP) # buttons side-by-side

		# go will begin drawing curves
		self.go_button = tkinter.Button(root, text="Go", command = self.go)
		self.go_button.pack(in_=frame, side=tkinter.LEFT)

		# stop will stop drawing cruves
		self.stop_button = tkinter.Button(root, text="Stop", command = self.stop)
		self.stop_button.pack(in_=frame, side=tkinter.RIGHT)


		# This is 1080 x 1920   but divided by 2
		self.canvas_width = 960
		self.canvas_height = 540
		self.canvas = tkinter.Canvas(root, width=self.canvas_width, height=self.canvas_height, bg="black")
		self.canvas.pack(side=tkinter.TOP)

		# This connects the "mouse move" event to erasing the canvas
		self.canvas.bind( "<B1-Motion>", self.eraser)

		# A bunch of control variables
		self.drawing_on = False
		self.gui_on = True
		self.curve_count = 0

		# Attaches the "x button in window title clicked" event
		# to the die method which turns off my main GUI loop
		self.root.protocol("WM_DELETE_WINDOW", self.die)


	def die(self):
		#print("dieing...")
		self.gui_on = False


	def main_loop(self):
		while(self.gui_on):
			self.root.update() # this should maybe be at end of loop?

			if(self.drawing_on):
				self.draw_curve()

			# If too many curves are on the screen the system starts
			# to slow down.  Seems to be an efficiency thing in tkinter
			# Solution: after 25 curves erase everything and 
			# reset the counter
			if(self.curve_count > 25):
				self.curve_count = 0
				self.canvas.delete("all")


	def go(self):
		#print("going...")
		self.drawing_on = True
		self.curve_count = 0
		self.canvas.delete("all")


	def draw_curve(self):
		#print("Going...")

		# For details on this method, see https://javascript.info/bezier-curve

		#self.canvas.create_rectangle(50, 25, 160, 75, fill="blue")
		control_points = [self.random_point() for x in range(3)]
		#control_points = [(50, 200), (150, 10), (300, 210)]

		control_points.sort()
		#print(control_points)
		#for p in control_points:
		#	self.canvas.create_oval(p[0], p[1], p[0]+5, p[1]+5, fill="orange")

		try:
			l1 = Line(control_points[0], control_points[1])
			l2 = Line(control_points[1], control_points[2])
			self.curve_count = self.curve_count + 1

		except ZeroDivisionError:
			# Just give-up on this round
			# This occurs when the control points
			# generated have the same x coordinates
			# such a line is impossible to create
			# solution: just give up
			return


		#print("l1.width: " + str(self.l1.width))
		#l3 = Line(control_points[2], control_points[3])

		#print("line1: " + str(self.l1))
		#print("line2: " + str(self.l2))
		#self.canvas.create_line(control_points[0], control_points[1], fill="green")
		#self.canvas.create_line(control_points[1], control_points[2], fill="green")

		color = self.random_color()
		# draw curve (in random color) using
		# 100 "tangent" lines
		for cur in range(0, 101):
			t = cur / 100
			left_x = t * l1.width + l1.p1[0]
			left_y = l1.eval(left_x)

			right_x = t * l2.width + l2.p1[0]
			right_y = l2.eval(right_x)
			self.canvas.create_line(left_x, left_y, right_x, right_y, fill=color)
			self.root.update() # new line is drawn, so update it
			if(self.drawing_on == False):
				break
			time.sleep(0.05)
			#print((left_x, left_y), (right_x, right_y))


	def stop(self):
		#print("stopping...")
		self.drawing_on = False


	def eraser(self, evt):
		# This colors black circles on the canvas
		# when the user clicks and drags
		mag = 30 # size of the box bounding the circle
		x1, y1 = (evt.x - mag, evt.y - mag)
		x2, y2 = (evt.x + mag, evt.y + mag)
		self.canvas.create_oval(x1, y1, x2, y2, fill = "#000000")


	def random_point(self):
		x = int(random.random() * self.canvas_width)
		y = int(random.random() * self.canvas_height)
		return (x, y)


	def random_color(self):
		red = int(random.random() * 255)
		green = int(random.random() * 255)
		blue = int(random.random() * 255)
		#print("r: "+ str(red) + "  g: " + str(green) + "  b: " + str(blue))
		return "#" + "{:02x}".format(red) + "{:02x}".format(green) + "{:02x}".format(blue)




class Line:

	def __init__(self, p1, p2):
		self.p1 = p1
		self.p2 = p2

		# Be aware, if p2[0] = p1[0] then 
		# there will be a divide by zero error
		# as such a line can't be constructed
		self.slope = (p2[1] - p1[1]) / (p2[0] - p1[0])

		# y = m*x + b
		# y - (m*x) = b
		self.y_intercept = p1[1] - (self.slope * p1[0])
		self.width = abs(p1[0] - p2[0])


	def eval(self, x):
		return x * self.slope + self.y_intercept


	def __str__(self):
		return "y = " + str(self.slope) + "*x + " + str(self.y_intercept)


	def test(self):
		# Just a really basic test case
		# this code isn't live
		p1 = (1, 2)
		p2 = (3, -4)

		l = Line(p1, p2)
		print(str(l))


def main():
	root = tkinter.Tk()
	gui = Window(root)

	# I did not use the typical tkinter mainloop() method
	# becuase I want to draw the curves gradually (like an animation)
	# My GUI implements the loop mechanism directly using a while() and 
	# root.update()
	gui.main_loop()

if __name__ == "__main__":
	main()

