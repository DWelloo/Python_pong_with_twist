import pygame as py
from pygame.locals import *
import random
from random import randint
import time
import timeit
import math
#game window initialization
py.init()
screen_width=800
screen_height=600
screen=py.display.set_mode((screen_width,screen_height))
py.display.set_caption("PONG")
#useful constants
running = True
white=(255,255,255)
black=(0,0,0)
lblue=(0,255,240)
lprple=(163.2,0,233.835)
basic_skin=py.image.load("pong_basic_skin.png")
basic_skin_small=py.image.load("pong_basic_skin_small.png")
red_velvet_left=py.image.load("pong_skin_red_velvet_left.png")
red_velvet_right=py.image.load("pong_skin_red_velvet_right.png")
red_velvet_left_small=py.image.load("pong_skin_red_velvet_small_left.png")
red_velvet_right_small=py.image.load("pong_skin_red_velvet_small_right.png")
royal_left=py.image.load("royal_left.png")
royal_right=py.image.load("royal_right.png")
royal_left_small=py.image.load("royal_left_small.png")
royal_right_small=py.image.load("royal_right_small.png")

p1_x=10
p1_y=240
p2_x=775
p2_y=240
players_speed=0.4
ball_x=400
ball_y=269
who_starts=randint(0,1)
#who_starts=0
print(who_starts)

max_score=5
font=py.font.SysFont('skeena',32)
def show_score(p1,p2):
    score_x=360
    score_y=50
    score=font.render(str(p1.score)+" : "+str(p2.score),True,white)
    screen.blit(score,(score_x,score_y))
    py.display.update()

timestamp=[]
small_palette_cd=5
class player():
    colour=white
    width=16
    height=60
    thickness=15
    speed=players_speed
    pos_x=0
    pos_y=0
    score=0
    skin=basic_skin
    small_skin=basic_skin_small
    big_skin=basic_skin
    def move_p(self,x,y):
        self.pos_x=x
        self.pos_y=y
        screen.blit(self.skin,(self.pos_x,self.pos_y))
        
class ball():
    colour=white
    radius=10
    thickness=0
    pos_x=0
    pos_y=0
    speed_x=-1
    speed_y=1
    def move_b(self,x,y):
        self.pos_x=x
        self.pos_y=y
        py.draw.circle(screen,self.colour,[self.pos_x,self.pos_y],self.radius,self.thickness)

class bar():
    colour=white
    p_colour=lblue
    ht_v=10
    wid_v=4
    thickness=5
    pos_x=0
    pos_y=0
    length=120+wid_v
    ht_h=4
    wid_h=length-wid_v
    power=0
    pow_wid=40
    how_many_bars=3
    bar_load_time=4
    def show_bar(self,x,y):
        self.pos_x=x
        self.pos_y=y
        py.draw.rect(screen,self.colour,(self.pos_x,self.pos_y,self.wid_v,
                                         self.ht_v),self.thickness)
        py.draw.rect(screen,self.colour,(self.pos_x+self.length,self.pos_y,self.wid_v,
                                         self.ht_v),self.thickness)
        py.draw.rect(screen,self.colour,(self.pos_x+self.wid_v,self.pos_y-self.wid_v
                                         ,self.wid_h,self.ht_h),self.thickness)
        py.draw.rect(screen,self.colour,(self.pos_x+self.wid_v,self.pos_y
                                         +self.ht_v,self.wid_h,self.ht_h),self.thickness)
        if self.power == max_power:
            self.p_colour=lprple
        else:
            self.p_colour=lblue
        if self.power > 0:
            for i in range(self.power):
                py.draw.rect(screen,self.p_colour,(self.pos_x+self.wid_v+
                i*self.pow_wid/self.bar_load_time,self.pos_y,
                self.pow_wid/self.bar_load_time,self.ht_v),self.thickness)
        for i in range(1,self.how_many_bars):
            py.draw.rect(screen,self.colour,(self.pos_x+self.wid_v+i*self.pow_wid,
                                             self.pos_y,self.wid_v,self.ht_v),self.thickness)

 
collision_cooldown=0.04
def collision_check(player,ball,timestamp=[time.time()-collision_cooldown]):
    if time.time()-timestamp[0]<=collision_cooldown:
        return False
    p_point_x=player.pos_x-9
    if player.pos_x<400:
        p_point_x = player.pos_x+player.width
    if ball.pos_y>=player.pos_y and ball.pos_y<=player.pos_y+player.height:
        p_point_y=ball.pos_y
    elif ball.pos_y>player.pos_y+player.height:
        p_point_y=player.pos_y+player.height
    elif ball.pos_y<player.pos_y:
        p_point_y=player.pos_y
    distance=pow((pow(ball.pos_x-p_point_x,2)+pow(ball.pos_y-p_point_y,2)),0.5)
    if distance<=ball.radius and p_point_x<ball.pos_x: ##
        timestamp[0]=time.time()
        return True
    else:
        return False

def bounce_dir(player,ball):
    if ball.pos_y<player.pos_y+int(player.height/3.75):
        return -1
    elif ball.pos_y>=player.pos_y+int(player.height/3.75) and ball.pos_y<=player.pos_y+int(player.height*2.75/3.75):
        return 0
    elif ball.pos_y>player.pos_y+int(player.height*2.75/3.75):
        return 1
    
#in-game loop variables
player1=player()
ball_1=ball()
player2=player()
acceleration = 0
ball_vel_x=0.4
ball_vel_y=0.0
bar1=bar()
bar2=bar()
bar_p1_x=200
bar_p1_y=550
bar_p2_x=470
bar_p2_y=550
max_power=12
ability_q_flag=(-1)
ability_i_flag=(-1)
slowdown_flag=0
acceleration_level=0
ability_o_flag=0
ability_w_flag=0
time_left_o=0
time_left_w=0
pause=False
deflect_intensity_y=0.52

def track_ball_p1(dir_y,bot,ball,deflect_intensity_y,ball_vel_x,a,a_lvl):#a->acceleration
    v_y=deflect_intensity_y
    v_x=ball_vel_x
    #print("v_x:",v_x)
    calc_x=ball.pos_x
    calc_y=ball.pos_y
    end_x=bot.pos_x-ball.radius
    delta_x=0
    if dir_y==0:
        return ball.pos_y
    else:
        direction=dir_y
        #print("direction:",direction)
        while calc_x+ball.radius <= end_x:
            function=calc_t(direction,bot,v_y,v_x,calc_x,calc_y,a)
            calc_x=function[0]
            calc_y=function[1]
            direction*=(-1)
        if calc_x > end_x:
            delta_x=calc_x-end_x+ball.radius
            #print(delta_x)
            if direction > 0:
                calc_y=v_y*delta_x/v_x
                #print("calc_y:",calc_y)
            else:
                calc_y=screen_height-(v_y*delta_x/v_x)
                #print("calc_y:",calc_y)
        return int(calc_y)

def calc_t(dir_y,bot,v_y,v_x,calc_x,calc_y,a):
    bound=screen_height-ball.radius
    znak=0
    if dir_y < 0:
        bound=ball.radius
        znak=1
    distance_y=int(abs(bound-calc_y))
    #print("distance_y:",distance_y)
    t=(distance_y/v_y)
    distance_x=(v_x*t)
    calc_x+=distance_x
    #print("calc_x+dist:",calc_x)
    if znak==1:
        calc_y-=distance_y
    else:
        calc_y+=distance_y
    #a+=1
    return calc_x,calc_y

def bot_aim(bot,player,ball):
    if abs(bot.pos_y-player.pos_y)>300:
        return 0
    else:
        if player.pos_y<300-player.height/2:
            return 1
        else:
            return -1
        
#in-game loop variables (bot)
I_r=py.K_i
II_r=py.K_o
III_r=py.K_p
mv_up=py.K_UP
mv_down=py.K_DOWN
bot_use_I=False
bot_use_II=False
bot_use_III=False
designated_bot_pos = 240
bot_tracked_ball = 0
can_bot_move = 1
acceleration_threshold = 6
max_acceleration_level = 4
def game_loop_bot(running,p1_y,p2_y,ability_o_flag,ability_w_flag,time_left_o,time_left_w,who_starts,ball_x,
                  ball_y,acceleration,acceleration_level,ball_vel_x,ball_vel_y,ability_q_flag,ability_i_flag,slowdown_flag,
                  pause,deflect_intensity_y,I_r,II_r,III_r,mv_up,mv_down,bot_use_I,bot_use_II,bot_use_III,designated_bot_pos,
                  bot_tracked_ball,acceleration_threshold,max_acceleration_level):
    while running:
        p1_delta = 0
        p2_delta = 0
        screen.fill(black)
        for event in py.event.get():
            if event.type == py.QUIT:
                running=False
            if event.type == py.KEYDOWN:
                if event.key == py.K_b:
                    pause=True
                    while pause:
                        for ev in py.event.get():
                            if ev.type == py.QUIT:
                                running=False
                                pause=False
                                bar1.power=0
                                bar2.power=0
                                ability_o_flag=0
                                ability_w_flag=0
                                player1.height=60
                                player2.height=60
                            if ev.type == py.KEYDOWN:
                                if ev.key == py.K_b:
                                    pause=False
                        screen.blit(font.render("PAUSE",True,white),(343,20))
                        player1.move_p(p1_x,p1_y)
                        player2.move_p(p2_x,p2_y)
                        ball_1.move_b(ball_x,ball_y)
                        bar1.show_bar(bar_p1_x,bar_p1_y)
                        bar2.show_bar(bar_p2_x,bar_p2_y)
                        show_score(player1,player2)
                        py.display.update()
                if event.key == I_r:
                    if ability_i_flag==1:
                        bar1.power+=4
                        if bar1.power>max_power:
                            bar1.power=max_power
                        ability_i_flag*=(-1)
                    else:
                        if bar1.power >= 4:
                            bar1.power-=4
                            ability_i_flag*=(-1)
        if can_bot_move==1:
            if player2.pos_y > designated_bot_pos:
                p2_delta = -1
            if player2.pos_y < designated_bot_pos:
                p2_delta = 1
        if bot_tracked_ball==1 and abs(player2.pos_x-ball_1.pos_x)<30:
            designated_bot_pos+=bot_aim(player2,player1,ball_1)*(0.5+0.1*acceleration_level)
#activation of bot's abilities
        if bot_use_I==True:
            if bar2.power >= 4 and ability_q_flag==(-1):
                bar2.power-=4
                ability_q_flag*=(-1)
                #print("bot_use_I-użyto")
            bot_use_I=False
        if bot_use_II:
            if bar2.power >= 8:
                bar2.power-=8
                ability_w_flag=1
                time_left_w=time.time()
                #print("bot_use_II-użyto")
            bot_use_II=False
        if bot_use_III:
            if bar2.power == max_power:
                bar2.power-=max_power
                ball_1.speed_x*=(-1)
                ball_1.speed_y*=(-1)
                #print("bot_use_III-użyto")
            bot_use_III=False
#conditions for activation of bot's abilities
        if ball_1.pos_x>776 and bar2.power == max_power:
            bot_use_III=True
            #print("bot_use_III-flaga")
        if abs(ball_1.pos_x-player1.pos_x)<10 and (abs(player1.pos_y-ball_1.pos_y)<16 or abs(player1.pos_y+player1.height-ball_1.pos_y)<16):
            bot_use_II=True #można eksperymentować z wartościami w warunkach y
            #print("bot_use_II-flaga")
        if acceleration_level>1 and abs(player1.pos_y-player2.pos_y)>450:
            bot_use_I=True
            #print("bot_use_I-flaga")
#player input processing with queue                            
        keys=py.key.get_pressed()
        if keys[mv_up]:
            p1_delta = player1.speed*(-1)
        if keys[mv_down]:
            p1_delta = player1.speed*1
        if keys[III_r]:
            if bar1.power >= max_power:
                bar1.power-=max_power
                ball_1.speed_x*=(-1)
                ball_1.speed_y*=(-1)
        if keys[II_r]:
            if bar1.power >= 8:
                bar1.power-=8
                ability_o_flag=1
                time_left_o=time.time()
#moving paddles            
        p1_y += p1_delta
        p2_y += p2_delta
        if p1_y<1:
            p1_y = 1
        elif p1_y>538:
            p1_y = 538
        if p2_y<1:
            p2_y = 1
        elif p2_y>538:
            p2_y = 538
        player1.move_p(p1_x,p1_y)
        player2.move_p(p2_x,p2_y)

        if ability_o_flag==1:
            p2_y+=7
            player2.height=45
            player2.skin=player2.small_skin
            ability_o_flag=2
            designated_bot_pos+=7
        if time.time()-time_left_o > small_palette_cd and ability_o_flag==2:
            player2.height=60
            player2.skin=player2.big_skin
            p2_y-=7.5
            designated_bot_pos-=7
            ability_o_flag=0

        if ability_w_flag==1:
            p1_y+=7
            player1.height=45
            player1.skin=player1.small_skin
            ability_w_flag=2
        if time.time()-time_left_w > small_palette_cd and ability_w_flag==2:
            player1.height=60
            player1.skin=player1.big_skin
            p1_y-=7.5
            ability_w_flag=0
#reseting game state on scoring        
        if ball_x<=ball.radius:
            player2.score +=1
            if player2.score == max_score:
                screen.blit(font.render("Player 2 wins",True,white),(310,150))
                py.display.update()
                running=False
            bar1.power=0
            bar2.power=0
            show_score(player1,player2)
            p1_y = 240
            p2_y = 240
            ball_x = 400
            ball_y = 269
            acceleration = 0
            acceleration_level=0
            ball_vel_x=0.4
            ball_vel_y=0.0 
            player1.speed = players_speed
            player2.speed = players_speed
            ability_o_flag=0
            ability_w_flag=0
            player1.height=60
            player2.height=60
            player1.skin=player1.big_skin
            player2.skin=player2.big_skin
            designated_bot_pos=240
            bot_track_ball = 0
            time.sleep(1)
            continue
        elif ball_x>=screen_width-ball.radius:
            print(ball_x," ",ball_y)
            player1.score +=1
            if player1.score == max_score:
                screen.blit(font.render("Player 1 wins",True,white),(310,150))
                py.display.update()
                running=False
            bar1.power=0
            bar2.power=0
            show_score(player1,player2)
            p1_y = 240
            p2_y = 240
            ball_x = 400
            ball_y = 269
            acceleration = 0
            acceleration_level=0
            ball_vel_x=0.4
            ball_vel_y=0.0 
            player1.speed = players_speed
            player2.speed = players_speed
            ability_o_flag=0
            ability_w_flag=0
            player1.height=60
            player2.height=60
            player1.skin=player1.big_skin
            player2.skin=player2.big_skin
            designated_bot_pos=240
            bot_track_ball = 0
            time.sleep(1)
            continue
#bouncing from ceiling and floor            
        if ball_y<=ball_1.radius or ball_y>=screen_height-ball_1.radius:
            #print("ball_1.pos_x",ball_1.pos_x)
            ball_1.speed_y *= (-1)
#collisions
        if collision_check(player2,ball_1):
            #print("player2.pos_y",player2.pos_y,"designated_y:",designated_bot_pos)
            ball_1.speed_x *= (-1)
            #ball_vel_x=0.4+0.1*(acceleration_level)
            if ball_vel_y == 0:
                ball_vel_y = deflect_intensity_y
            acceleration += 1
            if acceleration_level<max_acceleration_level:
                if acceleration==acceleration_threshold:
                    acceleration=0
                    acceleration_level+=1
                    ball_vel_x += 0.1
                    ball_vel_y += 0.0
                    player1.speed += 0.06
                    player2.speed += 0.06
            bar2.power += 2
            if bar2.power > max_power:
                bar2.power = max_power
            ball_1.speed_y = bounce_dir(player2,ball_1)
            #if ball_1.speed_y==0:
             #   ball_vel_y=0.6+0.1*(acceleration_level)
            if ability_q_flag==1:
                ability_q_flag=(-1)
                ball_1.speed_y = 0
                ball_vel_x *= 1.5
                slowdown_flag=1
            if ability_i_flag==(-1) and slowdown_flag==1:
                ball_vel_x *= 0.75 
                slowdown_flag=0
                
        if collision_check(player1,ball_1):
            #todo: zrobić, żeby jak prosto odbija to leci szybciej
            #print("ball_x",ball_x)
            #print("ball_y",ball_y)
            ball_1.speed_x *= (-1)
            if ball_vel_y == 0:
                ball_vel_y = deflect_intensity_y
            acceleration += 1
            if acceleration_level<max_acceleration_level:
                if acceleration==acceleration_threshold:
                    acceleration=0
                    acceleration_level+=1
                    ball_vel_x += 0.1
                    ball_vel_y += 0.0
                    player1.speed += 0.06
                    player2.speed += 0.06
            bar1.power += 2
            if bar1.power > max_power:
                bar1.power = max_power
            ball_1.speed_y = bounce_dir(player1,ball_1)
            if ability_i_flag==1:
                ability_i_flag=(-1)
                ball_1.speed_y = 0
                ball_vel_x *= 1.5
                slowdown_flag=1
            if ability_q_flag==(-1) and slowdown_flag==1:
                ball_vel_x *= 0.75 
                slowdown_flag=0
            #if bot_track_ball==1:
            designated_bot_pos=track_ball_p1(ball_1.speed_y,player2,ball_1,
                                             deflect_intensity_y,ball_vel_x,acceleration,acceleration_level)-player2.height/2
            bot_tracked_ball=1                
#ball movement        
        ball_x += (ball_vel_x)*ball_1.speed_x
        ball_y += (ball_vel_y)*ball_1.speed_y
        ball_1.move_b(ball_x,ball_y)
#bars display
        bar1.show_bar(bar_p1_x,bar_p1_y)
        bar2.show_bar(bar_p2_x,bar_p2_y)
        
        py.display.update()

#
#
#
#
#

def game_loop(running,p1_y,p2_y,ability_o_flag,ability_w_flag,time_left_o,time_left_w,who_starts,
              ball_x,ball_y,acceleration,acceleration_level,ball_vel_x,ball_vel_y,
              ability_q_flag,ability_i_flag,slowdown_flag,pause,deflect_intensity_y):
    while running:
        p1_delta = 0
        p2_delta = 0
        screen.fill(black)
        for event in py.event.get():
            if event.type == py.QUIT:
                running=False
            if event.type == py.KEYDOWN:
                if event.key == py.K_b:
                    pause=True
                    while pause:
                        for ev in py.event.get():
                            if ev.type == py.QUIT:
                                running=False
                                pause=False
                                bar1.power=0
                                bar2.power=0
                                ability_o_flag=0
                                ability_w_flag=0
                                player1.height=60
                                player2.height=60
                            if ev.type == py.KEYDOWN:
                                if ev.key == py.K_b:
                                    pause=False
                        screen.blit(font.render("PAUSE",True,white),(343,20))
                        player1.move_p(p1_x,p1_y)
                        player2.move_p(p2_x,p2_y)
                        ball_1.move_b(ball_x,ball_y)
                        bar1.show_bar(bar_p1_x,bar_p1_y)
                        bar2.show_bar(bar_p2_x,bar_p2_y)
                        show_score(player1,player2)
                        py.display.update()
                if event.key == py.K_q:
                    if ability_q_flag==1:
                        bar2.power+=4
                        if bar2.power>max_power:
                            bar2.power=max_power
                        ability_q_flag*=(-1) #ewentualnie dodać warunek max_power   #??
                    else:
                        if bar2.power >= 4:
                            bar2.power-=4
                            ability_q_flag*=(-1)
                if event.key == py.K_i:
                    if ability_i_flag==1:
                        bar1.power+=4
                        if bar1.power>max_power:
                            bar1.power=max_power
                        ability_i_flag*=(-1) #ewentualnie dodać warunek max_power   #??
                    else:
                        if bar1.power >= 4:
                            bar1.power-=4
                            ability_i_flag*=(-1)
                    
        keys=py.key.get_pressed()
        if keys[py.K_UP]:
            p1_delta = player1.speed*(-1)
        if keys[py.K_DOWN]:
            p1_delta = player1.speed*1
        if keys[py.K_s]:
            p2_delta = player2.speed*(-1)
        if keys[py.K_x]:
            p2_delta = player2.speed*1
        if keys[py.K_e]:
            if bar2.power >= max_power:
                bar2.power-=max_power
                ball_1.speed_x*=(-1)
                ball_1.speed_y*=(-1)
        if keys[py.K_w]:
            if bar2.power >= 8:
                bar2.power-=8
                ability_w_flag=1
                time_left_w=time.time()
        if keys[py.K_p]:
            if bar1.power >= max_power:
                bar1.power-=max_power
                ball_1.speed_x*=(-1)
                ball_1.speed_y*=(-1)
        if keys[py.K_o]:
            if bar1.power >= 8:
                bar1.power-=8
                ability_o_flag=1
                time_left_o=time.time()
                    
        p1_y += p1_delta
        p2_y += p2_delta
        if p1_y<1:
            p1_y = 1
        elif p1_y>538:
            p1_y = 538
        if p2_y<1:
            p2_y = 1
        elif p2_y>538:
            p2_y = 538
        player1.move_p(p1_x,p1_y)
        player2.move_p(p2_x,p2_y)

        if ability_o_flag==1:
            p2_y+=7.5
            player2.height=45
            player2.skin=player2.small_skin
            ability_o_flag=2
        if ability_o_flag==2 and time.time()-time_left_o > small_palette_cd:
            player2.height=60
            player2.skin=player2.big_skin
            p2_y-=7.5
            ability_o_flag=0

        if ability_w_flag==1:
            p1_y+=7.5
            player1.height=45
            player1.skin=player1.small_skin
            ability_w_flag=2
        if ability_w_flag==2 and time.time()-time_left_w > small_palette_cd:
            player1.height=60
            player1.skin=player1.big_skin
            p1_y-=7.5
            ability_w_flag=0
        
        if who_starts==0:
            ball_1.speed_x *= (-1)
        who_starts = -1
        
        if ball_x<=0:
            player2.score +=1
            if player2.score == max_score:
                screen.blit(font.render("Player 2 wins",True,white),(310,150))
                py.display.update()
                running=False
            bar1.power=0
            bar2.power=0
            show_score(player1,player2)
            p1_y = 240
            p2_y = 240
            ball_x = 400
            ball_y = 269
            acceleration = 0
            ball_vel_x=0.4
            ball_vel_y=0.0 
            player1.speed = players_speed
            player2.speed = players_speed
            ability_o_flag=0
            ability_w_flag=0
            player1.height=60
            player2.height=60
            player1.skin=player1.big_skin
            player2.skin=player2.big_skin
            time.sleep(1)
            continue
        elif ball_x>=780:
            player1.score +=1
            if player1.score == max_score:
                screen.blit(font.render("Player 1 wins",True,white),(310,150))
                py.display.update()
                running=False
            bar1.power=0
            bar2.power=0
            show_score(player1,player2)
            p1_y = 240
            p2_y = 240
            ball_x = 400
            ball_y = 269
            acceleration = 0
            ball_vel_x=0.4
            ball_vel_y=0.0 
            player1.speed = players_speed
            player2.speed = players_speed
            ability_o_flag=0
            ability_w_flag=0
            player1.height=60
            player2.height=60
            player1.skin=player1.big_skin
            player2.skin=player2.big_skin
            time.sleep(1)
            continue
            
        if ball_y<=ball_1.radius or ball_y>=600-ball_1.radius:
            ball_1.speed_y *= (-1)
            acceleration += 1

        if collision_check(player2,ball_1):
            ball_1.speed_x *= (-1)
            if ball_vel_y == 0:
                ball_vel_y = deflect_intensity_y
            acceleration += 1
            bar2.power += 2
            if bar2.power > max_power:
                bar2.power = max_power
            ball_1.speed_y = bounce_dir(player2,ball_1)
            if ability_q_flag==1:
                ability_q_flag=(-1)
                ball_1.speed_y = 0
                ball_vel_x *= 1.5
                slowdown_flag=1
            if ability_i_flag==(-1) and slowdown_flag==1:
                ball_vel_x *= 0.75 #jeżeli w momencie tej kolizji acc_lvl++ to troszkę wolniejsza jest piłka
                slowdown_flag=0    #można chyba dać sprawdzanie wcześniej->najpierw zwolni do oryginalnej szybkości, a potem przyspieszy 
                
            
        if collision_check(player1,ball_1):
            ball_1.speed_x *= (-1)
            if ball_vel_y == 0:
                ball_vel_y = deflect_intensity_y
            acceleration += 1
            bar1.power += 2
            if bar1.power > max_power:
                bar1.power = max_power
            ball_1.speed_y = bounce_dir(player1,ball_1)
            if ability_i_flag==1:
                ability_i_flag=(-1)
                ball_1.speed_y = 0
                ball_vel_x *= 1.5
                slowdown_flag=1
            if ability_q_flag==(-1) and slowdown_flag==1:
                ball_vel_x *= 0.75 #
                slowdown_flag=0

        if acceleration_level<5:  
            if acceleration==8:
                acceleration=0
                acceleration_level+=1
                ball_vel_x += 0.1
                ball_vel_y += 0.0
                player1.speed += 0.06
                player2.speed += 0.06
            
        ball_x += (ball_vel_x)*ball_1.speed_x
        ball_y += (ball_vel_y)*ball_1.speed_y
        ball_1.move_b(ball_x,ball_y)

        bar1.show_bar(bar_p1_x,bar_p1_y)
        bar2.show_bar(bar_p2_x,bar_p2_y)
        
        py.display.update()

menu_open=True
grey=(100,100,100)
red=(255,0,0)
single_button_x=270
single_button_y=270
single_button_width=250
single_button_height=25
play_button_x=270
play_button_y=300
play_button_width=250
play_button_height=25
skin_button_x=270
skin_button_y=330
skin_button_width=250
skin_button_height=25
quit_button_x=270
quit_button_y=360
quit_button_width=250
quit_button_height=25
big_font=py.font.SysFont('skeena',64)
pong_sign_x=325
pong_sign_y=50

chosen_p1=0
chosen_p2=0
def choose_skin():
    global chosen_p1
    global chosen_p2
    help_run=True
    width=100
    height=100
    row_1_y=50
    basic_x=50
    red_velv_x=160
    royal_x=270
    
    row_2_y=170
    sauce_x=50
    p1_sign=font.render("P1",True,white)
    p2_sign=font.render("P2",True,white)
    #score=font.render(str(p1.score)+" : "+str(p2.score),True,white)
    #pamiętać,żeby skiny displayować jako "left"
    #basic_skin , red_velvet_skin_direction
    while help_run:
        screen.fill(black)
        #drawing models
        screen.blit(basic_skin,(basic_x+42,row_1_y+20))
        screen.blit(red_velvet_left,(red_velv_x+42,row_1_y+20))
        screen.blit(royal_left,(royal_x+42,row_1_y+20))
        #screen.blit(sauce,(sauce_x+42,row_2_y+20))DWEllooo giereczka nr 1
        #checking mouse input
        mouse=py.mouse.get_pos()
        for event in py.event.get():
            if event.type==py.QUIT:
                help_run=False
            if event.type==py.MOUSEBUTTONDOWN and event.button==1:
                if basic_x<=mouse[0]<=basic_x+width and row_1_y<=mouse[1]<=row_1_y+height:
                    chosen_p1=0
                    player1.skin=basic_skin
                    player1.big_skin=basic_skin
                    player1.small_skin=basic_skin_small
                if red_velv_x<=mouse[0]<=red_velv_x+width and row_1_y<=mouse[1]<=row_1_y+height:
                    chosen_p1=1
                    player1.skin=red_velvet_left
                    player1.big_skin=red_velvet_left
                    player1.small_skin=red_velvet_left_small
                if royal_x<=mouse[0]<=royal_x+width and row_1_y<=mouse[1]<=row_1_y+height:
                    chosen_p1=2
                    player1.skin=royal_left
                    player1.big_skin=royal_left
                    player1.small_skin=royal_left_small
                    
            if event.type==py.MOUSEBUTTONDOWN and event.button==3:
                if basic_x<=mouse[0]<=basic_x+width and row_1_y<=mouse[1]<=row_1_y+height:
                    chosen_p2=0
                    player2.skin=basic_skin
                    player2.big_skin=basic_skin
                    player2.small_skin=basic_skin_small
                if red_velv_x<=mouse[0]<=red_velv_x+width and row_1_y<=mouse[1]<=row_1_y+height:
                    chosen_p2=1
                    player2.skin=red_velvet_right
                    player2.big_skin=red_velvet_right
                    player2.small_skin=red_velvet_right_small
                if royal_x<=mouse[0]<=royal_x+width and row_1_y<=mouse[1]<=row_1_y+height:
                    chosen_p2=2
                    player2.skin=royal_right
                    player2.big_skin=royal_right
                    player2.small_skin=royal_right_small

        #drawing signs "P1" and "P2" (indicators of which skin has been chosen)
        if chosen_p1==0:
            screen.blit(p1_sign,(basic_x+5,row_1_y+105))
        if chosen_p1==1:
            screen.blit(p1_sign,(red_velv_x+5,row_1_y+105))
        if chosen_p1==2:
            screen.blit(p1_sign,(royal_x+5,row_1_y+105))

        if chosen_p2==0:
            screen.blit(p2_sign,(basic_x+60,row_1_y+105))
        if chosen_p2==1:
            screen.blit(p2_sign,(red_velv_x+60,row_1_y+105))
        if chosen_p2==2:
            screen.blit(p2_sign,(royal_x+60,row_1_y+105))

        #drawing frames     
        if basic_x<=mouse[0]<=basic_x+width and row_1_y<=mouse[1]<=row_1_y+height:
            py.draw.rect(screen,red,(basic_x,row_1_y,width,height),1)
        else:
            py.draw.rect(screen,white,(basic_x,row_1_y,width,height),1)
            
        if red_velv_x<=mouse[0]<=red_velv_x+width and row_1_y<=mouse[1]<=row_1_y+height:
            py.draw.rect(screen,red,(red_velv_x,row_1_y,width,height),1)
        else:
            py.draw.rect(screen,white,(red_velv_x,row_1_y,width,height),1)
            
        if royal_x<=mouse[0]<=royal_x+width and row_1_y<=mouse[1]<=row_1_y+height:
            py.draw.rect(screen,red,(royal_x,row_1_y,width,height),1)
        else:
            py.draw.rect(screen,white,(royal_x,row_1_y,width,height),1)
            
        py.display.update()

while menu_open:
    screen.fill(black)
    screen.blit(big_font.render("PONG",True,white),(pong_sign_x,pong_sign_y))
    mouse=py.mouse.get_pos()
    for event in py.event.get():
        if event.type==py.QUIT:
            menu_open=False
        if event.type==py.MOUSEBUTTONDOWN:
            if play_button_x<=mouse[0]<=play_button_x+play_button_width and play_button_y<=mouse[1]<=play_button_y+play_button_height:
                player1.move_p(p1_x,p1_y)
                player2.move_p(p2_x,p2_y)
                ball_1.move_b(ball_x,ball_y)
                bar1.show_bar(bar_p1_x,bar_p1_y)
                bar2.show_bar(bar_p2_x,bar_p2_y)
                py.display.update()
                time.sleep(2)
                game_loop(running,p1_y,p2_y,ability_o_flag,ability_w_flag,time_left_o,time_left_w,who_starts,ball_x,ball_y,acceleration,
                          acceleration_level,ball_vel_x,ball_vel_y,ability_q_flag,ability_i_flag,slowdown_flag,pause,deflect_intensity_y)
                player1.score=0
                player2.score=0
            if single_button_x<=mouse[0]<=single_button_x+single_button_width and single_button_y<=mouse[1]<=single_button_y+single_button_height:
                player1.move_p(p1_x,p1_y)
                player2.move_p(p2_x,p2_y)
                ball_1.move_b(ball_x,ball_y)
                bar1.show_bar(bar_p1_x,bar_p1_y)
                bar2.show_bar(bar_p2_x,bar_p2_y)
                py.display.update()
                time.sleep(2)
                game_loop_bot(running,p1_y,p2_y,ability_o_flag,ability_w_flag,time_left_o,time_left_w,who_starts,ball_x,ball_y,acceleration,
                          acceleration_level,ball_vel_x,ball_vel_y,ability_q_flag,ability_i_flag,slowdown_flag,pause,deflect_intensity_y,
                              I_r,II_r,III_r,mv_up,mv_down,bot_use_I,bot_use_II,bot_use_III,designated_bot_pos,bot_tracked_ball,
                              acceleration_threshold,max_acceleration_level)
                player1.score=0
                player2.score=0
            if skin_button_x<=mouse[0]<=skin_button_x+skin_button_width and skin_button_y<=mouse[1]<=skin_button_y+skin_button_height:
                choose_skin()
            if quit_button_x<=mouse[0]<=quit_button_x+quit_button_width and quit_button_y<=mouse[1]<=quit_button_y+quit_button_height:
                menu_open=False
                
    if single_button_x<=mouse[0]<=single_button_x+single_button_width and single_button_y<=mouse[1]<=single_button_y+single_button_height:
        py.draw.rect(screen,red,(single_button_x,single_button_y,single_button_width,single_button_height))
        screen.blit(font.render("Play with bot",True,black),(single_button_x+55,single_button_y+1))
    else:
        py.draw.rect(screen,grey,(single_button_x,single_button_y,single_button_width,single_button_height))
        screen.blit(font.render("Play with bot",True,white),(single_button_x+55,single_button_y+1))
        
    if play_button_x<=mouse[0]<=play_button_x+play_button_width and play_button_y<=mouse[1]<=play_button_y+play_button_height:
        py.draw.rect(screen,red,(play_button_x,play_button_y,play_button_width,play_button_height))
        screen.blit(font.render("Play 2 players mode",True,black),(play_button_x+20,play_button_y+1))
    else:
        py.draw.rect(screen,grey,(play_button_x,play_button_y,play_button_width,play_button_height))
        screen.blit(font.render("Play 2 players mode",True,white),(play_button_x+20,play_button_y+1))
        
    if skin_button_x<=mouse[0]<=skin_button_x+skin_button_width and skin_button_y<=mouse[1]<=skin_button_y+skin_button_height:
        py.draw.rect(screen,red,(skin_button_x,skin_button_y,skin_button_width,skin_button_height))
        screen.blit(font.render("Skin selector",True,black),(skin_button_x+55,skin_button_y+1))
    else:
        py.draw.rect(screen,grey,(skin_button_x,skin_button_y,skin_button_width,skin_button_height))
        screen.blit(font.render("Skin selector",True,white),(skin_button_x+55,skin_button_y+1))

    if quit_button_x<=mouse[0]<=quit_button_x+quit_button_width and quit_button_y<=mouse[1]<=quit_button_y+quit_button_height:
        py.draw.rect(screen,red,(quit_button_x,quit_button_y,quit_button_width,quit_button_height))
        screen.blit(font.render("Quit the game",True,black),(quit_button_x+55,quit_button_y+1))
    else:
        py.draw.rect(screen,grey,(quit_button_x,quit_button_y,quit_button_width,quit_button_height))
        screen.blit(font.render("Quit the game",True,white),(quit_button_x+55,quit_button_y+1))

    py.display.update()
py.quit()
