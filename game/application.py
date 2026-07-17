"""Application-service layer coordinating UI, domain, and storage."""

from __future__ import annotations

import random
from collections import defaultdict
from pathlib import Path

from game.config import (
    CATEGORY_LABELS,
    DIFFICULTIES,
    LEADERBOARD_DISPLAY_LIMIT,
)
from game.data_manager import get_bank_statistics, select_random_word
from game.exceptions import LeaderboardError
from game.hangman import GuessStatus, HangmanGame
from game.leaderboard import save_score, top_scores
from game.types import WordBank
from game.ui import ConsoleUI


class GameApplication:
    """Coordinate menu navigation and complete game rounds."""

    def __init__(
        self,
        bank: WordBank,
        leaderboard_path: Path,
        ui: ConsoleUI,
        rng: random.Random | None = None,
    ) -> None:
        self._bank = bank
        self._leaderboard_path = leaderboard_path
        self._ui = ui
        self._rng = rng
        self._seen_by_pool: dict[tuple[str, int], set[str]] = defaultdict(set)

    def run(self) -> int:
        """Run the menu loop until the player exits."""
        player_name = self._ui.prompt_player_name("Masukkan nama pemain: ")
        while True:
            choice = self._ui.display_main_menu(player_name)
            if choice == 0:
                self._ui.clear()
                self._ui.write("Terima kasih sudah bermain.")
                return 0
            if choice == 1:
                self._play_round(player_name)
            elif choice == 2:
                self._show_leaderboard()
            elif choice == 3:
                self._ui.display_instructions(len(self._bank))
                self._ui.pause()
            elif choice == 4:
                self._ui.display_about(get_bank_statistics(self._bank))
                self._ui.pause()
            elif choice == 5:
                player_name = self._ui.prompt_player_name(
                    "Masukkan nama pemain baru: "
                )

    def _play_round(self, player_name: str) -> None:
        """Run one complete round, including persistence on a win."""
        category = self._ui.choose_category(self._bank)
        if category is None:
            return

        difficulty = self._ui.choose_difficulty()
        settings = DIFFICULTIES[difficulty]
        pool_key = (category, difficulty)
        seen = self._seen_by_pool[pool_key]
        source = self._bank[category][str(difficulty)]
        if len(seen) >= len(source):
            seen.clear()

        word = select_random_word(
            bank=self._bank,
            category=category,
            difficulty=difficulty,
            excluded_words=seen,
            rng=self._rng,
        )
        seen.add(word)

        game = HangmanGame(
            word=word,
            category=category,
            difficulty=difficulty,
            max_wrong=settings.max_wrong,
            score_multiplier=settings.score_multiplier,
        )
        category_label = CATEGORY_LABELS[category]
        message: tuple[GuessStatus, str] | None = None

        while not game.is_finished:
            self._ui.display_round(game, category_label)
            if message is not None:
                status, guess = message
                self._ui.write_message_for_outcome(status, guess)

            guess = self._ui.prompt_guess()
            if guess == "0":
                game.forfeit()
                break

            outcome = game.guess(guess)
            message = (outcome.status, guess)

        self._ui.display_round(game, category_label)
        if game.is_won:
            self._finish_win(game, player_name, category_label)
        elif game.forfeited:
            self._ui.write(
                f"Kamu menyerah. Jawabannya: {game.word.upper()}"
            )
            self._ui.write("Skor ronde: 0")
        else:
            self._ui.write(
                f"Kesempatan habis. Jawabannya: {game.word.upper()}"
            )
            self._ui.write("Skor ronde: 0")
        self._ui.pause()

    def _finish_win(
        self,
        game: HangmanGame,
        player_name: str,
        category_label: str,
    ) -> None:
        """Display and persist the score for a winning round."""
        score = game.calculate_score()
        self._ui.write(
            f"SELAMAT, {player_name}! Jawabannya: {game.word.upper()}"
        )
        self._ui.write(f"Skor ronde: {score}")
        try:
            save_score(
                path=self._leaderboard_path,
                player_name=player_name,
                score=score,
                category=category_label,
                difficulty=game.difficulty,
                word=game.word,
            )
        except LeaderboardError as error:
            self._ui.write(
                "Skor berhasil dihitung tetapi gagal disimpan: "
                f"{error}"
            )

    def _show_leaderboard(self) -> None:
        """Load and render the highest scores without crashing the menu."""
        try:
            scores = top_scores(
                self._leaderboard_path,
                LEADERBOARD_DISPLAY_LIMIT,
            )
            self._ui.display_leaderboard(scores)
        except LeaderboardError as error:
            self._ui.clear()
            self._ui.header("LEADERBOARD")
            self._ui.write(f"Leaderboard tidak dapat dibuka: {error}")
        self._ui.pause()
