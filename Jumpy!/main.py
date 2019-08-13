#with help of KidsCanCode

import pygame as pg
import random
from os import path
from settings import *
from sprites import *

class Game:
    def __init__(self):
        #initialize the game, game window, etc.
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Jumpy!")
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.load_data()

    def load_data(self):
        #load highscore
        self.dirname = path.dirname(__file__)
        with open(path.join(self.dirname, HS_FILE), 'r') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0
        #load images
        img_dir = path.join(self.dirname, 'Graphics', 'Spritesheets')
        self.spritesheet = Spritesheet(path.join(img_dir, SPRITESHEET))
        #load cloud images
        self.cloud_images = []
        for i in range (1, 4):
            self.cloud_images.append(pg.image.load(path.join(self.dirname, 'Graphics', 'Clouds', 'cloud{}.png'.format(i))).convert())
        #load sound
        self.snd_dir = path.join(self.dirname, 'Sounds')
        self.jump_snd = pg.mixer.Sound(path.join(self.snd_dir, 'Jump1.wav'))
        self.boost_snd = pg.mixer.Sound(path.join(self.snd_dir, 'Boost1.wav'))

    def run(self):
        #Game loop
        pg.mixer.music.play(loops=-1)
        self.clock.tick(FPS)
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        pg.mixer.music.fadeout(500)

    def update(self):
        #update game loop
        self.all_sprites.update()

        #spawn a mob
        now = pg.time.get_ticks()
        if now - self.mob_timer > MOB_FRQ + random.choice([-1000, -500, 0, 500, 1000]):
            self.mob_timer = now
            Mob(self)

        #hit the mob
            #to improve speed at first rect collision, then mask collision
        mob_hits = pg.sprite.spritecollide(self.player, self.mobs, False, pg.sprite.collide_mask)
        if mob_hits:
            self.playing = False

        #check collison with platform, only if falling
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                for hit in hits:
                    lowest = hits[0]
                    if hit.rect.bottom > lowest.rect.centery:
                        lowest = hit
                if self.player.pos.x < lowest.rect.right + 10 and \
                    self.player.pos.x > lowest.rect.left - 10:
                    if self.player.pos.y < lowest.rect.bottom:
                        self.player.pos.y = lowest.rect.top
                        self.player.vel.y = 0
                        self.player.jumping = False
        #move camera if player reaches top 1/4 of the screen
        if self.player.rect.y <= HEIGHT / 4:
            self.player.pos.y += max(abs(self.player.vel.y), 2)
            if random.randrange(100) < 10:
                Cloud(self)
            for cloud in self.clouds:
                cloud.rect.y += max(abs(self.player.vel.y / cloud.scroll_vel_koef), 2)
            for mob in self.mobs:
                mob.rect.y += max(abs(self.player.vel.y), 2)
            for plat in self.platforms:
                plat.rect.y += max(abs(self.player.vel.y), 2)
                if plat.rect.top >= HEIGHT:
                    plat.kill()
                    self.score += 10

        #check collision with powerups
        pow_hits = pg.sprite.spritecollide(self.player, self.powerups, True)
        for pow in pow_hits:
            if pow.type == 'boost':
                self.boost_snd.play()
                self.player.vel.y = -BOOST_POWER
                self.player.jumping = False


        #if player dies
        if self.player.rect.top > HEIGHT:
            for spr in self.all_sprites:
                spr.rect.y -= max(self.player.vel.y, 10)
                if spr.rect.bottom < 0:
                    spr.kill()
            if len(self.platforms) == 0:
                self.playing = False
        #spawn new platforms
        while len(self.platforms) < 6:
            width = random.randrange(50, 100)
            Platform(self, random.randrange(0, WIDTH - width),
                    random.randrange(-80, -10))

    def events(self):
        #events game loop
        for event in pg.event.get():
            #check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()
            if event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                    self.player.jump_cut()

    def draw(self):
        #draw game
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.score), 22, WHITE, WIDTH / 2, 20)
        #at the very end
        pg.display.flip()

    def new(self):
        #create new game
        self.score = 0
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.platforms = pg.sprite.Group()
        self.powerups = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.clouds = pg.sprite.Group()
        self.player = Player(self)
        for pl in PLATFORM_LIST:
            Platform(self, *pl)
        self.mob_timer = 0
        for i in range(5):
            c = Cloud(self)
            c.rect.y += 500
        song_name = random.choice([
                                'Avicii - Wake Me Up.ogg',
                                'Imagine Dragons - Tiptoe.ogg'])
        pg.mixer.music.load(path.join(self.snd_dir, song_name))
        pg.mixer.music.set_volume(0.3)
        self.run()

    def show_start_screen(self):
        #show game start screen
        pg.mixer.music.load(path.join(self.snd_dir, 'Of Monsters And Men - Little Talks.ogg'))
        pg.mixer.music.set_volume(0.3)
        pg.mixer.music.play(loops=-1)
        self.screen.fill(BGCOLOR)
        self.draw_text(TITLE, 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Arrows to move, Space to jump", 24, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press a key to play", 24, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        self.draw_text("High score: " + str(self.highscore),
                       24, WHITE, WIDTH / 2, 15)
        pg.display.flip()
        self.wait_for_key()
        pg.mixer.music.fadeout(500)

    def show_go_screen(self):
        #show game over show_go_screen
        pg.mixer.music.load(path.join(self.snd_dir, 'Of Monsters And Men - Little Talks.ogg'))
        pg.mixer.music.set_volume(0.3)
        pg.mixer.music.play(loops=-1)
        if not self.running:
            return
        self.screen.fill(BGCOLOR)
        self.draw_text("Game over", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Score: " + str(self.score), 24, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press a key to play again", 24, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("NEW HIGH SCORE!", 32, WHITE, WIDTH / 2, HEIGHT / 2 + 40)
            with open(path.join(self.dirname, HS_FILE), "w") as f:
                f.write(str(self.score))
        else:
                self.draw_text("High score: " + str(self.highscore),
                               24, WHITE, WIDTH / 2, 15)
        pg.display.flip()
        self.wait_for_key()
        pg.mixer.music.fadeout(500)

    def wait_for_key(self):
        #waiting for pressed key to start Game
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False

    def draw_text(self, text, size, color, x, y):
        #draw text on the screen
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()
