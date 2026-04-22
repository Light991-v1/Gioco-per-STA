import arcade
import arcade.future.background as background
import os
import random
from player import Player
from nemici import Nemico, PAVIMENTO

CAMERA_SPEED  = 0.1
GRAVITY       = 1
PLAYER_SPEED      = 350
PLAYER_JUMP_SPEED = 15
PLAYER_SCALE      = 3
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
LEVEL_START = 0
LEVEL_END   = 9600

SPAWN_INTERVAL  = 7.0    # secondi tra uno spawn e l'altro
SPAWN_DISTANZA  = 300    # px tra player e nemico
SPAWN_DELAY     = 10.0   # primo spawn del nemico


class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.scene          = None
        self.physics_engine = None
        self.camera         = arcade.Camera2D()
        self.backgrounds    = background.ParallaxGroup()

        base_path = os.path.dirname(os.path.abspath(__file__))
        bg_size   = (WINDOW_WIDTH, WINDOW_HEIGHT)

        depths = [100, 50, 25, 12, 6, 3]
        for i, depth in enumerate(depths, start=1):
            self.backgrounds.add_from_file(
                os.path.join(base_path, "assets", f"sfondo{i}.png"),
                size=bg_size, depth=depth
            )

        self.left_pressed  = False
        self.right_pressed = False
        self.player_sprite = Player()

        # Nemici
        self.nemici: arcade.SpriteList = arcade.SpriteList()
        self.spawn_timer: float        = -SPAWN_DELAY
        self.player_hp: int            = 10
        self.nemici_uccisi: int        = 0
        self.gia_colpiti: set          = set()
        self._player_era_locked: bool  = False

    def setup(self):
        # crea la scena vuota dove poi spawnera il resto
        self.scene = arcade.Scene()

        # metti il giocatore a sinistra a una certa altezza
        self.player_sprite.center_x = 128
        self.player_sprite.center_y = 200
        self.player_sprite.scale    = PLAYER_SCALE
        self.scene.add_sprite("Player", self.player_sprite)

        self.scene.add_sprite_list("Walls", use_spatial_hash=True)

        base_path = os.path.dirname(os.path.abspath(__file__))
        # crea il pavimento basato sui limiti
        for x in range(LEVEL_START, LEVEL_END, 64):
            wall = arcade.Sprite(os.path.join(base_path, "assets", "sfondo_gioco.png"), scale=0.1)
            wall.center_x = x
            wall.center_y = 32
            self.scene.add_sprite("Walls", wall)

        # si attiva la grvita e le collisioni
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, walls=self.scene["Walls"], gravity_constant=GRAVITY
        )

    def _spawna_nemico(self):
        # qui sceglie una posizione tra 10 dove nascera il nemico
        for _ in range(10):
            lato = random.choice([-1, 1])
            x = self.player_sprite.center_x + lato * SPAWN_DISTANZA
            troppo_vicino = False
            # controlla che non nasca un nemico uno spra laltro
            for altro in self.nemici:
                if abs(altro.center_x - x) < 100:
                    troppo_vicino = True
                    break
            if not troppo_vicino:
                break
        # crea il nemico e lo aggiuge alla lista per tenerlo in mente
        nemico = Nemico(x, PAVIMENTO)
        nemico.scale = PLAYER_SCALE
        nemico.hp = 3
        self.nemici.append(nemico)

    def on_draw(self):
        self.clear()
        self.camera.use()
        # disegna gli sfondi parallax che si muovono a velocità diverse
        bg = self.backgrounds
        bg.offset = self.camera.bottom_left
        bg.pos    = self.camera.bottom_left
        bg.draw()
        self.scene.draw()
        # disegna i nemici sopra tutto il resto
        self.nemici.draw()

        # mostra i cuori della vita in alto a sinistra
        cuori = "❤️ " * self.player_hp
        arcade.draw_text(
            cuori,
            self.camera.position[0] - WINDOW_WIDTH // 2 + 20,
            self.camera.position[1] + WINDOW_HEIGHT // 2 - 50,
            arcade.color.RED,
            font_size=22,
        )
        # mostra il contatore dei nemici ammazzati in alto a destra
        arcade.draw_text(
            f"Nemici: {self.nemici_uccisi}/10",
            self.camera.position[0] + WINDOW_WIDTH // 2 - 180,
            self.camera.position[1] + WINDOW_HEIGHT // 2 - 50,
            arcade.color.WHITE,
            font_size=22,
        )

    def pan_camera_to_player(self):
        half_w = self.window.width  // 2
        half_h = self.window.height // 2

        target_x = self.player_sprite.center_x
        # la camera resta sempre alla stessa altezza, si muove solo orizzontalmente
        target_y = self.window.height // 2

        # non far andare la camera fuori dai bordi del livello
        target_x = max(half_w,             target_x)
        target_x = min(LEVEL_END - half_w, target_x)

        # muovi la camera piano piano verso il player (effetto smooth)
        self.camera.position = arcade.math.lerp_2d(
            self.camera.position,
            (target_x, target_y),
            CAMERA_SPEED,
        )

    def _update_player_velocity(self):
        # muovi il player a destra o sinistra in base ai tasti premuti
        if self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = PLAYER_SPEED / 60
        elif self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -PLAYER_SPEED / 60
        else:
            # nessun tasto premuto, il player si ferma
            self.player_sprite.change_x = 0

    def _clamp_player(self):
        # se il player va troppo a sinistra, rispingilo al bordo
        if self.player_sprite.left < LEVEL_START:
            self.player_sprite.left    = LEVEL_START
            self.player_sprite.change_x = 0
        # stesso ma per il bordo destro
        if self.player_sprite.right > LEVEL_END:
            self.player_sprite.right   = LEVEL_END
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):
        # aggiorna velocità, fisica e animazione del player ogni frame
        self._update_player_velocity()
        self.physics_engine.update()
        self._clamp_player()
        self.player_sprite.update_animation(delta_time)
        self.pan_camera_to_player()

        # specchia lo sprite del player a seconda di dove sta andando
        if self.player_sprite.change_x < 0:
            self.player_sprite.scale = (-PLAYER_SCALE, PLAYER_SCALE)
        elif self.player_sprite.change_x > 0:
            self.player_sprite.scale = (PLAYER_SCALE, PLAYER_SCALE)

        # conta il tempo e spawna un nemico ogni tot secondi
        self.spawn_timer += delta_time
        if self.spawn_timer >= SPAWN_INTERVAL:
            self.spawn_timer = 0.0
            self._spawna_nemico()

        # spingi i nemici lontano l'uno dall'altro se si sovrappongono
        for i, a in enumerate(self.nemici):
            for b in self.nemici[i+1:]:
                dist = a.center_x - b.center_x
                if abs(dist) < 80:
                    spinta = (80 - abs(dist)) / 2
                    if dist >= 0:
                        a.center_x += spinta
                        b.center_x -= spinta
                    else:
                        a.center_x -= spinta
                        b.center_x += spinta

        # fai muovere e animare tutti i nemici verso il player
        for nemico in self.nemici:
            nemico.update(self.player_sprite, delta_time)
            nemico.update_animation(delta_time)

            # specchia anche il nemico in base alla direzione
            if nemico.change_x < 0:
                nemico.scale = (-PLAYER_SCALE, PLAYER_SCALE)
            elif nemico.change_x > 0:
                nemico.scale = (PLAYER_SCALE, PLAYER_SCALE)

        # se un nemico sta attaccando e tocca il player, togli una vita
        for nemico in self.nemici:
            if nemico.locked and arcade.check_for_collision(nemico, self.player_sprite):
                if not self.player_sprite.locked:
                    self.player_sprite.trigger_hurt()
                    self.player_hp -= 1
                    # se la vita arriva a zero, mostra la schermata di morte
                    if self.player_hp <= 0:
                        from morte import MorteView
                        self.window.show_view(MorteView(self))

        # quando il player finisce di attaccare, svuota la lista dei nemici gia colpiti
        if self._player_era_locked and not self.player_sprite.locked:
            self.gia_colpiti.clear()
        self._player_era_locked = self.player_sprite.locked

        # se il player sta attaccando, guarda quali nemici vengono colpiti
        if self.player_sprite.locked:
            attack_box = self.player_sprite.get_attack_box()
            colpiti = arcade.check_for_collision_with_list(
                attack_box, self.nemici
            )
            for nemico in colpiti:
                # evita di colpire lo stesso nemico due volte nella stessa animaziome
                if id(nemico) not in self.gia_colpiti:
                    self.gia_colpiti.add(id(nemico))
                    nemico.trigger_hurt()
                    nemico.hp -= 1
                    if nemico.hp <= 0:
                        # rimuovi il nemico morto e aggiorna il conteggio
                        nemico.remove_from_sprite_lists()
                        self.nemici_uccisi += 1
                        # se ne hai uccisi 10 hai vinto, vai alla schermata vittoria
                        if self.nemici_uccisi >= 10:
                            from vittoria import VittoriaView
                            self.window.show_view(VittoriaView(self))

    def on_key_press(self, key, modifiers):
        # ESC apre il menu di pausa
        if key == arcade.key.ESCAPE:
            from pausa import PauseView
            self.window.show_view(PauseView(self))

        if key == arcade.key.D:
            self.right_pressed = True
        if key == arcade.key.A:
            self.left_pressed = True

        # W fa saltare il player solo se è a terra
        if key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED

    def on_key_release(self, key, modifiers):
        # quando lasci il tasto il player si ferma in quella direzione
        if key == arcade.key.D:
            self.right_pressed = False
        if key == arcade.key.A:
            self.left_pressed = False

    def on_mouse_press(self, x, y, key, modifiers):
        # click sinistro del mouse fa attaccare il player
        if key == arcade.MOUSE_BUTTON_LEFT:
            self.player_sprite.trigger_attack()