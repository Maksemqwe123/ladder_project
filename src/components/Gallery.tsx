import { INSTAGRAM_URL, works } from "../data/site";
import { useReveal } from "../hooks/useReveal";
import "./Gallery.css";

export function Gallery() {
  const ref = useReveal<HTMLElement>();

  return (
    <section className="section gallery" id="works" ref={ref}>
      <div className="section-inner">
        <div className="section-head reveal">
          <span className="eyebrow">Портфолио</span>
          <h2>Работы</h2>
          <p>
            Лестницы из массива для частных интерьеров — от классики до современных
            акцентов.
          </p>
        </div>

        <div className="gallery-grid">
          {works.map((item, index) => (
            <a
              key={item.src}
              className={`gallery-item reveal reveal-delay-${(index % 3) + 1}`}
              href={INSTAGRAM_URL}
              target="_blank"
              rel="noreferrer"
            >
              <img src={item.src} alt={item.alt} loading="lazy" />
              <span className="gallery-hint">Открыть в Instagram</span>
            </a>
          ))}
        </div>

        <div className="gallery-cta reveal">
          <a className="btn btn-primary" href={INSTAGRAM_URL} target="_blank" rel="noreferrer">
            Все работы в Instagram
          </a>
        </div>
      </div>
    </section>
  );
}
