import pygame
from settings import WAVE,SPRAY,COIN, WIN_WIDTH, WIN_HEIGHT, HP_IMAGE, HP_GRAY_IMAGE, BACKGROUND_IMAGE
from color_settings import *
clock = pygame.time.Clock() 

class GameView:
    def __init__(self):
        self.win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        #self.font = pygame.font.SysFont("comicsans", 30)
        self.font = pygame.font.Font(pygame.font.match_font('arial'), 25)
        self.coin_count = 0
        self.spray_count = 0
        
    def draw_bg(self):
        self.win.blit(BACKGROUND_IMAGE, (0, 0))

    def draw_enemies(self, enemies):
        for en in enemies.get():
            self.win.blit(en.image, en.rect)
            # draw health bar
            bar_width = en.rect.w * (en.health / en.max_health)
            max_bar_width = en.rect.w
            bar_height = 5
            pygame.draw.rect(self.win, RED, [en.rect.x, en.rect.y - 10, max_bar_width, bar_height])
            pygame.draw.rect(self.win, GREEN, [en.rect.x, en.rect.y - 10, bar_width, bar_height])
            
    def draw_fire_balls(self, fire_ball):
        for fire in fire_ball.get():
            self.win.blit(fire.image, fire.rect)
            
    def draw_towers(self, towers):
        # draw tower
        for tw in towers:
            if tw :
                self.win.blit(SPRAY[self.spray_count % 3], tw.rect)
                self.spray_count += 1
            self.win.blit(tw.image, tw.rect)

    def draw_range(self, selected_tower):
        # draw tower range
        if selected_tower is not None:
            tw = selected_tower
            # create a special surface that is able to render semi-transparent image
            surface = pygame.Surface((WIN_WIDTH, WIN_HEIGHT), pygame.SRCALPHA)
            transparency = 120
            pygame.draw.circle(surface, (128, 128, 128, transparency), tw.rect.center, tw.range)
            self.win.blit(surface, (0, 0))

    def draw_menu(self, menu):
        self.win.blit(menu.image, menu.rect)
        for btn in menu.buttons:
            self.win.blit(btn.image, btn.rect)

    def draw_plots(self, plots):
        for pt in plots:
            self.win.blit(pt.image, pt.rect)

    def draw_money(self, money: int):
        """ (Q2.1)render the money"""
        text = self.font.render(f"       : {money}", True, (255, 255, 255))
        self.win.blit(text, (5, 45))
        self.win.blit(COIN[self.coin_count % 2], (3, 40))
        if (1000-money) % 2 != 0:
            self.coin_count += 1
            self.win.blit(COIN[self.coin_count % 2], (3, 40))

    def draw_wave(self, wave: int):
        """(Q2.2)render the wave"""
        text = self.font.render(f"       : {wave}", True, (255, 255, 255))
        self.win.blit(WAVE, (3, 10))
        self.win.blit(text, (5, 15))

    def draw_hp(self, lives):
        # draw_lives
        hp_rect = HP_IMAGE.get_rect()
        for i in range(10):
            self.win.blit(HP_GRAY_IMAGE, (WIN_WIDTH // 2 - hp_rect.w * (2.5 - i % 5), hp_rect.h * (i // 5)))
        for i in range(lives):
            self.win.blit(HP_IMAGE, (WIN_WIDTH // 2 - hp_rect.w * (2.5 - i % 5), hp_rect.h * (i // 5)))
        
    def draw_end(self, model):
#         largeText = pygame.font.SysFont("comicsansms",115)
#         TextSurf = largeText.render('You dead', True, (255,0,0))
#         self.win.blit(TextSurf, (WIN_WIDTH // 3 -50 , WIN_HEIGHT // 3))
        end = True
        pygame.init()
        pygame.font.init()
        while end and model.events["game quit"] == False: 
                end = True
                largeText = pygame.font.Font(pygame.font.match_font('arial'), 115)
                #largeText = pygame.font.SysFont("comicsansms",115)
                TextSurf = largeText.render('Game over', True, (255,255,255))
                self.win.blit(TextSurf, (WIN_WIDTH // 3 - 50  , WIN_HEIGHT // 3))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        model.events["game quit"] = True
                        end = False
                        break
                    elif event.type == pygame.KEYDOWN :
                        if event.key == pygame.K_r:  # Unpausing
                            end = False
                            break
                pygame.display.update()
                
    def draw_count_down(self,wait):
        #font= pygame.font.SysFont("comicsansms",100)
        font = pygame.font.Font(pygame.font.match_font('arial'), 100)
        count_down_text = font.render(str(wait), True, (255,255,255))
        count_down_rect = count_down_text.get_rect()
        surface = pygame.Surface((WIN_WIDTH, WIN_HEIGHT), pygame.SRCALPHA)
        transparency = 100
        pygame.draw.circle(surface, (128, 128, 128, transparency), (512,300),150)
        self.win.blit(surface, (0, 0))
        count_down_rect.center = (512,300)
        self.win.blit(count_down_text, count_down_rect)
        
    def draw_win(self, model):
#         largeText = pygame.font.SysFont("comicsansms",115)
#         TextSurf = largeText.render('You dead', True, (255,0,0))
#         self.win.blit(TextSurf, (WIN_WIDTH // 3 -50 , WIN_HEIGHT // 3))
        win = True
        pygame.init()
        pygame.font.init()
        while win:
                win = True
                #largeText = pygame.font.SysFont("comicsansms",115)
                largeText = pygame.font.Font(pygame.font.match_font('arial'), 115)
                TextSurf = largeText.render('You win', True, (255,255,255))
                self.win.blit(TextSurf, (WIN_WIDTH // 3 - 50  , WIN_HEIGHT // 3))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        model.events["game quit"] = True
                        win = False
                        break
                    elif event.type == pygame.KEYDOWN :
                        if event.key == pygame.K_r:  # Unpausing
                            win = False
                            break
                pygame.display.update()
