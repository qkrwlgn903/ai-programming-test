from pathlib import Path
import pytest
from load_scores import load_scores

BASE_DIR = Path(__file__).resolve().parent


def test_?뺤긽_?뚯씪???쎈뒗??):
    kept, skipped = load_scores(str(BASE_DIR / "scores.csv"))
    assert len(kept) == 5


def test_鍮?以꾩?_嫄대꼫?대떎(tmp_path):
    csv_file = tmp_path / "blank_lines.csv"
    csv_file.write_text(
        "name,score\n\n源?섎굹,88\n\n?대몮,92\n\n",
        encoding="utf-8",
    )
    kept, skipped = load_scores(str(csv_file))
    assert len(kept) == 2


def test_?대쫫???쇳몴媛_?덉뼱???쎈뒗??tmp_path):
    csv_file = tmp_path / "comma_name.csv"
    csv_file.write_text(
        'name,score\n"??湲몃룞",90\n',
        encoding="utf-8",
    )
    kept, skipped = load_scores(str(csv_file))
    assert len(kept) == 1
    assert kept[0][0] == "??湲몃룞"


def test_?녿뒗_?뚯씪?대㈃_?ㅻ쪟媛_?쒕떎():
    with pytest.raises(FileNotFoundError):
        load_scores(str(BASE_DIR / "?녿뒗?뚯씪.csv"))


def test_?ㅻ뜑留??덉쑝硫?鍮?寃곌낵():
    kept, skipped = load_scores(str(BASE_DIR / "empty.csv"))
    assert kept == []
    assert skipped == []


@pytest.mark.parametrize(
    "score, expected_valid",
    [
        (-1, False),
        (0, True),
        (1, True),
        (99, True),
        (100, True),
        (101, False),
    ],
)
def test_?먯닔_寃쎄퀎媛?tmp_path, score, expected_valid):
    csv_file = tmp_path / f"boundary_{score}.csv"
    csv_file.write_text(
        f"name,score\n?뚯뒪?명븰??{score}\n",
        encoding="utf-8",
    )
    kept, skipped = load_scores(str(csv_file))
    assert (len(kept) == 1) is expected_valid

def test_?섎せ???먯닔_?됱?_嫄대꼫?대떎(tmp_path):
    csv_file = tmp_path / "invalid_score.csv"
    csv_file.write_text(
        "name,score\n?뺤긽?숈깮,80\n遺덈웾?숈깮,abc\n",
        encoding="utf-8",
    )
    kept, skipped = load_scores(str(csv_file))
    assert len(kept) == 1
    assert len(skipped) >= 1
