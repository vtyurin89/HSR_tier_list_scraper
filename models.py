from dataclasses import dataclass


@dataclass
class Character:
    url: str
    real_name: str = None
    element: str = None
    best_relic_sets: list = None
    best_planetary_sets: list = None
    best_stats: list = None
