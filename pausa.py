import arcade
import arcade.gui
from gioco import (WINDOW_HEIGHT,WINDOW_WIDTH)
from play import GameView


class PauseView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view

        

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
        from menu import MenuView   # ← IMPORT QUI
        self.window.show_view(MenuView())

    def on_quit(self, event):
        arcade.exit()

    def on_draw(self):
        self.game_view.on_draw()
        

        
        bg = self.game_view.backgrounds
        
        
        bg.draw()
        self.game_view.scene.draw()

        w = self.window.width
        h = self.window.height

        arcade.draw_rect_filled(
            arcade.XYWH(self.position, WINDOW_HEIGHT / 2, WINDOW_WIDTH, WINDOW_HEIGHT),
            (0, 0, 0, 150)
        )
        self.pause_text.draw()
        self.manager.draw()

    def on_update(self, delta_time):
        self.game_view.on_update(delta_time)
        self.pause_text=arcade.Text("PAUSA", x=self.game_view.player_sprite.center_x, y = WINDOW_HEIGHT/2 + 200, color = arcade.color.WHITE, font_name = "Broadway BT", font_size = 48, anchor_x="center", anchor_y="center")
        self.position = self.game_view.player_sprite.center_x

    def on_hide_view(self):
        self.manager.disable()
