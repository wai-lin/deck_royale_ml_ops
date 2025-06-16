from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}


def test_get_decks():
    response = client.get("/decks")
    assert response.status_code == 200
    decks = response.json()
    assert len(decks) == 2
    assert isinstance(decks, list)
    for deck in decks:
        assert isinstance(deck, dict)
        assert all(
            key in deck
            for key in [
                "deck_id",
                "name",
                "cards",
                "avg_elixir",
                "cycle_cost",
                "copy_link",
            ]
        )


def test_get_deck_exists():
    response = client.get("/decks/1")
    assert response.status_code == 200
    deck = response.json()
    assert deck["deck_id"] == "1"
    assert deck["name"] == "EvoRG FishBoy Ghost 3.3 Cycle"
    assert deck["cards"] == ["FishBoy", "Ghost", "Ice Spirit", "Skeletons"]
    assert deck["avg_elixir"] == 3.3
    assert deck["cycle_cost"] == 4.0
    assert deck["copy_link"] == "https://link-to-deck.com/1"


def test_get_deck_not_found():
    response = client.get("/decks/999")
    assert response.status_code == 404  # Correctly check for 404
    assert response.json() == {"detail": "Deck not found"}  # FastAPI uses "detail"
