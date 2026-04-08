from fanstatsy.scoring import calculate_fantasy_points


def test_calculate_fantasy_points() -> None:
    """
    Tests that we correctly calculate a fantasy score
    based on stats and a scoring format.
    """
    stats = {"touchdown": 1, "rushing_yards": 10}
    scoring_format = {"touchdown": 7, "rushing_yards": 0.5}
    expected = 12
    actual = calculate_fantasy_points(stats, scoring_format)
    assert actual == expected


def test_calculate_fantasy_points_with_non_scoring_stats() -> None:
    """
    Tests that we correctly calculate a fantasy score
    but ignore stats that don't have a score
    """
    stats = {"touchdown": 1, "rushing_yards": 10}
    scoring_format = {"touchdown": 7}
    expected = 7
    actual = calculate_fantasy_points(stats, scoring_format)
    assert actual == expected


def test_calculate_fantasy_points_with_negative_stats() -> None:
    """
    Tests that we correctly calculate a fantasy score
    with negative stats
    """
    stats = {"interception": 3}
    scoring_format = {"interception": -0.5}
    expected = -1.5
    actual = calculate_fantasy_points(stats, scoring_format)
    assert actual == expected


def test_calculate_fantasy_points_with_empty_stats() -> None:
    """
    Tests that we correctly calculate a fantasy score
    with empty stats
    """
    stats = {}
    scoring_format = {"interception": -0.5}
    expected = 0.0
    actual = calculate_fantasy_points(stats, scoring_format)
    assert actual == expected
