import { useState } from "react";
import { faqs } from "../data/site";
import { useReveal } from "../hooks/useReveal";
import "./Faq.css";

export function Faq() {
  const ref = useReveal<HTMLElement>();
  const [openIndex, setOpenIndex] = useState<number | null>(0);

  return (
    <section className="section faq" id="faq" ref={ref}>
      <div className="section-inner faq-layout">
        <div className="section-head reveal">
          <span className="eyebrow">F.A.Q.</span>
          <h2>Ваши вопросы</h2>
          <p>Короткие ответы перед тем, как написать нам в Instagram.</p>
        </div>

        <div className="faq-list">
          {faqs.map((item, index) => {
            const open = openIndex === index;
            return (
              <div key={item.q} className={`faq-item ${open ? "is-open" : ""}`}>
                <button
                  type="button"
                  className="faq-trigger"
                  aria-expanded={open}
                  onClick={() => setOpenIndex(open ? null : index)}
                >
                  <span>{item.q}</span>
                  <span className="faq-icon" aria-hidden="true" />
                </button>
                {open ? (
                  <div className="faq-panel">
                    <p>{item.a}</p>
                  </div>
                ) : null}
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
