import Avatar from "@/components/avatar";
import Chat from "@/components/chat";
import { links } from "@/lib/links";

const summary =
  "10 years of production 3D/VR pipeline delivery, now paired with hands-on generative AI systems development. Prototype, build, evaluate, and deploy AI agents, automations, and generative media systems — spanning workflow orchestration, real-time interaction tools, and local image/video/music generation pipelines — turning business and creative requirements into production-ready deliverables. Background in asset pipeline architecture (3DS Max, Unreal, Unity, Substance Suite), cross-functional delivery under strict technical specs, and bridging technical and creative stakeholders.";

export default function Home() {
  return (
    <main className="mx-auto flex h-dvh max-w-6xl flex-col items-center gap-2 overflow-hidden px-4 py-3 sm:gap-4 sm:px-6 sm:py-6">
      <section className="flex w-full shrink-0 flex-row items-center gap-3 text-left sm:items-stretch">
        <Avatar />
        <div className="flex min-w-0 flex-1 flex-col items-start gap-1.5 sm:gap-2">
          <div>
            <h1 className="text-lg font-semibold tracking-wide sm:text-4xl">Valeriya Paine</h1>
            <p className="mt-0.5 text-xs font-semibold leading-snug text-gold sm:mt-2 sm:text-2xl">
              Custom AI Solutions | Agentic Workflows | <span className="whitespace-nowrap">AI Automation Systems</span>
            </p>
          </div>
          <div className="flex flex-wrap gap-2 sm:gap-3">
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
          <p className="hidden max-w-2xl text-sm leading-snug text-white/80 sm:block">{summary}</p>
        </div>
      </section>

      <Chat />
    </main>
  );
}
