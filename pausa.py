import arcade
import arcade.gui
from gioco import WINDOW_HEIGHT, WINDOW_WIDTH
from play import GameView


class PauseView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        resume_button = arcade.gui.UIFlatButton(text="RIPRENDI",        width=200)
        menu_button   = arcade.gui.UIFlatButton(text="MENU PRINCIPALE", width=200)
        quit_button   = arcade.gui.UIFlatButton(text="ESCI",            width=200)

        resume_button.on_click = self.on_resume
        menu_button.on_click   = self.on_menu
        quit_button.on_click   = self.on_quit

        layout = arcade.gui.UIBoxLayout(spacing=20)
        layout.add(resume_button)
        layout.add(menu_button)
        layout.add(quit_button)

        self.manager.add(arcade.gui.UIAnchorLayout(children=[layout]))

        self.pausa_text = arcade.Text(
            "PAUSA",
            x=WINDOW_WIDTH // 2,
            y=WINDOW_HEIGHT // 2 + 200,
            color=arcade.color.WHITE,
            font_size=48,
            anchor_x="center",
            anchor_y="center",
        )

    def on_resume(self, event):
        self.window.show_view(self.game_view)

    def on_menu(self, event):
        from menu import MenuView
        self.window.show_view(MenuView())

    def on_quit(self, event):
        arcade.exit()

    def on_draw(self):
        self.game_view.on_draw()

        cam_x = self.game_view.camera.position[0]
        cam_y = self.game_view.camera.position[1]

        arcade.draw_rect_filled(
            arcade.XYWH(cam_x, cam_y, WINDOW_WIDTH, WINDOW_HEIGHT),
            (0, 0, 0, 150)
        )

        self.pausa_text.x = cam_x
        self.pausa_text.y = cam_y + 200
        self.pausa_text.draw()

        self.manager.draw()

    def on_hide_view(self):
        self.manager.disable()