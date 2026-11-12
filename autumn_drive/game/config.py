"""Constantes e ajustes do jogo. Mexa aqui para balancear / personalizar."""

# --- Tela -----------------------------------------------------------------
W, H = 320, 240          # resolucao interna (pixel art)
SCALE = 3                # janela = W*SCALE x H*SCALE
FPS = 60

# --- Perspectiva ----------------------------------------------------------
HORIZON = 96             # linha do horizonte (px)
K = 100.0                # distancia de visao (unidades de pista)
RW = 1.25                # largura da pista na perspectiva
CK = 0.012               # intensidade das curvas na tela

# --- Gameplay -------------------------------------------------------------
MAX_SPEED = 40.0         # unidades/s (x6 = km/h mostrado)
OFFROAD_MAX_SPEED = 14.0
ACCEL = 18.0
BRAKE = 45.0
COAST_DECEL = 8.0
STEER_RATE = 2.2
CENTRIFUGAL = 1.1
LANES = (-0.75, -0.25, 0.25, 0.75)
TRAFFIC_COUNT = 16
START_TIME = 45.0
CHECKPOINT_DIST = 1200
CHECKPOINT_BONUS = 20
CRASH_SPEED_FACTOR = 0.25
CRASH_INVULN = 1.3

# --- Cores da pista -------------------------------------------------------
ROAD = ((36, 98, 104), (30, 86, 94))
GRASS = ((190, 60, 32), (150, 36, 36))
RUMBLE = ((250, 200, 50), (225, 120, 30))
LANE_LINE = (250, 215, 70)
