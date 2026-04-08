def calculate_fantasy_points(
    stats: dict[str, float], scoring_format: dict[str, float]
) -> float:
    """Calculate fantasy points from player stats and a scoring format.

    Multiplies each stat by its scoring weight and sums the results.
    Stats not present in the scoring format are ignored.

    Args:
        stats: Player game stats (e.g., {"passing_tds": 2}).
        scoring_format: Points per stat (e.g., {"passing_tds": 4}).

    Returns:
        Total fantasy points as a float.
    """
    total = 0

    for k, stat in stats.items():
        score = scoring_format.get(k)
        # If a stat is not in the scoring format, ignore it
        if score is not None:
            total += stat * score

    return total
