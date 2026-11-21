from pathlib import Path

from src.validate_dataset import validate


def test_repository_benchmark_invariants():
    validate(Path("deliverables/final_benchmark_70.csv"))
