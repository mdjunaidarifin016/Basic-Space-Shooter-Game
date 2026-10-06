import pygame
from random import randint


pygame.init()
pygame.font.init()
screen=pygame.display.set_mode((1280,720))
clock=pygame.time.Clock()
pygame.display.set_caption("Space Shooter")
font=pygame.font.Font(None,25)
score=0
score_txt=font.render(f"score={score}",True,"white","Black")

running=True
player_rect=pygame.Rect(screen.get_width()/2,screen.get_height()/2,100,100)
player_rect.center=screen.get_rect().center
bullet_list=[]
enemy=pygame.Rect(randint(0,screen.get_width()-50),-50,50,50)
enemy_speed=100
lives=3
live_txt=font.render(f"lives={lives}",True,"white","Black")
game_over=False
font2=pygame.font.Font(None,60)
game_over_txt=font2.render("Game Over",True,"RED")
restart_txt=font2.render("Press R to Restart",True,"White")

def game_reset():
    global score ,score_txt, running, player_rect,bullet_list,enemy,enemy_speed,lives,live_txt,game_over
    score=0
    score_txt=font.render(f"score={score}",True,"white","Black")
    player_rect=pygame.Rect(screen.get_width()/2,screen.get_height()/2,100,100)
    player_rect.center=screen.get_rect().center
    bullet_list=[]
    enemy=pygame.Rect(randint(0,screen.get_width()-50),-50,50,50)
    enemy_speed=100
    lives=3
    live_txt=font.render(f"lives={lives}",True,"white","Black")
    game_over=False

while running:
    screen.fill("orange")
    dt=clock.tick(120)/1000
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running= False

        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_SPACE and not game_over:
                bullet=pygame.Rect(player_rect.x,player_rect.y,30,30)
                bullet.center=player_rect.center
                bullet.bottom=player_rect.top
                bullet_list.append(bullet)
            if event.key==pygame.K_r and game_over:
                game_reset()


    if not game_over:
        new_bulletlist=[]
        for bullet in bullet_list:
            bullet.y-=350*dt
            pygame.draw.circle(screen,"black",bullet.center,15)
            if bullet.colliderect(enemy):
                score+=1
                enemy_speed+=100
                enemy_speed=min(enemy_speed,500)
                score_txt=font.render(f"score={score}",True,"white","Black")
                enemy=pygame.Rect(randint(0,screen.get_width()-50),-50,50,50)
            elif not  ( bullet.y<=-30):
                new_bulletlist.append(bullet)
        bullet_list=new_bulletlist

        key=pygame.key.get_pressed()
        if key[pygame.K_w]:
            player_rect.y-=300*dt
            if player_rect.y<=0 :
                player_rect.y=0
        if key[pygame.K_s]:
            player_rect.y+=300*dt
            if player_rect.y>=screen.get_height()-100:
                player_rect.y=screen.get_height()-100
        if key[pygame.K_a]:
            player_rect.x-=300*dt
            if player_rect.x<=0:
                player_rect.x=0
        if key[pygame.K_d]:
            player_rect.x+=300*dt
            if player_rect.x>=screen.get_width()-100:
                player_rect.x=screen.get_width()-100

        pygame.draw.rect(screen,"GREEN",player_rect)

        if player_rect.colliderect(enemy):
            lives-=1
            live_txt=font.render(f"lives={lives}",True,"white","Black")
            enemy=pygame.Rect(randint(0,screen.get_width()-50),-50,50,50)

        enemy.y+=enemy_speed*dt
        pygame.draw.ellipse(screen,"blue",enemy)
        if enemy.bottom>screen.get_height()+50:
            lives-=1
            live_txt=font.render(f"lives={lives}",True,"white","Black")
            enemy=pygame.Rect(randint(0,screen.get_width()-50),-50,50,50)
    if lives<=0:
        game_over=True
        screen.blit(game_over_txt,(500,250))
        screen.blit(restart_txt,(450,320))

    screen.blit(score_txt,(0,0))
    screen.blit(live_txt,(0,20))
    pygame.display.flip()

pygame.quit()