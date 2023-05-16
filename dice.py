import random
import sys
import pygame
import time
import threading
import main
import requests
from collections import OrderedDict
from queue import Queue
from win32con import MB_OK
from win32api import MessageBox
from re import findall
IP='127.0.0.1'
#IP_in=input('Server_IP:')
#if IP_in!='':
#    IP=IP_in
URL_ACCOUNT = 'http://'+IP+':54088/accounts'
URL_JOIN='http://'+IP+':54088/join'
URL_LOAD='http://'+IP+':54088/load'
URL_INPUT='http://'+IP+':54088/gameinput'
# global user
class waiting_lobby:
    def  __init__ ( self , width= 900 , height= 700 ) :
        #desktop
        global user
        pygame.init()
        pygame.display.set_caption("Yahtzee")
        pygame.mixer.music.load("lobby/waiting.mp3")
        pygame.mixer.music.play(-1)
        pygame_icon = pygame.image.load('dice/dice1.png')
        pygame.display.set_icon(pygame_icon)
        self.size = width, height
        self .screen = pygame.display.set_mode(self.size)
        self.background_image = pygame.image.load("lobby/background2.png").convert()
        self.background_image = pygame.transform.scale(self.background_image, (900, 700))
        self.useless_image = pygame.image.load("lobby/useless.png").convert()
        self.useless_image = pygame.transform.scale(self.useless_image, (900, 700))
        self.top_image = pygame.image.load("lobby/up.jpg").convert()
        self.top_image = pygame.transform.scale(self.top_image, (350, 100))
        self.square_image = pygame.image.load("lobby/square.jpg").convert()
        self.label_font = pygame.font.SysFont("freesansbppld.ttf",20)
        self.button= pygame.image.load("lobby/button.png").convert_alpha()
        self.button = pygame.transform.scale(self.button, (600, 200))
        self.label_font = pygame.font.SysFont("freesansbppld.ttf",20)
        self.label_button = pygame.font.SysFont("freesansbppld.ttf",60)
        self.Yname_text=self.label_font.render("Your Name:",True,(0,0,0))
        self.name_text=self.label_font.render(user["name"],True,(0,0,0))
        self.Ymoney_text=self.label_font.render("Your Money:",True,(0,0,0))
        self.money_text=self.label_font.render(str(user["dollar"]),True,(0,0,0))
        self.button1_text=self.label_button.render("Local Games",True,(0,0,0))
        self.button2_text=self.label_button.render("Multiple Games",True,(0,0,0))
        self. touchSound = pygame.mixer.Sound("map/touch.mp3")
        #up is background
        self.waittable= pygame.image.load("lobby/waittable.png").convert_alpha()
        self.waittable = pygame.transform.scale(self.waittable, (700, 700))
        self.cancel= pygame.image.load("lobby/cancel.png").convert_alpha()
        self.cancel = pygame.transform.scale(self.cancel, (200, 100))
        self.p1= pygame.image.load("lobby/1p.png").convert_alpha()
        self.p2= pygame.image.load("lobby/2p.png").convert_alpha()
        self.p3= pygame.image.load("lobby/3p.png").convert_alpha()
        self.p4= pygame.image.load("lobby/4p.png").convert_alpha()
        #up is multiple
        self.connected=False
        self .clock = pygame.time.Clock()
        self.run()
    def  run ( self ) :
        global Multiple_sign
        global cpu_player
        global user
        global Local_sign
        Multiple_sign=False
        Local_sign=False
        self.send=True
        mainloop=True
        dice=[Dice(285,425),
        Dice(550,425),
        Dice(410,300),
        Dice(285,175),
        Dice(550,175)
        ]
        times=0
        while mainloop:
            if user["dollar"]<300:
                self.screen.blit(self.useless_image,[0,0])
                for event in pygame.event.get():
                    if event.type == pygame. QUIT:
                        sys.exit()
                    elif  event.type == pygame.MOUSEBUTTONDOWN: 
                        sys.exit()
                pygame.display.flip()
            else:
                self.screen.blit(self.background_image,[0,0])
                self.screen.blit(self.square_image,[0,3])
                self.screen.blit(self.square_image,[800,3])
                self.screen.blit(self.Yname_text,[10,30])
                self.screen.blit(self.Ymoney_text,[810,30])
                self.screen.blit(self.name_text,[10,50])
                self.screen.blit(self.money_text,[810,50])
                self.screen.blit(self.button,[150,150])
                self.screen.blit(self.button,[150,350])
                self.screen.blit(self.button1_text,[300,225])
                self.screen.blit(self.button2_text,[285,425])
                if Multiple_sign or Local_sign:
                    self.screen.blit(self.waittable,[100,25])
                    if Multiple_sign:
                        for i in range(5):
                            self.screen.blit(dice[i].diceSpin[dice[i].SpinStatus],dice[i].diceRect)
                        times+=1
                        if (times%40==0):
                            for i in range(5):                      
                                dice[i].move()
                        if self.send:
                            t=threading.Thread(target=self.connect)
                            t.setDaemon(True)
                            t.start()
                            self.send=False
                        if self.connected==True:
                            cpu_player="#"
                            return
                    if Local_sign:
                        self.screen.blit(self.cancel,[360,500])
                        button_rect1 = self.cancel.get_rect(topleft = (360, 500))
                        self.screen.blit(self.p1,[300,200])
                        self.screen.blit(self.p2,[500,200])
                        self.screen.blit(self.p3,[300,350])
                        self.screen.blit(self.p4,[500,350])
                for i in range(2):
                    self.screen.blit(self.top_image,[100+350*i,3])
                for event in pygame.event.get():
                    if event.type == pygame. QUIT:
                        if Multiple_sign:
                            MessageBox(0,"You can't close windows when pairing!", "Yahtzee",MB_OK)
                            continue
                        sys.exit()
                    elif  event.type == pygame.MOUSEBUTTONDOWN: 
                        self. touchSound.play()
                        x,y=event.pos
                        if not Multiple_sign and not Local_sign:
                            button_rect1 = self.button.get_rect(topleft = (150, 150))
                            button_rect2 = self.button.get_rect(topleft = (150, 350))
                            if button_rect1.collidepoint(x, y):
                                Local_sign=True
                            elif button_rect2.collidepoint(x, y):
                                Multiple_sign=True
                        elif Local_sign:
                            button_rect1 = self.cancel.get_rect(topleft = (360, 500))
                            p1_rect = self.p1.get_rect(topleft = (300, 200))
                            p2_rect = self.p2.get_rect(topleft = (500, 200))
                            p3_rect = self.p3.get_rect(topleft = (300, 350))
                            p4_rect = self.p4.get_rect(topleft = (500, 350))
                            if button_rect1.collidepoint(x, y):
                                Local_sign=False
                            elif p1_rect.collidepoint(x, y):
                                cpu_player="#123"
                                return
                            elif p2_rect.collidepoint(x, y):
                                cpu_player="#23"
                                return
                            elif p3_rect.collidepoint(x, y):
                                cpu_player="#3"
                                return
                            elif p4_rect.collidepoint(x, y):
                                cpu_player="#"
                                return
                pygame.display.flip()
    def connect(self):
        global player_state
        global Multiple_sign
        my_params = {}
        my_params["uid"] = user["id"]
        response = requests.post(URL_JOIN, params = my_params)
        print(response.status_code)
        print(response.headers)
        player_state = response.json()				# response.json() is json records
        if "You are waiting"in str(player_state):
            Multiple_sign=False
            self.send=True
            MessageBox(0,"You are Waiting", "Yahtzee",MB_OK)
            return 
        elif "You are playing"in str(player_state):
            Multiple_sign=False
            self.send=True
            MessageBox(0,"You are Playing", "Yahtzee",MB_OK)
            return 
        print("player_state:"+str(player_state))
        self.connected=True
class InputBox:
    def __init__(self,rect: pygame.Rect = pygame.Rect(100, 100, 140, 32)) -> None:
        #bool True= login False = Register
        self.boxBody: pygame.Rect = rect
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('dodgerblue2')
        self.color = self.color_inactive
        self.active = False
        self.text = ''
        self.done = False
        self.font = pygame.font.Font(None, 32)
    def dealEvent(self,check, event: pygame.event.Event):
        global user
        if(event.type == pygame.MOUSEBUTTONDOWN):
            if(self.boxBody.collidepoint(event.pos)):
                self.active = not self.active
            else:
                self.active = False
            self.color = self.color_active if(
                self.active) else self.color_inactive
        if(event.type == pygame.KEYDOWN):
            if(self.active):
                if(event.key == pygame.K_RETURN):
                    if check==True:
                        #login
                        try:
                            my_params = {}
                            my_params["name"] = self.text
                            response = requests.get(URL_ACCOUNT, params = my_params)
                            print(response.status_code)
                            print(response.headers)
                            json_rec = response.json()				# response.json() is json records
                            for item in json_rec:
                                user=item  
                                MessageBox(0,"Login Successfull", "Yahtzee",MB_OK)
                                return
                            MessageBox(0,"No account", "Yahtzee",MB_OK)
                        except:
                            MessageBox(0,"Server is crash", "Warn",MB_OK)
                    else:
                        try:
                            #register
                            new_dict = {}
                            new_dict["name"] = self.text
                            response = requests.post(URL_ACCOUNT, json=new_dict)
                            print(response.status_code)
                            print(response.headers)
                            print(response.text)
                            if response.text.find("erro")!=-1:
                                MessageBox(0,response.text[14:len(response.text)-4:1],"Warn",MB_OK)
                            else:
                                MessageBox(0,"Register Successfull","Yahtzee",MB_OK)
                        except:
                            MessageBox(0,"Server is crash", "Warn",MB_OK)
                    print(self.text)
                    self.text=''
                elif(event.key == pygame.K_BACKSPACE):
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

    def draw(self, screen: pygame.surface.Surface):
        txtSurface = self.font.render(self.text, True, self.color)
        width = max(200, txtSurface.get_width()+10)
        self.boxBody.w = width
        screen.blit(txtSurface, (self.boxBody.x+5, self.boxBody.y+5))
        pygame.draw.rect(screen, self.color, self.boxBody, 2)

class login_lobby:
    def  __init__ ( self , width= 900 , height= 700 ) :
        #desktop
        pygame.init()
        pygame.display.set_caption("Yahtzee")
        pygame_icon = pygame.image.load('dice/dice1.png')
        pygame.display.set_icon(pygame_icon)
        pygame.mixer.music.load("lobby/lobby music.mp3")
        pygame.mixer.music.play(-1)
        self.size = width, height
        self .screen = pygame.display.set_mode(self.size)
        self.background_image = pygame.image.load("lobby/background.png").convert()
        self.background_image = pygame.transform.scale(self.background_image, (900, 700))
        self.console = pygame.image.load("lobby/console.png").convert_alpha()
        self.console = pygame.transform.scale(self.console, (400, 400))
        self. touchSound = pygame.mixer.Sound("map/touch.mp3")
        #up is background
        self.inputbox1 = InputBox(pygame.Rect(100, 450, 100, 32))
        self.inputbox2 = InputBox(pygame.Rect(350, 450, 100, 32))
        self.label_font = pygame.font.SysFont("freesansbppld.ttf",50)
        self.label1_text=self.label_font.render("Login",True,pygame.Color('lightskyblue3'))
        self.label2_text=self.label_font.render("Register",False,pygame.Color('lightskyblue3'))
        self .clock = pygame.time.Clock()
        self.run()
    def  run ( self ) :
        mainloop=True
        global user
        user={}
        while mainloop:
            if(user=={}):
                self.screen.blit(self.background_image,[0,0])
                self.screen.blit(self.console,[0,250])
                self.screen.blit(self.console,[250,250])
                self.screen.blit(self.label1_text, (160,400))
                self.screen.blit(self.label2_text, (390,400))
                for event in pygame.event.get():
                    if event.type == pygame. QUIT:
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self. touchSound.play()
                    self.inputbox1.dealEvent(True,event)
                    self.inputbox2.dealEvent(False,event)
                self.inputbox1.draw(self.screen)
                self.inputbox2.draw(self.screen)
                pygame.display.flip()
            else:
                return

class  Dice : 
    def __init__ ( self ,width,hieght) :
        self .diceRect = pygame.Rect( width , hieght,  100 ,  100 )
        self .diceSpin = [
            pygame.image.load( "roll/roll1.png" ),
            pygame.image.load( "roll/roll2.png" ),
            pygame.image.load( "roll/roll3.png" ),
            pygame.image.load( "roll/roll4.png" ),
            pygame.image.load( "roll/roll5.png" ),
            pygame.image.load( "roll/roll6.png" ),
            pygame.image.load( "roll/roll7.png" ),
            pygame.image.load( "roll/roll8.png" ),
            pygame.image.load( "roll/roll9.png" ),
            pygame.image.load( "roll/roll10.png" ),
            pygame.image.load( "roll/roll11.png" ),
            pygame.image.load( "roll/roll12.png" )
        ]
        self.diceStop = [
            pygame.image.load( "dice/dice1.gif" ),
            pygame.image.load( "dice/dice2.gif" ),
            pygame.image.load( "dice/dice3.gif" ),
            pygame.image.load( "dice/dice4.gif" ),
            pygame.image.load( "dice/dice5.gif" ),
            pygame.image.load( "dice/dice6.gif" ),
            pygame.image.load( "dice/dice7.gif" ),
        ]
        self .StopStatus=0
        self .SpinStatus =  0
        self .reset = True
        self .rollTimes =  0   # reality rolltime
        self .start = False   # status
        self .rolls = False
        self .rollCount = random.randint( 3 ,  10 )   # rolltime random
        self. rollSound = pygame.mixer.Sound("dice/roll_sound.mp3")
    def  roll ( self ) :
        self.move()
        self.rolls=True
        self. rollSound.play()
        self.rollTimes +=  1 
        if  self .rollTimes >  self . rollCount: 
            self .start = False
            self .rollCount = random.randint( 3 ,  10 )
            #self .StopStatus = random.randint( 0 ,  5 )
            self. rollTimes =  0
        self.rolls=False
    def  stop ( self ) :
        return self.StopStatus +1
    def  move ( self ) :
        self .SpinStatus +=  1 
        if self .SpinStatus == len( self .diceSpin):
            self .SpinStatus =  0

class  Game : 
    def  __init__ ( self , width= 900+408 , height= 581 ) :
        #desktop
        pygame.init()
        pygame.display.set_caption("Yahtzee")
        pygame.mixer.music.load("map/ocean fight.mp3")
        pygame.mixer.music.play(-1)
        pygame_icon = pygame.image.load('dice/dice1.png')
        pygame.display.set_icon(pygame_icon)
        self.size = width, height
        self .screen = pygame.display.set_mode(self.size)
        self.background_image = pygame.image.load("map/background.jpg").convert()
        self.background_image = pygame.transform.scale(self.background_image, (900, 581))
        self.grade_image = pygame.image.load("map/grade.jpg").convert()
        self.grade_image = pygame.transform.scale(self.grade_image, (408, 581))
        self. touchSound = pygame.mixer.Sound("map/touch.mp3")
        self. endSound = pygame.mixer.Sound("map/end.mp3")
        self .clock = pygame.time.Clock()
        #roll button
        self.start_image = pygame.image.load('map/780.png').convert_alpha()
        self.start_image = pygame.transform.scale(self.start_image, (200, 200))

        self.end_image = pygame.image.load('map/end.png').convert_alpha()
        self.end_image = pygame.transform.scale(self.end_image, (950, 500))
        #start_text
        self.start_font = pygame.font.SysFont("freesansbppld.ttf",30)
        self.reset_time = 3
        self.time_text = self.start_font.render("time:"+str(self.reset_time-1),True,(255,255,255))
        #dice
        self.Dice1 = Dice(350,280)
        self.Dice2 = Dice(450,280)
        self.Dice3 = Dice(300,180)
        self.Dice4 = Dice(400,180)
        self.Dice5 = Dice(500,180)
        #label_text
        self.label_font = pygame.font.SysFont("freesansbppld.ttf",20)
        # for player in range(true_player):
        #     for index in range(14):
        #         locals()['self.label'+str(player)+str(index)+'_text'] = self.label_font.render("select",True,(0,0,0))
        self.label00_text=self.label_font.render("select",True,(0,0,0))
        self.label01_text=self.label_font.render("select",True,(0,0,0))
        self.label02_text=self.label_font.render("select",True,(0,0,0))
        self.label03_text=self.label_font.render("select",True,(0,0,0))
        self.label04_text=self.label_font.render("select",True,(0,0,0))
        self.label05_text=self.label_font.render("select",True,(0,0,0))
        self.label06_text=self.label_font.render("select",True,(0,0,0))
        self.label07_text=self.label_font.render("select",True,(0,0,0))
        self.label08_text=self.label_font.render("select",True,(0,0,0))
        self.label09_text=self.label_font.render("select",True,(0,0,0))
        self.label010_text=self.label_font.render("select",True,(0,0,0))
        self.label011_text=self.label_font.render("select",True,(0,0,0))
        self.label012_text=self.label_font.render("select",True,(0,0,0))
        self.label013_text=self.label_font.render("select",True,(0,0,0))
        self.label10_text=self.label_font.render("select",True,(0,0,0))
        self.label11_text=self.label_font.render("select",True,(0,0,0))
        self.label12_text=self.label_font.render("select",True,(0,0,0))
        self.label13_text=self.label_font.render("select",True,(0,0,0))
        self.label14_text=self.label_font.render("select",True,(0,0,0))
        self.label15_text=self.label_font.render("select",True,(0,0,0))
        self.label16_text=self.label_font.render("select",True,(0,0,0))
        self.label17_text=self.label_font.render("select",True,(0,0,0))
        self.label18_text=self.label_font.render("select",True,(0,0,0))
        self.label19_text=self.label_font.render("select",True,(0,0,0))
        self.label110_text=self.label_font.render("select",True,(0,0,0))
        self.label111_text=self.label_font.render("select",True,(0,0,0))
        self.label112_text=self.label_font.render("select",True,(0,0,0))
        self.label113_text=self.label_font.render("select",True,(0,0,0))
        self.label20_text=self.label_font.render("select",True,(0,0,0))
        self.label21_text=self.label_font.render("select",True,(0,0,0))
        self.label22_text=self.label_font.render("select",True,(0,0,0))
        self.label23_text=self.label_font.render("select",True,(0,0,0))
        self.label24_text=self.label_font.render("select",True,(0,0,0))
        self.label25_text=self.label_font.render("select",True,(0,0,0))
        self.label26_text=self.label_font.render("select",True,(0,0,0))
        self.label27_text=self.label_font.render("select",True,(0,0,0))
        self.label28_text=self.label_font.render("select",True,(0,0,0))
        self.label29_text=self.label_font.render("select",True,(0,0,0))
        self.label210_text=self.label_font.render("select",True,(0,0,0))
        self.label211_text=self.label_font.render("select",True,(0,0,0))
        self.label212_text=self.label_font.render("select",True,(0,0,0))
        self.label213_text=self.label_font.render("select",True,(0,0,0))
        self.label30_text=self.label_font.render("select",True,(0,0,0))
        self.label31_text=self.label_font.render("select",True,(0,0,0))
        self.label32_text=self.label_font.render("select",True,(0,0,0))
        self.label33_text=self.label_font.render("select",True,(0,0,0))
        self.label34_text=self.label_font.render("select",True,(0,0,0))
        self.label35_text=self.label_font.render("select",True,(0,0,0))
        self.label36_text=self.label_font.render("select",True,(0,0,0))
        self.label37_text=self.label_font.render("select",True,(0,0,0))
        self.label38_text=self.label_font.render("select",True,(0,0,0))
        self.label39_text=self.label_font.render("select",True,(0,0,0))
        self.label310_text=self.label_font.render("select",True,(0,0,0))
        self.label311_text=self.label_font.render("select",True,(0,0,0))
        self.label312_text=self.label_font.render("select",True,(0,0,0))
        self.label313_text=self.label_font.render("select",True,(0,0,0))

        self.Lowsec0=self.label_font.render("0",True,(0,0,0))
        self.Upsec0=self.label_font.render("0",True,(0,0,0))
        self.Total0=self.label_font.render("0",True,(0,0,0))
        self.Lowsec1=self.label_font.render("0",True,(0,0,0))
        self.Upsec1=self.label_font.render("0",True,(0,0,0))
        self.Total1=self.label_font.render("0",True,(0,0,0))
        self.Lowsec2=self.label_font.render("0",True,(0,0,0))
        self.Upsec2=self.label_font.render("0",True,(0,0,0))
        self.Total2=self.label_font.render("0",True,(0,0,0))
        self.Lowsec3=self.label_font.render("0",True,(0,0,0))
        self.Upsec3=self.label_font.render("0",True,(0,0,0))
        self.Total3=self.label_font.render("0",True,(0,0,0))
        self.score_sheet={}
        self.score_sheet['player0']=0
        self.score_sheet['player1']=0
        self.score_sheet['player2']=0
        self.score_sheet['player3']=0
        #round_text
        #self.round_text = self.start_font.render("round:"+str(self.round),True,(255,255,255))
        #done_image
        self.done_font = pygame.font.SysFont("freesansbppld.ttf",55)
        self.turn=self.done_font.render("It's Player0 Turn",True,pygame.Color('goldenrod1'))
        self.end_text = self.done_font.render("",True,(255,255,255))
        #lock
        self.locked_image = pygame.image.load('dice/lock.png').convert_alpha()
        self.locked_image = pygame.transform.scale(self.locked_image, (30, 30))


    # def dice_move(self,Dice):
    #     position = DiceDice1.diceSpin[Dice1.SpinStatus]
    #     up=random.randint( 100,  400 )  
    #     right=random.randint( 100 ,  500 )
    #     speed = [ up/10,right/10]
    #     position = position.move(speed)
    #     for i in range(0,9):
    #         self.screen.blit(Dice,position)
    def reset_Dice(self):
        self.Dice1.reset=True
        self.Dice1.start=True
        self.Dice2.reset=True
        self.Dice2.start=True
        self.Dice3.reset=True
        self.Dice3.start=True
        self.Dice4.reset=True
        self.Dice4.start=True
        self.Dice5.reset=True
        self.Dice5.start=True

    def  run ( self ) :
        mainloop=True
        global listen_mainloop
        global Multiple_sign
        global player_state
        my_turn=True
        while mainloop:
            self.reset_time = 3
            self.getpoint=0
            self.player=-1
            self.cpu=False
            self.reset_Dice()
            while True:
                if back_game.q_out.qsize()!=0:
                    out=back_game.q_out.get()
                    if '~~end~~' == str(out):
                        self. endSound.play()
                        print('return')
                        listen_mainloop=False
                        mainloop=False
                    elif '*in*' == str(out):
                        #back_game.q_in.put(input('FNC:'))
                        fnc=''
                        if self.getpoint!=0:#從這裡  要開發點擊計分
                            fnc+='$'+str(self.getpoint)
                            print('Fnc:'+fnc)
                            back_game.q_in.put(fnc)
                            if Multiple_sign:
                                my_params={}
                                my_params["input"]=fnc
                                my_params["uid"]=user["id"]
                                response = requests.put(URL_INPUT, json = my_params)
                            continue
                        else:
                            fnc+='#'
                            if self.Dice1.reset==True:
                                fnc+='0'
                            if self.Dice2.reset==True:
                                fnc+='1'
                            if self.Dice3.reset==True:
                                fnc+='2'
                            if self.Dice4.reset==True:
                                fnc+='3'
                            if self.Dice5.reset==True:
                                fnc+='4'
                            print('Fnc:'+fnc)
                            back_game.q_in.put(fnc)
                            if Multiple_sign and player_state[str(user["id"])][0]==self.player:
                                try:
                                    my_params={}
                                    my_params["input"]=fnc
                                    my_params["uid"]=user["id"]
                                    response = requests.put(URL_INPUT, json = my_params)
                                except:
                                    print("send erro")
                            continue
                    else:
                        if out[0]=='-':
                            self.getpoint=0
                            pass
                        elif out[0]=='[' and out[1]=='[':
                            global grade
                            temp=findall(r"\d+",out)
                            temp_index=0
                            for player in range(true_player):
                                for index in range(14):
                                    grade[player][index]=temp[temp_index]
                                    temp_index+=1
                            if(int(grade[0][0])!=0):
                                self.label00_text=self.label_font.render(grade[0][0],True,(227, 38, 54))
                            if(int(grade[0][1])!=0):
                                self.label01_text=self.label_font.render(grade[0][1],True,(227, 38, 54))
                            if(int(grade[0][2])!=0):
                                self.label02_text=self.label_font.render(grade[0][2],True,(227, 38, 54))
                            if(int(grade[0][3])!=0):
                                self.label03_text=self.label_font.render(grade[0][3],True,(227, 38, 54))
                            if(int(grade[0][4])!=0):
                                self.label04_text=self.label_font.render(grade[0][4],True,(227, 38, 54))
                            if(int(grade[0][5])!=0):
                                self.label05_text=self.label_font.render(grade[0][5],True,(227, 38, 54))
                            if(int(grade[0][6])!=0):
                                self.label06_text=self.label_font.render(grade[0][6],True,(227, 38, 54))
                            if(int(grade[0][7])!=0):
                                self.label07_text=self.label_font.render(grade[0][7],True,(227, 38, 54))
                            if(int(grade[0][8])!=0):
                                self.label08_text=self.label_font.render(grade[0][8],True,(227, 38, 54))
                            if(int(grade[0][9])!=0):
                                self.label09_text=self.label_font.render(grade[0][9],True,(227, 38, 54))
                            if(int(grade[0][10])!=0):
                                self.label010_text=self.label_font.render(grade[0][10],True,(227, 38, 54))
                            if(int(grade[0][11])!=0):
                                self.label011_text=self.label_font.render(grade[0][11],True,(227, 38, 54))
                            if(int(grade[0][12])!=0):
                                self.label012_text=self.label_font.render(grade[0][12],True,(227, 38, 54))
                            if(int(grade[0][13])!=0):
                                self.label013_text=self.label_font.render(grade[0][13],True,(227, 38, 54))
                            if(int(grade[1][0])!=0):
                                self.label10_text=self.label_font.render(grade[1][0],True,(227, 38, 54))
                            if(int(grade[1][1])!=0):
                                self.label11_text=self.label_font.render(grade[1][1],True,(227, 38, 54))
                            if(int(grade[1][2])!=0):
                                self.label12_text=self.label_font.render(grade[1][2],True,(227, 38, 54))
                            if(int(grade[1][3])!=0):
                                self.label13_text=self.label_font.render(grade[1][3],True,(227, 38, 54))
                            if(int(grade[1][4])!=0):
                                self.label14_text=self.label_font.render(grade[1][4],True,(227, 38, 54))
                            if(int(grade[1][5])!=0):
                                self.label15_text=self.label_font.render(grade[1][5],True,(227, 38, 54))
                            if(int(grade[1][6])!=0):
                                self.label16_text=self.label_font.render(grade[1][6],True,(227, 38, 54))
                            if(int(grade[1][7])!=0):
                                self.label17_text=self.label_font.render(grade[1][7],True,(227, 38, 54))
                            if(int(grade[1][8])!=0):
                                self.label18_text=self.label_font.render(grade[1][8],True,(227, 38, 54))
                            if(int(grade[1][9])!=0):
                                self.label19_text=self.label_font.render(grade[1][9],True,(227, 38, 54))
                            if(int(grade[1][10])!=0):
                                self.label110_text=self.label_font.render(grade[1][10],True,(227, 38, 54))
                            if(int(grade[1][11])!=0):
                                self.label111_text=self.label_font.render(grade[1][11],True,(227, 38, 54))
                            if(int(grade[1][12])!=0):
                                self.label112_text=self.label_font.render(grade[1][12],True,(227, 38, 54))
                            if(int(grade[1][13])!=0):
                                self.label113_text=self.label_font.render(grade[1][13],True,(227, 38, 54))
                            if(int(grade[2][0])!=0):
                                self.label20_text=self.label_font.render(grade[2][0],True,(227, 38, 54))
                            if(int(grade[2][1])!=0):
                                self.label21_text=self.label_font.render(grade[2][1],True,(227, 38, 54))
                            if(int(grade[2][2])!=0):
                                self.label22_text=self.label_font.render(grade[2][2],True,(227, 38, 54))
                            if(int(grade[2][3])!=0):
                                self.label23_text=self.label_font.render(grade[2][3],True,(227, 38, 54))
                            if(int(grade[2][4])!=0):
                                self.label24_text=self.label_font.render(grade[2][4],True,(227, 38, 54))
                            if(int(grade[2][5])!=0):
                                self.label25_text=self.label_font.render(grade[2][5],True,(227, 38, 54))
                            if(int(grade[2][6])!=0):
                                self.label26_text=self.label_font.render(grade[2][6],True,(227, 38, 54))
                            if(int(grade[2][7])!=0):
                                self.label27_text=self.label_font.render(grade[2][7],True,(227, 38, 54))
                            if(int(grade[2][8])!=0):
                                self.label28_text=self.label_font.render(grade[2][8],True,(227, 38, 54))
                            if(int(grade[2][9])!=0):
                                self.label29_text=self.label_font.render(grade[2][9],True,(227, 38, 54))
                            if(int(grade[2][10])!=0):
                                self.label210_text=self.label_font.render(grade[2][10],True,(227, 38, 54))
                            if(int(grade[2][11])!=0):
                                self.label211_text=self.label_font.render(grade[2][11],True,(227, 38, 54))
                            if(int(grade[2][12])!=0):
                                self.label212_text=self.label_font.render(grade[2][12],True,(227, 38, 54))
                            if(int(grade[2][13])!=0):
                                self.label213_text=self.label_font.render(grade[2][13],True,(227, 38, 54))
                            if(int(grade[3][0])!=0):
                                self.label30_text=self.label_font.render(grade[3][0],True,(227, 38, 54))
                            if(int(grade[3][1])!=0):
                                self.label31_text=self.label_font.render(grade[3][1],True,(227, 38, 54))
                            if(int(grade[3][2])!=0):
                                self.label32_text=self.label_font.render(grade[3][2],True,(227, 38, 54))
                            if(int(grade[3][3])!=0):
                                self.label33_text=self.label_font.render(grade[3][3],True,(227, 38, 54))
                            if(int(grade[3][4])!=0):
                                self.label34_text=self.label_font.render(grade[3][4],True,(227, 38, 54))
                            if(int(grade[3][5])!=0):
                                self.label35_text=self.label_font.render(grade[3][5],True,(227, 38, 54))
                            if(int(grade[3][6])!=0):
                                self.label36_text=self.label_font.render(grade[3][6],True,(227, 38, 54))
                            if(int(grade[3][7])!=0):
                                self.label37_text=self.label_font.render(grade[3][7],True,(227, 38, 54))
                            if(int(grade[3][8])!=0):
                                self.label38_text=self.label_font.render(grade[3][8],True,(227, 38, 54))
                            if(int(grade[3][9])!=0):
                                self.label39_text=self.label_font.render(grade[3][9],True,(227, 38, 54))
                            if(int(grade[3][10])!=0):
                                self.label310_text=self.label_font.render(grade[3][10],True,(227, 38, 54))
                            if(int(grade[3][11])!=0):
                                self.label311_text=self.label_font.render(grade[3][11],True,(227, 38, 54))
                            if(int(grade[3][12])!=0):
                                self.label312_text=self.label_font.render(grade[3][12],True,(227, 38, 54))
                            if(int(grade[3][13])!=0):
                                self.label313_text=self.label_font.render(grade[3][13],True,(227, 38, 54))
                            temp0=0
                            temp1=0
                            temp2=0
                            temp3=0
                            for i in range(6):
                                temp0+=int(grade[0][i])
                                temp1+=int(grade[1][i])
                                temp2+=int(grade[2][i])
                                temp3+=int(grade[3][i])
                            self.Upsec0=self.label_font.render(str(temp0),True,(0,0,0))
                            self.Upsec1=self.label_font.render(str(temp1),True,(0,0,0))
                            self.Upsec2=self.label_font.render(str(temp2),True,(0,0,0))
                            self.Upsec3=self.label_font.render(str(temp3),True,(0,0,0))
                            temp4=0
                            temp5=0
                            temp6=0
                            temp7=0   
                            for i in range(6,14):
                                temp4+=int(grade[0][i])
                                temp5+=int(grade[1][i])
                                temp6+=int(grade[2][i])
                                temp7+=int(grade[3][i])
                            self.Lowsec0=self.label_font.render(str(temp4),True,(0,0,0))
                            self.Lowsec1=self.label_font.render(str(temp5),True,(0,0,0))
                            self.Lowsec2=self.label_font.render(str(temp6),True,(0,0,0))
                            self.Lowsec3=self.label_font.render(str(temp7),True,(0,0,0))
                            
                            self.Total0=self.label_font.render(str(temp0+temp4),True,(0,0,0))
                            self.Total1=self.label_font.render(str(temp1+temp5),True,(0,0,0))
                            self.Total2=self.label_font.render(str(temp2+temp6),True,(0,0,0))
                            self.Total3=self.label_font.render(str(temp3+temp7),True,(0,0,0))
                            self.score_sheet['player0'] = temp0+temp4
                            self.score_sheet['player1'] = temp1+temp5
                            self.score_sheet['player2'] = temp2+temp6
                            self.score_sheet['player3'] = temp3+temp7
                            self.score_sheet=OrderedDict(sorted(self.score_sheet.items(), key=lambda x: x[1]))
                            break
                        elif out[0]=='[':
                            self.Dice1.StopStatus = int(out[1])-1
                            self.Dice2.StopStatus = int(out[4])-1
                            self.Dice3.StopStatus = int(out[7])-1
                            self.Dice4.StopStatus = int(out[10])-1
                            self.Dice5.StopStatus = int(out[13])-1
                            self.reset_time-=1
                            self.time_text = self.start_font.render("time:"+str(self.reset_time),True,(255,255,255))
                            if self.cpu==True:
                                self.reset_Dice()
                                cpu_time=10
                        elif out.find('player turn(cpu)')!=-1: 
                            my_turn==False
                            self.turn=self.done_font.render("Not your Turn!!",True,pygame.Color('goldenrod1'))
                            self.cpu=True
                            continue
                        elif out.find('player turn')!=-1:
                            self.player=int(findall(r"\d+",out)[0])
                            print(self.player)
                            if Multiple_sign and player_state[str(user["id"])][0]!=self.player:
                                print("not my turn")
                                my_turn=False
                                self.cpu=True
                            else:
                                if Multiple_sign:
                                    if player_state[str(user["id"])][0]==self.player:
                                        my_turn=True
                                self.cpu=False
                            self.turn=self.done_font.render("It's Player"+str(self.player+1)+" Turn",True,pygame.Color('goldenrod1'))
                            if not my_turn:
                                self.turn=self.done_font.render("Not your Turn!!",True,pygame.Color('goldenrod1'))
                            # for index in range(6):
                            #     locals()['self.label'+str(self.player)+str(index)+'_rect'] = locals()['self.label'+str(self.player)+str(index)+'_text'].get_rect(topleft = (1122+self.player*45, 37+25*index))
                            # for index in range(7):
                            #     locals()['self.label'+str(self.player)+str(index+7)+'_rect'] = locals()['self.label'+str(self.player)+str(index+7)+'_text'].get_rect(topleft = (1122+self.player*45, 280+25*index))
                            if self.player==0:
                                self.label1_rect = self.label01_text.get_rect(topleft = (1122+self.player*45, 37+25*0))
                                self.label2_rect = self.label02_text.get_rect(topleft = (1122+self.player*45, 37+25*1))
                                self.label3_rect = self.label03_text.get_rect(topleft = (1122+self.player*45, 37+25*2))
                                self.label4_rect = self.label04_text.get_rect(topleft = (1122+self.player*45, 37+25*3))
                                self.label5_rect = self.label05_text.get_rect(topleft = (1122+self.player*45, 37+25*4))
                                self.label6_rect = self.label06_text.get_rect(topleft = (1122+self.player*45, 37+25*5))
                                self.label7_rect = self.label07_text.get_rect(topleft = (1122+self.player*45, 280+25*0))
                                self.label8_rect = self.label08_text.get_rect(topleft = (1122+self.player*45, 280+25*1))
                                self.label9_rect = self.label09_text.get_rect(topleft = (1122+self.player*45, 280+25*2))
                                self.label10_rect = self.label010_text.get_rect(topleft = (1122+self.player*45, 280+25*3))
                                self.label11_rect = self.label011_text.get_rect(topleft = (1122+self.player*45, 280+25*4))
                                self.label12_rect = self.label012_text.get_rect(topleft = (1122+self.player*45, 280+25*5))
                                self.label13_rect = self.label013_text.get_rect(topleft = (1122+self.player*45, 280+25*6))
                            elif self.player==1:
                                self.label1_rect = self.label11_text.get_rect(topleft = (1122+self.player*45, 37+25*0))
                                self.label2_rect = self.label12_text.get_rect(topleft = (1122+self.player*45, 37+25*1))
                                self.label3_rect = self.label13_text.get_rect(topleft = (1122+self.player*45, 37+25*2))
                                self.label4_rect = self.label14_text.get_rect(topleft = (1122+self.player*45, 37+25*3))
                                self.label5_rect = self.label15_text.get_rect(topleft = (1122+self.player*45, 37+25*4))
                                self.label6_rect = self.label16_text.get_rect(topleft = (1122+self.player*45, 37+25*5))
                                self.label7_rect = self.label17_text.get_rect(topleft = (1122+self.player*45, 280+25*0))
                                self.label8_rect = self.label18_text.get_rect(topleft = (1122+self.player*45, 280+25*1))
                                self.label9_rect = self.label19_text.get_rect(topleft = (1122+self.player*45, 280+25*2))
                                self.label10_rect = self.label110_text.get_rect(topleft = (1122+self.player*45, 280+25*3))
                                self.label11_rect = self.label111_text.get_rect(topleft = (1122+self.player*45, 280+25*4))
                                self.label12_rect = self.label112_text.get_rect(topleft = (1122+self.player*45, 280+25*5))
                                self.label13_rect = self.label113_text.get_rect(topleft = (1122+self.player*45, 280+25*6))
                            elif self.player==2:  
                                self.label1_rect = self.label21_text.get_rect(topleft = (1122+self.player*45, 37+25*0))
                                self.label2_rect = self.label22_text.get_rect(topleft = (1122+self.player*45, 37+25*1))
                                self.label3_rect = self.label23_text.get_rect(topleft = (1122+self.player*45, 37+25*2))
                                self.label4_rect = self.label24_text.get_rect(topleft = (1122+self.player*45, 37+25*3))
                                self.label5_rect = self.label25_text.get_rect(topleft = (1122+self.player*45, 37+25*4))
                                self.label6_rect = self.label26_text.get_rect(topleft = (1122+self.player*45, 37+25*5))
                                self.label7_rect = self.label27_text.get_rect(topleft = (1122+self.player*45, 280+25*0))
                                self.label8_rect = self.label28_text.get_rect(topleft = (1122+self.player*45, 280+25*1))
                                self.label9_rect = self.label29_text.get_rect(topleft = (1122+self.player*45, 280+25*2))
                                self.label10_rect = self.label210_text.get_rect(topleft = (1122+self.player*45, 280+25*3))
                                self.label11_rect = self.label211_text.get_rect(topleft = (1122+self.player*45, 280+25*4))
                                self.label12_rect = self.label212_text.get_rect(topleft = (1122+self.player*45, 280+25*5))
                                self.label13_rect = self.label213_text.get_rect(topleft = (1122+self.player*45, 280+25*6))
                            elif self.player==3:
                                self.label1_rect = self.label31_text.get_rect(topleft = (1122+self.player*45, 37+25*0))
                                self.label2_rect = self.label32_text.get_rect(topleft = (1122+self.player*45, 37+25*1))
                                self.label3_rect = self.label33_text.get_rect(topleft = (1122+self.player*45, 37+25*2))
                                self.label4_rect = self.label34_text.get_rect(topleft = (1122+self.player*45, 37+25*3))
                                self.label5_rect = self.label35_text.get_rect(topleft = (1122+self.player*45, 37+25*4))
                                self.label6_rect = self.label36_text.get_rect(topleft = (1122+self.player*45, 37+25*5))
                                self.label7_rect = self.label37_text.get_rect(topleft = (1122+self.player*45, 280+25*0))
                                self.label8_rect = self.label38_text.get_rect(topleft = (1122+self.player*45, 280+25*1))
                                self.label9_rect = self.label39_text.get_rect(topleft = (1122+self.player*45, 280+25*2))
                                self.label10_rect = self.label310_text.get_rect(topleft = (1122+self.player*45, 280+25*3))
                                self.label11_rect = self.label311_text.get_rect(topleft = (1122+self.player*45, 280+25*4))
                                self.label12_rect = self.label312_text.get_rect(topleft = (1122+self.player*45, 280+25*5))
                                self.label13_rect = self.label313_text.get_rect(topleft = (1122+self.player*45, 280+25*6))
                            continue
                        else:
                            continue
                elif not my_turn:
                    pass
                else:
                    time.sleep(0.1)
                    continue
                while  True: 
                    self.getpoint=0
                    self .clock.tick( 18 )
                    self.screen.blit(self.background_image,[0,0])
                    self.screen.blit(self.grade_image,[900,0])
                    self.screen.blit(self.time_text,(410,400))
                    self.screen.blit(self.start_image, (325, 400))
                    self.screen.blit(self.label01_text, (1122+0*45, 37+25*0))
                    self.screen.blit(self.label02_text, (1122+0*45, 37+25*1))
                    self.screen.blit(self.label03_text, (1122+0*45, 37+25*2))
                    self.screen.blit(self.label04_text, (1122+0*45, 37+25*3))
                    self.screen.blit(self.label05_text, (1122+0*45, 37+25*4))
                    self.screen.blit(self.label06_text, (1122+0*45, 37+25*5))
                    self.screen.blit(self.label07_text, (1122+0*45, 280+25*0))
                    self.screen.blit(self.label08_text, (1122+0*45, 280+25*1))
                    self.screen.blit(self.label09_text, (1122+0*45, 280+25*2))
                    self.screen.blit(self.label010_text, (1122+0*45, 280+25*3))
                    self.screen.blit(self.label011_text, (1122+0*45, 280+25*4))
                    self.screen.blit(self.label012_text, (1122+0*45, 280+25*5))
                    self.screen.blit(self.label013_text, (1122+0*45, 280+25*6))
                    self.screen.blit(self.Lowsec0, (1122+0*45, 280+25*9))
                    self.screen.blit(self.Upsec0, (1122+0*45, 280+25*10))
                    self.screen.blit(self.Total0, (1122+0*45, 280+25*11))
                    self.screen.blit(self.label11_text, (1122+1*45, 37+25*0))
                    self.screen.blit(self.label12_text, (1122+1*45, 37+25*1))
                    self.screen.blit(self.label13_text, (1122+1*45, 37+25*2))
                    self.screen.blit(self.label14_text, (1122+1*45, 37+25*3))
                    self.screen.blit(self.label15_text, (1122+1*45, 37+25*4))
                    self.screen.blit(self.label16_text, (1122+1*45, 37+25*5))
                    self.screen.blit(self.label17_text, (1122+1*45, 280+25*0))
                    self.screen.blit(self.label18_text, (1122+1*45, 280+25*1))
                    self.screen.blit(self.label19_text, (1122+1*45, 280+25*2))
                    self.screen.blit(self.label110_text, (1122+1*45, 280+25*3))
                    self.screen.blit(self.label111_text, (1122+1*45, 280+25*4))
                    self.screen.blit(self.label112_text, (1122+1*45, 280+25*5))
                    self.screen.blit(self.label113_text, (1122+1*45, 280+25*6))
                    self.screen.blit(self.Lowsec1, (1122+1*45, 280+25*9))
                    self.screen.blit(self.Upsec1, (1122+1*45, 280+25*10))
                    self.screen.blit(self.Total1, (1122+1*45, 280+25*11))
                    self.screen.blit(self.label21_text, (1122+2*45, 37+25*0))
                    self.screen.blit(self.label22_text, (1122+2*45, 37+25*1))
                    self.screen.blit(self.label23_text, (1122+2*45, 37+25*2))
                    self.screen.blit(self.label24_text, (1122+2*45, 37+25*3))
                    self.screen.blit(self.label25_text, (1122+2*45, 37+25*4))
                    self.screen.blit(self.label26_text, (1122+2*45, 37+25*5))
                    self.screen.blit(self.label27_text, (1122+2*45, 280+25*0))
                    self.screen.blit(self.label28_text, (1122+2*45, 280+25*1))
                    self.screen.blit(self.label29_text, (1122+2*45, 280+25*2))
                    self.screen.blit(self.label210_text, (1122+2*45, 280+25*3))
                    self.screen.blit(self.label211_text, (1122+2*45, 280+25*4))
                    self.screen.blit(self.label212_text, (1122+2*45, 280+25*5))
                    self.screen.blit(self.label213_text, (1122+2*45, 280+25*6))
                    self.screen.blit(self.Lowsec2, (1122+2*45, 280+25*9))
                    self.screen.blit(self.Upsec2, (1122+2*45, 280+25*10))
                    self.screen.blit(self.Total2, (1122+2*45, 280+25*11))
                    self.screen.blit(self.label31_text, (1122+3*45, 37+25*0))
                    self.screen.blit(self.label32_text, (1122+3*45, 37+25*1))
                    self.screen.blit(self.label33_text, (1122+3*45, 37+25*2))
                    self.screen.blit(self.label34_text, (1122+3*45, 37+25*3))
                    self.screen.blit(self.label35_text, (1122+3*45, 37+25*4))
                    self.screen.blit(self.label36_text, (1122+3*45, 37+25*5))
                    self.screen.blit(self.label37_text, (1122+3*45, 280+25*0))
                    self.screen.blit(self.label38_text, (1122+3*45, 280+25*1))
                    self.screen.blit(self.label39_text, (1122+3*45, 280+25*2))
                    self.screen.blit(self.label310_text, (1122+3*45, 280+25*3))
                    self.screen.blit(self.label311_text, (1122+3*45, 280+25*4))
                    self.screen.blit(self.label312_text, (1122+3*45, 280+25*5))
                    self.screen.blit(self.label313_text, (1122+3*45, 280+25*6))
                    self.screen.blit(self.Lowsec3, (1122+3*45, 280+25*9))
                    self.screen.blit(self.Upsec3, (1122+3*45, 280+25*10))
                    self.screen.blit(self.Total3, (1122+3*45, 280+25*11))
                    self.screen.blit(self.turn,[300,0])
                    button_clicked=False
                    for  event  in  pygame.event.get():
                        if  event.type == pygame. QUIT:
                            if Multiple_sign :
                                listen_mainloop=False
                                my_params={}
                                my_params["input"]="@@"+str(player_state[str(user["id"])][0]+1)
                                my_params["uid"]=user["id"]
                                response = requests.put(URL_INPUT, json = my_params)
                                if my_turn:
                                    if Multiple_sign:
                                        my_params={}
                                        my_params["input"]='$12'
                                        my_params["uid"]=user["id"]
                                        response = requests.put(URL_INPUT, json = my_params)
                            sys.exit()
                        if  mainloop==False and  event.type == pygame.MOUSEBUTTONDOWN:
                            self. touchSound.play()
                            print("im quit")
                            if Multiple_sign:
                                for i in range(4):
                                    if str(player_state[str(user["id"])][0])==list(self.score_sheet.keys())[i][6]:
                                        if i==3:
                                            self.change_money(600)
                                            user["dollar"]+=600
                                            print("changemoney600")
                                        elif i==2:
                                            self.change_money(300)
                                            user["dollar"]+=300
                                            print("changemoney300")
                                        elif i==1:
                                            self.change_money(-300)
                                            user["dollar"]-=300
                                            print("changemoney-300")
                                        elif i==0:
                                            self.change_money(-600)
                                            user["dollar"]-=600
                                            print("changemoney-600")
                                        break
                                    print("money round")
                                if player_state[str(user["id"])][0]==0:
                                    try:
                                        #register
                                        my_params={}
                                        my_params["input"]='end'
                                        my_params["uid"]=user["id"]
                                        response = requests.put(URL_INPUT, json = my_params)
                                        print(response.status_code)
                                        print(response.headers)
                                        print(response.text)
                                    except:
                                        MessageBox(0,"Server is crash", "Warn",MB_OK)
                            elif Local_sign==True:
                                self.change_money(300)
                                user["dollar"]+=300
                                print("changemoney300")
                            player_state={}
                            pygame.quit()
                            pygame.display.quit()
                            return 0
                        elif self.cpu==False and my_turn==True:
                            if  event.type == pygame.MOUSEBUTTONDOWN: 
                                self. touchSound.play()
                                x,y=event.pos
                                button_rect = self.start_image.get_rect(topleft = (325, 400)) #dice locked_image
                                if self.Dice1.diceRect.collidepoint(x, y):
                                    if self.Dice1.reset==False:
                                        self.Dice1.reset=True
                                    else: 
                                        self.Dice1.reset=False
                                elif self.Dice2.diceRect .collidepoint(x, y):
                                    if self.Dice2.reset==False:
                                        self.Dice2.reset=True
                                    else: 
                                        self.Dice2.reset=False
                                elif self.Dice3.diceRect.collidepoint(x, y):
                                    if self.Dice3.reset==False:
                                        self.Dice3.reset=True
                                    else: 
                                        self.Dice3.reset=False
                                elif self.Dice4.diceRect .collidepoint(x, y):
                                    if self.Dice4.reset==False:
                                        self.Dice4.reset=True
                                    else: 
                                        self.Dice4.reset=False
                                elif self.Dice5.diceRect .collidepoint(x, y):
                                    if self.Dice5.reset==False:
                                        self.Dice5.reset=True
                                    else: 
                                        self.Dice5.reset=False
                                #grade chose
                                if self.label1_rect.collidepoint(x, y):
                                    print("1")
                                    self.getpoint=1
                                    break
                                elif self.label2_rect.collidepoint(x, y):
                                    print("2")
                                    self.getpoint=2
                                    break
                                elif self.label3_rect.collidepoint(x, y):
                                    print("3")
                                    self.getpoint=3
                                    break
                                elif self.label4_rect.collidepoint(x, y):
                                    print("4")
                                    self.getpoint=4
                                    break
                                elif self.label5_rect.collidepoint(x, y):
                                    print("5")
                                    self.getpoint=5
                                    break
                                elif self.label6_rect.collidepoint(x, y):
                                    print("6")
                                    self.getpoint=6
                                    break
                                elif self.label7_rect.collidepoint(x, y):
                                    print("7")
                                    self.getpoint=7
                                    break
                                elif self.label8_rect.collidepoint(x, y):
                                    print("8")
                                    self.getpoint=8
                                    break
                                elif self.label9_rect.collidepoint(x, y):
                                    print("9")
                                    self.getpoint=9
                                    break
                                elif self.label10_rect.collidepoint(x, y):
                                    print("10")
                                    self.getpoint=10
                                    break
                                elif self.label11_rect.collidepoint(x, y):
                                    print("11")
                                    self.getpoint=11
                                    break
                                elif self.label12_rect.collidepoint(x, y):
                                    print("12")
                                    self.getpoint=12
                                    break
                                elif self.label13_rect.collidepoint(x, y):
                                    print("13")
                                    self.getpoint=13
                                    break
                                #reroll
                                if button_rect.collidepoint(x, y) and self.reset_time>0:
                                    if(self.Dice1.reset== True):
                                        self.Dice1.start=True
                                    if(self.Dice2.reset== True):
                                        self.Dice2.start=True
                                    if(self.Dice3.reset== True):
                                        self.Dice3.start=True
                                    if(self.Dice4.reset== True):
                                        self.Dice4.start=True
                                    if(self.Dice5.reset== True):
                                        self.Dice5.start=True
                                    self.time_text = self.start_font.render("time:"+str(self.reset_time),True,(255,255,255))
                                    button_clicked=True
                                    break
                                #end
                        else:
                            if  event.type == pygame.MOUSEBUTTONDOWN: 
                                self. touchSound.play()
                                print("@")
                    if button_clicked:
                        break
                    if  self.Dice1.start: 
                        self.screen.blit(self.Dice1.diceSpin[self.Dice1.SpinStatus],self.Dice1.diceRect)
                        self.Dice1.roll()
                    else:
                        self.screen.blit(self.Dice1.diceStop[self.Dice1.StopStatus],self.Dice1.diceRect)
                        if self.Dice1.reset == False:
                            self.screen.blit(self.locked_image, (380, 270))
                    if  self.Dice2.start: 
                        self.screen.blit(self.Dice2.diceSpin[self.Dice2.SpinStatus],self.Dice2.diceRect)
                        self.Dice2.roll()
                    else:
                        self.screen.blit(self.Dice2.diceStop[self.Dice2.StopStatus],self.Dice2.diceRect)
                        if self.Dice2.reset == False:
                            self.screen.blit(self.locked_image, (480, 270))
                    if  self.Dice3.start: 
                        self.screen.blit(self.Dice3.diceSpin[self.Dice3.SpinStatus],self.Dice3.diceRect)
                        self.Dice3.roll()
                    else:
                        self.screen.blit(self.Dice3.diceStop[self.Dice3.StopStatus],self.Dice3.diceRect)
                        if self.Dice3.reset == False:
                            self.screen.blit(self.locked_image, (330, 170))
                    if  self.Dice4.start: 
                        self.screen.blit(self.Dice4.diceSpin[self.Dice4.SpinStatus],self.Dice4.diceRect)
                        self.Dice4.roll()
                    else:
                        self.screen.blit(self.Dice4.diceStop[self.Dice4.StopStatus],self.Dice4.diceRect)
                        if self.Dice4.reset == False:
                            self.screen.blit(self.locked_image, (430, 170))
                    if  self.Dice5.start: 
                        self.screen.blit(self.Dice5.diceSpin[self.Dice5.SpinStatus],self.Dice5.diceRect)
                        self.Dice5.roll()
                    else:
                        self.screen.blit(self.Dice5.diceStop[self.Dice5.StopStatus],self.Dice5.diceRect)
                        if self.Dice5.reset == False:
                            self.screen.blit(self.locked_image, (530, 170))
                    if  mainloop == False:
                        if Multiple_sign:
                            self.screen.blit(self.end_image, (0, 20))
                            self.end_text1 =self.done_font.render("1 st is "+list(self.score_sheet.keys())[3]+" get:"+str(list(self.score_sheet.values())[3])+" point. earn$600!",True,(255,255,255))
                            self.end_text2 =self.done_font.render("2 nd is "+list(self.score_sheet.keys())[2]+" get:"+str(list(self.score_sheet.values())[2])+" point. earn$300!",True,pygame.Color('chartreuse1'))
                            self.end_text3 =self.done_font.render("3 rd is "+list(self.score_sheet.keys())[1]+" get:"+str(list(self.score_sheet.values())[1])+" point. lose$300!",True,pygame.Color('cyan4'))
                            self.end_text4 =self.done_font.render("4 th is "+list(self.score_sheet.keys())[0]+" get:"+str(list(self.score_sheet.values())[0])+" point. lose$600!",True,pygame.Color('firebrick3'))
                            self.screen.blit(self.end_text1, ((125,self.size[1]/4)))
                            self.screen.blit(self.end_text2, ((125,self.size[1]/4+60)))
                            self.screen.blit(self.end_text3, ((125,self.size[1]/4+120)))
                            self.screen.blit(self.end_text4, ((125,self.size[1]/4+180)))
                        elif Local_sign:
                            self.screen.blit(self.end_image, (0, 20))
                            self.end_text1 =self.done_font.render("1 st is "+list(self.score_sheet.keys())[3]+" get:"+str(list(self.score_sheet.values())[3])+" point.",True,(255,255,255))
                            self.end_text2 =self.done_font.render("2 nd is "+list(self.score_sheet.keys())[2]+" get:"+str(list(self.score_sheet.values())[2])+" point.",True,pygame.Color('chartreuse1'))
                            self.end_text3 =self.done_font.render("3 rd is "+list(self.score_sheet.keys())[1]+" get:"+str(list(self.score_sheet.values())[1])+" point.",True,pygame.Color('cyan4'))
                            self.end_text4 =self.done_font.render("4 th is "+list(self.score_sheet.keys())[0]+" get:"+str(list(self.score_sheet.values())[0])+" point.",True,pygame.Color('firebrick3'))
                            self.screen.blit(self.end_text1, ((125,self.size[1]/4)))
                            self.screen.blit(self.end_text2, ((125,self.size[1]/4+60)))
                            self.screen.blit(self.end_text3, ((125,self.size[1]/4+120)))
                            self.screen.blit(self.end_text4, ((125,self.size[1]/4+180)))
                    if (self.cpu==True ) :
                        if self.Dice1.start==True or self.Dice2.start==True or self.Dice3.start==True or self.Dice4.start==True or self.Dice5.start==True:
                            pass
                        else:
                            if cpu_time>0:
                                cpu_time-=1
                                pass
                            else:
                                break
                    if  (self.getpoint!=0):#這裡壞的
                        break
                    pygame.display.update()
    def change_money(self,money):
        try:

            new_dict = {}
            new_dict["uid"] = user["id"]
            new_dict["money"] = money
            response = requests.put(URL_ACCOUNT, json=new_dict)
            print(response.status_code)
            print(response.headers)
            print(response.text)
            MessageBox(0,"You "+str(money)+" dollars","Yahtzee",MB_OK)
        except:
            MessageBox(0,"Server is crash", "Warn",MB_OK)

class Multiple_temp(threading.Thread):
    def __init__(self):
        super(Multiple_temp,self).__init__()
        self.q_in = Queue()
        self.q_out = Queue()
        self.font=0
    def run(self):
        global listen_mainloop
        global player_state #{uid:[playid,room]}
        listen_mainloop=True
        while listen_mainloop:
            time.sleep(0.5)
            if listen_mainloop:
                try:
                    my_params = {}
                    my_params["uid"] = user["id"]
                    my_params["font"] = self.font
                    print(URL_LOAD)
                    response = requests.get(URL_LOAD, json = my_params)
                    print(response.status_code)
                    print(response.headers)
                    queue = response.json()				# response.json() is json records
                    for item in queue:
                        self.q_out.put(item)
                        self.font+=1
                except:
                    MessageBox(0,"Server is crash", "Warn",MB_OK)
                #recv server Queue
            
            
if __name__ ==  '__main__' : 
    global grade
    global user
    global cpu_player
    global Local_sign
    global Multiple_sign
    global back_game
    user={}
    true_player=4    
    
    while(True):
        if user=={}:
            login_lobby()
        grade = [[0 for _ in range(14)] for _ in range(true_player)]
        waiting_lobby()
        print(cpu_player)
        if Local_sign:
            back_game=main.main_dice(str(true_player),cpu_player)
        if Multiple_sign:
            back_game=Multiple_temp()
        back_game.setDaemon(True)
        back_game.start()
        Game().run()
            
        

    