
from cam import WebcamVideoStream
from handDetector import handsDetector
from Gui import *
import cv2
import traceback



class Game(Gui_Window):
	def __init__(self, w, h,title="None"):
		super(Game, self).__init__(w, h,title)

		self.image_texture =None

		self.putCursor = False
		self.cursorPosition = [0, 0]
		self.frame = np.zeros((h,w,3), np.uint8)
		self.width = w
		self.height = h
		#self.xgrids = xgrids
		#self.ygrids = ygrids

		self.game_logic=Tictactoe()
		self.playerNumber = 0


		self.vs = WebcamVideoStream().start()
		self.hands = handsDetector()
		self.prevHandState = ""



	def set_frame(self, frame):
		self.frame = frame

	def drawGrid(self):
		draw_list = imgui.get_window_draw_list()

		draw_list.add_line(self.width/3, 0, self.width/3, self.height, imgui.get_color_u32_rgba(1,1,0,1), 3)
		draw_list.add_line(2*self.width/3, 0, 2*self.width/3, self.height, imgui.get_color_u32_rgba(1,1,0,1), 3)
		draw_list.add_line(0, self.height/3, self.width, self.height/3, imgui.get_color_u32_rgba(1,1,0,1), 3)
		draw_list.add_line(0, 2*self.height/3, self.width, 2*self.height/3, imgui.get_color_u32_rgba(1,1,0,1), 3)

	def put_o(self, position):
		xshift = position%self.xgrids + 1
		yshift = int(position/self.ygrids)+1
		x_center = (2*xshift -1 )*self.width/self.xgrids/2
		y_center = (2*yshift -1 )*self.height/self.ygrids/2
		draw_list = imgui.get_window_draw_list()
		draw_list.add_circle(x_center, y_center, self.height/self.ygrids/3, imgui.get_color_u32_rgba(1,1,0,1), thickness=3)

	def put_x(self, position):
		xshift = position%self.xgrids + 1
		yshift = int(position/self.ygrids)+1
		x_center = (2*xshift -1 )*self.width/self.xgrids/2
		y_center = (2*yshift -1 )*self.height/self.ygrids/2
		line_width = self.height/self.ygrids/3
		draw_list = imgui.get_window_draw_list()
		draw_list.add_line(
			x_center-line_width, y_center-line_width,
			x_center+line_width, y_center+line_width,
			imgui.get_color_u32_rgba(1,1,0,1), 3
			)
		draw_list.add_line(
			x_center-line_width, y_center+line_width,
			x_center+line_width, y_center-line_width,
			imgui.get_color_u32_rgba(1,1,0,1), 3
			)

	def findSquareNumber(self, cursorPosition):
		xprev = 0
		yprev = 0
		for i in range(self.xgrids*self.ygrids):
			xshift = i%self.xgrids + 1
			yshift = int(i/self.ygrids)+1
			x_pos = (xshift)*self.width/self.xgrids
			y_pos = (yshift)*self.height/self.ygrids

			if xshift == 1:
				xprev = 0

			if (cursorPosition[0] < x_pos and
				cursorPosition[0] > xprev and
				cursorPosition[1] < y_pos and
				cursorPosition[1] > yprev):
				return i

			xprev = x_pos
			y_pos = y_pos

	def context(self):
		frame = self.vs.read()
		frame = cv2.flip(frame, 1)  # mirror the image
		self.hands.getHandAction(frame)
		self.image_texture,w,h = mat_2_tex(frame,self.image_texture)
		
		if(self.prevHandState == "Closed" and self.hands.state == "Open"):
			self.putCursor = True
			self.cursorPosition = self.hands.cursorPosition
		self.prevHandState = self.hands.state



		io = imgui.get_io()
		imgui.set_next_window_position(0, 0, 1, pivot_x =0, pivot_y = 0)
		imgui.set_next_window_size(w, h)
		imgui.begin("image",closable=False,flags=imgui.WINDOW_NO_SCROLLBAR | imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_SCROLL_WITH_MOUSE)

		imgui.image(self.image_texture, w, h)
		self.drawGrid()

		if self.putCursor:
			squareNumber = self.findSquareNumber(self.cursorPosition)
			self.game_logic.step(self.playerNumber,squareNumber)
			self.putCursor = False

		for idx,item in enumerate(self.game_logic.get_state()):
			if item == "o":
				self.put_o(idx)
			elif item == "x":
				self.put_x(idx)

		imgui.end()
	

	def start_loop(self):
		try:
			while not glfw.window_should_close(self.window):
				self.render_frame()
		except Exception as e:
			print(str(e))
    		#traceback.print_exc()
			#print(sys.exc_info())
		finally:
			self.impl.shutdown()
			glfw.terminate()
			self.vs.stop()
			cv2.destroyAllWindows()




