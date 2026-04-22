import os
import arcade
from sprite_animato import SpriteAnimato

FRAME_SIZE   = 96
RANGE_ATTACK = 96   # px davanti al player — modifica a piacere
_HERE        = os.path.dirname(os.path.abspath(__file__))


class Player(SpriteAnimato):

    ANIMAZIONI = [
        ("idle",   "assets/IDLE.png",      10,  0.8, True,  True),
        ("run",    "assets/RUN.png",        16,  0.5, True,  False),
        ("attack", "assets/ATTACK 1.png",    7,  0.3, False, False),
        ("hurt",   "assets/HURT.png",        4,  0.3, False, False),
    ]

    def __init__(self):
        super().__init__()
        self.facing_right = True
        self.locked       = False

        for nome, file, n_frame, durata, loop, default in self.ANIMAZIONI:
            percorso = os.path.join(_HERE, file)

            self.aggiungi_animazione(
                nome=nome + "_dx",
                percorso=percorso,
                frame_width=FRAME_SIZE, frame_height=FRAME_SIZE,
                num_frame=n_frame, colonne=n_frame,
                durata=durata,
                loop=loop,
                default=default,
            )
            self.aggiungi_animazione(
                nome=nome + "_sx",
                percorso=percorso,
                frame_width=FRAME_SIZE, frame_height=FRAME_SIZE,
                num_frame=n_frame, colonne=n_frame,
                durata=durata,
                loop=loop,
                default=default,
            )

        self.animazione_default = "idle_dx"

    def _anim(self, nome: str) -> str:
        return nome + ("_dx" if self.facing_right else "_sx")

    def get_attack_box(self) -> arcade.SpriteSolidColor:
        """
        Ritorna uno sprite invisibile posizionato davanti al player.
        Usalo in play.py per il check collisione invece del player stesso.
        """
        box = arcade.SpriteSolidColor(RANGE_ATTACK, self.height, color=(255, 0, 0, 0))
        if self.facing_right:
            box.center_x = self.center_x + self.width // 2 + RANGE_ATTACK // 2
        else:
            box.center_x = self.center_x - self.width // 2 - RANGE_ATTACK // 2
        box.center_y = self.center_y
        return box

    def trigger_attack(self):
        if not self.locked:
            self.locked = True
            self.imposta_animazione(self._anim("attack"))

    def trigger_hurt(self):
        self.locked = True
        self.imposta_animazione(self._anim("hurt"))

    def update_animation(self, delta_time=1/60):
        if self.change_x < 0:
            self.facing_right = False
        if self.change_x > 0:
            self.facing_right = True

        if not self.locked:
            if self.change_x != 0:
                self.imposta_animazione(self._anim("run"))
            else:
                self.imposta_animazione(self._anim("idle"))

        anim_prima = self.animazione_corrente
        super().update_animation(delta_time)

        if self.locked and self.animazione_corrente in ("idle_dx", "idle_sx"):
            self.locked = False