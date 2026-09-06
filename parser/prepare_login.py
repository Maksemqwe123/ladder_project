"""
Шаг 1: вход в Instagram в ОБЫЧНОМ Firefox (без Selenium).

Так капча проходит нормально. Сессия сохранится в firefox_profile/,
потом scrape_instagram.py подхватит её.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PROFILE_DIR = BASE_DIR / "firefox_profile"
LOGIN_URL = "https://www.instagram.com/accounts/login/"


def find_firefox() -> str:
    for name in ("firefox", "firefox-bin"):
        path = shutil.which(name)
        if path:
            return path
    sys.exit("Firefox не найден. Установите Firefox и повторите.")


def main() -> None:
    PROFILE_DIR.mkdir(parents=True, exist_ok=True)
    firefox = find_firefox()

    print("[login] Открываю обычный Firefox (не Selenium).")
    print(f"[login] Профиль: {PROFILE_DIR}")
    print("[login] 1) Войдите в Instagram и пройдите капчу.")
    print("[login] 2) Убедитесь, что открывается лента/профиль без капчи.")
    print("[login] 3) Полностью закройте это окно Firefox.")
    print("[login] 4) Затем запустите: python scrape_instagram.py")
    print()

    # -no-remote: отдельный процесс со своим профилем
    subprocess.run(
        [firefox, "-no-remote", "-profile", str(PROFILE_DIR), LOGIN_URL],
        check=False,
    )
    print("[login] Firefox закрыт. Можно запускать парсер.")


if __name__ == "__main__":
    main()
