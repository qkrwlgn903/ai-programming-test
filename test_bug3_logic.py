import pytest

from bug3_logic import count_pass, find_max


@pytest.mark.parametrize(
    ("scores", "expected"),
    [
        ([95, 85, 70, 60], 95),
        ([10, 20, 30], 30),
        ([4], 4),
    ],
)
def test_find_max_returns_largest_score(scores, expected):
    assert find_max(scores) == expected


@pytest.mark.parametrize(
    ("scores", "cutoff", "expected"),
    [
        ([70, 85, 95], 60, 3),
        ([60, 60, 59], 60, 2),
        ([40, 50, 51], 50, 2),
    ],
)
def test_count_pass_includes_scores_at_cutoff(scores, cutoff, expected):
    assert count_pass(scores, cutoff) == expected


def test_count_pass_uses_default_cutoff_of_60():
    assert count_pass([60, 61, 59]) == 2
