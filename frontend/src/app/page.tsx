import Avatar from "@/components/avatar";
import Chat from "@/components/chat";
import { links } from "@/lib/links";

const summary =
  "10 years of production 3D/VR pipeline delivery, now paired with hands-on generative AI systems development. Prototype, build, evaluate, and deploy AI agents, automations, and generative media systems — spanning workflow orchestration, real-time interaction tools, and local image/video/music generation pipelines — turning business and creative requirements into production-ready deliverables. Background in asset pipeline architecture (3DS Max, Unreal, Unity, Substance Suite), cross-functional delivery under strict technical specs, and bridging technical and creative stakeholders.";

export default function Home() {
  return (
    <main className="mx-auto flex max-w-6xl flex-col items-center gap-10 px-6 py-16">
      <section className="flex flex-col items-center gap-6 text-center sm:flex-row sm:items-stretch sm:text-left">
        <Avatar />
        <div className="flex flex-col items-center gap-4 sm:items-start">
          <div>
            <h1 className="text-4xl font-semibold tracking-wide sm:text-5xl">Valeriya Paine</h1>
            <p className="mt-3 text-2xl font-semibold leading-snug text-gold sm:text-3xl">
              Custom AI Solutions | Agentic Workflows | AI Automation Systems
            </p>
          </div>
          <div className="flex flex-wrap justify-center gap-3 sm:justify-start">
            {links.map((link) => (
              <a
                key={link.label}
                href={link.href}
                target="_blank"
                rel="noreferrer"
                className="gold-pill"
              >
                {link.label}
              </a>
            ))}
          </div>
          <p className="max-w-2xl text-lg leading-relaxed text-white/80">{summary}</p>
        </div>
      </section>

      <div className="flex flex-col items-center gap-3">
        <div className="gold-rule" />
        <p className="text-base font-medium uppercase tracking-[0.15em] text-gold">
          Please chat with the assistant below
        </p>
      </div>

      <Chat />
    </main>
  );
}
