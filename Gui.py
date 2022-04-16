print("Start")
import glfw
import OpenGL.GL as gl
import imgui
from imgui.integrations.glfw import GlfwRenderer
import cv2 as cv 
path_to_font = None  # "path/to/font.ttf"

opened_state = True

def impl_glfw_init(w,h):
	width, height = w, h
	window_name = "Tic Tac yeeee"

	if not glfw.init():
		print("Could not initialize OpenGL context")
		sys.exit(1)

	glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
	glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
	glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
	glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, gl.GL_TRUE)

	window = glfw.create_window(int(width), int(height), window_name, None, None)
	glfw.make_context_current(window)

	if not window:
		glfw.terminate()
		print("Could not initialize Window")
		sys.exit(1)

	return window


cam = cv.VideoCapture(0)
def load_image(image_name='test.jpg',texture=None):
	s, image = cam.read()
	#image = cv.imread(image_name)
	h,w,c=image.shape
	#cv.imshow("asd",image)
	if texture is None:
		texture = gl.glGenTextures(1)
	gl.glBindTexture(gl.GL_TEXTURE_2D, texture)
	gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
	gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
	gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, w, h, 0, gl.GL_BGR,gl.GL_UNSIGNED_BYTE, image)
	return texture, w, h
	#input("Press Enter to continue.")

	#gl.glDeleteTextures([texture])


texture=None
w=None
h=None
def frame_commands():
	global texture
	global cam
	texture,w,h = load_image(texture=texture)
	imgui.text('An image:')
	imgui.image(texture, w, h)
	pass


def render_frame(impl, window, font):
	glfw.poll_events()
	impl.process_inputs()
	imgui.new_frame()

	gl.glClearColor(0.1, 0.1, 0.1, 1)
	gl.glClear(gl.GL_COLOR_BUFFER_BIT)

	if font is not None:
		imgui.push_font(font)
	frame_commands()
	if font is not None:
		imgui.pop_font()

	imgui.render()
	impl.render(imgui.get_draw_data())
	glfw.swap_buffers(window)


def main():
	imgui.create_context()
	window = impl_glfw_init(500,500)

	impl = GlfwRenderer(window)

	io = imgui.get_io()
	jb = io.fonts.add_font_from_file_ttf(path_to_font, 30) if path_to_font is not None else None
	impl.refresh_font_texture()

	global texture
	global w
	global h


	texture, w, h = load_image()

	while not glfw.window_should_close(window):
		render_frame(impl, window, jb)

	impl.shutdown()
	glfw.terminate()


if __name__ == "__main__":
	main()