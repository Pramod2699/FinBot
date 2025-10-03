import { ChatInterface } from "@/components/chat-interface"
import { Header } from "@/components/header"

export default function Home() {
  return (
    <div className="min-h-screen bg-background flex flex-col">
      <Header />
      <main className="flex-1 flex items-center justify-center p-4">
        <ChatInterface />
      </main>
    </div>
  )
}
