import Avatar from "@/components/avatar";
import Chat from "@/components/chat";
import { links } from "@/lib/links";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center gap-8 px-6 py-16">
      <div className="flex flex-col items-center gap-4 text-center">
        <Avatar />
        <div>
          <h1 className="text-2xl font-semibold">Valeriya Paine</h1>
          <p className="mt-1 text-sm text-neutral-400">
            AI Solutions Engineer | Creative Technologist
          </p>
        </div>
        <div className="flex gap-4 text-sm">
          {links.map((link) => (
            <a
              key={link.label}
              href={link.href}
              target="_blank"
              rel="noreferrer"
              className="text-blue-400 hover:text-blue-300"
            >
              {link.label}
            </a>
          ))}
        </div>
      </div>
      <Chat />
    </main>
  );
}
