"""Application-specific exception hierarchy."""


class AppError(Exception):
    """Base exception for expected application failures."""


class BankKataError(AppError):
    """Raised when the word bank is missing or invalid."""


class LeaderboardError(AppError):
    """Raised when leaderboard persistence fails or is invalid."""
