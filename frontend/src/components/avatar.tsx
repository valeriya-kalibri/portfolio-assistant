"use client";

import { useState } from "react";

export default function Avatar() {
  const [broken, setBroken] = useState(false);

  if (broken) {
    return (
      <div className="flex h-28 w-28 items-center justify-center rounded-full bg-blue-600 text-2xl font-semibold text-white">
        VP
      </div>
    );
  }

  return (
    // eslint-disable-next-line @next/next/no-img-element
    <img
      src="/photo.jpg"
      alt="Valeriya Paine"
      className="h-28 w-28 rounded-full object-cover"
      onError={() => setBroken(true)}
    />
  );
}
