# This file contains the Tetris class. We are following a structure similar to the one we did in java. Where each class instantiates another class used for a small part of the game.

import math
from settings import *
from tetromino import Tetromino

class Tetris:
    def __init__(self, app):
        self.app = app
        self.sprite_group = pg.sprite.Group()
        self.field_array = self.make_field_array()
        self.tetromino = Tetromino(self)
        self.speed_up = False


    
    def check_full_lines(self):
        row = FIELD_HEIGHT - 1
        for y in range(FIELD_HEIGHT - 1, -1, -1):
            for x in range(FIELD_WIDTH):
                self.field_array[row][x] = self.field_array[y][x]
                if self.field_array[y][x]:
                    self.field_array[row][x].position = vec(x, y)

            if sum(map(bool, self.field_array[y])) < FIELD_WIDTH:
                row -= 1

            else:
                for x in range(FIELD_WIDTH):
                    self.field_array[row][x].alive = False
                    self.field_array[row][x] = 0
                self.app.score += FIELD_WIDTH

    def is_game_over(self):
        if any(self.field_array[0]):
            pg.time.wait(1000)
            return True

    def make_field_array(self):
        return [[0 for x in range(FIELD_WIDTH)] for y in range(FIELD_HEIGHT)]

    def put_tetromino_in_field_array(self):
        for block in self.tetromino.blocks:
            self.field_array[int(block.position.y)][int(block.position.x)] = block

    def check_tetromino_landing(self):
        if self.tetromino.landed:
            if self.is_game_over():
                # self.__init__(app=self.app)
                self.app.running = False
            self.put_tetromino_in_field_array()
            self.tetromino = Tetromino(self)
            self.speed_up = False

    def control(self, pressed_key):
        self.speed_up = False
        if pressed_key == pg.K_LEFT or pressed_key == pg.K_a:
            self.tetromino.move("left")
        elif pressed_key == pg.K_RIGHT or pressed_key == pg.K_d:
            self.tetromino.move("right")
        elif (
            pressed_key == pg.K_DOWN
            or pressed_key == pg.K_s
            or pressed_key == pg.K_SPACE
        ):
            self.speed_up = True
            # self.tetromino.move("down")
        elif pressed_key == pg.K_UP or pressed_key == pg.K_w:
            self.tetromino.rotate()
        else:
            self.speed_up = False

    def draw_grid(self):
        for x in range(FIELD_WIDTH):
            for y in range(FIELD_HEIGHT):
                pg.draw.rect(
                    self.app.screen,
                    pg.Color("gray"),
                    (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE),
                    width=1,
                    border_radius=1,
                )

    def update(self):
        if self.app.anim_trigger or (self.speed_up and self.app.fast_anim_trigger):
            self.check_full_lines()
            self.tetromino.update()
            self.check_tetromino_landing()
        self.sprite_group.update()
        
    def draw(self):
        self.draw_grid()
        self.sprite_group.draw(surface=self.app.screen)
