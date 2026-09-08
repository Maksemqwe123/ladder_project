import {
  EMAIL,
  EMAIL_HREF,
  INSTAGRAM_URL,
  PHONE_DISPLAY,
  PHONE_HREF,
} from "../data/site";
import { useReveal } from "../hooks/useReveal";
import "./Footer.css";

export function Footer() {
  const ref = useReveal<HTMLElement>();

  return (
    <footer className="footer" id="contact" ref={ref}>
      <div className="section-inner footer-inner">
        <div className="footer-main reveal">
          <p className="footer-brand">OPENWIDELLC</p>
          <p className="footer-lead">
            Хотите заказать лестницу? Позвоните — так быстрее всего. Мы на связи и
            перезвоним, если нужно уточнить детали.
          </p>
          <div className="cta-row">
            <a className="btn btn-primary" href={PHONE_HREF}>
              Позвонить {PHONE_DISPLAY}
            </a>
            <a className="btn btn-ghost" href={EMAIL_HREF}>
              Написать на почту
            </a>
          </div>
        </div>

        <div className="footer-meta reveal reveal-delay-1">
          <p>📍 Минская и Гомельская области</p>
          <p>
            <a href={PHONE_HREF}>{PHONE_DISPLAY}</a>
          </p>
          <p>
            <a href={EMAIL_HREF}>{EMAIL}</a>
          </p>
          <p>
            <a href={INSTAGRAM_URL} target="_blank" rel="noreferrer">
              Instagram @openwidellc
            </a>
          </p>
        </div>
      </div>
      <div className="footer-bottom">
        <div className="section-inner">
          <p>© {new Date().getFullYear()} Open Wide LLC</p>
        </div>
      </div>
    </footer>
  );
}
