"use client"

import { useState } from "react"
import { Sparkles } from "lucide-react"
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"

interface AddThoughtDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
}

export function AddThoughtDialog({ open, onOpenChange }: AddThoughtDialogProps) {
  const [content, setContent] = useState("")
  const [isProcessing, setIsProcessing] = useState(false)

  const handleSubmit = async () => {
    if (!content.trim()) return

    setIsProcessing(true)

    // Simulate AI processing
    await new Promise((resolve) => setTimeout(resolve, 1500))

    setIsProcessing(false)
    setContent("")
    onOpenChange(false)
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-lg">
        <DialogHeader>
          <DialogTitle className="text-2xl font-bold">Add a Thought</DialogTitle>
        </DialogHeader>

        <div className="space-y-4 py-4">
          <Textarea
            placeholder="What's on your mind?"
            value={content}
            onChange={(e) => setContent(e.target.value)}
            className="min-h-[150px] resize-none bg-secondary/50 border-border focus:border-primary"
            disabled={isProcessing}
          />

          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            <Sparkles className="h-4 w-4 text-primary" />
            <span>AI will extract tasks automatically</span>
          </div>
        </div>

        <div className="flex justify-end gap-3">
          <Button variant="outline" onClick={() => onOpenChange(false)} disabled={isProcessing}>
            Cancel
          </Button>
          <Button
            onClick={handleSubmit}
            disabled={!content.trim() || isProcessing}
            className="bg-primary hover:bg-primary/90"
          >
            {isProcessing ? (
              <>
                <Sparkles className="h-4 w-4 mr-2 animate-spin" />
                Processing...
              </>
            ) : (
              "Save Thought"
            )}
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  )
}

