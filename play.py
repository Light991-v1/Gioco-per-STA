import arcade
import arcade.future.background as background
import os
from player import Player

CAMERA_SPEED  = 0.1
GRAVITY       = 1
PLAYER_SPEED      = 250
PLAYER_JUMP_SPEED = 18
PLAYER_SCALE      = 2.5
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
LEVEL_START = 0       
LEVEL_END   = 9600    


class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.scene          = None
        self.physics_engine = None
        self.camera         = arcade.Camera2D()
        self.backgrounds    = background.ParallaxGroup()

        base_path = os.path.dirname(os.path.abspath(__file__))
        bg_size   = (WINDOW_WIDTH, WINDOW_HEIGHT)

        depths = [100, 50,25,12,6,3]
        for i, depth in enumerate(depths, start=1):
            self.backgrounds.add_from_file(
                os.path.join(base_path, "assets", f"sfondo{i}.png"),
                size=bg_size, depth=depth
            )

        self.left_pressed  = False
        self.right_pressed = False
        self.player_sprite = Player()

    def setup(self):
        self.scene = arcade.Scene()

        self.player_sprite.center_x = 128
        self.player_sprite.center_y = 200
        self.player_sprite.scale    = PLAYER_SCALE
        self.scene.add_sprite("Player", self.player_sprite)

        self.scene.add_sprite_list("Walls", use_spatial_hash=True)

        base_path = os.path.dirname(os.path.abspath(__file__))
        for x in range(LEVEL_START, LEVEL_END, 64):
            wall = arcade.Sprite(os.path.join(base_path, "assets", "sfondo_gioco.png"), scale=0.1)
            wall.center_x = x
            wall.center_y = 32
            self.scene.add_sprite("Walls", wall)

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, walls=self.scene["Walls"], gravity_constant=GRAVITY
        )

    def on_draw(self):
        self.clear()
        self.camera.use()
        bg = self.backgrounds
        bg.offset = self.camera.bottom_left
        bg.pos = self.camera.bottom_left
        bg.draw()
        self.scene.draw()

    def pan_camera_to_player(self):
        half_w = self.window.width  // 2
        half_h = self.window.height // 2

        target_x = self.player_sprite.center_x
        target_y = self.window.height // 2

        target_x = max(half_w,            target_x)
        target_x = min(LEVEL_END - half_w, target_x)

        self.camera.position = arcade.math.lerp_2d(
            self.camera.position,
            (target_x, target_y),
            CAMERA_SPEED,
        )

    def _update_player_velocity(self):
        if self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = PLAYER_SPEED / 60
        elif self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -PLAYER_SPEED / 60
        else:
            self.player_sprite.change_x = 0

    def _clamp_player(self):
        """Impedisce al personaggio di uscire dai bordi del livello."""
        half = self.player_sprite.width // 2
        if self.player_sprite.left < LEVEL_START:
            self.player_sprite.left = LEVEL_START
            self.player_sprite.change_x = 0
        if self.player_sprite.right > LEVEL_END:
            self.player_sprite.right = LEVEL_END
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):
        self._update_player_velocity()
        self.physics_engine.update()
        self._clamp_player()
        self.player_sprite.update_animation(delta_time)
        self.pan_camera_to_player()

        if self.player_sprite.change_x < 0: 
            self.player_sprite.scale = (-PLAYER_SCALE, PLAYER_SCALE)
        elif self.player_sprite.change_x > 0:
            self.player_sprite.scale = (PLAYER_SCALE, PLAYER_SCALE)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            from pausa import PauseView
            self.window.show_view(PauseView(self))

        if key == arcade.key.D:
            self.right_pressed = True
        if key == arcade.key.A:
            self.left_pressed = True

        if key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED

        if key == arcade.key.SPACE:
            self.player_sprite.trigger_attack()

    def on_key_release(self, key, modifiers):
        if key == arcade.key.D:
            self.right_pressed = False
        if key == arcade.key.A:
            self.left_pressed = False