"""Pure domain logic for one Hangman round."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Final

from game.validation import normalize_answer

HANGMAN_STAGES: Final[tuple[str, ...]] = (
    r"""
      +---+
      |   |
          |
          |
          |
          |
    =========
    """,
    r"""
      +---+
      |   |
      O   |
          |
          |
          |
    =========
    """,
    r"""
      +---+
      |   |
      O   |
      |   |
          |
          |
    =========
    """,
    r"""
      +---+
      |   |
      O   |
     /|   |
          |
          |
    =========
    """,
    r"""
      +---+
      |   |
      O   |
     /|\  |
          |
          |
    =========
    """,
    r"""
      +---+
      |   |
      O   |
     /|\  |
     /    |
          |
    =========
    """,
    r"""
      +---+
      |   |
      O   |
     /|\  |
     / \  |
          |
    =========
    """,
    r"""
      +---+
      |   |
     [O   |
     /|\  |
     / \  |
          |
    =========
    """,
    r"""
      +---+
      |   |
     [O]  |
     /|\  |
     / \  |
          |
    =========
    """,
)


class GuessStatus(str, Enum):
    """Possible outcomes from a letter guess."""

    CORRECT = "correct"
    WRONG = "wrong"
    DUPLICATE = "duplicate"
    INVALID = "invalid"
    FINISHED = "finished"


@dataclass(frozen=True, slots=True)
class GuessOutcome:
    """Structured result of a guess operation."""

    status: GuessStatus
    is_correct: bool


def _validate_letter_set(name: str, letters: set[str]) -> set[str]:
    """Normalize and validate one constructor-provided letter set."""
    if not isinstance(letters, set):
        raise ValueError(f"{name} harus berupa set.")

    normalized: set[str] = set()
    for value in letters:
        if not isinstance(value, str):
            raise ValueError(f"{name} hanya boleh berisi teks.")
        letter = value.strip().lower()
        if len(letter) != 1 or not letter.isascii() or not letter.isalpha():
            raise ValueError(f"{name} hanya boleh berisi huruf a-z.")
        normalized.add(letter)
    return normalized


@dataclass(slots=True)
class HangmanGame:
    """Mutable state and rules for one Hangman round."""

    word: str
    category: str
    difficulty: int
    max_wrong: int
    score_multiplier: int = 1
    guessed_letters: set[str] = field(default_factory=set)
    wrong_letters: set[str] = field(default_factory=set)
    forfeited: bool = False

    def __post_init__(self) -> None:
        """Normalize constructor values and reject inconsistent state."""
        try:
            self.word = normalize_answer(self.word)
        except ValueError as error:
            raise ValueError(str(error)) from error

        if not isinstance(self.category, str):
            raise ValueError("Kategori harus berupa teks.")
        self.category = self.category.strip().lower()
        if not self.category:
            raise ValueError("Kategori tidak boleh kosong.")
        if self.difficulty not in {1, 2, 3}:
            raise ValueError("Kesulitan harus bernilai 1, 2, atau 3.")
        if not isinstance(self.max_wrong, int) or isinstance(self.max_wrong, bool):
            raise ValueError("Maksimal kesalahan harus berupa bilangan bulat.")
        if self.max_wrong <= 0:
            raise ValueError("Maksimal kesalahan harus lebih dari nol.")
        if (
            not isinstance(self.score_multiplier, int)
            or isinstance(self.score_multiplier, bool)
            or self.score_multiplier <= 0
        ):
            raise ValueError("Pengali skor harus berupa bilangan bulat positif.")
        if not isinstance(self.forfeited, bool):
            raise ValueError("Status menyerah harus berupa boolean.")

        self.guessed_letters = _validate_letter_set(
            "Huruf tebakan", self.guessed_letters
        )
        self.wrong_letters = _validate_letter_set(
            "Huruf salah", self.wrong_letters
        )

        if not self.wrong_letters.issubset(self.guessed_letters):
            raise ValueError("Huruf salah harus termasuk dalam huruf tebakan.")
        if self.wrong_letters & self.required_letters:
            raise ValueError("Huruf salah tidak boleh terdapat pada jawaban.")
        if self.wrong_count > self.max_wrong:
            raise ValueError("Jumlah kesalahan melebihi batas permainan.")
        if self.is_won and self.is_lost:
            raise ValueError("State permainan tidak boleh menang dan kalah sekaligus.")

    @property
    def required_letters(self) -> set[str]:
        """Unique letters that must be guessed to win."""
        return {letter for letter in self.word if letter.isalpha()}

    @property
    def wrong_count(self) -> int:
        """Number of unique incorrect guesses."""
        return len(self.wrong_letters)

    @property
    def remaining_attempts(self) -> int:
        """Number of incorrect guesses still available."""
        if self.forfeited:
            return 0
        return max(0, self.max_wrong - self.wrong_count)

    @property
    def masked_word(self) -> str:
        """Return the visible answer, using underscores for hidden letters."""
        visible = (
            "/"
            if letter == " "
            else letter
            if letter in self.guessed_letters
            else "_"
            for letter in self.word
        )
        return " ".join(visible)

    @property
    def is_won(self) -> bool:
        """Whether every required letter has been guessed."""
        return self.required_letters.issubset(self.guessed_letters)

    @property
    def is_lost(self) -> bool:
        """Whether attempts are exhausted or the player forfeited."""
        return self.forfeited or self.wrong_count >= self.max_wrong

    @property
    def is_finished(self) -> bool:
        """Whether the round can no longer accept guesses."""
        return self.is_won or self.is_lost

    @property
    def stage_index(self) -> int:
        """Map wrong guesses monotonically to a valid display stage."""
        if self.forfeited:
            return len(HANGMAN_STAGES) - 1
        numerator = self.wrong_count * (len(HANGMAN_STAGES) - 1)
        index = (numerator + self.max_wrong - 1) // self.max_wrong
        return max(0, min(index, len(HANGMAN_STAGES) - 1))

    def guess(self, raw_letter: object) -> GuessOutcome:
        """Validate and apply one letter guess."""
        if self.is_finished:
            return GuessOutcome(GuessStatus.FINISHED, False)
        if not isinstance(raw_letter, str):
            return GuessOutcome(GuessStatus.INVALID, False)

        letter = raw_letter.strip().lower()
        if len(letter) != 1 or not letter.isascii() or not letter.isalpha():
            return GuessOutcome(GuessStatus.INVALID, False)
        if letter in self.guessed_letters:
            return GuessOutcome(
                GuessStatus.DUPLICATE,
                letter in self.required_letters,
            )

        self.guessed_letters.add(letter)
        if letter in self.required_letters:
            return GuessOutcome(GuessStatus.CORRECT, True)

        self.wrong_letters.add(letter)
        return GuessOutcome(GuessStatus.WRONG, False)

    def forfeit(self) -> None:
        """End an unfinished round without awarding a score."""
        if not self.is_finished:
            self.forfeited = True

    def calculate_score(self) -> int:
        """Return zero for losses, otherwise calculate the final score."""
        if not self.is_won:
            return 0

        letter_count = sum(letter.isalpha() for letter in self.word)
        base_score = letter_count * 10
        attempt_bonus = self.remaining_attempts * 15
        accuracy_bonus = max(
            0,
            len(self.required_letters) * 5 - self.wrong_count * 5,
        )
        return (
            base_score + attempt_bonus + accuracy_bonus
        ) * self.score_multiplier

    def hangman_art(self) -> str:
        """Return the Hangman drawing for the current state."""
        return HANGMAN_STAGES[self.stage_index]
