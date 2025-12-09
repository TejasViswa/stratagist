"use client"

import { useEffect, useState } from "react"
import { Brain } from "lucide-react"

export function SplashScreen() {
  const [fadeIn, setFadeIn] = useState(false)
  const [fadeOut, setFadeOut] = useState(false)

  useEffect(() => {
    setFadeIn(true)

    const timer = setTimeout(() => {
      setFadeOut(true)
    }, 2500)

    return () => clearTimeout(timer)
  }, [])

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-background overflow-hidden">
      {/* Purple glow orb at bottom */}
      <div className="absolute bottom-0 left-1/2 -translate-x-1/2 w-[150vw] h-[150vw] rounded-full bg-primary/20 glow-orb blur-3xl" />

      {/* Content */}
      <div
        className={`relative z-10 flex flex-col items-center gap-6 transition-opacity duration-1000 ${
          fadeIn && !fadeOut ? "opacity-100" : "opacity-0"
        }`}
      >
        <div className="w-28 h-28 rounded-2xl bg-gradient-to-br from-primary/30 to-primary/10 flex items-center justify-center backdrop-blur-sm border border-primary/20">
          <Brain className="w-16 h-16 text-primary" strokeWidth={1.5} />
        </div>

        <h1 className="text-5xl font-bold text-foreground tracking-tight glow-primary">StrataGist</h1>
      </div>
    </div>
  )
}

