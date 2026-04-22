import arcade
import arcade.gui
from gioco import WINDOW_HEIGHT, WINDOW_WIDTH
from play import GameView


class PauseView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        # tieniti una copia del gioco per usarlo come sfondo 
        self.game_view = game_view

        # ci fa accedere a lmeccanismo di pulsanti di arcade
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        # crea i tre bottoni del menu di pausa
        resume_button = arcade.gui.UIFlatButton(text="RIPRENDI",        width=200)
        menu_button   = arcade.gui.UIFlatButton(text="MENU PRINCIPALE", width=200)
        quit_button   = arcade.gui.UIFlatButton(text="ESCI",            width=200)

        # collega ogni bottone alla sua funzione
        resume_button.on_click = self.on_resume
        menu_button.on_click   = self.on_menu
        quit_button.on_click   = self.on_quit

        # impila i bottoni in colonna con spazio tra loro
        layout = arcade.gui.UIBoxLayout(spacing=20)
        layout.add(resume_button)
        layout.add(menu_button)
        layout.add(quit_button)

        # centra tutto in mezzo allo schermo
        self.manager.add(arcade.gui.UIAnchorLayout(children=[layout]))

        # prepara la scritta PAUSA grande in alto, sopra ai botoni
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
        # torna al gioco che era in corso
        self.window.show_view(self.game_view)

    def on_menu(self, event):
        # torna al menu ed elimina la vecchia partita
        from menu import MenuView
        self.window.show_view(MenuView())

    def on_quit(self, event):
        # chiudi tutto
        arcade.exit()

    def on_draw(self):
        # prima disegna il gioco sotto come se stesse girando normalmente
        self.game_view.on_draw()

        # prendi la posizione attuale della camera per disegnare nel posto giusto
        cam_x = self.game_view.camera.position[0]
        cam_y = self.game_view.camera.position[1]

        # metti un rettangolo nero semitrasparente sopra il gioco per scurirlo
        arcade.draw_rect_filled(
            arcade.XYWH(cam_x, cam_y, WINDOW_WIDTH, WINDOW_HEIGHT),
            (0, 0, 0, 150)
        )

        # sposta la scritta PAUSA dove punta la camera e disegnala
        self.pausa_text.x = cam_x
        self.pausa_text.y = cam_y + 200
        self.pausa_text.draw()

        # disegna i bottoni sopra a tutto
        self.manager.draw()

    def on_hide_view(self):
        # quando esci dalla pausa spegni i bottoni
        self.manager.disable()