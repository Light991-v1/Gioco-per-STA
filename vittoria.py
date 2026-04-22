import arcade
import arcade.gui
from gioco import WINDOW_HEIGHT, WINDOW_WIDTH


class VittoriaView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        # tieniti una copia del gioco per usarlo come sfondo 
        self.game_view = game_view

        # ci fa accedere a lmeccanismo di pulsanti di arcade
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        # crea i tre bottoni della schermata di vittoria
        riprendi_button = arcade.gui.UIFlatButton(text="RIAVVIA",        width=200)
        menu_button     = arcade.gui.UIFlatButton(text="MENU PRINCIPALE", width=200)
        quit_button     = arcade.gui.UIFlatButton(text="ESCI",            width=200)

        # collega ogni bottone alla sua funzione
        riprendi_button.on_click = self.on_riprendi
        menu_button.on_click     = self.on_menu
        quit_button.on_click     = self.on_quit

        # impila i bottoni in colonna con spazio tra loro
        layout = arcade.gui.UIBoxLayout(spacing=20)
        layout.add(riprendi_button)
        layout.add(menu_button)
        layout.add(quit_button)

        # centra tutto in mezzo allo schermo
        self.manager.add(arcade.gui.UIAnchorLayout(children=[layout]))

        # prepara la scritta HAI VINTO in giallo dorato grande in alto
        self.titolo = arcade.Text(
            "HAI VINTO!",
            x=WINDOW_WIDTH // 2,
            y=WINDOW_HEIGHT // 2 + 200,
            color=arcade.color.GOLD,
            font_size=48,
            anchor_x="center",
            anchor_y="center",
        )

    def on_riprendi(self, event):
        # ricomincia la partita da capo con tutto resettato
        from play import GameView
        view = GameView()
        self.window.show_view(view)
        # setup viene chiamato dopo show_view, stesso ordine strano di morte.py
        view.setup()

    def on_menu(self, event):
        # torna al menu principale e lascia perdere la partita corrente
        from menu import MenuView
        self.window.show_view(MenuView())

    def on_quit(self, event):
        # chiudi il gioco
        arcade.exit()

    def on_draw(self):
        # prima disegna il gioco congelato sotto come sfondo
        self.game_view.on_draw()

        # prendi la posizione della camera per disegnare nel posto giusto
        cam_x = self.game_view.camera.position[0]
        cam_y = self.game_view.camera.position[1]

        # metti un velo nero semitrasparente sopra il gioco per scurirlo un po
        arcade.draw_rect_filled(
            arcade.XYWH(cam_x, cam_y, WINDOW_WIDTH, WINDOW_HEIGHT),
            (0, 0, 0, 150)
        )

        # sposta la scritta dove punta la camera e disegnala
        self.titolo.x = cam_x
        self.titolo.y = cam_y + 200
        self.titolo.draw()

        # disegna i bottoni sopra a tutto il resto
        self.manager.draw()

    def on_hide_view(self):
        # quando esci da questa schermata spegni i bottoni
        self.manager.disable()