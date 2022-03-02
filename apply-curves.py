#!/usr/bin/env python

import pygame, sys, math, random, os
import numpy as np

from utils.shader import Shader
from utils.spectralhandler import SpectralHandler
from utils.responsecurve import ResponseCurve
from utils.defines import Defines
from utils.gui import GuiHandler

from ctypes import *
from OpenGL.GL import *
from pygame.locals import *


import dearpygui.dearpygui as dpg

import os
os.environ['SDL_VIDEO_CENTERED'] = '1'

#Maximum frames per second
max_fps = 120

clicking = False

def get_normalized_mouse_pos(win_size):
	""" returns the mouse position from 0 to 1 (x,y) """
	pos = pygame.mouse.get_pos()
	return (pos[0] / win_size[0], pos[1] / win_size[1])

# pywavefront

if __name__ == '__main__':
	if len(sys.argv) != 3:
		print("usage:", sys.argv[0], "<path/to/.pickle> <path/to/response.csv>")
		exit(1)

	pygame.init()

	# set up main objects:
	images = SpectralHandler(sys.argv[1]) # spectral renders
	curve = ResponseCurve(sys.argv[2]) # current response curve
	gui = GuiHandler() # gui
	defines = Defines() # constant defines for the shader
	defines['N_WAVELENGTHS'] = curve.c_wl_samples # number of wavelengths
	# check we have the same number of wavelengths in the renders and the curve:
	assert images.r_wl_samples == curve.c_wl_samples

	# --------------
	# Set up gui:
	parent = curve.setup_gui()

	#with dpg.window(label="Exposure", tag="exp_window"):
	gui.add_slider_float(parent=parent, max_value=100.0, default_value=1, format="exposure = %.1f", key="exposure")
	curve.add_curve_plot()

	# ---------------

	# initialize pygame display:
	win_size = (images.width, images.height)
	window = pygame.display.set_mode(win_size, OPENGL | DOUBLEBUF)
	pygame.mouse.set_visible(True)

	images.init()

	#======================================================
	# Shader compilation:
	shader = Shader()
	shader.set("exposure",1.0)
	program = shader.compile(defines)
	print("Compiled!")
	print(glGetProgramInfoLog(program))


	mouse_posID = glGetUniformLocation(program, "mouse_pos")
	# resID = glGetUniformLocation(program, "iResolution")
	curveID = glGetUniformLocation(program, "iCurve")


	glUseProgram(program)

	curve.send_curve(curveID)

	clock = pygame.time.Clock()
	frame_num = 0
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				break
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_c:
					pygame.image.save(window, 'screenshot.png')
					print("saved screenshot.png")
				elif event.key == pygame.K_ESCAPE:
					break


		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		# glUniformMatrix4fv(matID, 1, False, mat)
		# glUniformMatrix4fv(prevMatID, 1, False, prevMat)
		mouse_pos = get_normalized_mouse_pos(win_size)
		# glUniform3f(colorID, 0.5, mouse_pos[0], mouse_pos[1])
		glUniform2f(mouse_posID, mouse_pos[0], mouse_pos[1])

		glDrawArrays(GL_TRIANGLES, 0, 3)
		pygame.display.flip()
		clock.tick(max_fps)
		frame_num += 1
		if frame_num % 1000 == 0:
			print("fps:",round(clock.get_fps(),2))

		if dpg.is_dearpygui_running():
		    dpg.render_dearpygui_frame()

		# if a new curve was selected, send it
		curve.check_send_curve(curveID)
		# send changed gui variables:
		gui.send_vars(shader)

	dpg.destroy_context()
	glDeleteTexture(images.tex_obj)
