import sys

def log_to_console(message: str) -> None:
    """コンソールにログメッセージを出力します。

    Args:
        message (str): 出力するメッセージ内容
    """
    print(f"[LOG] {message}")