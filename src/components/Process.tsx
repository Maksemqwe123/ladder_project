import { processSteps } from "../data/site";
import { useReveal } from "../hooks/useReveal";
import "./Process.css";

export function Process() {
  const ref = useReveal<HTMLElement>();

  return (
    <section className="section process" id="order" ref={ref}>
      <div className="section-inner">
        <div className="section-head reveal">
          <span className="eyebrow">Оформление заказа</span>
          <h2>Как заказать</h2>
          <p>Короткий путь от сообщения до готовой лестницы на объекте.</p>
        </div>

        <ol className="process-list">
          {processSteps.map((item, index) => (
            <li
              key={item.step}
              className={`process-item reveal reveal-delay-${(index % 3) + 1}`}
            >
              <span className="process-step">{item.step}</span>
              <h3>{item.title}</h3>
              <p>{item.text}</p>
            </li>
          ))}
        </ol>
      </div>
    </section>
  );
}
