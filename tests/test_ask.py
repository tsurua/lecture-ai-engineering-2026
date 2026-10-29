from types import SimpleNamespace

from app import ask


def test_ask_prints_input_and_output_token_counts(monkeypatch, capsys):
    response = SimpleNamespace(
        text="回答",
        usage_metadata=SimpleNamespace(
            prompt_token_count=12,
            candidates_token_count=5,
        ),
    )

    class FakeClient:
        def __init__(self, *, api_key):
            pass

        models = SimpleNamespace(generate_content=lambda **kwargs: response)

    monkeypatch.setattr(ask.genai, "Client", FakeClient)
    monkeypatch.setattr(ask, "get_api_key", lambda: "test-key")

    assert ask.ask("質問") == "回答"
    output = capsys.readouterr().out
    assert "入力: 12" in output
    assert "出力: 5" in output