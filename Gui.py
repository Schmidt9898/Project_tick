
import glfw
import OpenGL.GL as gl
import imgui
from imgui.integrations.glfw import GlfwRenderer
import cv2 as cv
import numpy as np

path_to_font = None  # "path/to/font.ttf"


def impl_glfw_init(w,h,window_name = "Test title"):
	width, height = w, h
	#window_name = "Tic Tac yeeee"

	if not glfw.init():
		print("Could not initialize OpenGL context")
		exit(1)

	glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
	glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
	glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
	glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, gl.GL_TRUE)

	window = glfw.create_window(int(width), int(height), window_name, None, None)
	glfw.make_context_current(window)

	if not window:
		glfw.terminate()
		print("Could not initialize Window")
		exit(1)

	return window

class Gui_Window:
	def __init__(self,w=640,h=480):
		imgui.create_context()
		self.window = impl_glfw_init(w,h)
		self.impl = GlfwRenderer(self.window)
		self.io = imgui.get_io()
		self.jb = self.io.fonts.add_font_from_file_ttf(path_to_font, 30) if path_to_font is not None else None
		self.impl.refresh_font_texture()
		self.frame = np.zeros((h,w,3), np.uint8)

	def context(self):
		imgui.show_test_window()

	def terminate(self):
		self.impl.shutdown()
		glfw.terminate()


	def render_frame(self):
			glfw.poll_events()
			self.impl.process_inputs()
			imgui.new_frame()

			gl.glClearColor(0.1, 0.1, 0.1, 1)
			gl.glClear(gl.GL_COLOR_BUFFER_BIT)

			if self.jb is not None:
				imgui.push_font(self.jb)
			self.context()
			if self.jb is not None:
				imgui.pop_font()

			imgui.render()
			self.impl.render(imgui.get_draw_data())
			glfw.swap_buffers(self.window)

	def start_loop(self):
		while not glfw.window_should_close(self.window):
			self.render_frame()

		
#def set_frame(self, frame):
#	self.frame = frame


cam = cv.VideoCapture(0)#this gives the error message when exit
def get_cam_image():
	s, image = cam.read()
	if s:
		return image


# load image to vram texture
def mat_2_tex(mat,texture=None):
	h,w,_=mat.shape
	#cv.imshow("mat_2_tex",mat)
	if texture is None:
		texture = gl.glGenTextures(1)
	gl.glBindTexture(gl.GL_TEXTURE_2D, texture)
	gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
	gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
	gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, w, h, 0, gl.GL_BGR,gl.GL_UNSIGNED_BYTE, mat)
	return texture, w, h
	#do not forget to delete the textures


class Game_Gui(Gui_Window):
	def __init__(self, w, h):
		super(Game_Gui, self).__init__(w,h)
		self.texture=None


	def process(self):

		self.texture,w,h = mat_2_tex(self.frame,self.texture)
		io = imgui.get_io()
		imgui.set_next_window_position(0, 0, 1, pivot_x =0, pivot_y = 0)
		imgui.set_next_window_size(w, h)
		imgui.begin("image",closable=False,flags=imgui.WINDOW_NO_SCROLLBAR | imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_SCROLL_WITH_MOUSE)
		if imgui.button("asd"):
			print("pressed")
		#imgui.text('An image:')
		imgui.image(self.texture, w, h)
		imgui.end()
		

if __name__ == "__main__":
	tw= Gui_Window()
	#tw= Game_Gui()
	tw.start_loop()
	tw.terminate()
	cv.destroyAllWindows()
