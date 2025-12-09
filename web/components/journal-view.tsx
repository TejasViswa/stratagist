"use client"

import { useState, useEffect } from "react"
import { ChevronLeft, ChevronRight, Edit2, Trash2 } from "lucide-react"
import { Button } from "./ui/button"
import { Card } from "./ui/card"

interface Thought {
  id: string
  content: string
  timestamp: Date
}

export function JournalView() {
  const [currentDateIndex, setCurrentDateIndex] = useState(0)
  const [availableDates, setAvailableDates] = useState<Date[]>([])
  const [thoughts, setThoughts] = useState<Thought[]>([])

  useEffect(() => {
    // Initialize with last 7 days
    const dates: Date[] = []
    for (let i = 0; i < 7; i++) {
      const date = new Date()
      date.setDate(date.getDate() - i)
      dates.push(date)
    }
    setAvailableDates(dates)

    // Load sample data
    loadSampleThoughts()
  }, [])

  const loadSampleThoughts = () => {
    const sampleThoughts: Thought[] = [
      {
        id: "1",
        content: "Had a great brainstorming session about the new project. Need to follow up on the design mockups.",
        timestamp: new Date(),
      },
      {
        id: "2",
        content: "Remember to schedule the team meeting for next week. Also, review the quarterly goals.",
        timestamp: new Date(Date.now() - 3600000),
      },
      {
        id: "3",
        content: "Interesting idea: What if we integrated AI-powered suggestions into the workflow?",
        timestamp: new Date(Date.now() - 7200000),
      },
    ]
    setThoughts(sampleThoughts)
  }

  const currentDate = availableDates[currentDateIndex] || new Date()

  const formatDate = (date: Date) => {
    const today = new Date()
    if (
      date.getDate() === today.getDate() &&
      date.getMonth() === today.getMonth() &&
      date.getFullYear() === today.getFullYear()
    ) {
      return "Today"
    }
    return date.toLocaleDateString("en-US", { month: "long", day: "numeric", year: "numeric" })
  }

  const formatTime = (date: Date) => {
    return date.toLocaleTimeString("en-US", { hour: "numeric", minute: "2-digit" })
  }

  const filteredThoughts = thoughts.filter((thought) => {
    return (
      thought.timestamp.getDate() === currentDate.getDate() &&
      thought.timestamp.getMonth() === currentDate.getMonth() &&
      thought.timestamp.getFullYear() === currentDate.getFullYear()
    )
  })

  return (
    <div className="flex flex-col h-full">
      {/* Date navigator */}
      <div className="sticky top-0 z-10 bg-card/95 backdrop-blur border-b border-primary/20 px-4 py-4">
        <div className="container max-w-4xl mx-auto flex items-center justify-between">
          <Button
            variant="ghost"
            size="icon"
            onClick={() => setCurrentDateIndex(Math.max(0, currentDateIndex - 1))}
            disabled={currentDateIndex === 0}
            className="text-primary hover:bg-primary/10 disabled:opacity-30"
          >
            <ChevronLeft className="h-5 w-5" />
          </Button>

          <div className="text-center">
            <h2 className="text-xl font-bold glow-primary">{formatDate(currentDate)}</h2>
            <p className="text-sm text-muted-foreground">
              {currentDate.toLocaleDateString("en-US", { weekday: "long" })}
            </p>
          </div>

          <Button
            variant="ghost"
            size="icon"
            onClick={() => setCurrentDateIndex(Math.min(availableDates.length - 1, currentDateIndex + 1))}
            disabled={currentDateIndex >= availableDates.length - 1}
            className="text-primary hover:bg-primary/10 disabled:opacity-30"
          >
            <ChevronRight className="h-5 w-5" />
          </Button>
        </div>
      </div>

      {/* Thoughts list */}
      <div className="flex-1 overflow-auto">
        <div className="container max-w-4xl mx-auto py-6 px-4 space-y-4">
          {filteredThoughts.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-20">
              <p className="text-muted-foreground mb-4">No thoughts for {formatDate(currentDate)}</p>
              <Button
                variant="outline"
                className="border-primary/50 text-primary hover:bg-primary/10 bg-transparent"
                onClick={loadSampleThoughts}
              >
                Add Sample Data
              </Button>
            </div>
          ) : (
            <>
              <div className="flex items-center justify-between mb-4">
                <p className="text-sm text-muted-foreground">
                  {filteredThoughts.length} thought{filteredThoughts.length !== 1 ? "s" : ""}
                </p>
                <Button variant="ghost" size="sm" className="text-destructive hover:bg-destructive/10 h-8">
                  <Trash2 className="h-4 w-4 mr-2" />
                  Clear
                </Button>
              </div>

              {filteredThoughts.map((thought) => (
                <Card key={thought.id} className="p-4 hover:border-primary/50 transition-colors">
                  <div className="flex items-start justify-between gap-4">
                    <div className="flex-1">
                      <p className="text-foreground leading-relaxed mb-2">{thought.content}</p>
                      <p className="text-sm text-muted-foreground">{formatTime(thought.timestamp)}</p>
                    </div>
                    <Button variant="ghost" size="icon" className="text-primary hover:bg-primary/10 shrink-0">
                      <Edit2 className="h-4 w-4" />
                    </Button>
                  </div>
                </Card>
              ))}
            </>
          )}
        </div>
      </div>
    </div>
  )
}

