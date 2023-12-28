import pygame
import random
import math
import sys

#khởi tạo môi trường pygame
pygame.init()
#khởi tạo môi trường âm thanh
pygame.mixer.init()
#Tạo đối tượng kiểm soát tốc độkhung hình
clock = pygame.time.Clock()
#FPS
game_speed = 60
#Tạo màu
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
color_list=[white,yellow,green,blue,red]

#Tạo hướng di chuyển
LEFT=270.0
RIGHT=90.0
UP=0.0
DOWN=180.0
LEFT_UP=315.0
LEFT_DOWN=225.0
RIGHT_UP=45.0
RIGHT_DOWN=135.0
#góc quay
angle=0

#kichthuoc
Small=7
Big=20
#Load background
background=pygame.image.load(r"image\background.jpg")
bg_width,bg_height=background.get_size()
background=pygame.transform.scale(background,(((bg_width-9)//10*10),((bg_height-9)//10*10)))
bg_width,bg_height=background.get_size()
dis_width = bg_width*3
dis_height = bg_height*3
#load background menu
bg_menu=pygame.image.load(r"image\backgroundmenu.jpg")
bg_menu=pygame.transform.scale(bg_menu,(dis_width,dis_height))
#background lost
bg_lost=pygame.transform.scale(bg_menu,(200,270))

#tên trò chơi
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Game Rắn Săn Mồi')

#icon game
icon_game=pygame.image.load(r"image\icon.jpg")
pygame.display.set_icon(icon_game)

# #load đầu rắn
head_img_goc=pygame.image.load(r"image\dauran.png")
head_img_goc=pygame.transform.scale(head_img_goc,(45,45))
head_img=head_img_goc
#load bom
bom_img=pygame.image.load(r"image\bom.png")
bom_img=pygame.transform.scale(bom_img,(40,40))

#font
font_style = pygame.font.Font("font\\aachenb.ttf", 25)

# sound
background_sound=pygame.mixer.Sound(r"sound\background_sound.mp3")
sound=pygame.mixer.Sound(r"sound\eat.mp3")
sound_belch=pygame.mixer.Sound(r"sound\eat_belch.mp3")
lost_sound=pygame.mixer.Sound(r"sound\lost_sound.mp3")

#class snake
class Snake:
    def __init__(self,block,speed):
        self.snake_block=block
        self.snake_list=[]
        self.Length_of_snake=10
        self.x_change=0
        self.y_change=0
        self.speed=speed
    
    #hàm tạo vị trí bắt đầu
    def start(self,direction):
        self.direction=direction
        if direction=="RIGHT":
            self.x = ((dis_width/2)-9)//10*10+dis_width/2
            self.y = ((dis_height/2)-9)//10*10
    #cặp nhật tọa độ thay đổi
    def change(self):
        self.y += (self.y_change )
        self.x += (self.x_change )
#hàm vẽ rắn
def our_snake(snake_block, snake_list,current_direction):
    global head_img
    global angle
    head_rect=head_img.get_rect(center=(snake_list[len(snake_list)-2]))
    angle +=(current_direction[0]-current_direction[1])
    angle=angle%360
    rotated_head  = pygame.transform.rotate( head_img , angle)
    rotated_rect = rotated_head.get_rect(center=head_rect.center)
    dis.blit(rotated_head,(rotated_rect.topleft))
    #vẽ thân rắn
    for x in snake_list[:-5]:
        pygame.draw.circle(dis, yellow,( x[0], x[1]), snake_block,0)

#Hàm hiển thị chữ
def message(msg, color,Coordinates):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [Coordinates[0], Coordinates[1]])
    
#class food
class food:
    def __init__(self,big=False):
        if big:
            self.size=Big
            self.color=random.choice(color_list)
            
        else:
            self.size=Small
            self.color=random.choice(color_list)
        self.x=round(random.randrange(self.size, dis_width - self.size) )
        self.y=round(random.randrange(self.size, dis_height - self.size) )
            
#class bom
class bom:
    def __init__(self):
        self.size=10
        self.x=round(random.randrange(self.size, dis_width - self.size) )
        self.y=round(random.randrange(self.size, dis_height - self.size) )
            
#hàm main
def gameLoop(sl_bom):
    global head_img
    global angle
    lost_sound_play=False
    head_img=head_img_goc
    angle=0
    background_sound.play(-1)
    current_direction=[-1.0,-1.0]
    Score =0
    Score_big_food=0
    Speed_Score=0
    game_over = False
    game_close = False
    Snake1=Snake(10,4)
    Snake1.start("RIGHT")
    current_direction=[LEFT,LEFT]

    List_Food=[]
    List_Bom=[]
    
    #vòng lặp chính
    while not game_over:
        #sự kiện game over
        while game_close == True:
            if not lost_sound_play:
                lost_sound.play()
                lost_sound_play=True
            
            background_sound.stop()
            lost=lost_menu()
            if lost==1:
                gameLoop(sl_bom)
                game_over=True
                game_close=False
                return
            elif lost==2:
                game_over = True
                game_close = False
                return
            
        #sự kiện thoát
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                sys.exit()
        #bắt tất cả các sự kiện trên bàn phím
        keys = pygame.key.get_pressed()
        
        #tăng tốc
        if keys[pygame.K_k]and Snake1.Length_of_snake>1 and Score>1:
            game_speed=60
            if Speed_Score==25:
                Score-=1
                Speed_Score=0
                del Snake1.snake_list[0]
                Snake1.Length_of_snake-=1
            else:
                Speed_Score+=1
        else:
            game_speed=30

        #Di chuyển
        if ((keys[pygame.K_a] and keys[pygame.K_w]))and current_direction[1]!=RIGHT_DOWN :
            Snake1.x_change = -Snake1.speed/math.sqrt(2)
            Snake1.y_change = -Snake1.speed/math.sqrt(2)
            current_direction[0]=current_direction[1]
            current_direction[1]=LEFT_UP
        elif ((keys[pygame.K_a] and keys[pygame.K_s])and current_direction[1]!=RIGHT_UP):
            Snake1.x_change = -Snake1.speed/math.sqrt(2)
            Snake1.y_change = +Snake1.speed/math.sqrt(2)
            current_direction[0]=current_direction[1]
            current_direction[1]=LEFT_DOWN
        elif ((keys[pygame.K_d] and keys[pygame.K_w]))and current_direction[1]!=LEFT_DOWN:
            Snake1.x_change = +Snake1.speed/math.sqrt(2)
            Snake1.y_change = -Snake1.speed/math.sqrt(2)
            current_direction[0]=current_direction[1]
            current_direction[1]=RIGHT_UP
        elif ((keys[pygame.K_d] and keys[pygame.K_s])and current_direction[1]!= LEFT_UP):
            Snake1.x_change = +Snake1.speed/math.sqrt(2)
            Snake1.y_change = +Snake1.speed/math.sqrt(2)
            current_direction[0]=current_direction[1]
            current_direction[1]=RIGHT_DOWN
        
        elif ( keys[pygame.K_w])and current_direction[1]!=DOWN:
            Snake1.y_change = -Snake1.speed
            Snake1.x_change = 0
            current_direction[0]=current_direction[1]
            current_direction[1]=UP
        elif ( keys[pygame.K_d]and current_direction[1]!=LEFT):
            Snake1.x_change = Snake1.speed
            Snake1.y_change = 0
            current_direction[0]=current_direction[1]
            current_direction[1]=RIGHT
        elif( keys[pygame.K_s])and current_direction[1]!=UP:
            Snake1.y_change = Snake1.speed
            Snake1.x_change = 0
            current_direction[0]=current_direction[1]
            current_direction[1]=DOWN
        elif (keys[pygame.K_a])and current_direction[1]!=RIGHT:
            Snake1.x_change = -Snake1.speed
            Snake1.y_change = 0
            current_direction[0]=current_direction[1]
            current_direction[1]=LEFT
        
        else:
            current_direction[0]=current_direction[1]
        
        #Va chạm vách

        if Snake1.x >= dis_width or Snake1.x < 0 or Snake1.y >= dis_height or Snake1.y < 0:
            game_close = True
            
        #cập nhật tọa độ thay đổi
        Snake1.change()
        #vẽ background
        dis.blit(background,(0,0))
        dis.blit(background,(bg_width,0))
        dis.blit(background,(bg_width*2,0))
        dis.blit(background,(0,bg_height))
        dis.blit(background,(bg_width,bg_height))
        dis.blit(background,(bg_width*2,bg_height))
        dis.blit(background,(0,bg_height*2))
        dis.blit(background,(bg_width,bg_height*2))
        dis.blit(background,(bg_width*2,bg_height*2))

        #tạo thức ăn
        Food=food(False)
        if Score_big_food>=10:
            bigFood=food(True)
            List_Food.append(bigFood)
            Score_big_food=0

        if len(List_Food)<100:
            List_Food.append(Food)
        # vẽ thức ăn
        for f in List_Food:
            pygame.draw.circle(dis, f.color, (f.x, f.y),f.size)
        #tạo bom
        
        if len(List_Bom)<sl_bom:
            Bom=bom()
            if ((Bom.x<Snake1.x-2*Bom.size or Bom.x>Snake1.x+2*Bom.size) and (Bom.y<Snake1.y-2*Bom.size or Bom.y>Snake1.y+2*Bom.size)):
                List_Bom.append(Bom)
        #vẽ bom
        for b in List_Bom:
            dis.blit(bom_img,(b.x-bom_img.get_width()/2,b.y-bom_img.get_height()/2))
            
        #tạo list tọa độ rắn
        snake_Head = []
        snake_Head.append(Snake1.x)
        snake_Head.append(Snake1.y)
        Snake1.snake_list.append(snake_Head)
        
        if len(Snake1.snake_list) > Snake1.Length_of_snake:
            del Snake1.snake_list[0]

         #cắn trúng đuôi
        for x in Snake1.snake_list[:-10]:
            if x == snake_Head:
                game_close = True
                
        #vẽ rắn
        our_snake(Snake1.snake_block, Snake1.snake_list,current_direction)
        #Ăn
        for f in List_Food:
            distance=math.sqrt((Snake1.x-f.x)**2+(Snake1.y-f.y)**2)
            if distance<((Snake1.snake_block)*(1)+f.size/4):
                List_Food.remove(f)
                
                if f.size==Small:
                    sound.play()
                    Score+=1
                    Score_big_food+=1
                    Snake1.Length_of_snake += 1
                else:
                    sound_belch.play()
                    Score+=10
                    Snake1.Length_of_snake += 5
        #Ăn bom
        for b in List_Bom:
            distance=math.sqrt((Snake1.x-b.x)**2+(Snake1.y-b.y)**2)
            if distance<((Snake1.snake_block)*(0.5)+b.size):
                game_close=True
                lost_sound.play()

        #hiển thị điểm số
        message(f"Điểm: {Score}", red,[0,0])
        #cập nhật lại màn hình
        pygame.display.update()
        #kiểm soát tốc độ khung hình
        clock.tick(game_speed)

    #lost menu
def lost_menu():
    #tạo chữ
    thongbao=font_style.render("BẠN ĐÃ THUA!",True,white)
    play_again=font_style.render("Chơi Lại",True,black)
    back_menu=font_style.render("Trở Về Menu",True,black)
    
    #lấy khối bao quanh
    thongbao_rect=thongbao.get_rect(center=(dis_width//2,130))
    play_again_rect=play_again.get_rect(center=(dis_width//2,190))
    back_menu_rect=back_menu.get_rect(center=(dis_width//2,250))
   
   #vòng lập chính
    running=True
    while running==True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running=False
                sys.exit()
                
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button==1:
                cursor_position = pygame.mouse.get_pos()
                cursor_rect = pygame.Rect(cursor_position[0], cursor_position[1], 1, 1)

                if cursor_rect.colliderect(play_again_rect):
                    return 1

                elif cursor_rect.colliderect(back_menu_rect): 
                    return 2
                
        #vẽ background menu
        dis.blit(bg_lost,((dis_width-200)//2,(dis_height-270)//4))
        
       #vẽ chữ
        dis.blit(thongbao,thongbao_rect)
        dis.blit(play_again,play_again_rect)
        dis.blit(back_menu,back_menu_rect)

        pygame.display.update()
    
#hàm menu
def menu():
    #Khoi bao quanh
    menu_size=pygame.Rect((dis_width-200)//2, (dis_height-250)//4, 200, 320)
  #tạo chữ
    menu_name=font_style.render("MENU",True,red)
    play_easy=font_style.render("Chơi dễ",True,black)
    play_medium=font_style.render("Chơi Trung bình",True,black)
    play_hard=font_style.render("Chơi khó",True,black)
    button_exit=font_style.render("Thoát game",True,black)
# tạo khối bao quanh
    menu_name_rect=menu_name.get_rect(center=((dis_width//2,130)))
    play_easy_rect=play_easy.get_rect(center=(dis_width//2,190))
    play_medium_rect=play_medium.get_rect(center=(dis_width//2,250))
    play_hard_rect=play_hard.get_rect(center=(dis_width//2,310))
    button_exit_rect=button_exit.get_rect(center=(dis_width//2,370))
   
   #vòng lặp chính
    running=True
    while running==True:
        #bắt sự kiện thoát
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running=False
                sys.exit()
            #bắt sự kiện lựa chọn menu
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button==1:
                cursor_position = pygame.mouse.get_pos()
                cursor_rect = pygame.Rect(cursor_position[0], cursor_position[1], 1, 1)
                if cursor_rect.colliderect(play_easy_rect):
                    gameLoop(5)
                    continue
                elif cursor_rect.colliderect(play_medium_rect):
                    gameLoop(10)
                    continue

                elif cursor_rect.colliderect(play_hard_rect):
                    gameLoop(30)
                    continue
                elif cursor_rect.colliderect(button_exit_rect):
                    sys.exit()

        #background
        dis.blit(bg_menu,(0,0))
        # Vẽ menu
        pygame.draw.rect(dis, yellow, menu_size)
        #vẽ chữ
        dis.blit(menu_name,menu_name_rect)
        dis.blit(play_easy,play_easy_rect)
        dis.blit(play_medium,play_medium_rect)
        dis.blit(play_hard,play_hard_rect)
        dis.blit(button_exit,button_exit_rect)

        pygame.display.update()
    pygame.quit()
    

menu()

