"use client";

import { useState } from "react";

export default function Avatar() {
  const [broken, setBroken] = useState(false);

  if (broken) {
    return (
      <div className="flex aspect-[4/5] w-56 shrink-0 items-center justify-center rounded-2xl bg-gold text-4xl font-semibold text-ink ring-2 ring-gold/60 shadow-[0_0_30px_rgba(212,175,55,0.25)] sm:aspect-auto sm:w-96">
        VP
      </div>
    );
  }

  return (
    <div className="aspect-[4/5] w-56 shrink-0 overflow-hidden rounded-2xl ring-2 ring-gold/60 shadow-[0_0_30px_rgba(212,175,55,0.25)] sm:aspect-auto sm:w-96">
      {/* eslint-disable-next-line @next/next/no-img-element */}
      <img
        src="/photo.jpg"
        alt="Valeriya Paine"
        className="h-full w-full object-cover"
        onError={() => setBroken(true)}
      />
    </div>
  );
}
