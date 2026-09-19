"""Coverage for the submission builder: file round-trip + schema validation errors."""
import json
import pytest

from arcsolver import dsl
from arcsolver.submission import write_submission, validate_submission, solve_challenges

BASE = [[1, 2, 0], [0, 3, 0], [4, 0, 0]]


def _task(fn):
    g = dsl.to_grid(BASE)
    pair = {"input": dsl.to_list(g), "output": dsl.to_list(fn(g))}
    return {"train": [pair, pair], "test": [{"input": BASE}]}


def test_write_submission_roundtrip(tmp_path):
    challenges = {"t_rot": _task(dsl.rotate180), "t_ref": _task(dsl.reflect_h)}
    cpath = tmp_path / "ch.json"
    cpath.write_text(json.dumps(challenges))
    out = tmp_path / "submission.json"
    sub = write_submission(cpath, out)
    assert out.exists()
    on_disk = json.loads(out.read_text())
    assert set(on_disk) == {"t_rot", "t_ref"}
    validate_submission(sub, challenges)  # must not raise
    assert on_disk["t_rot"][0]["attempt_1"] == dsl.to_list(dsl.rotate180(dsl.to_grid(BASE)))


def test_solve_challenges_counts_solved():
    challenges = {"t_rot": _task(dsl.rotate180)}
    sub = solve_challenges(challenges)
    assert sub["_meta_solved"] >= 1
    assert "t_rot" in sub


def test_validate_rejects_missing_task():
    challenges = {"t_rot": _task(dsl.rotate180)}
    with pytest.raises(AssertionError):
        validate_submission({}, challenges)


def test_validate_rejects_wrong_test_count():
    challenges = {"t_rot": _task(dsl.rotate180)}
    bad = {"t_rot": []}  # zero entries, expected one per test input
    with pytest.raises(AssertionError):
        validate_submission(bad, challenges)


def test_validate_rejects_bad_color():
    challenges = {"t_rot": _task(dsl.rotate180)}
    bad = {"t_rot": [{"attempt_1": [[99]], "attempt_2": [[0]]}]}
    with pytest.raises(AssertionError):
        validate_submission(bad, challenges)
