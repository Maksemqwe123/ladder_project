"""
Десктопный парсер Instagram-профиля Open Wide LLC.

Сначала один раз войдите через обычный Firefox (капча там проходит):
  python prepare_login.py
Закройте то окно, затем:
  python scrape_instagram.py

Парсер использует тот же профиль (cookies) и ждёт Enter, пока вы не будете готовы.
"""

from __future__ import annotations

import hashlib
import json
import re
import time
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

PROFILE_URL = "https://www.instagram.com/openwidellc/"
BASE_DIR = Path(__file__).resolve().parent
DOWNLOAD_DIR = BASE_DIR / "downloads"
MANIFEST_PATH = DOWNLOAD_DIR / "manifest.json"
PROFILE_DIR = BASE_DIR / "firefox_profile"
GECKODRIVER = "/snap/bin/geckodriver"

PAUSE_SHORT = 0.8
PAUSE_MED = 1.6
PAUSE_LONG = 2.5


def log(msg: str) -> None:
    print(f"[parser] {msg}", flush=True)


def build_driver() -> webdriver.Firefox:
    PROFILE_DIR.mkdir(parents=True, exist_ok=True)

    options = Options()
    # Тот же профиль, что и в prepare_login.py — сессия сохраняется
    options.add_argument("-profile")
    options.add_argument(str(PROFILE_DIR))
    options.add_argument("-width=1400")
    options.add_argument("-height=900")

    options.set_preference("permissions.default.image", 1)
    options.set_preference("dom.webdriver.enabled", False)
    options.set_preference("useAutomationExtension", False)
    options.set_preference("toolkit.telemetry.enabled", False)

    service = Service(executable_path=GECKODRIVER)
    driver = webdriver.Firefox(service=service, options=options)
    driver.set_window_size(1400, 900)
    try:
        driver.maximize_window()
    except Exception:
        pass
    return driver


def dismiss_cookies(driver: webdriver.Firefox) -> None:
    candidates = [
        "//button[contains(., 'Allow all')]",
        "//button[contains(., 'Allow All')]",
        "//button[contains(., 'Accept all')]",
        "//button[contains(., 'Accept')]",
        "//button[contains(., 'Принять')]",
        "//button[contains(., 'Разрешить')]",
        "//button[contains(., 'Only allow essential')]",
        "//button[contains(., 'Decline optional')]",
    ]
    for xpath in candidates:
        try:
            btn = driver.find_element(By.XPATH, xpath)
            if btn.is_displayed():
                log(f"Нажимаю cookie-кнопку: {btn.text!r}")
                btn.click()
                time.sleep(PAUSE_MED)
                return
        except NoSuchElementException:
            continue


def wait_until_ready() -> None:
    """Только Enter — парсер сам не продолжит по таймеру."""
    log("Если нужно — дологиньтесь / пройдите капчу в окне.")
    log("Когда видите посты профиля openwidellc — нажмите Enter здесь.")
    try:
        input()
    except EOFError:
        time.sleep(10)
    log("Продолжаю парсинг.")


def normalize_post_url(href: str) -> str | None:
    if not href:
        return None
    m = re.search(
        r"(?:https?://(?:www\.)?instagram\.com)?/(p|reel)/([A-Za-z0-9_-]+)",
        href,
    )
    if not m:
        return None
    return f"https://www.instagram.com/{m.group(1)}/{m.group(2)}/"


def harvest_post_urls_from_dom(driver: webdriver.Firefox) -> set[str]:
    """Достаём URL постов несколькими способами — Instagram часто меняет вёрстку."""
    found: set[str] = set()

    # 1) Все href через JS (надёжнее, чем Selenium find_elements)
    try:
        hrefs = driver.execute_script(
            """
            const out = [];
            for (const a of document.querySelectorAll('a[href]')) {
              out.push(a.href || a.getAttribute('href') || '');
            }
            return out;
            """
        )
        for href in hrefs or []:
            url = normalize_post_url(str(href))
            if url:
                found.add(url)
    except Exception as exc:
        log(f"JS-сбор ссылок не удался: {exc}")

    # 2) Сырой HTML / встроенный JSON
    try:
        html = driver.page_source or ""
        for kind, code in re.findall(r"/(p|reel)/([A-Za-z0-9_-]+)", html):
            if code.lower() in {"p", "reel"}:
                continue
            found.add(f"https://www.instagram.com/{kind}/{code}/")
        for code in re.findall(r'"shortcode"\s*:\s*"([A-Za-z0-9_-]+)"', html):
            found.add(f"https://www.instagram.com/p/{code}/")
        for code in re.findall(r'"code"\s*:\s*"([A-Za-z0-9_-]+)"', html):
            if len(code) >= 5:
                found.add(f"https://www.instagram.com/p/{code}/")
    except Exception as exc:
        log(f"Разбор HTML не удался: {exc}")

    return found


def debug_dom_snapshot(driver: webdriver.Firefox) -> None:
    """Пишем в лог, что реально есть на странице — если снова 0 постов."""
    try:
        info = driver.execute_script(
            """
            const as = [...document.querySelectorAll('a[href]')].slice(0, 30)
              .map(a => a.getAttribute('href'));
            const imgs = document.querySelectorAll('main img, article img').length;
            const html = document.documentElement.innerHTML;
            return {
              url: location.href,
              anchors: document.querySelectorAll('a[href]').length,
              sample: as,
              imgs,
              hasP: html.includes('/p/'),
              hasReel: html.includes('/reel/'),
              hasShortcode: html.includes('shortcode'),
            };
            """
        )
        log(f"DEBUG url={info.get('url')}")
        log(
            f"DEBUG anchors={info.get('anchors')} imgs={info.get('imgs')} "
            f"/p/={info.get('hasP')} /reel/={info.get('hasReel')} shortcode={info.get('hasShortcode')}"
        )
        sample = info.get("sample") or []
        log(f"DEBUG sample hrefs: {sample[:12]}")
    except Exception as exc:
        log(f"DEBUG не удалось: {exc}")


def collect_post_urls(driver: webdriver.Firefox, max_scrolls: int = 40) -> list[str]:
    log("Собираю ссылки на посты, прокручивая ленту...")
    # Дождаться сетки
    try:
        WebDriverWait(driver, 15).until(
            lambda d: d.execute_script(
                "return document.querySelectorAll('main img, article img, a[href*=\"/p/\"]').length"
            )
            > 0
        )
    except TimeoutException:
        log("Сетка долго не появляется — снимок DOM:")
        debug_dom_snapshot(driver)

    urls: set[str] = set()
    stagnant = 0

    for i in range(max_scrolls):
        before = len(urls)
        urls |= harvest_post_urls_from_dom(driver)
        gained = len(urls) - before
        log(f"Скролл {i + 1}/{max_scrolls}: постов собрано {len(urls)} (+{gained})")

        if i == 0 and len(urls) == 0:
            debug_dom_snapshot(driver)

        if gained == 0:
            stagnant += 1
        else:
            stagnant = 0
        if stagnant >= 4:
            log("Новых постов больше нет — останавливаю прокрутку.")
            break

        driver.execute_script(
            "window.scrollBy(0, Math.floor(window.innerHeight * 0.85));"
        )
        time.sleep(PAUSE_MED + 0.4)

    # Фоллбек: клик по превью в сетке и чтение URL диалога
    if not urls:
        log("Пробую открыть превью по клику...")
        urls |= open_grid_thumbnails(driver)

    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(PAUSE_SHORT)
    return sorted(urls)


def open_grid_thumbnails(driver: webdriver.Firefox, limit: int = 31) -> set[str]:
    """Кликает по ячейкам сетки и забирает URL открытого поста."""
    found: set[str] = set()
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.35);")
    time.sleep(PAUSE_MED)

    hrefs = driver.execute_script(
        """
        const nodes = [...document.querySelectorAll('main a[href], article a[href]')];
        const out = [];
        const seen = new Set();
        for (const a of nodes) {
          const h = a.getAttribute('href') || '';
          if (!h || seen.has(h)) continue;
          // пропускаем хайлайты / навигацию
          if (h.includes('/stories/') || h === '/' || h.startsWith('/direct')) continue;
          seen.add(h);
          out.push(h);
        }
        return out;
        """
    ) or []

    log(f"Кандидаты ссылок в main: {len(hrefs)} → {hrefs[:8]}")
    for i, href in enumerate(hrefs[:limit]):
        url = normalize_post_url(href)
        if url:
            found.add(url)
            continue
        # Не post-url — пробуем клик
        try:
            el = driver.find_element(By.CSS_SELECTOR, f'main a[href="{href}"]')
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
            time.sleep(0.3)
            el.click()
            time.sleep(PAUSE_MED)
            opened = normalize_post_url(driver.current_url)
            if opened:
                found.add(opened)
                log(f"  клик {i + 1}: {opened}")
            try:
                driver.find_element(
                    By.CSS_SELECTOR,
                    "svg[aria-label='Close'], button[aria-label='Close'], "
                    "svg[aria-label='Закрыть'], button[aria-label='Закрыть']",
                ).click()
            except NoSuchElementException:
                ActionChains(driver).send_keys(Keys.ESCAPE).perform()
            time.sleep(0.4)
        except Exception as exc:
            log(f"  клик {i + 1} не удался: {exc}")

    return found


def extract_images_from_post(driver: webdriver.Firefox) -> list[str]:
    image_urls: list[str] = []
    seen: set[str] = set()

    def grab() -> None:
        imgs = driver.find_elements(By.CSS_SELECTOR, "article img, div[role='dialog'] img, main img")
        for img in imgs:
            try:
                src = img.get_attribute("src") or ""
                alt = (img.get_attribute("alt") or "").lower()
            except StaleElementReferenceException:
                continue
            if not src.startswith("http"):
                continue
            if "s150x150" in src or "s320x320" in src:
                continue
            if "profile" in alt and "photo" in alt:
                continue
            if src in seen:
                continue
            seen.add(src)
            image_urls.append(src)

    grab()

    for _ in range(12):
        next_btns = driver.find_elements(
            By.CSS_SELECTOR,
            "button[aria-label='Next'], button[aria-label='Далее'], "
            "button[aria-label='Next slide'], button[aria-label='Следующее фото']",
        )
        clicked = False
        for btn in next_btns:
            try:
                if btn.is_displayed() and btn.is_enabled():
                    btn.click()
                    clicked = True
                    time.sleep(PAUSE_SHORT)
                    grab()
                    break
            except Exception:
                continue
        if not clicked:
            break

    image_urls.sort(key=lambda u: ("s1080x1080" in u or "s960x960" in u, len(u)), reverse=True)
    return image_urls


def download_image(url: str, dest: Path) -> bool:
    try:
        req = Request(
            url,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) "
                    "Gecko/20100101 Firefox/128.0"
                ),
                "Referer": "https://www.instagram.com/",
            },
        )
        with urlopen(req, timeout=45) as resp:
            data = resp.read()
        if len(data) < 2_000:
            return False
        dest.write_bytes(data)
        return True
    except Exception as exc:
        log(f"Не удалось скачать {url[:80]}... ({exc})")
        return False


def guess_ext(url: str) -> str:
    path = urlparse(url).path.lower()
    for ext in (".jpg", ".jpeg", ".png", ".webp"):
        if ext in path:
            return ".jpg" if ext == ".jpeg" else ext
    return ".jpg"


def scrape_profile(profile_url: str = PROFILE_URL) -> None:
    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
    manifest: list[dict] = []

    if not any(PROFILE_DIR.glob("*")):
        log("Профиль ещё пустой. Сначала войдите обычным Firefox:")
        log("  python prepare_login.py")
        log("Потом закройте то окно и снова запустите scrape_instagram.py")

    driver = build_driver()
    try:
        log(f"Открываю {profile_url}")
        driver.get(profile_url)
        time.sleep(PAUSE_LONG)
        dismiss_cookies(driver)
        wait_until_ready()
        dismiss_cookies(driver)

        if "openwidellc" not in driver.current_url.lower():
            log("Перехожу снова на профиль...")
            driver.get(profile_url)
            time.sleep(PAUSE_LONG)
            dismiss_cookies(driver)

        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='/p/'], header, main"))
            )
        except TimeoutException:
            log("Страница профиля долго грузится. Проверьте окно браузера.")

        post_urls = collect_post_urls(driver)
        log(f"Всего постов к обходу: {len(post_urls)}")

        if not post_urls:
            log("Посты не найдены. Сделайте python prepare_login.py и войдите снова.")
            log("Оставлю браузер открытым на 60 секунд...")
            time.sleep(60)
            return

        for index, post_url in enumerate(post_urls, start=1):
            log(f"[{index}/{len(post_urls)}] Открываю {post_url}")
            driver.get(post_url)
            time.sleep(PAUSE_LONG)
            dismiss_cookies(driver)

            try:
                WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "article img, main img"))
                )
            except TimeoutException:
                log("  Картинки не появились — пропускаю.")
                continue

            images = extract_images_from_post(driver)
            unique: list[str] = []
            fingerprints: set[str] = set()
            for url in images:
                fp = hashlib.md5(urlparse(url).path.encode()).hexdigest()
                if fp in fingerprints:
                    continue
                fingerprints.add(fp)
                unique.append(url)

            log(f"  Найдено изображений: {len(unique)}")
            saved_files: list[str] = []
            for img_i, img_url in enumerate(unique, start=1):
                ext = guess_ext(img_url)
                filename = f"post_{index:03d}_{img_i:02d}{ext}"
                dest = DOWNLOAD_DIR / filename
                if dest.exists() and dest.stat().st_size > 2_000:
                    log(f"  Уже есть: {filename}")
                    saved_files.append(filename)
                    continue
                ok = download_image(img_url, dest)
                if ok:
                    log(f"  Сохранено: {filename}")
                    saved_files.append(filename)
                time.sleep(0.35)

            manifest.append({"post_url": post_url, "images": saved_files})

        MANIFEST_PATH.write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        total_files = sum(len(item["images"]) for item in manifest)
        log(f"Готово. Постов: {len(manifest)}, файлов: {total_files}")
        log(f"Папка: {DOWNLOAD_DIR}")
        log(f"Манифест: {MANIFEST_PATH}")
        log("Браузер закроется через 5 секунд...")
        time.sleep(5)
    finally:
        driver.quit()


def main() -> None:
    log("Старт парсера (профиль с сохранённой сессией)")
    scrape_profile(PROFILE_URL)


if __name__ == "__main__":
    main()
