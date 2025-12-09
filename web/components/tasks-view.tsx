"use client"

import { useState } from "react"
import { CheckCircle2, Circle, Edit2, Plus } from "lucide-react"
import { Button } from "./ui/button"
import { Card } from "./ui/card"

interface Task {
  id: string
  title: string
  description: string
  isCompleted: boolean
  dueDate?: Date
  createdAt: Date
}

export function TasksView() {
  const [tasks, setTasks] = useState<Task[]>([
    {
      id: "1",
      title: "Review design mockups",
      description: "Check the new UI designs and provide feedback",
      isCompleted: false,
      dueDate: new Date(Date.now() + 86400000),
      createdAt: new Date(),
    },
    {
      id: "2",
      title: "Schedule team meeting",
      description: "Set up next week's planning session",
      isCompleted: false,
      createdAt: new Date(),
    },
    {
      id: "3",
      title: "Update documentation",
      description: "Add new API endpoints to docs",
      isCompleted: true,
      createdAt: new Date(Date.now() - 86400000),
    },
  ])

  const toggleTask = (id: string) => {
    setTasks(tasks.map((task) => (task.id === id ? { ...task, isCompleted: !task.isCompleted } : task)))
  }

  const activeTasks = tasks.filter((t) => !t.isCompleted)
  const completedTasks = tasks.filter((t) => t.isCompleted)

  const formatDueDate = (date: Date) => {
    return date.toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" })
  }

  const TaskCard = ({ task }: { task: Task }) => (
    <Card className="p-4 hover:border-primary/50 transition-colors">
      <div className="flex items-start gap-4">
        <button onClick={() => toggleTask(task.id)} className="shrink-0 mt-0.5">
          {task.isCompleted ? (
            <CheckCircle2 className="h-6 w-6 text-primary" />
          ) : (
            <Circle className="h-6 w-6 text-muted-foreground hover:text-primary transition-colors" />
          )}
        </button>

        <div className="flex-1 min-w-0">
          <h3
            className={`font-medium mb-1 ${task.isCompleted ? "line-through text-muted-foreground" : "text-foreground"}`}
          >
            {task.title}
          </h3>
          {task.description && <p className="text-sm text-muted-foreground mb-2">{task.description}</p>}
          <p className="text-xs text-muted-foreground">
            {task.dueDate ? `Due: ${formatDueDate(task.dueDate)}` : `Created: ${formatDueDate(task.createdAt)}`}
          </p>
        </div>

        <Button variant="ghost" size="icon" className="text-primary hover:bg-primary/10 shrink-0">
          <Edit2 className="h-4 w-4" />
        </Button>
      </div>
    </Card>
  )

  return (
    <div className="container max-w-4xl py-6 px-4 space-y-8">
      {activeTasks.length > 0 && (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-bold">Active Tasks</h2>
            <span className="text-sm text-muted-foreground">
              {activeTasks.length} task{activeTasks.length !== 1 ? "s" : ""}
            </span>
          </div>
          {activeTasks.map((task) => (
            <TaskCard key={task.id} task={task} />
          ))}
        </div>
      )}

      {completedTasks.length > 0 && (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-bold">Completed Tasks</h2>
            <span className="text-sm text-muted-foreground">
              {completedTasks.length} task{completedTasks.length !== 1 ? "s" : ""}
            </span>
          </div>
          {completedTasks.map((task) => (
            <TaskCard key={task.id} task={task} />
          ))}
        </div>
      )}

      {tasks.length === 0 && (
        <div className="flex flex-col items-center justify-center py-20">
          <p className="text-muted-foreground mb-4">No tasks yet</p>
          <Button className="bg-primary hover:bg-primary/90">
            <Plus className="h-4 w-4 mr-2" />
            Create Task
          </Button>
        </div>
      )}
    </div>
  )
}

