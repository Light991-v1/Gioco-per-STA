import arcade
import arcade.gui
from play import GameView

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
        from play import GameView   
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
