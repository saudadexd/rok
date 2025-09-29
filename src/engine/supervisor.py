import time
from enum import Enum
from typing import Callable, Tuple

try:
    import cv2
    import numpy as np
except Exception:
    cv2 = None
    np = None

class ScreenState(Enum):
    GAME = "game"
    NOT_GAME = "not_game"
    EXIT = "exit"

class Supervisor:
    def __init__(self, capture_fn: Callable[[], object], templates: dict, match_threshold: float = 0.8, poll_interval: float = 1.0):
        """
        capture_fn: callable that returns a screenshot image (numpy array compatible with OpenCV) when called
        templates: dict with keys 'game' and 'exit' each mapping to template images (numpy arrays) or callables
        match_threshold: normalized cross-correlation eşik değeri
        poll_interval: NOT_GAME bekleme aralığı (saniye)
        """
        self.capture_fn = capture_fn
        self.templates = templates
        self.match_threshold = match_threshold
        self.poll_interval = poll_interval

    def _match_template(self, image, template) -> float:
        if cv2 is None or np is None:
            return 0.0
        res = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
        return float(res.max())

    def check(self) -> ScreenState:
        img = self.capture_fn()
        # template'lar callable olabilir
        game_tpl = self.templates.get("game")
        exit_tpl = self.templates.get("exit")
        game_conf = 0.0
        exit_conf = 0.0
        if callable(game_tpl):
            game_conf = game_tpl(img)
        elif game_tpl is not None:
            game_conf = self._match_template(img, game_tpl)
        if callable(exit_tpl):
            exit_conf = exit_tpl(img)
        elif exit_tpl is not None:
            exit_conf = self._match_template(img, exit_tpl)

        if game_conf >= self.match_threshold and exit_conf < self.match_threshold:
            return ScreenState.GAME
        if exit_conf >= self.match_threshold:
            return ScreenState.EXIT
        return ScreenState.NOT_GAME

    def wait_for_game_entry(self, timeout: float = None):
        start = time.time()
        while True:
            state = self.check()
            if state == ScreenState.GAME:
                time.sleep(2.0)  # oyun ekranına geçince 2s bekle
                return True
            if state == ScreenState.EXIT:
                # script durmalı, burada blocking bekleme
                while self.check() == ScreenState.EXIT:
                    time.sleep(self.poll_interval)
                continue
            # NOT_GAME: periyodik tekrar
            if timeout is not None and (time.time() - start) > timeout:
                return False
            time.sleep(self.poll_interval)
