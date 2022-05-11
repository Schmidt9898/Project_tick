
import glfw
import OpenGL.GL as gl
import imgui
from imgui.integrations.glfw import GlfwRenderer
import cv2 as cv
import numpy as np
from Gamelogic import Tictactoe

path_to_font = None  # "path/to/font.ttf"


def impl_glfw_init(w,h,window_name = "Test title"):
	width, height = w, h

	if not glfw.init():
		print("Could not initialize OpenGL context")
		exit(1)

	glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
	glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
	glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
	glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, gl.GL_TRUE)

	window = glfw.create_window(int(width), int(height), window_name, None, None)
	glfw.make_context_current(window)
	glfw.swap_interval(1)
	#glfw.glfwSwapInterval( 0 );

	if not window:
		glfw.terminate()
		print("Could not initialize Window")
		exit(1)

	return window

class Gui_Window:
	"""Standar Class for Gui_Window.

	.. note::

	   This function can be used as a help to implement a Gui_windows,
       it shows every feature in the GUI

	"""
	def __init__(self,w=640,h=480,title="None was given"):
		"""Constructor of Game.

		It starts game UI, camera and tictactoe logic
		:param w: width of the gui
		:type name: int
  		:param h: height of the gui
		:type name: int
  		:param title: title of the GUI
		:type name: str
		"""
		imgui.create_context()
		self.window = impl_glfw_init(w,h,title)
		self.impl = GlfwRenderer(self.window)
		self.io = imgui.get_io()
		self.jb = self.io.fonts.add_font_from_file_ttf(path_to_font, 30) if path_to_font is not None else None
		self.impl.refresh_font_texture()

	def context(self):
		"""It show the context to be show on render_frame
		"""
		imgui.show_test_window()

	def terminate(self):
		"""Terminates the process of the GUI
		"""
		self.impl.shutdown()
		glfw.terminate()


	def render_frame(self):
			"""Render the actual frame processed by context
			"""
			glfw.poll_events()
			self.impl.process_inputs()
			imgui.new_frame()

			gl.glClearColor(0.1, 0.1, 0.1, 1)
			gl.glClear(gl.GL_COLOR_BUFFER_BIT)

			if self.jb is not None:
				imgui.push_font(self.jb)
			self.set_style()
			self.context()
			self.pop_style()
			if self.jb is not None:
				imgui.pop_font()

			imgui.render()
			self.impl.render(imgui.get_draw_data())
			glfw.swap_buffers(self.window)

	def start_loop(self):
		"""Main loop of the game GUI, it calls every time to render_frame untill the gui_windows finishes
		"""
		while not glfw.window_should_close(self.window):
			self.render_frame()

	def set_style(self):
		pass
	def pop_style(self):
		pass

# load image to vram texture
def mat_2_tex(mat,texture=None):
	"""Transform a opencv mat into a gl texture

 	:returns:  texture,w,h -- texture and dimensions of the texture
	"""
	h,w,_=mat.shape
	if texture is None:
		texture = gl.glGenTextures(1)
	gl.glPixelStorei(gl.GL_UNPACK_ALIGNMENT, 1);
	gl.glBindTexture(gl.GL_TEXTURE_2D, texture)
	gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
	gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
	if mat.shape[-1] == 4:
		gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, w, h, 0, gl.GL_BGRA,gl.GL_UNSIGNED_BYTE, mat)
	else:
		gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, w, h, 0, gl.GL_BGR,gl.GL_UNSIGNED_BYTE, mat)
	return texture, w, h

if __name__ == "__main__":
	tw= Gui_Window()
	#tw= Game_Gui()
	tw.start_loop()
	tw.terminate()
	cv.destroyAllWindows()
