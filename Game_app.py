
from cam import WebcamVideoStream
from handDetector import handsDetector
from Gui import *
import cv2
import traceback
import imgui
from server import Tic_net_client


def hand_button(label,x,y,sx,sy,cursore=(0,0)):
	#imgui.dummy(sx,sy)
	bx,by=x-sx/2,y-sy/2
	rx,ry=x+sx/2,y+sy/2
	
	draw_list = imgui.get_window_draw_list()
	draw_list.add_rect_filled(bx,by, rx,ry, imgui.get_color_u32_rgba(0.1,0.2,0.8,1))
	draw_list.add_text(x,y, imgui.get_color_u32_rgba(1,1,0,1), label)
	if bx<cursore[0] and cursore[0]<rx and by<cursore[1] and cursore[1]<ry :
		draw_list.add_rect_filled(bx,by, rx,ry, imgui.get_color_u32_rgba(0.2,0.5,1,1))
		draw_list.add_text(x,y, imgui.get_color_u32_rgba(1,1,0,1), label)
		return True
	
	#print(nx)

def is_over(min,max,pos):
	minx,miny=min
	maxx,maxy=max
	px,py=pos
	return minx<px and px<maxx and miny<py and py<maxy



class Game(Gui_Window):
	def __init__(self, w, h,title="None"):
		super(Game, self).__init__(w, h,title)

		self.page_id=0 #0 menu 1 game 2 etc..

		self.image_texture =None

		self.last_hoverred_selectable=0

		self.isClicked = False
		self.cursorPosition = [0, 0]
		self.frame = np.zeros((h,w,3), np.uint8)
		self.width = w
		self.height = h
		self.xgrids = 3 #xgrids
		self.ygrids = 3 #ygrids

		self.game_logic=Tictactoe()
		self.playerNumber = 0


		self.vs = WebcamVideoStream().start()
		self.hands = handsDetector()
		self.prevHandState = ""

		
		self.net=Tic_net_client()
		self.net.Start()



	def set_frame(self, frame):
		self.frame = frame

	def drawGrid(self):
		draw_list = imgui.get_window_draw_list()
		draw_list.add_line(self.width/3, 0, self.width/3, self.height, imgui.get_color_u32_rgba(1,1,0,1), 3)
		draw_list.add_line(2*self.width/3, 0, 2*self.width/3, self.height, imgui.get_color_u32_rgba(1,1,0,1), 3)
		draw_list.add_line(0, self.height/3, self.width, self.height/3, imgui.get_color_u32_rgba(1,1,0,1), 3)
		draw_list.add_line(0, 2*self.height/3, self.width, 2*self.height/3, imgui.get_color_u32_rgba(1,1,0,1), 3)

	def draw_x(x,y,r): # TODO may reduce operation
		ltx=x-r
		lty=y-r
		rtx=x+r
		rty=y-r
		lbx=x-r
		lby=y+r
		rbx=x+r
		rby=y+r
		draw_list = imgui.get_window_draw_list()
		draw_list.add_line( ltx,lty,rbx,rby, imgui.get_color_u32_rgba(1,1,0,1), 3 )
		draw_list.add_line( lbx,lby,rtx,rty , imgui.get_color_u32_rgba(1,1,0,1), 3 )


	def context(self):

		io = imgui.get_io()
		

		frame = self.vs.read()		#get frame
		frame = cv2.flip(frame, 1)  # mirror the image
		self.hands.getHandAction(frame) #processing
		self.image_texture,w,h = mat_2_tex(frame,self.image_texture) # generate texture

		imgui.set_next_window_position(0, 0, 1, pivot_x =0, pivot_y = 0)
		imgui.set_next_window_size(self.width, self.height)

		imgui.begin("background",closable=False,flags=imgui.WINDOW_NO_SCROLLBAR | imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_SCROLL_WITH_MOUSE | imgui.WINDOW_NO_BRING_TO_FRONT_ON_FOCUS)
		imgui.image(self.image_texture, w, h) ## TODO different size
		imgui.end()
		#self.cursorPosition=self.hands.cursorPosition # for graphics only 
		self.cursorPosition = self.hands.cursorPosition
		
		#get click event
		self.isClicked=False
		if(self.prevHandState == "Closed" and self.hands.state == "Open"): # something feels off
			self.isClicked=True
		self.prevHandState = self.hands.state
			
		

		imgui.set_next_window_position(0, 0, 1, pivot_x =0, pivot_y = 0)
		imgui.set_next_window_size(self.width, self.height)
		imgui.push_style_color(imgui.COLOR_WINDOW_BACKGROUND, 	0	, 0	, 0,0)
		imgui.begin("Main",closable=False,flags=imgui.WINDOW_NO_SCROLLBAR | imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_SCROLL_WITH_MOUSE )
		draw_list=imgui.get_window_draw_list()
		
		if self.page_id==0:
			self.Draw_menu()
		elif self.page_id==1:
			self.Draw_game()
		else:
			pass

		draw_list.add_circle_filled(self.cursorPosition[0], self.cursorPosition[1], 15, imgui.get_color_u32_rgba(0.1,0.7,0.8,1)) # cursore draw

		imgui.end()
		imgui.pop_style_color(1)

	def Draw_menu(self):
		if hand_button("alma",self.width/2,200,200,100,self.cursorPosition) and self.isClicked:
			print("most")
			self.page_id=1


		imgui.listbox_header("List", 200, 300)
		for id,p in self.net.clients_avil.items():
			imgui.selectable(p, id==self.last_hoverred_selectable)
			if is_over(imgui.core.get_item_rect_min(),imgui.core.get_item_rect_max(),self.cursorPosition):
				#imgui.core.get_item_rect_max()
				self.last_hoverred_selectable=id
				if self.isClicked:
					print("i selected",id)
					
		#imgui.selectable("Not Selected", False)
		imgui.listbox_footer()

		pass
	def Draw_game(self):
		w,h=self.width,self.height

		if self.isClicked:
			squareNumber = int(self.cursorPosition[1]/h*3)*3+int(self.cursorPosition[0]/w*3)
			self.game_logic.step(self.playerNumber,squareNumber)# this is not how this work but okay
		self.drawGrid()
		u_h=h/3
		u_w=w/3
		draw_list=imgui.get_window_draw_list()
		#draw_list.add_circle_filled(int(p%3)*(u_w)+u_w/2, int(p/3)*(u_h)+u_h/2, 15, imgui.get_color_u32_rgba(0.1,0.7,0.8,1))
		for p,item in enumerate(self.game_logic.get_state()):
	
			if item == "o":
				draw_list.add_circle(int(p%3)*(u_w)+u_w/2, int(p/3)*(u_h)+u_h/2, self.height/self.ygrids/3, imgui.get_color_u32_rgba(1,1,0,1),32, thickness=3)
			elif item == "x":
				Game.draw_x(int(p%3)*(u_w)+u_w/2, int(p/3)*(u_h)+u_h/2, self.height/self.ygrids/3)
			
			#draw_list.add_circle(int(p%3)*(u_w)+u_w/2, int(p/3)*(u_h)+u_h/2, self.height/self.ygrids/3, imgui.get_color_u32_rgba(1,1,0,1),32, thickness=3)
			#Game.draw_x(int(p%3)*(u_w)+u_w/2, int(p/3)*(u_h)+u_h/2, self.height/self.ygrids/3)

		#p = int(self.cursorPosition[1]/h*3)*3+int(self.cursorPosition[0]/w*3)
		#print("y",int(p/3)*(u_h),"x",int(p%3)*(u_w))
		pass
	def Draw_test(self):
		pass
	

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




