import pytest

from load_scores import load_scores


def test_정상_점수와_공백을_정리하고_중복_이름도_유지한다(tmp_path):
    csv_file = tmp_path / "scores.csv"
    csv_file.write_text(
        "name,score\n"
        "  김하나  , 0 \n"
        "이둘,100\n"
        "김하나,88\n",
        encoding="utf-8",
    )

    kept, skipped = load_scores(csv_file)

    assert kept == [("김하나", 0), ("이둘", 100), ("김하나", 88)]
    assert skipped == []


def test_헤더만_있는_파일은_빈_결과를_반환한다(tmp_path):
    csv_file = tmp_path / "header_only.csv"
    csv_file.write_text("name,score\n", encoding="utf-8")

    assert load_scores(csv_file) == ([], [])


def test_utf8_bom이_있는_파일도_읽는다(tmp_path):
    csv_file = tmp_path / "bom.csv"
    csv_file.write_text("name,score\n학생,75\n", encoding="utf-8-sig")

    assert load_scores(csv_file) == ([("학생", 75)], [])


def test_잘못된_행을_정확한_행번호와_사유로_기록한다(tmp_path):
    csv_file = tmp_path / "invalid_rows.csv"
    csv_file.write_text(
        "name,score\n"
        "\n"
        "한열\n"
        "세,80,추가\n"
        " ,80\n"
        "점수없음, \n"
        "문자점수,abc\n"
        "최솟값초과,-1\n"
        "최댓값초과,101\n"
        "정상,90\n",
        encoding="utf-8",
    )

    kept, skipped = load_scores(csv_file)

    assert kept == [("정상", 90)]
    assert skipped == [
        (3, "한열", "열 개수가 2가 아님"),
        (4, "세,80,추가", "열 개수가 2가 아님"),
        (5, " ,80", "이름이 비어 있음"),
        (6, "점수없음, ", "점수가 비어 있음"),
        (7, "문자점수,abc", "점수가 정수가 아님"),
        (8, "최솟값초과,-1", "점수가 0~100 밖"),
        (9, "최댓값초과,101", "점수가 0~100 밖"),
    ]


@pytest.mark.parametrize(
    ("score", "expected_kept", "expected_skipped"),
    [
        (0, [("경계학생", 0)], []),
        (100, [("경계학생", 100)], []),
        (-1, [], [(2, "경계학생,-1", "점수가 0~100 밖")]),
        (101, [], [(2, "경계학생,101", "점수가 0~100 밖")]),
    ],
)
def test_점수_범위의_경계값(
    tmp_path, score, expected_kept, expected_skipped
):
    csv_file = tmp_path / "boundary.csv"
    csv_file.write_text(
        f"name,score\n경계학생,{score}\n",
        encoding="utf-8",
    )

    assert load_scores(csv_file) == (expected_kept, expected_skipped)


def test_파일이_없으면_FileNotFoundError를_그대로_발생시킨다(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_scores(tmp_path / "missing.csv")