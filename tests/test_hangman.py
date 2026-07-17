"""Tests for pure Hangman domain rules."""

from __future__ import annotations

import unittest

from game.hangman import GuessStatus, HANGMAN_STAGES, HangmanGame


def make_game(**overrides: object) -> HangmanGame:
    """Build a valid game with optional field overrides."""
    values: dict[str, object] = {
        "word": "sapi",
        "category": "hewan",
        "difficulty": 1,
        "max_wrong": 8,
        "score_multiplier": 1,
    }
    values.update(overrides)
    return HangmanGame(**values)  # type: ignore[arg-type]


class HangmanGameTest(unittest.TestCase):
    def test_constructor_normalizes_word_category_and_sets(self) -> None:
        game = make_game(
            word="  Arab   Saudi ",
            category=" Negara ",
            difficulty=3,
            guessed_letters={" A ", "z"},
            wrong_letters={"Z"},
        )
        self.assertEqual(game.word, "arab saudi")
        self.assertEqual(game.category, "negara")
        self.assertEqual(game.guessed_letters, {"a", "z"})
        self.assertEqual(game.wrong_letters, {"z"})

    def test_constructor_rejects_invalid_basic_state(self) -> None:
        invalid_cases = (
            {"word": ""},
            {"word": "café"},
            {"category": ""},
            {"category": 1},
            {"difficulty": 0},
            {"max_wrong": 0},
            {"max_wrong": True},
            {"score_multiplier": 0},
            {"score_multiplier": True},
            {"forfeited": "tidak"},
        )
        for overrides in invalid_cases:
            with self.subTest(overrides=overrides), self.assertRaises(ValueError):
                make_game(**overrides)

    def test_constructor_rejects_inconsistent_letter_state(self) -> None:
        cases = (
            {"guessed_letters": ["a"]},
            {"guessed_letters": {"1"}},
            {"guessed_letters": {1}},
            {"guessed_letters": set(), "wrong_letters": {"z"}},
            {"guessed_letters": {"s"}, "wrong_letters": {"s"}},
            {
                "max_wrong": 1,
                "guessed_letters": {"x", "y"},
                "wrong_letters": {"x", "y"},
            },
            {
                "max_wrong": 1,
                "guessed_letters": {"s", "a", "p", "i", "x"},
                "wrong_letters": {"x"},
            },
        )
        for overrides in cases:
            with self.subTest(overrides=overrides), self.assertRaises(ValueError):
                make_game(**overrides)

    def test_correct_wrong_duplicate_invalid_and_finished_guesses(self) -> None:
        game = make_game()
        self.assertEqual(game.guess(None).status, GuessStatus.INVALID)
        self.assertEqual(game.guess("ab").status, GuessStatus.INVALID)
        self.assertEqual(game.guess("1").status, GuessStatus.INVALID)
        self.assertEqual(game.guess("é").status, GuessStatus.INVALID)

        self.assertEqual(game.guess("s").status, GuessStatus.CORRECT)
        duplicate = game.guess("S")
        self.assertEqual(duplicate.status, GuessStatus.DUPLICATE)
        self.assertTrue(duplicate.is_correct)

        self.assertEqual(game.guess("z").status, GuessStatus.WRONG)
        wrong_duplicate = game.guess("z")
        self.assertEqual(wrong_duplicate.status, GuessStatus.DUPLICATE)
        self.assertFalse(wrong_duplicate.is_correct)
        self.assertEqual(game.wrong_count, 1)
        self.assertEqual(game.remaining_attempts, 7)

        for letter in "api":
            game.guess(letter)
        self.assertTrue(game.is_won)
        self.assertEqual(game.guess("x").status, GuessStatus.FINISHED)

    def test_phrase_mask_score_and_loss_score(self) -> None:
        game = make_game(word="arab saudi", difficulty=3, score_multiplier=3)
        self.assertIn("/", game.masked_word)
        for letter in set("arabsaudi"):
            game.guess(letter)
        self.assertTrue(game.is_won)
        self.assertGreater(game.calculate_score(), 0)

        lost = make_game(max_wrong=1)
        lost.guess("z")
        self.assertTrue(lost.is_lost)
        self.assertEqual(lost.calculate_score(), 0)

    def test_forfeit_is_idempotent_and_shows_final_stage(self) -> None:
        game = make_game(difficulty=2, max_wrong=7, score_multiplier=2)
        game.forfeit()
        game.forfeit()
        self.assertTrue(game.is_finished)
        self.assertEqual(game.remaining_attempts, 0)
        self.assertEqual(game.calculate_score(), 0)
        self.assertEqual(game.hangman_art(), HANGMAN_STAGES[-1])

        won = make_game()
        for letter in "sapi":
            won.guess(letter)
        won.forfeit()
        self.assertFalse(won.forfeited)

    def test_score_uses_multiplier_and_accuracy_penalty(self) -> None:
        clean = make_game(score_multiplier=1)
        with_error = make_game(score_multiplier=1)
        hard = make_game(difficulty=3, score_multiplier=3)

        with_error.guess("z")
        for letter in "sapi":
            clean.guess(letter)
            with_error.guess(letter)
            hard.guess(letter)

        self.assertLess(with_error.calculate_score(), clean.calculate_score())
        self.assertEqual(hard.calculate_score(), clean.calculate_score() * 3)

    def test_stage_progression_is_monotonic_and_ends_at_final_stage(self) -> None:
        game = make_game(max_wrong=6)
        indices = [game.stage_index]
        for letter in "zxyqwv":
            game.guess(letter)
            indices.append(game.stage_index)
        self.assertEqual(indices, sorted(indices))
        self.assertEqual(indices[-1], len(HANGMAN_STAGES) - 1)


if __name__ == "__main__":
    unittest.main()
