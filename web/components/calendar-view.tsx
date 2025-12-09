"use client"

import { useState } from "react"
import { ChevronLeft, ChevronRight } from "lucide-react"
import { Button } from "./ui/button"
import { Card } from "./ui/card"

export function CalendarView() {
  const [currentDate, setCurrentDate] = useState(new Date())

  const monthNames = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
  ]

  const daysInMonth = new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 0).getDate()

  const firstDayOfMonth = new Date(currentDate.getFullYear(), currentDate.getMonth(), 1).getDay()

  const days = Array.from({ length: daysInMonth }, (_, i) => i + 1)
  const emptyDays = Array.from({ length: firstDayOfMonth }, (_, i) => i)

  const previousMonth = () => {
    setCurrentDate(new Date(currentDate.getFullYear(), currentDate.getMonth() - 1))
  }

  const nextMonth = () => {
    setCurrentDate(new Date(currentDate.getFullYear(), currentDate.getMonth() + 1))
  }

  const isToday = (day: number) => {
    const today = new Date()
    return (
      day === today.getDate() &&
      currentDate.getMonth() === today.getMonth() &&
      currentDate.getFullYear() === today.getFullYear()
    )
  }

  return (
    <div className="container max-w-4xl py-8 px-4">
      {/* Month selector */}
      <div className="flex items-center justify-between mb-8">
        <Button variant="ghost" size="icon" onClick={previousMonth} className="text-primary hover:bg-primary/10">
          <ChevronLeft className="h-5 w-5" />
        </Button>

        <div className="text-center">
          <h2 className="text-2xl font-bold glow-primary">{monthNames[currentDate.getMonth()]}</h2>
          <p className="text-sm text-muted-foreground">{currentDate.getFullYear()}</p>
        </div>

        <Button variant="ghost" size="icon" onClick={nextMonth} className="text-primary hover:bg-primary/10">
          <ChevronRight className="h-5 w-5" />
        </Button>
      </div>

      {/* Calendar grid */}
      <Card className="p-6">
        <div className="grid grid-cols-7 gap-4 mb-4">
          {["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"].map((day) => (
            <div key={day} className="text-center text-sm font-semibold text-muted-foreground">
              {day}
            </div>
          ))}
        </div>

        <div className="grid grid-cols-7 gap-4">
          {emptyDays.map((_, index) => (
            <div key={`empty-${index}`} />
          ))}

          {days.map((day) => (
            <button
              key={day}
              className={`aspect-square flex items-center justify-center rounded-lg text-sm font-medium transition-all hover:bg-primary/10 ${
                isToday(day) ? "bg-primary text-primary-foreground hover:bg-primary/90" : "text-foreground"
              }`}
            >
              {day}
            </button>
          ))}
        </div>
      </Card>
    </div>
  )
}

