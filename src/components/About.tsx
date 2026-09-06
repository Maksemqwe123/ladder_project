import { useReveal } from "../hooks/useReveal";
import "./About.css";

export function About() {
  const ref = useReveal<HTMLElement>();

  return (
    <section className="section about" id="about" ref={ref}>
      <div className="section-inner about-layout">
        <div className="about-visual reveal" aria-hidden="true">
          <img src="/works/work-4.jpg" alt="" />
        </div>
        <div className="about-copy">
          <span className="eyebrow reveal">Мы</span>
          <h2 className="reveal reveal-delay-1">Лестница как акцент интерьера</h2>
          <p className="reveal reveal-delay-2">
            Open Wide LLC делает лестницы из массива так, чтобы они собирали
            пространство вокруг себя: свет, линии, фактура дерева.
          </p>
          <p className="reveal reveal-delay-3">
            Работаем по Минской и Гомельской областям — от идеи и замера до
            изготовления и монтажа.
          </p>
        </div>
      </div>
    </section>
  );
}
