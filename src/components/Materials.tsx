import { materials } from "../data/site";
import { useReveal } from "../hooks/useReveal";
import "./Materials.css";

export function Materials() {
  const ref = useReveal<HTMLElement>();

  return (
    <section className="section materials" id="materials" ref={ref}>
      <div className="section-inner materials-layout">
        <div className="section-head reveal">
          <span className="eyebrow">Материалы</span>
          <h2>Массив, отделка, металл</h2>
          <p>
            Подбираем породу, тон и ограждение так, чтобы лестница стала акцентом
            интерьера — а не просто переходом между этажами.
          </p>
        </div>

        <ol className="materials-list">
          {materials.map((item, index) => (
            <li
              key={item.title}
              className={`materials-item reveal reveal-delay-${index + 1}`}
            >
              <span className="materials-index">0{index + 1}</span>
              <div>
                <h3>{item.title}</h3>
                <p>{item.text}</p>
              </div>
            </li>
          ))}
        </ol>
      </div>
    </section>
  );
}
