import { useEffect, useRef } from "react";

/** Reveal on scroll. Uses data-revealed so React re-renders don't wipe visibility. */
export function useReveal<T extends HTMLElement>() {
  const ref = useRef<T | null>(null);

  useEffect(() => {
    const node = ref.current;
    if (!node) return;

    const markVisible = (el: Element) => {
      el.setAttribute("data-revealed", "true");
    };

    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      markVisible(node);
      node.querySelectorAll(".reveal").forEach(markVisible);
      return;
    }

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            markVisible(entry.target);
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.14, rootMargin: "0px 0px -6% 0px" },
    );

    const targets = node.querySelectorAll(".reveal");
    if (targets.length === 0) {
      node.classList.add("reveal");
      observer.observe(node);
    } else {
      targets.forEach((el) => observer.observe(el));
    }

    return () => observer.disconnect();
  }, []);

  return ref;
}
