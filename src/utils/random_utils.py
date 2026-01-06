import random
import uuid
from typing import List, Any


def generate_uuid() -> str:
    """
    Generates a UUIDv4 string.
    """
    return str(uuid.uuid4())


def weighted_choice(choices: List[Any], weights: List[float]) -> Any:
    """
    Returns a random element from `choices` based on `weights`.
    """
    return random.choices(choices, weights=weights, k=1)[0]


def random_bool(probability: float) -> bool:
    """
    Returns True with given probability (0.0 to 1.0).
    """
    return random.random() < probability


def random_subset(items: List[Any], max_items: int) -> List[Any]:
    """
    Returns a random subset of items up to max_items.
    """
    if not items:
        return []

    k = random.randint(0, min(len(items), max_items))
    return random.sample(items, k)
