# Парсер Instagram (desktop Selenium)

## Почему капча не проходит в Selenium

Instagram часто блокирует вход в автоматизированном Firefox. Поэтому логин делается
в **обычном** Firefox, а парсер потом использует ту же сессию.

## Порядок действий

**1. Закройте все окна Firefox** (важно — профиль не должен быть занят).

**2. Войдите обычным браузером (капча тут нормальная):**
```bash
cd parser
source .venv/bin/activate
python prepare_login.py
```
Войдите, пройдите капчу, убедитесь что аккаунт открылся, **закройте это окно Firefox**.

**3. Запустите парсер:**
```bash
python scrape_instagram.py
```
Он подхватит cookies из `firefox_profile/`. Когда увидите посты `openwidellc` — нажмите **Enter**.
Парсер сам по таймеру больше не стартует.

## Результат

- `parser/downloads/post_XXX_YY.jpg`
- `parser/downloads/manifest.json`

Скопируйте нужные фото в `public/works/` для сайта.
