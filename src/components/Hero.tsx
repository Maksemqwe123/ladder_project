import { useEffect, useState } from "react";
import { heroSlides, PHONE_DISPLAY, PHONE_HREF } from "../data/site";
import "./Hero.css";

export function Hero() {
  const [active, setActive] = useState(0);

  useEffect(() => {
    const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (reduced || heroSlides.length < 2) return;

    const id = window.setInterval(() => {
      setActive((i) => (i + 1) % heroSlides.length);
    }, 5200);

    return () => window.clearInterval(id);
  }, []);

  useEffect(() => {
    const frame = requestAnimationFrame(() => {
      document.querySelectorAll(".hero .reveal").forEach((el) => {
        el.setAttribute("data-revealed", "true");
      });
    });
    return () => cancelAnimationFrame(frame);
  }, []);

  return (
    <header className="hero">
      <div className="hero-media" aria-hidden="true">
        {heroSlides.map((src, index) => (
          <img
            key={src}
            src={src}
            alt=""
            className={`hero-slide ${index === active ? "is-active" : ""}`}
            loading={index === 0 ? "eager" : "lazy"}
            decoding="async"
          />
        ))}
        <div className="hero-shade" />
      </div>

      <nav className="hero-nav">
        <a className="hero-logo" href="#top" aria-label="OPENWIDELLC — наверх">
          <img src="/brand/mark.svg" alt="" width={28} height={28} />
          <span>OPENWIDELLC</span>
        </a>
        <a className="hero-nav-link" href={PHONE_HREF}>
          {PHONE_DISPLAY}
        </a>
      </nav>

      <div className="hero-content">
        <p className="hero-brand reveal">OPENWIDELLC</p>
        <h1 className="sr-only">Open Wide LLC — лестницы из массива</h1>
        <p className="hero-lead reveal reveal-delay-1">
          Изготовление и монтаж лестниц из массива. Самый простой способ заказать —
          позвонить.
        </p>
        <div className="cta-row reveal reveal-delay-2">
          <a className="btn btn-primary" href={PHONE_HREF}>
            Позвонить
          </a>
          <a className="btn btn-ghost" href="#works">
            Смотреть работы
          </a>
        </div>

        <div className="hero-dots" role="tablist" aria-label="Слайды">
          {heroSlides.map((src, index) => (
            <button
              key={src}
              type="button"
              role="tab"
              aria-selected={index === active}
              className={`hero-dot ${index === active ? "is-active" : ""}`}
              onClick={() => setActive(index)}
            >
              <span className="sr-only">Фото {index + 1}</span>
            </button>
          ))}
        </div>
      </div>
    </header>
  );
}
