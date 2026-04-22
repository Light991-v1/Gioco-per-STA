import os
import arcade
from sprite_animato import SpriteAnimato

FRAME_SIZE   = 96
RANGE_ATTACK = 80   # px davanti al player — modifica a piacere
_HERE        = os.path.dirname(os.path.abspath(__file__))


class Player(SpriteAnimato):

    # lista di tutte le animazioni del player con i loro parametri
    ANIMAZIONI = [
        ("idle",   "assets/IDLE.png",      10,  0.8, True,  True),
        ("run",    "assets/RUN.png",        16,  0.5, True,  False),
        ("attack", "assets/ATTACK 1.png",    7,  0.3, False, False),
        ("hurt",   "assets/HURT.png",        4,  0.3, False, False),
    ]

    def __init__(self):
        super().__init__()
        # il player guarda a destra all'inizio
        self.facing_right = True
        # locked = True significa che il player sta facendo un'azione che non si può interrompere
        self.locked       = False

        # carica ogni animazione due volte: una versione destra e una sinistra
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

        # l'animazione di riposo di base è quella che guarda a destra
        self.animazione_default = "idle_dx"

    def _anim(self, nome: str) -> str:
        # aggiunge _dx o _sx al nome dell'animazione in base a dove guarda il player
        return nome + ("_dx" if self.facing_right else "_sx")

    def get_attack_box(self) -> arcade.SpriteSolidColor:
        # crea un rettangolo invisibile davanti al player che rappresenta il colpo
        SPRITE_W = FRAME_SIZE * 3   # 96 * PLAYER_SCALE
        box = arcade.SpriteSolidColor(RANGE_ATTACK, FRAME_SIZE * 3, color=arcade.color.RED)
        # posiziona il rettangolo a destra o sinistra a seconda di dove guarda
        if self.facing_right:
            box.center_x = self.center_x + SPRITE_W // 2 + RANGE_ATTACK // 2
        else:
            box.center_x = self.center_x - SPRITE_W // 2 - RANGE_ATTACK // 2
        box.center_y = self.center_y
        return box

    def trigger_attack(self):
        # fai attaccare il player solo se non sta già facendo qualcosa
        if not self.locked:
            self.locked = True
            self.imposta_animazione(self._anim("attack"))

    def trigger_hurt(self):
        # fai fare l'animazione del dolore, blocca tutto il resto mentre dura
        self.locked = True
        self.imposta_animazione(self._anim("hurt"))

    def update_animation(self, delta_time=1/60):
        # aggiorna la direzione del player in base a dove si sta muovendo
        if self.change_x < 0:
            self.facing_right = False
        if self.change_x > 0:
            self.facing_right = True

        # se il player è libero di muoversi usa l'animazione giusta
        if not self.locked:
            if self.change_x != 0:
                # sta correndo, usa l'animazione di corsa
                self.imposta_animazione(self._anim("run"))
            else:
                # è fermo, usa l'animazione di riposo
                self.imposta_animazione(self._anim("idle"))

        anim_prima = self.animazione_corrente
        # fai avanzare l'animazione di un frame
        super().update_animation(delta_time)

        # se l'animazione di attacco o dolore è finita il player torna a stare in idle
        if self.locked and self.animazione_corrente in ("idle_dx", "idle_sx"):
            self.locked = False