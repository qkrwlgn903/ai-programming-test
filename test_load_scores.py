from pathlib import Path
import pytest
from load_scores import load_scores

BASE_DIR = Path(__file__).resolve().parent


def test_정상_파일을_읽는다():
    kept, skipped = load_scores(str(BASE_DIR / "scores.csv"))
    assert len(kept) == 5


def test_빈_줄은_건너뛴다(tmp_path):
    csv_file = tmp_path / "blank_lines.csv"
    csv_file.write_text(
        "name,score\n\n김하나,88\n\n이둘,92\n\n",
        encoding="utf-8",
    )
    kept, skipped = load_scores(str(csv_file))
    assert len(kept) == 2


def test_이름에_쉼표가_있어도_읽는다(tmp_path):
    csv_file = tmp_path / "comma_name.csv"
    csv_file.write_text(
        'name,score\n"홍,길동",90\n',
        encoding="utf-8",
    )
    kept, skipped = load_scores(str(csv_file))
    assert len(kept) == 1
    assert kept[0][0] == "홍,길동"


def test_없는_파일이면_오류가_난다():
    with pytest.raises(FileNotFoundError):
        load_scores(str(BASE_DIR / "없는파일.csv"))


def test_헤더만_있으면_빈_결과():
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
def test_점수_경계값(tmp_path, score, expected_valid):
    csv_file = tmp_path / f"boundary_{score}.csv"
    csv_file.write_text(
        f"name,score\n테스트학생,{score}\n",
        encoding="utf-8",
    )
    kept, skipped = load_scores(str(csv_file))
    assert (len(kept) == 1) is expected_valid

def test_잘못된_점수_행은_건너뛴다(tmp_path):
    csv_file = tmp_path / "invalid_score.csv"
    csv_file.write_text(
        "name,score\n정상학생,80\n불량학생,abc\n",
        encoding="utf-8",
    )
    kept, skipped = load_scores(str(csv_file))
    assert len(kept) == 1
    assert len(skipped) >= 1