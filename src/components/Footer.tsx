import { INSTAGRAM_URL, THREADS_URL } from "../data/site";
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
            Изготовление и монтаж лестниц из массива. Минская и Гомельская области.
          </p>
          <div className="cta-row">
            <a className="btn btn-primary" href={INSTAGRAM_URL} target="_blank" rel="noreferrer">
              Написать в Instagram
            </a>
            <a className="btn btn-ghost" href={THREADS_URL} target="_blank" rel="noreferrer">
              Threads
            </a>
          </div>
        </div>

        <div className="footer-meta reveal reveal-delay-1">
          <p>📍 Минская и Гомельская области</p>
          <p>
            <a href={INSTAGRAM_URL} target="_blank" rel="noreferrer">
              @openwidellc
            </a>
          </p>
          <p className="footer-tag">#openwidellc</p>
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
