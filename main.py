import pygame
from random import randint


pygame.init()
pygame.font.init()
pygame.mixer.init()
pygame.mixer.music.load("background_music.mp3")
pygame.mixer.music.play(-1)
screen=pygame.display.set_mode((1280,720))
clock=pygame.time.Clock()
pygame.display.set_caption("Space Shooter")
font=pygame.font.Font(None,25)
score=0
score_txt=font.render(f"score={score}",True,"white","Black")
shoot_sound=pygame.mixer.Sound("gun_sound.wav")
hit_sound=pygame.mixer.Sound("hit_sound1.wav")
player_hit_sound=pygame.mixer.Sound("anemy_player_hit.wav")
game_over_sound=pygame.mixer.Sound("game_over.mp3")

running=True
player_rect=pygame.Rect(screen.get_width()/2,screen.get_height()/2,100,100)
player_rect.center=screen.get_rect().center
bullet_list=[]
enemies=[]
for i in range(5):
    size=randint(40,80)
    enemy=pygame.Rect(randint(0,screen.get_width()-size),randint(-100,0),size,size)
    enemies.append(enemy)

enemy_speed=100
lives=10
live_txt=font.render(f"lives={lives}",True,"white","Black")
game_over=False
font2=pygame.font.Font(None,60)
game_over_txt=font2.render("Game Over",True,"RED")
restart_txt=font2.render("Press R to Restart",True,"White")

def game_reset():
    global score ,score_txt, running, player_rect,bullet_list,enemies,enemy_speed,lives,live_txt,game_over
    score=0
    score_txt=font.render(f"score={score}",True,"white","Black")
    player_rect=pygame.Rect(screen.get_width()/2,screen.get_height()/2,100,100)
    player_rect.center=screen.get_rect().center
    bullet_list=[]
    enemies=[]
    for i in range(5):
        size=randint(40,80)
        enemy=pygame.Rect(randint(0,screen.get_width()-size),randint(-100,0),size,size)
        enemies.append(enemy)
    enemy_speed=100
    lives=10
    live_txt=font.render(f"lives={lives}",True,"white","Black")
    game_over=False

while running:
    screen.fill("black")
    dt=clock.tick(120)/1000
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running= False

        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_SPACE and not game_over:
                shoot_sound.play()
                bullet=pygame.Rect(player_rect.x,player_rect.y,30,30)
                bullet.center=player_rect.center
                bullet.bottom=player_rect.top
                bullet_list.append(bullet)
            if event.key==pygame.K_r and game_over:
                game_reset()


    if not game_over:
        for index,enemy in enumerate(enemies):
            enemy.y+=enemy_speed*dt
            pygame.draw.ellipse(screen,"crimson",enemy)
            pygame.draw.polygon(screen,"crimson",[
                (enemy.centerx,enemy.top),
                (enemy.right,enemy.bottom),
                (enemy.left,enemy.bottom),
            ])
            pygame.draw.circle(screen,"Black",(enemy.left+15,enemy.top+15),5)
            pygame.draw.circle(screen,"Black",(enemy.right-15,enemy.top+15),5)
            pygame.draw.circle(screen,"white",(enemy.left+15,enemy.top+15),2)
            pygame.draw.circle(screen,"white",(enemy.right-15,enemy.top+15),2)
            pygame.draw.circle(screen,"chartreuse",(enemy.centerx,enemy.centery+10),15)
            pygame.draw.circle(screen,"violet",(enemy.centerx,enemy.centery+10),11)
            pygame.draw.circle(screen,"aquamarine",(enemy.centerx,enemy.centery+10),9)

            if player_rect.colliderect(enemy):
                player_hit_sound.play()
                size=randint(40,80)
                lives-=1
                live_txt=font.render(f"lives={lives}",True,"white","Black")
                enemies[index]=pygame.Rect(randint(0,screen.get_width()-size),randint(-100,0),size,size)
            if enemy.bottom>screen.get_height()+50:
                size=randint(40,80)
                lives-=1
                live_txt=font.render(f"lives={lives}",True,"white","Black")
                enemies[index]=pygame.Rect(randint(0,screen.get_width()-size),randint(-100,0),size,size)
        new_bulletlist=[]
        for bullet in bullet_list:
            hit=False
            bullet.y-=350*dt
            pygame.draw.circle(screen,"yellow",bullet.center,15)
            pygame.draw.polygon(screen,"cyan",[
                (bullet.centerx,bullet.top-5),
                (bullet.left,bullet.bottom-5),
                (bullet.right,bullet.bottom-5)
            ])
            pygame.draw.circle(screen, "white", bullet.center, 5)
            for index,enemy in enumerate(enemies):
                if bullet.colliderect(enemy):
                    hit_sound.play()
                    size=randint(40,80)
                    hit=True
                    score+=1
                    enemy_speed+=5
                    enemy_speed=min(enemy_speed,300)
                    score_txt=font.render(f"score={score}",True,"white","Black")
                    enemies[index]=pygame.Rect(randint(0,screen.get_width()-size),randint(-100,0),size,size)
            if not hit and  not (bullet.y<=-30):
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
            player_rect.x-=500*dt
            if player_rect.x<=0:
                player_rect.x=0
        if key[pygame.K_d]:
            player_rect.x+=500*dt
            if player_rect.x>=screen.get_width()-100:
                player_rect.x=screen.get_width()-100

        pygame.draw.polygon(screen,"deeppink",
        [   
            (player_rect.centerx, player_rect.top),
            (player_rect.left, player_rect.bottom),
            (player_rect.centerx, player_rect.bottom - 20),
            (player_rect.right, player_rect.bottom),

        ])
        pygame.draw.circle(screen,"cyan",(player_rect.centerx,player_rect.centery-10),15)
        pygame.draw.polygon(screen,"YELLOW",[
            (player_rect.left,player_rect.bottom),
            (player_rect.left-5,player_rect.bottom+3),
            (player_rect.left+5,player_rect.bottom+3)
        ])
        pygame.draw.polygon(screen,"YELLOW",[
            (player_rect.right,player_rect.bottom),
            (player_rect.right-5,player_rect.bottom+3),
            (player_rect.right+5,player_rect.bottom+3)
        ])

    if lives<=0 and not game_over:
        game_over=True
        game_over_sound.play()
    if game_over:
        screen.blit(game_over_txt,(500,250))
        screen.blit(restart_txt,(450,320))

    screen.blit(score_txt,(0,0))
    screen.blit(live_txt,(0,20))
    pygame.display.flip()

pygame.quit()