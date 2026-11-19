import pytest

from load_scores import load_scores


def test_유효한_점수와_중복_이름을_모두_유지한다(tmp_path):
    csv_file = tmp_path / "scores.csv"
    csv_file.write_text(
        "name,score\n"
        "  김하나  , 88 \n"
        "김하나,92\n",
        encoding="utf-8",
    )

    kept, skipped = load_scores(csv_file)

    assert kept == [("김하나", 88), ("김하나", 92)]
    assert skipped == []


def test_헤더만_있는_파일은_빈_결과를_반환한다(tmp_path):
    csv_file = tmp_path / "header_only.csv"
    csv_file.write_text("name,score\n", encoding="utf-8")

    assert load_scores(csv_file) == ([], [])


def test_파일이_없으면_FileNotFoundError가_발생한다(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_scores(tmp_path / "missing.csv")


def test_잘못된_행을_건너뛰고_행번호와_사유를_기록한다(tmp_path):
    csv_file = tmp_path / "invalid_rows.csv"
    csv_file.write_text(
        "name,score\n"
        "정상학생,80\n"
        "\n"
        "열하나\n"
        "열이,셋,개\n"
        " ,80\n"
        "점수없음, \n"
        "문자점수,abc\n"
        "최솟값초과,-1\n"
        "최댓값초과,101\n",
        encoding="utf-8",
    )

    kept, skipped = load_scores(csv_file)

    assert kept == [("정상학생", 80)]
    assert skipped == [
        (4, "열하나", "열 개수가 2가 아님"),
        (5, "열이,셋,개", "열 개수가 2가 아님"),
        (6, " ,80", "이름이 비어 있음"),
        (7, "점수없음, ", "점수가 비어 있음"),
        (8, "문자점수,abc", "점수가 정수가 아님"),
        (9, "최솟값초과,-1", "점수가 0~100 밖"),
        (10, "최댓값초과,101", "점수가 0~100 밖"),
    ]


@pytest.mark.parametrize(
    ("score", "expected"),
    [
        (-1, ([], [(2, "경계학생,-1", "점수가 0~100 밖")])),
        (0, ([("경계학생", 0)], [])),
        (100, ([("경계학생", 100)], [])),
        (101, ([], [(2, "경계학생,101", "점수가 0~100 밖")])),
    ],
)
def test_점수_범위의_경계값(tmp_path, score, expected):
    csv_file = tmp_path / "boundary.csv"
    csv_file.write_text(
        f"name,score\n경계학생,{score}\n",
        encoding="utf-8",
    )

    assert load_scores(csv_file) == expected