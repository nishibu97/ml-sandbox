class AppError(Exception):
    """アプリケーション共通の例外ベース。"""

    def __init__(self, message: str, *, code: str = "app_error") -> None:
        super().__init__(message)
        self.message = message
        self.code = code
