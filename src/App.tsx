import { About } from "./components/About";
import { Faq } from "./components/Faq";
import { Footer } from "./components/Footer";
import { Gallery } from "./components/Gallery";
import { Hero } from "./components/Hero";
import { Materials } from "./components/Materials";
import { Process } from "./components/Process";
import { Services } from "./components/Services";

function App() {
  return (
    <div className="site" id="top">
      <Hero />
      <main>
        <Gallery />
        <Services />
        <Materials />
        <Process />
        <About />
        <Faq />
      </main>
      <Footer />
    </div>
  );
}

export default App;
