"""Console input/output isolated from application logic."""

from __future__ import annotations

import os
import sys
from collections.abc import Callable, Iterable, Mapping

from game.config import CATEGORY_LABELS, DIFFICULTIES
from game.data_manager import BankStatistics
from game.hangman import GuessStatus, HangmanGame
from game.types import ScoreEntry, WordBank
from game.validation import normalize_player_name

InputFunction = Callable[[str], str]
OutputFunction = Callable[[str], None]
SEPARATOR = "=" * 66
LINE = "-" * 66


class ConsoleUI:
    """Terminal adapter with injectable input and output functions."""

    def __init__(
        self,
        input_function: InputFunction = input,
        output_function: OutputFunction = print,
        clear_enabled: bool = True,
    ) -> None:
        self._input = input_function
        self._output = output_function
        self._clear_enabled = clear_enabled

    def clear(self) -> None:
        """Clear an interactive terminal without affecting redirected output."""
        if not self._clear_enabled or not sys.stdout.isatty():
            return
        os.system("cls" if os.name == "nt" else "clear")

    def write(self, message: str = "") -> None:
        """Write one line to the configured output."""
        self._output(message)

    def pause(self) -> None:
        """Wait until the user confirms continuation."""
        self._input("\nTekan Enter untuk melanjutkan...")

    def header(self, title: str) -> None:
        """Render a consistent page header."""
        self.write(SEPARATOR)
        self.write(title.center(len(SEPARATOR)))
        self.write(SEPARATOR)

    def prompt_player_name(self, prompt: str) -> str:
        """Prompt until a normalized and terminal-safe name is entered."""
        while True:
            raw_name = self._input(prompt)
            try:
                return normalize_player_name(raw_name)
            except ValueError as error:
                self.write(str(error))

    def prompt_number(self, prompt: str, minimum: int, maximum: int) -> int:
        """Prompt until an integer inside the requested range is entered."""
        while True:
            raw_value = self._input(prompt).strip()
            try:
                value = int(raw_value)
            except ValueError:
                self.write("Masukkan angka yang valid.")
                continue
            if minimum <= value <= maximum:
                return value
            self.write(f"Pilihan harus antara {minimum} dan {maximum}.")

    def choose_category(self, bank: WordBank) -> str | None:
        """Render all categories and return the selected category key."""
        categories = sorted(bank, key=lambda key: CATEGORY_LABELS[key])
        self.clear()
        self.header("PILIH KATEGORI")
        for index, category in enumerate(categories, start=1):
            total = sum(len(words) for words in bank[category].values())
            self.write(
                f"{index:>2}. {CATEGORY_LABELS[category]:<22} "
                f"({total:>3} entri)"
            )
        back_option = len(categories) + 1
        self.write(f"{back_option:>2}. Kembali")
        choice = self.prompt_number(
            "\nPilih kategori: ",
            1,
            back_option,
        )
        return None if choice == back_option else categories[choice - 1]

    def choose_difficulty(self) -> int:
        """Render difficulty rules and return the selected level."""
        self.clear()
        self.header("PILIH KESULITAN")
        for level, settings in DIFFICULTIES.items():
            self.write(
                f"{level}. {settings.label:<8} | "
                f"Maksimal salah: {settings.max_wrong} | "
                f"Pengali skor: x{settings.score_multiplier}"
            )
        return self.prompt_number("\nPilih kesulitan (1-3): ", 1, 3)

    def display_round(self, game: HangmanGame, category_label: str) -> None:
        """Render the current state of a round."""
        self.clear()
        self.header("GAME TEBAK KATA BAHASA INDONESIA")
        self.write(f"Kategori    : {category_label}")
        self.write(f"Kesulitan   : {DIFFICULTIES[game.difficulty].label}")
        self.write(
            "Jumlah huruf: "
            f"{sum(character.isalpha() for character in game.word)}"
        )
        if " " in game.word:
            self.write(f"Jumlah kata : {len(game.word.split())}")
        self.write(game.hangman_art())
        self.write(f"Jawaban     : {game.masked_word}")
        self.write(
            "Huruf dipakai: "
            + self._join_or_dash(game.guessed_letters)
        )
        self.write(
            "Huruf salah  : "
            + self._join_or_dash(game.wrong_letters)
        )
        self.write(f"Kesempatan  : {game.remaining_attempts}")
        self.write(LINE)

    def prompt_guess(self) -> str:
        """Read one raw guess or the forfeit command."""
        return self._input(
            "\nMasukkan satu huruf (atau ketik 0 untuk menyerah): "
        ).strip().lower()

    def display_leaderboard(self, scores: Iterable[ScoreEntry]) -> None:
        """Render leaderboard entries as a fixed-width table."""
        score_list = list(scores)
        self.clear()
        self.header("LEADERBOARD")
        if not score_list:
            self.write("Belum ada skor yang tersimpan.")
            return

        self.write(
            f"{'No':<4}{'Nama':<20}{'Skor':>8}  "
            f"{'Kategori':<19}{'Lv':>3}"
        )
        self.write(LINE)
        for index, item in enumerate(score_list, start=1):
            self.write(
                f"{index:<4}{item['nama'][:18]:<20}"
                f"{item['skor']:>8}  "
                f"{item['kategori'][:17]:<19}"
                f"{item['kesulitan']:>3}"
            )

    def display_main_menu(self, player_name: str) -> int:
        """Render the main menu and return the chosen action number."""
        self.clear()
        self.header("GAME TEBAK KATA BAHASA INDONESIA")
        self.write(f"Pemain: {player_name}")
        self.write(
            "\n1. Mulai bermain\n"
            "2. Leaderboard\n"
            "3. Cara bermain\n"
            "4. Tentang proyek\n"
            "5. Ganti nama pemain\n"
            "0. Keluar"
        )
        return self.prompt_number("\nPilih menu: ", 0, 5)

    def display_instructions(self, category_count: int) -> None:
        """Render gameplay instructions using current dataset statistics."""
        self.clear()
        self.header("CARA BERMAIN")
        self.write(
            "1. Masukkan nama pemain.\n"
            f"2. Pilih salah satu dari {category_count} kategori.\n"
            "3. Pilih kesulitan 1 sampai 3.\n"
            "4. Tebak jawaban dengan satu huruf setiap giliran.\n"
            "5. Spasi pada frasa terbuka otomatis.\n"
            "6. Tebakan salah mengurangi kesempatan.\n"
            "7. Tebakan yang sama tidak dihitung dua kali.\n"
            "8. Ketik 0 untuk menyerah.\n\n"
            "Skor dasar berasal dari panjang jawaban, akurasi, dan "
            "sisa kesempatan, lalu dikalikan tingkat kesulitan."
        )

    def display_about(self, statistics: BankStatistics) -> None:
        """Render project information without category-specific counters."""
        self.clear()
        self.header("TENTANG PROYEK")
        self.write(
            "Game Tebak Kata Bahasa Indonesia\n"
            "Proyek Akhir Algoritma dan Pemrograman\n\n"
            f"Bank lokal: {statistics.category_count} kategori, "
            f"{statistics.entry_count:,} entri, "
            f"{statistics.phrase_count:,} frasa, dan 3 tingkat kesulitan.\n"
            "Kandidat data: Contek Sambung Kata dan kurasi tambahan.\n"
            "Atribusi sumber kandidat: By MizuuDev Tim NepuhSoft.\n"
            "Seluruh data disimpan lokal; permainan tidak memakai API."
        )

    def write_message_for_outcome(
        self,
        status: GuessStatus,
        guess: str,
    ) -> None:
        """Render a user-facing message for a guess outcome."""
        messages: Mapping[GuessStatus, str] = {
            GuessStatus.INVALID: "Input harus tepat satu huruf alfabet a-z.",
            GuessStatus.DUPLICATE: (
                f"Huruf '{guess}' sudah pernah dimasukkan."
            ),
            GuessStatus.CORRECT: (
                f"Benar! Huruf '{guess}' terdapat pada jawaban."
            ),
            GuessStatus.WRONG: (
                f"Salah! Huruf '{guess}' tidak terdapat pada jawaban."
            ),
            GuessStatus.FINISHED: "Ronde ini sudah selesai.",
        }
        self.write(messages[status])

    @staticmethod
    def _join_or_dash(values: Iterable[str]) -> str:
        """Join sorted values or return a dash when empty."""
        sorted_values = sorted(values)
        return ", ".join(sorted_values) if sorted_values else "-"
