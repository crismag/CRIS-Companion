"""Tests for CRIS Companion CLI behavior."""

from __future__ import annotations

from companion.interface import cli


def test_run_cli_prints_usage_without_arguments(capsys) -> None:
    """CLI should print usage and exit with non-zero code when no args are provided."""
    exit_code = cli.run_cli([])
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Usage:" in captured.out


def test_run_cli_passes_task_to_engine(monkeypatch, capsys) -> None:
    """CLI should pass task to engine and print formatted output."""

    def fake_load_settings() -> dict:
        return {"fake": True}

    def fake_run_engine(task: str, settings: dict, output_path: str | None = None) -> dict:
        assert task == "create hello script"
        assert settings == {"fake": True}
        assert output_path is None
        return {"status": "ok", "message": "Generated response"}

    monkeypatch.setattr(cli, "load_settings", fake_load_settings)
    monkeypatch.setattr(cli, "run_engine", fake_run_engine)

    exit_code = cli.run_cli(["create", "hello", "script"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "[ok] Generated response" in captured.out


def test_run_cli_passes_output_path_when_provided(monkeypatch, capsys) -> None:
    """CLI should pass --output value to engine."""

    def fake_load_settings() -> dict:
        return {"fake": True}

    def fake_run_engine(task: str, settings: dict, output_path: str | None = None) -> dict:
        assert task == "create hello script"
        assert output_path == "hello.py"
        return {
            "status": "ok",
            "message": "Generated response and saved file",
            "file_path": "hello.py",
        }

    monkeypatch.setattr(cli, "load_settings", fake_load_settings)
    monkeypatch.setattr(cli, "run_engine", fake_run_engine)

    exit_code = cli.run_cli(["--output", "hello.py", "create", "hello", "script"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "hello.py" in captured.out
