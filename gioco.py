import arcade
import arcade.gui
import arcade.future.background as background
import os

# misure
WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080
WINDOW_TITLE = "Il mio gioco"
CAMERA_SPEED = 0.1
GRAVITY = 1

# menu
class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        play_button = arcade.gui.UIFlatButton(text="PLAY", width=200)
        quit_button = arcade.gui.UIFlatButton(text="ESCI", width=200)

        play_button.on_click = self.on_play
        quit_button.on_click = self.on_quit

        layout = arcade.gui.UIBoxLayout(spacing=20)
        layout.add(play_button)
        layout.add(quit_button)

        self.manager.add(arcade.gui.UIAnchorLayout(children=[layout]))

    def on_play(self, event):
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)

    def on_quit(self, event):
        arcade.exit()

    def on_draw(self):
        self.clear()
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)
        self.manager.draw()

    def on_hide_view(self):
        self.manager.disable()


# gioco
class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.scene = None
        self.physics_engine = None
        self.background_color = arcade.csscolor.CORNFLOWER_BLUE
        self.camera = arcade.Camera2D()
        self.backgrounds = background.ParallaxGroup()

        base_path = os.path.dirname(os.path.abspath(__file__))
        bg_size = (WINDOW_WIDTH, WINDOW_HEIGHT)

        # CORREZIONE PERCORSI
        self.backgrounds.add_from_file(os.path.join(base_path, "assets", "sfondo_gioco.png"), size=bg_size, depth=10.0)
        self.backgrounds.add_from_file(os.path.join(base_path, "assets", "sfondo_gioco.png"), size=(WINDOW_WIDTH, 500), depth=3.0)

        self.player_sprite = arcade.Sprite(os.path.join(base_path, "assets", "sfondo_gioco.png"), scale=0.5)
        self.x_velocity = 0

    def setup(self):
        self.scene = arcade.Scene()
        self.player_sprite.scale = 0.5
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 128
        self.scene.add_sprite("Player", self.player_sprite)

        self.scene.add_sprite_list("Walls", use_spatial_hash=True)

        base_path = os.path.dirname(os.path.abspath(__file__))

        # CORREZIONE PERCORSI
        for x in range(0, 12000, 64):
            wall = arcade.Sprite(os.path.join(base_path, "assets", "sfondo_gioco.png"), scale=0.5)
            wall.center_x = x
            wall.center_y = 32
            self.scene.add_sprite("Walls", wall)

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, walls=self.scene["Walls"], gravity_constant=GRAVITY
        )
        self.velocita = 4
        self.score = 0

    def on_draw(self):
        self.clear()
        self.camera.use()
        bg = self.backgrounds
        bg.offset = self.camera.bottom_left
        bg.pos = self.camera.bottom_left
        bg.draw()
        if self.scene:
            self.scene.draw()

    def pan_camera_to_player(self):
        self.camera.position = arcade.math.lerp_2d(
            self.camera.position,
            (self.player_sprite.center_x, self.window.height // 2),
            CAMERA_SPEED
        )

    def on_update(self, delta_time: float):
        if self.physics_engine:
            self.physics_engine.update()
        self.player_sprite.center_x += self.x_velocity * delta_time
        self.pan_camera_to_player()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(PauseView(self))
        if key == arcade.key.R:
            self.setup()
        if key == arcade.key.RIGHT:
            self.x_velocity = 200
        if key == arcade.key.LEFT:
            self.x_velocity = -200

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.RIGHT, arcade.key.LEFT):
            self.x_velocity = 0


# pausa
class PauseView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view

        # 🔥 Reset della camera quando entri in pausa
        self.game_view.camera.position = (self.window.width // 2, self.window.height // 2)

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        resume_button = arcade.gui.UIFlatButton(text="RIPRENDI", width=200)
        menu_button   = arcade.gui.UIFlatButton(text="MENU PRINCIPALE", width=200)
        quit_button   = arcade.gui.UIFlatButton(text="ESCI", width=200)

        resume_button.on_click = self.on_resume
        menu_button.on_click   = self.on_menu
        quit_button.on_click   = self.on_quit

        layout = arcade.gui.UIBoxLayout(spacing=20)
        layout.add(resume_button)
        layout.add(menu_button)
        layout.add(quit_button)

        self.manager.add(arcade.gui.UIAnchorLayout(children=[layout]))


    def on_resume(self, event):
        self.window.show_view(self.game_view)

    def on_menu(self, event):
        self.window.show_view(MenuView())

    def on_quit(self, event):
        arcade.exit()

    def on_draw(self):
        self.clear()

        # sfondo congelato
        self.game_view.camera.use()
        bg = self.game_view.backgrounds
        bg.offset = self.game_view.camera.bottom_left
        bg.pos = self.game_view.camera.bottom_left
        bg.draw()
        if self.game_view.scene:
            self.game_view.scene.draw()

        w = self.window.width
        h = self.window.height

        arcade.draw_rect_filled(
            arcade.XYWH(w // 2, h // 2, w, h),
            (0, 0, 0, 150)
        )
        arcade.draw_text(
            "PAUSA",
            w // 2,
            h // 2 + 150,
            arcade.color.WHITE,
            48,
            anchor_x="center",
            anchor_y="center"
        )
        self.manager.draw()

    def on_hide_view(self):
        self.manager.disable()


def main():
    global WINDOW_WIDTH, WINDOW_HEIGHT
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, fullscreen=True)
    WINDOW_WIDTH, WINDOW_HEIGHT = window.get_size()
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()

main()
