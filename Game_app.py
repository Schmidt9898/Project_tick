
import time
from cam import WebcamVideoStream
from handDetector import handsDetector
from Gui import *
import cv2
import traceback
import imgui
from ticlient import Tic_net_client
import datetime

def hand_button(label,x,y,sx,sy,cursore=(0,0)):
	#imgui.dummy(sx,sy)
	bx,by=x-sx/2,y-sy/2
	rx,ry=x+sx/2,y+sy/2

	draw_list = imgui.get_window_draw_list()
	draw_list.add_rect_filled(bx,by, rx,ry, imgui.get_color_u32_rgba(0.1,0.2,0.8,1))
	draw_list.add_text(x-100,y, imgui.get_color_u32_rgba(1,1,0,1), label)
	if bx<cursore[0] and cursore[0]<rx and by<cursore[1] and cursore[1]<ry :
		draw_list.add_rect_filled(bx,by, rx,ry, imgui.get_color_u32_rgba(0.2,0.5,1,1))
		draw_list.add_text(x-100,y, imgui.get_color_u32_rgba(1,1,0,1), label)
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


		io = imgui.get_io()												 #font
		self.new_font = io.fonts.add_font_from_file_ttf("./DroidSans.ttf", 30,)
		self.impl.refresh_font_texture()
		# states
		# 0 menu machmaking
		# 1 in game ai bot
		# 2 challenging
		# 3 game online
		# 4 accepting page
		self.page_id=0 #0 menu 1 game 2 e

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
		self.hands = handsDetector(2)
		self.prevHandState = ""

		self.aiplayer = True

		self.net=Tic_net_client()
		#self.net.name = from_file / no name()
		self.net.Start()

		self.next_player_list_update_t=time.time()+2;

		self.Label_message="Challenging..."
		self.opponent=("server",0) # 0 is no one
		self.mark=None

		








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



		# states
		# 0 menu machmaking
		# 1 in game ai bot
		# 2 challenging
		# 3 game online
		# 4 accepting page

	def handle_inbox(self):
		msgs=self.net.get_messages()
		for m in msgs:
			print(m)					# TODO remove False
			if m["dest"] != self.net.id and False: # scip if its not sent to us
				continue
			if m["data"] == "CHALLENGE":
				if self.page_id == 0:
					self.opponent=("todo name",m["src"])
					self.page_id=4
			if m["data"] == "CANCEL" and m["src"]==self.opponent[1]:
				#if self.page_id == 4:
				self.opponent=("none",0)
				self.page_id=0
			if m["data"] == "ACCEPT" and m["src"]==self.opponent[1]:
				if self.page_id == 2:
					self.mark = 1 if self.net.id<self.opponent[1] else 0
					self.game_logic.reset()
					self.page_id=3
			if m["data"] == "STEP" and m["src"]==self.opponent[1]:
				mark = 1 if self.mark==0 else 0
				self.game_logic.step(mark,m["to"])

		pass

	def context(self):
		self.handle_inbox()


		imgui.push_font(self.new_font)
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
		self.isClicked=self.hands.isAction


		imgui.set_next_window_position(0, 0, 1, pivot_x =0, pivot_y = 0)
		imgui.set_next_window_size(self.width, self.height)
		imgui.push_style_color(imgui.COLOR_WINDOW_BACKGROUND, 	0	, 0	, 0,0)
		imgui.begin("Main",closable=False,flags=imgui.WINDOW_NO_SCROLLBAR | imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_SCROLL_WITH_MOUSE )
		draw_list=imgui.get_window_draw_list()

		if self.page_id==0:
			self.Draw_menu()
		elif self.page_id==1:
			self.Draw_game()
		elif self.page_id==2:
			self.Draw_challange_page()
		elif self.page_id==3:
			self.Draw_game_online()
		elif self.page_id==4:
			self.Draw_accepting_page()
		else:
			pass
		#print("Position",self.hands.cursorPosition)
		draw_list.add_circle_filled(self.hands.cursorPosition[0], self.hands.cursorPosition[1], 15, imgui.get_color_u32_rgba(0.1,0.7,0.8,1)) # cursore draw
		draw_list.add_circle(self.hands.cursorPosition[0], self.hands.cursorPosition[1], 14+15*(1-self.hands.progres), imgui.get_color_u32_rgba(0.9,0.9,0.8,1)) # cursore draw
		#if self.hands.holdStatus == 0:
		#	circle_color = imgui.get_color_u32_rgba(0.1,0.7,0.8,1)
		#else:
		#	circle_color = imgui.get_color_u32_rgba(0.8,0.7,0.1,1)
#
		#if self.hands.holdStatus == 1 or self.hands.holdStatus == 2:
		#	draw_list.add_circle_filled(self.hands.cursorPosition[0], self.hands.cursorPosition[1], 15, circle_color) # cursore draw
		#else:
		#	draw_list.add_circle_filled(self.cursorPosition[0], self.cursorPosition[1], 15, circle_color) # cursore draw
#
#
		#if self.hands.holdStatus == 1 or self.hands.holdStatus == 2:
		#	time_delta = (datetime.datetime.now() - self.hands.closedTime).total_seconds()
		#	if time_delta != 0 :
		#		time_prop = (self.hands.holdTime/(time_delta))
		#		if time_prop > 5:
		#			time_prop = 5
		imgui.end()
		imgui.pop_style_color(1)
		imgui.pop_font()

	def Draw_menu(self):

		if self.next_player_list_update_t<time.time():
			#print("refresh players")
			self.net.refresh_playes()
			self.next_player_list_update_t=time.time()+2


		if hand_button("Play against BOB the BOT",self.width/4*3,200,200,100,self.hands.cursorPosition) and self.isClicked:
			print("most")
			self.page_id=1

		imgui.dummy(100,30)
		imgui.same_line()
		imgui.begin_child("##listc", -50, 0, border=False)
		imgui.dummy(30,0)
		imgui.text("Available players")

		imgui.listbox_header("##", 200, 300)
		for id,user, in self.net.clients_avil.items():
			p,ttl=user
			imgui.selectable(str(id)+". "+p , id==self.last_hoverred_selectable)
			if is_over(imgui.core.get_item_rect_min(),imgui.core.get_item_rect_max(),self.hands.cursorPosition):
				#imgui.core.get_item_rect_max()
				self.last_hoverred_selectable=id
				if self.isClicked:
					self.opponent=(p,id)
					self.Label_message="Challenging "+str(id)+". "+p
					self.page_id=2
					data={"data":"CHALLENGE"}
					self.net.send(data,id)
					#print("i selected",id)

		#imgui.selectable("Not Selected", False)
		imgui.listbox_footer()
		imgui.end_child()

		pass
	def Draw_game(self):
		w,h=self.width,self.height

		if self.isClicked:
			print("aca")
			squareNumber = int(self.hands.cursorPosition[1]/h*3)*3+int(self.hands.cursorPosition[0]/w*3)
			self.game_logic.step(self.playerNumber,squareNumber)# this is not how this work but okay

		if self.aiplayer and self.game_logic.mark==1 and self.game_logic.is_win is None:
			self.game_logic.ai_player_move()

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

		if  self.game_logic.is_win is not None:
			print("won player", self.game_logic.is_win)
		#p = int(self.cursorPosition[1]/h*3)*3+int(self.cursorPosition[0]/w*3)
		#print("y",int(p/3)*(u_h),"x",int(p%3)*(u_w))
		pass
	def Draw_challange_page(self):
		imgui.text("Challenging "+str(self.opponent[1])+". "+self.opponent[0] )
		if hand_button("Cancel",self.width/4*3,200,200,100,self.hands.cursorPosition) and self.isClicked:
			data={"data":"CANCEL"}
			self.net.send(data,self.opponent[1])
			self.page_id=0
	def Draw_accepting_page(self):	
		imgui.text("You have been challanged! "+str(self.opponent[1])+". "+self.opponent[0] )
		if hand_button("Accept",self.width/4*3,200,200,100,self.hands.cursorPosition) and self.isClicked:
			data={"data":"ACCEPT"}
			self.net.send(data,self.opponent[1])
			self.page_id=3
			self.mark = 1 if self.net.id<self.opponent[1] else 0
			self.game_logic.reset()
		if hand_button("Cancel",self.width/4*3,350,200,100,self.hands.cursorPosition) and self.isClicked:
			data={"data":"CANCEL"}
			self.net.send(data,self.opponent[1])
			self.opponent=("server",0)
			self.page_id=0

	def Draw_game_online(self):
		w,h=self.width,self.height

		if self.isClicked:
			#print("aca")
			squareNumber = int(self.hands.cursorPosition[1]/h*3)*3+int(self.hands.cursorPosition[0]/w*3)
			data={"data":"STEP","to":squareNumber}
			self.net.send(data,self.opponent[1])
			self.game_logic.step(self.mark,squareNumber)

		self.drawGrid()
		u_h=h/3
		u_w=w/3
		draw_list=imgui.get_window_draw_list()
		for p,item in enumerate(self.game_logic.get_state()):
			if item == "o":
				draw_list.add_circle(int(p%3)*(u_w)+u_w/2, int(p/3)*(u_h)+u_h/2, self.height/self.ygrids/3, imgui.get_color_u32_rgba(1,1,0,1),32, thickness=3)
			elif item == "x":
				Game.draw_x(int(p%3)*(u_w)+u_w/2, int(p/3)*(u_h)+u_h/2, self.height/self.ygrids/3)


		if  self.game_logic.is_win is not None:
			print("won player", self.game_logic.is_win)

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
