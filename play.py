import arcade
import arcade.future.background as background
import os

WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080
CAMERA_SPEED = 0.1
GRAVITY = 1

class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.scene = None
        self.physics_engine = None
        self.camera = arcade.Camera2D()
        self.backgrounds = background.ParallaxGroup()

        base_path = os.path.dirname(os.path.abspath(__file__))
        bg_size = (WINDOW_WIDTH, WINDOW_HEIGHT)

        self.backgrounds.add_from_file(os.path.join(base_path, "assets", "sfondo1.png"), size=bg_size, depth=10.0)
        self.backgrounds.add_from_file(os.path.join(base_path, "assets", "sfondo2.png"), size=(WINDOW_WIDTH, 500), depth=3.0)

        self.player_sprite = arcade.Sprite(os.path.join(base_path, "assets", "sfondo_gioco.png"), scale=0.5)
        self.x_velocity = 0

    def setup(self):
        self.scene = arcade.Scene()
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 128
        self.scene.add_sprite("Player", self.player_sprite)

        self.scene.add_sprite_list("Walls", use_spatial_hash=True)

        base_path = os.path.dirname(os.path.abspath(__file__))
        for x in range(0, 12000, 64):
            wall = arcade.Sprite(os.path.join(base_path, "assets", "sfondo_gioco.png"), scale=0.5)
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
        self.camera.position = arcade.math.lerp_2d(
            self.camera.position,
            (self.player_sprite.center_x, self.window.height // 2),
            CAMERA_SPEED
        )

    def on_update(self, delta_time):
        self.physics_engine.update()
        self.player_sprite.center_x += self.x_velocity * delta_time
        self.pan_camera_to_player()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            from pausa import PauseView   # ← IMPORT QUI
            self.window.show_view(PauseView(self))

        if key == arcade.key.RIGHT:
            self.x_velocity = 200
        if key == arcade.key.LEFT:
            self.x_velocity = -200

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.RIGHT, arcade.key.LEFT):
            self.x_velocity = 0
