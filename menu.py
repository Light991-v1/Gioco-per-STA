import arcade
import arcade.gui
from play import GameView

class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        # ci fa accedere a lmeccanismo di pulsanti di arcade
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        # crea i due bottoni del menu principale
        play_button = arcade.gui.UIFlatButton(text="PLAY", width=200)
        quit_button = arcade.gui.UIFlatButton(text="ESCI", width=200)

        # collega ogni bottone alla sua funzione
        play_button.on_click = self.on_play
        quit_button.on_click = self.on_quit

        # metti i bottoni uno sotto l'altro
        layout = arcade.gui.UIBoxLayout(spacing=20)
        layout.add(play_button)
        layout.add(quit_button)

        # centra tutto in mezzo allo schermo
        self.manager.add(arcade.gui.UIAnchorLayout(children=[layout]))

    def on_play(self, event):
        # carica la schermata di gioco prendendola da play.py
        from play import GameView   
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)

    def on_quit(self, event):
        # chiudi il gioco
        arcade.exit()

    def on_draw(self):
        # pulisci lo schermo e rimette la personalizzazione del menu
        self.clear()
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)
        self.manager.draw()

    def on_hide_view(self):
        # quando esci dal menu tutti i pulsanto scoompaiono
        self.manager.disable()