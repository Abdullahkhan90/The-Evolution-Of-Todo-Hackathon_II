import './globals.css'
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import { TaskProvider } from '@/contexts/TaskContext'
import { ChatProvider } from '@/contexts/ChatContext'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Todo App',
  description: 'A simple todo application with user authentication',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <TaskProvider>
          <ChatProvider>{children}</ChatProvider>
        </TaskProvider>
      </body>
    </html>
  )
}