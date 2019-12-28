import pygame as pg

from Const import *


class Player(object):
    def __init__(self, x_pos, y_pos):
        self.numOfLives = 3
        self.score = 0
        self.coins = 0

        self.visible = True
        self.spriteTick = 0
        self.powerLVL = 0

        self.unkillable = False
        self.unkillableTime = 0

        self.inLevelUpAnimation = False
        self.inLevelUpAnimationTime = 0
        self.inLevelDownAnimation = False
        self.inLevelDownAnimationTime = 0

        self.already_jumped = False
        self.next_jump_time = 0
        self.next_fireball_time = 0
        self.x_vel = 0
        self.y_vel = 0
        self.direction = True
        self.on_ground = False
        self.fast_moving = False
        
        self.pos_x = x_pos

        self.image = pg.image.load('images/mario/mario.png').convert_alpha()
        self.sprites = []
        self.load_sprites()

        self.rect = pg.Rect(x_pos, y_pos, 32, 32)

    def load_sprites(self):
        self.sprites = [
            # 0 Small, stay
            pg.image.load('images/Mario/mario.png'),

            # 1 Small, move 0
            pg.image.load('images/Mario/mario_move0.png'),

            # 2 Small, move 1
            pg.image.load('images/Mario/mario_move1.png'),

            # 3 Small, move 2
            pg.image.load('images/Mario/mario_move2.png'),

            # 4 Small, jump
            pg.image.load('images/Mario/mario_jump.png'),

            # 5 Small, end 0
            pg.image.load('images/Mario/mario_end.png'),

            # 6 Small, end 1
            pg.image.load('images/Mario/mario_end1.png'),

            # 7 Small, stop
            pg.image.load('images/Mario/mario_st.png'),

            # =============================================

            # 8 Big, stay
            pg.image.load('images/Mario/mario1.png'),

            # 9 Big, move 0
            pg.image.load('images/Mario/mario1_move0.png'),

            # 10 Big, move 1
            pg.image.load('images/Mario/mario1_move1.png'),

            # 11 Big, move 2
            pg.image.load('images/Mario/mario1_move2.png'),

            # 12 Big, jump
            pg.image.load('images/Mario/mario1_jump.png'),

            # 13 Big, end 0
            pg.image.load('images/Mario/mario1_end.png'),

            # 14 Big, end 1
            pg.image.load('images/Mario/mario1_end1.png'),

            # 15 Big, stop
            pg.image.load('images/Mario/mario1_st.png'),

            # =============================================

            # 16 Big_fireball, stay
            pg.image.load('images/Mario/mario2.png'),

            # 17 Big_fireball, move 0
            pg.image.load('images/Mario/mario2_move0.png'),

            # 18 Big_fireball, move 1
            pg.image.load('images/Mario/mario2_move1.png'),

            # 19 Big_fireball, move 2
            pg.image.load('images/Mario/mario2_move2.png'),

            # 20 Big_fireball, jump
            pg.image.load('images/Mario/mario2_jump.png'),

            # 21 Big_fireball, end 0
            pg.image.load('images/Mario/mario2_end.png'),

            # 22 Big_fireball, end 1
            pg.image.load('images/Mario/mario2_end1.png'),

            # 23 Big_fireball, stop
            pg.image.load('images/Mario/mario2_st.png'),
        ]

        # Left side
        for i in range(len(self.sprites)):
            self.sprites.append(pg.transform.flip(self.sprites[i], 180, 0))

        # Power level changing, right
        self.sprites.append(pg.image.load('images/Mario/mario_lvlup.png').convert_alpha())

        # Power level changing, left
        self.sprites.append(pg.transform.flip(self.sprites[-1], 180, 0))

        # Death
        self.sprites.append(pg.image.load('images/Mario/mario_death.png').convert_alpha())

    def update(self, core):
        self.player_physics(core)
        self.update_image(core)
        self.update_unkillable_time()

    def player_physics(self, core):
        if core.keyR:
            self.x_vel += SPEED_INCREASE_RATE
            self.direction = True
        if core.keyL:
            self.x_vel -= SPEED_INCREASE_RATE
            self.direction = False
        if not core.keyU:
            self.already_jumped = False
        elif core.keyU:
            if self.on_ground and not self.already_jumped:
                self.y_vel = -JUMP_POWER
                self.already_jumped = True
                self.next_jump_time = pg.time.get_ticks() + 750
                if self.powerLVL >= 1:
                    core.get_sound().play('big_mario_jump', 0, 0.5)
                else:
                    core.get_sound().play('small_mario_jump', 0, 0.5)

        # Fireball shoot and fast moving
        self.fast_moving = False
        if core.keyShift:
            self.fast_moving = True
            if self.powerLVL == 2:
                if pg.time.get_ticks() > self.next_fireball_time:
                    if not (self.inLevelUpAnimation or self.inLevelDownAnimation):
                        if len(core.get_map().projectiles) < 2:
                            self.shoot_fireball(core, self.rect.x, self.rect.y, self.direction)

        if not (core.keyR or core.keyL):
            if self.x_vel > 0:
                self.x_vel -= SPEED_DECREASE_RATE
            elif self.x_vel < 0:
                self.x_vel += SPEED_DECREASE_RATE
        else:
            if self.x_vel > 0:
                if self.fast_moving:
                    if self.x_vel > MAX_FASTMOVE_SPEED:
                        self.x_vel = MAX_FASTMOVE_SPEED
                else:
                    if self.x_vel > MAX_MOVE_SPEED:
                        self.x_vel = MAX_MOVE_SPEED
            if self.x_vel < 0:
                if self.fast_moving:
                    if (-self.x_vel) > MAX_FASTMOVE_SPEED: self.x_vel = -MAX_FASTMOVE_SPEED
                else:
                    if (-self.x_vel) > MAX_MOVE_SPEED:
                        self.x_vel = -MAX_MOVE_SPEED

        # removing the computational error
        if 0 < self.x_vel < SPEED_DECREASE_RATE:
            self.x_vel = 0
        if 0 > self.x_vel > -SPEED_DECREASE_RATE:
            self.x_vel = 0

        if not self.on_ground:
            # Moving up, button is pressed
            if (self.y_vel < 0 and core.keyU):
                self.y_vel += GRAVITY
                
            # Moving up, button is not pressed - low jump
            elif (self.y_vel < 0 and not core.keyU):
                self.y_vel += GRAVITY * LOW_JUMP_MULTIPLIER
            
            # Moving down
            else:
                self.y_vel += GRAVITY * FALL_MULTIPLIER
            
            if self.y_vel > MAX_FALL_SPEED:
                self.y_vel = MAX_FALL_SPEED

        blocks = core.get_map().get_blocks_for_collision(self.rect.x // 32, self.rect.y // 32)
        
        self.pos_x += self.x_vel
        self.rect.x = self.pos_x
        
        self.update_x_pos(blocks)

        self.rect.y += self.y_vel
        self.update_y_pos(blocks, core)

        # on_ground parameter won't be stable without this piece of code
        coord_y = self.rect.y // 32
        if self.powerLVL > 0:
            coord_y += 1
        for block in core.get_map().get_blocks_below(self.rect.x // 32, coord_y):
            if block != 0 and block.type != 'BGObject':
                if pg.Rect(self.rect.x, self.rect.y + 1, self.rect.w, self.rect.h).colliderect(block.rect):
                    self.on_ground = True

        # Map border check
        if self.rect.y > 448:
            core.get_map().player_death(core)

        # End Flag collision check
        if self.rect.colliderect(core.get_map().flag.pillar_rect):
            core.get_map().player_win(core)

    def set_image(self, image_id):

        # "Dead" sprite
        if image_id == len(self.sprites):
            self.image = self.sprites[-1]

        elif self.direction:
            self.image = self.sprites[image_id + self.powerLVL * 8]
        else:
            self.image = self.sprites[image_id + self.powerLVL * 8 + 24]

    def update_image(self, core):

        self.spriteTick += 1
        if (core.keyShift):
            self.spriteTick += 1

        if self.powerLVL in (0, 1, 2):

            if self.x_vel == 0:
                self.set_image(0)
                self.spriteTick = 0

            # Player is running
            elif (
                    ((self.x_vel > 0 and core.keyR and not core.keyL) or
                     (self.x_vel < 0 and core.keyL and not core.keyR)) or
                    (self.x_vel > 0 and not (core.keyL or core.keyR)) or
                    (self.x_vel < 0 and not (core.keyL or core.keyR))
            ):
                             
                if (self.spriteTick > 30):
                    self.spriteTick = 0
                   
                if self.spriteTick <= 10:
                    self.set_image(1)
                elif 11 <= self.spriteTick <= 20:
                    self.set_image(2)
                elif 21 <= self.spriteTick <= 30:
                    self.set_image(3)
                elif self.spriteTick == 31:
                    self.spriteTick = 0
                    self.set_image(1)

            # Player decided to move in the another direction, but hasn't stopped yet
            elif (self.x_vel > 0 and core.keyL and not core.keyR) or (self.x_vel < 0 and core.keyR and not core.keyL):
                self.set_image(7)
                self.spriteTick = 0

            if not self.on_ground:
                self.spriteTick = 0
                self.set_image(4)

    def update_unkillable_time(self):
        if self.unkillable:
            self.unkillableTime -= 1
            if self.unkillableTime == 0:
                self.unkillable = False

    def update_x_pos(self, blocks):
        for block in blocks:
            if block != 0 and block.type != 'BGObject':
                block.debugLight = True
                if pg.Rect.colliderect(self.rect, block.rect):
                    if self.x_vel > 0:
                        self.rect.right = block.rect.left
                        self.pos_x = self.rect.left
                        self.x_vel = 0
                    elif self.x_vel < 0:
                        self.rect.left = block.rect.right
                        self.pos_x = self.rect.left
                        self.x_vel = 0

    def update_y_pos(self, blocks, core):
        self.on_ground = False
        for block in blocks:
            if block != 0 and block.type != 'BGObject':
                if pg.Rect.colliderect(self.rect, block.rect):

                    if self.y_vel > 0:
                        self.on_ground = True
                        self.rect.bottom = block.rect.top
                        self.y_vel = 0

                    elif self.y_vel < 0:
                        self.rect.top = block.rect.bottom
                        self.y_vel = -self.y_vel / 3
                        self.activate_block_action(core, block)

    def activate_block_action(self, core, block):
        # Question Block
        if block.typeID == 22:
            core.get_sound().play('block_hit', 0, 0.5)
            if not block.isActivated:
                block.spawn_bonus(core)

        # Brick Platform
        elif block.typeID == 23:
            if self.powerLVL == 0:
                block.shaking = True
                core.get_sound().play('block_hit', 0, 0.5)
            else:
                block.destroy(core)
                core.get_sound().play('brick_break', 0, 0.5)
                self.add_score(50)

    def reset(self, reset_all):
        self.direction = True
        self.rect.x = 96
        self.pos_x = 96
        self.rect.y = 351
        if self.powerLVL != 0:
            self.powerLVL = 0
            self.rect.y += 32
            self.rect.h = 32

        if reset_all:
            self.score = 0
            self.coins = 0
            self.numOfLives = 3

            self.visible = True
            self.spriteTick = 0
            self.powerLVL = 0
            self.inLevelUpAnimation = False
            self.inLevelUpAnimationTime = 0

            self.unkillable = False
            self.unkillableTime = 0

            self.inLevelDownAnimation = False
            self.inLevelDownAnimationTime = 0

            self.already_jumped = False
            self.x_vel = 0
            self.y_vel = 0
            self.on_ground = False

    def reset_jump(self):
        self.y_vel = 0
        self.already_jumped = False

    def reset_move(self):
        self.x_vel = 0
        self.y_vel = 0

    def jump_on_mob(self):
        self.already_jumped = True
        self.y_vel = -4
        self.rect.y -= 6

    def set_powerlvl(self, power_lvl, core):
        if self.powerLVL == 0 == power_lvl and not self.unkillable:
            core.get_map().player_death(core)
            self.inLevelUpAnimation = False
            self.inLevelDownAnimation = False

        elif self.powerLVL == 0 and self.powerLVL < power_lvl:
            self.powerLVL = 1
            core.get_sound().play('mushroom_eat', 0, 0.5)
            core.get_map().spawn_score_text(self.rect.x + 16, self.rect.y, score=1000)
            self.add_score(1000)
            self.inLevelUpAnimation = True
            self.inLevelUpAnimationTime = 61

        elif self.powerLVL == 1 and self.powerLVL < power_lvl:
            core.get_sound().play('mushroom_eat', 0, 0.5)
            core.get_map().spawn_score_text(self.rect.x + 16, self.rect.y, score=1000)
            self.add_score(1000)
            self.powerLVL = 2

        elif self.powerLVL > power_lvl:
            core.get_sound().play('pipe', 0, 0.5)
            self.inLevelDownAnimation = True
            self.inLevelDownAnimationTime = 200
            self.unkillable = True
            self.unkillableTime = 200

        else:
            core.get_sound().play('mushroom_eat', 0, 0.5)
            core.get_map().spawn_score_text(self.rect.x + 16, self.rect.y, score=1000)
            self.add_score(1000)

    def change_powerlvl_animation(self):

        if self.inLevelDownAnimation:
            self.inLevelDownAnimationTime -= 1

            if self.inLevelDownAnimationTime == 0:
                self.inLevelDownAnimation = False
                self.visible = True
            elif self.inLevelDownAnimationTime % 20 == 0:
                if self.visible:
                    self.visible = False
                else:
                    self.visible = True
                if self.inLevelDownAnimationTime == 100:
                    self.powerLVL = 0
                    self.rect.y += 32
                    self.rect.h = 32

        elif self.inLevelUpAnimation:
            self.inLevelUpAnimationTime -= 1

            if self.inLevelUpAnimationTime == 0:
                self.inLevelUpAnimation = False
                self.rect.y -= 32
                self.rect.h = 64

            elif self.inLevelUpAnimationTime in (60, 30):
                self.image = self.sprites[-3] if self.direction else self.sprites[-2]
                self.rect.y -= 16
                self.rect.h = 48

            elif self.inLevelUpAnimationTime in (45, 15):
                self.image = self.sprites[0] if self.direction else self.sprites[24]
                self.rect.y += 16
                self.rect.h = 32

    def flag_animation_move(self, core, walk_to_castle):
        if walk_to_castle:
            self.direction = True

            if not self.on_ground:
                self.y_vel += GRAVITY if self.y_vel <= MAX_FALL_SPEED else 0

            x = self.rect.x // 32
            y = self.rect.y // 32
            blocks = core.get_map().get_blocks_for_collision(x, y)

            self.rect.x += self.x_vel
            if self.rect.colliderect(core.get_map().map[205][11]):
                self.visible = False
                core.get_map().get_event().player_in_castle = True
            self.update_x_pos(blocks)

            self.rect.top += self.y_vel
            self.update_y_pos(blocks, core)

            # on_ground works incorrect without this piece of code
            x = self.rect.x // 32
            y = self.rect.y // 32
            if self.powerLVL > 0:
                y += 1
            for block in core.get_map().get_blocks_below(x, y):
                if block != 0 and block.type != 'BGObject':
                    if pg.Rect(self.rect.x, self.rect.y + 1, self.rect.w, self.rect.h).colliderect(block.rect):
                        self.on_ground = True

        else:
            if core.get_map().flag.flag_rect.y + 20 > self.rect.y + self.rect.h:
                self.rect.y += 3

    def shoot_fireball(self, core, x, y, move_direction):
        core.get_map().spawn_fireball(x, y, move_direction)
        core.get_sound().play('fireball', 0, 0.5)
        self.next_fireball_time = pg.time.get_ticks() + 400

    def add_coins(self, count):
        self.coins += count

    def add_score(self, count):
        self.score += count

    def render(self, core):
        if self.visible:
            core.screen.blit(self.image, core.get_map().get_camera().apply(self))
