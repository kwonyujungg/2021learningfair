import pygame
from pygame.rect import *
import random

#1.<변수초기화>
isActive = True
SCREEN_WIDTH = 450
SCREEN_HEIGHT = 600
move = Rect(0,0,0,0)
time_delay_500ms = 0
time_dealy_4sec = 0
toggle = False
score = 0
isGameOver = False


#2.<스크린생성>
pygame.init()
screen = pygame.display.set_mode((450,600))
pygame.display.set_caption('과제 피하기 게임')


#3.<player 생성>
player = pygame.image.load("D:/teamgame/superman.png")
player = pygame.transform.scale(player, (40,40))
recplayer = player.get_rect()
recplayer.centerx = (SCREEN_WIDTH/2)
recplayer.centery = (SCREEN_HEIGHT/2)



#4.<과제 아이콘 생성>
  #book
book = [pygame.image.load("D:/teamgame/book3.png") for i in range(25)]
recbook = [None for i in range(len(book))]
for i in range(len(book)):
    book[i] = pygame.transform.scale(book[i], (25,25))
    recbook[i] = book[i].get_rect()
    recbook[i].y = -1
   

#5.<기타>
clock = pygame.time.Clock()

# <player 조작>

def restart():
    global isGameOver, score
    isGameOver = False
    score = 0
    for i in range(len(book)):
        recbook[i].y = -1
    pass

def eventprocess():
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                
            if event.key == pygame.K_LEFT:
                move.x = -1
            if event.key == pygame.K_RIGHT:
                move.x = 1
            if event.key == pygame.K_UP:
                move.y = -1
            if event.key == pygame.K_DOWN:
                move.y = 1
            if event.key == pygame.K_r:
                restart()
        
            
             
            


# <함수들>
 #player 
def moveplayer():
    if not isGameOver:
        recplayer.x += move.x
        recplayer.y += move.y
    
    if recplayer.x < 0:
        recplayer.x = 0
    if recplayer.x > SCREEN_WIDTH-recplayer.width:
        recplayer.x = SCREEN_WIDTH-recplayer.width   
        
    if recplayer.y < 0:
        recplayer.y = 0    
    if recplayer.y > SCREEN_HEIGHT-recplayer.height:
        recplayer.y = SCREEN_HEIGHT-recplayer.height
        
    screen.blit(player, recplayer)




    ##<아이템 분산시키기>##
def timeDelay500ms():
    global time_delay_500ms
    if time_delay_500ms > 5:
        time_delay_500ms = 0
        return True
    
    time_delay_500ms += 1
    return False 




    ## <아이콘 여러개 떨어지기> ##
def makebook():
    if isGameOver:
        return
    if timeDelay500ms():
        idex = random.randint(0, len(book)-1)
        if recbook[idex].y == -1:
            recbook[idex].x = random.randint(0, SCREEN_WIDTH)
            recbook[idex].y = 0




    # <과제아이콘>
def movebook():
    makebook()
    
    for i in range(len(book)):
        if recbook[i].y == -1:
            continue
        
        if not isGameOver:
            recbook[i].y += 1
        if recbook[i].y > SCREEN_HEIGHT:
            recbook[i].y = 0
        
        screen.blit(book[i], recbook[i])
    
    
    
  
  #<출동확인>
def CheckCollision():
      global score, isGameOver

      if isGameOver:
          return
        
      for rec in recbook:
          if rec.y == -1:
              continue
          if rec.top < recplayer.bottom \
             and recplayer.top < rec.bottom \
             and rec.left < recplayer.right \
             and recplayer.left < rec.right:
             print('충돌')
             isGameOver = True
             break
      score += 1

def blinking():
    global time_dealy_4sec, toggle
    time_dealy_4sec += 1
    if time_dealy_4sec > 40:
        time_dealy_4sec = 0
        toggle = ~toggle

    return toggle
        

def setText():
    mFont = pygame.font.SysFont("arial",20, True, False)
    screen.blit(mFont.render(
        f'score : {score}', True, 'blue'),(10,10,0,0))
    
    if isGameOver and blinking():
        screen.blit(mFont.render(
            'Game Over!!', True, 'red'),(150,300,0,0))

        screen.blit(mFont.render(
            'press r - Restart', True, 'red'),(140,320,0,0))

        if score >= 600 :
            screen.blit(mFont.render(
                'Final Credit : A+', True, 'red'),(160,350,0,0))
        elif score >= 500 :
            screen.blit(mFont.render(
                'Final Credit : A', True, 'red'),(160,350,0,0))
        elif score >= 400 :
            screen.blit(mFont.render(
                'Final Credit : B', True, 'red'),(160,350,0,0))
        elif score >= 300 :
            screen.blit(mFont.render(
                'Final Credit : C', True, 'red'),(160,350,0,0))
        elif score < 300 :
            screen.blit(mFont.render(
                'Final Credit : F', True, 'red'),(160,350,0,0))






##반복##
while True:
    
    #화면지움
    screen.fill((192,192,192))
    
    #이벤트부분정리 
    eventprocess()
    
    #move
    moveplayer() 
    movebook()
    
    #text업데이트
    setText()
    
   #화면구현
    pygame.display.flip()
    clock.tick(100)

    #충돌확인
    CheckCollision()
