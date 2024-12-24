from project import create_text, write_score_to_file, get_highscore_from_file
import pytest
from constants import *

font = pygame.font.SysFont("monospace", 16)
screen = pygame.display.set_mode((100,100))
filepath = "test_scores.csv"

def test_create_text():
    with pytest.raises(TypeError):
        create_text(["Text", "to", "render"], font, "black", (0,0), screen)

    with pytest.raises(ValueError):
        create_text("Text to render", font, "invalid_color", (0,0), screen)
        create_text("Text to render", font, "black", -1, screen)


def test_write_score_to_file():
    with pytest.raises(TypeError):
        write_score_to_file(filepath, "name", None)


def test_get_highscore_from_file():
    get_highscore_from_file("DNE.csv")
    assert HIGH_SCORE == 0