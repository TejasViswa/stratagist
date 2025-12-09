"use client"

import { useState } from "react"
import { CalendarDays, BookOpen, CheckSquare, Plus, Menu } from "lucide-react"
import { CalendarView } from "./calendar-view"
import { JournalView } from "./journal-view"
import { TasksView } from "./tasks-view"
import { AddThoughtDialog } from "./add-thought-dialog"
import { Button } from "./ui/button"

type View = "calendar" | "journal" | "tasks"

export function AppShell() {
  const [currentView, setCurrentView] = useState<View>("journal")
  const [showAddDialog, setShowAddDialog] = useState(false)

  const views = {
    calendar: { title: "Calendar", component: CalendarView },
    journal: { title: "Journal", component: JournalView },
    tasks: { title: "Tasks", component: TasksView },
  }

  const CurrentViewComponent = views[currentView].component

  return (
    <div className="flex flex-col h-screen bg-background">
      {/* Header */}
      <header className="sticky top-0 z-40 border-b border-border/50 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container flex h-16 items-center justify-between px-4">
          <h1 className="text-3xl font-black tracking-tight glow-primary">{views[currentView].title}</h1>

          <div className="flex items-center gap-2">
            <Button
              variant="ghost"
              size="icon"
              onClick={() => setCurrentView("tasks")}
              className="text-primary hover:text-primary hover:bg-primary/10"
            >
              <CheckSquare className="h-5 w-5" />
            </Button>

            <Button variant="ghost" size="icon" className="text-muted-foreground hover:text-foreground">
              <Menu className="h-5 w-5" />
            </Button>
          </div>
        </div>
      </header>

      {/* Main content */}
      <main className="flex-1 overflow-auto">
        <CurrentViewComponent />
      </main>

      {/* Bottom navigation */}
      <nav className="sticky bottom-0 z-40 border-t border-border/50 bg-card/95 backdrop-blur supports-[backdrop-filter]:bg-card/60">
        <div className="container flex h-20 items-center justify-around px-4">
          <button
            onClick={() => setCurrentView("calendar")}
            className={`flex flex-col items-center gap-1 transition-colors ${
              currentView === "calendar" ? "text-primary" : "text-muted-foreground"
            }`}
          >
            <CalendarDays className="h-6 w-6" />
            <span className="text-xs font-medium">Calendar</span>
          </button>

          <button onClick={() => setShowAddDialog(true)} className="flex flex-col items-center gap-1 -mt-8">
            <div className="w-14 h-14 rounded-full bg-primary flex items-center justify-center shadow-lg shadow-primary/50 hover:shadow-primary/70 transition-shadow">
              <Plus className="h-7 w-7 text-primary-foreground" strokeWidth={3} />
            </div>
          </button>

          <button
            onClick={() => setCurrentView("journal")}
            className={`flex flex-col items-center gap-1 transition-colors ${
              currentView === "journal" ? "text-primary" : "text-muted-foreground"
            }`}
          >
            <BookOpen className="h-6 w-6" />
            <span className="text-xs font-medium">Journal</span>
          </button>
        </div>
      </nav>

      {/* Add thought dialog */}
      <AddThoughtDialog open={showAddDialog} onOpenChange={setShowAddDialog} />
    </div>
  )
}

