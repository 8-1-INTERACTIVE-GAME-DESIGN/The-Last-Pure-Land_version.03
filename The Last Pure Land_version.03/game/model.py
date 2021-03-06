import pygame
import os
from tower.towers import Tower, Vacancy
from enemy.enemies import EnemyGroup
from fire import FireGroup
from menu.menus import UpgradeMenu, BuildMenu, MainMenu
from game.user_request import RequestSubject, TowerFactory, TowerSeller, TowerDeveloper, EnemyGenerator, Muse, Music, Pause, A_O_E,Heal
from settings import WIN_WIDTH, WIN_HEIGHT, BACKGROUND_IMAGE
clock = pygame.time.Clock()

class GameModel:
    def __init__(self):
        # data
        self.bg_image = pygame.transform.scale(BACKGROUND_IMAGE, (WIN_WIDTH, WIN_HEIGHT))
        self.__towers = []
        self.__enemies = EnemyGroup()
        self.__fire_balls = FireGroup()
        self.__menu = None
        self.__main_menu = MainMenu()
        self.__plots = [Vacancy(702, 483), Vacancy(555,412), Vacancy(663,290),Vacancy(816, 342),Vacancy(970, 328),Vacancy(839, 200),
                        Vacancy(722, 124), Vacancy(492,225), Vacancy(409,344),Vacancy(406, 490),Vacancy(224, 268)]
        self.wave_to_enemies = [20, 20, 40]
        self.count_down = 5
        self.count = 0
        self.attack = 0
        self.fire_attack = 0
        # selected item
        self.selected_plot = None
        self.selected_tower = None
        self.selected_button = None
        # apply observer pattern
        self.subject = RequestSubject(self)
        self.seller = TowerSeller(self.subject)
        self.developer = TowerDeveloper(self.subject)
        self.factory = TowerFactory(self.subject)
        self.generator = EnemyGenerator(self.subject)
        self.muse = Muse(self.subject)
        self.music = Music(self.subject)
        self.pause = Pause(self.subject)
        self.aoe = A_O_E(self.subject)
        self.heal = Heal(self.subject)
        #
        self.wave = 0
        self.money = 1000
        self.max_hp = 10
        self.hp = self.max_hp
        self.sound = pygame.mixer.Sound(os.path.join("sound", "background_01.wav"))
#       self.sound = pygame.mixer.Sound(os.path.join("sound", "switch.wav"))
    def user_request(self, user_request: str):
        """ add tower, sell tower, upgrade tower"""
        self.subject.notify(user_request)

    def get_request(self, events: dict) -> str:
        """get keyboard response or button response"""
        # initial
        self.selected_button = None
        # key event
        if events["keyboard key"] == pygame.K_n :
            if  self.enemies_is_empty() and self.count_down < 0:
                self.count_down = 5
                self.count = 0
            return "start new wave"
        # mouse event
        if events["mouse position"] is not None:
            x, y = events["mouse position"]
            self.select(x, y)
            if self.selected_button is not None:
                return self.selected_button.response
            return "nothing"
        return "nothing"

    def select(self, mouse_x: int, mouse_y: int) -> None:
        """change the state of whether the items are selected"""
        # if the item is clicked, select the item
        for tw in self.__towers:
            if tw.clicked(mouse_x, mouse_y):
                self.selected_tower = tw
                self.selected_plot = None
                return

        for pt in self.__plots:
            if pt.clicked(mouse_x, mouse_y):
                self.selected_tower = None
                self.selected_plot = pt
                return

        # if the button is clicked, get the button response.
        # and keep selecting the tower/plot.
        if self.__menu is not None:
            for btn in self.__menu.buttons:
                if btn.clicked(mouse_x, mouse_y):
                    self.selected_button = btn
            if self.selected_button is None:
                self.selected_tower = None
                self.selected_plot = None
        # menu btn
        for btn in self.__main_menu.buttons:
            if btn.clicked(mouse_x, mouse_y):
                self.selected_button = btn

    def call_menu(self):
        if self.selected_tower is not None:
            x, y = self.selected_tower.rect.center
            self.__menu = UpgradeMenu(x, y)
        elif self.selected_plot is not None:
            x, y = self.selected_plot.rect.center
            self.__menu = BuildMenu(x, y)
        else:
            self.__menu = None

    def towers_attack(self):
        for tw in self.__towers:
            tw.attack(self.__enemies.get())
            
    def enemies_advance(self):
        self.__enemies.advance(self)
        
    def fire_balls_advance(self):
        self.__fire_balls.advance(self)

    def enemies_is_empty(self):
        return True if self.enemies.is_empty() else False
    
    def fire_balls_are_empty(self):
        return True if self.fire_balls.is_empty() else False

    @property
    def fire_balls(self):
        return self.__fire_balls
    
    @property
    def enemies(self):
        return self.__enemies

    @property
    def towers(self):
        return self.__towers

    @property
    def menu(self):
        return self.__menu

    @menu.setter
    def menu(self, new_menu):
        self.__menu = new_menu

    @property
    def plots(self):
        return self.__plots
    










