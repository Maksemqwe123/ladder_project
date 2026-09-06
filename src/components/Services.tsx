import { services } from "../data/site";
import { useReveal } from "../hooks/useReveal";
import "./Services.css";

export function Services() {
  const ref = useReveal<HTMLElement>();

  return (
    <section className="section services" id="services" ref={ref}>
      <div className="section-inner">
        <div className="section-head reveal">
          <span className="eyebrow">Услуги</span>
          <h2>Производство и монтаж</h2>
          <p>
            Производство и монтаж лестниц и других конструкций любой сложности.
          </p>
        </div>

        <ul className="services-list">
          {services.map((item, index) => (
            <li
              key={item.title}
              className={`services-item reveal reveal-delay-${index + 1}`}
            >
              <h3>{item.title}</h3>
              <p>{item.text}</p>
            </li>
          ))}
        </ul>
      </div>
    </section>
  );
}
