"use client";

import { useState } from "react";

export default function Avatar() {
  const [broken, setBroken] = useState(false);

  if (broken) {
    return (
      <div className="flex aspect-square w-16 shrink-0 items-center justify-center rounded-full bg-gold text-lg font-semibold text-ink ring-2 ring-gold/60 shadow-[0_0_20px_rgba(212,175,55,0.25)] sm:aspect-auto sm:w-96 sm:rounded-2xl sm:text-4xl sm:shadow-[0_0_30px_rgba(212,175,55,0.25)]">
        VP
      </div>
    );
  }

  return (
    <div className="aspect-square w-16 shrink-0 overflow-hidden rounded-full ring-2 ring-gold/60 shadow-[0_0_20px_rgba(212,175,55,0.25)] sm:aspect-auto sm:w-96 sm:rounded-2xl sm:shadow-[0_0_30px_rgba(212,175,55,0.25)]">
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
