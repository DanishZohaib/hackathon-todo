import React, { useState, useRef, useEffect } from "react";
import { useAuth } from "../../hooks/useAuth";
import { useTodos } from "../../hooks/useTodos";
import { getAuthToken } from "../../services/apiClient";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
}

const Chatbot: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputMessage, setInputMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const { user } = useAuth();
  const { addTodo, toggleTodo, deleteTodo, updateTodo } = useTodos();

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async () => {
    if (!inputMessage.trim() || !user?.id) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: inputMessage,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage("");
    setIsLoading(true);

    try {
      // Get API base URL from environment or default
      const API_BASE_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

      // Call the backend chat API - the route is /api/{user_id}/chat according to the backend router configuration
      const response = await fetch(`${API_BASE_URL}/api/${user.id}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${getAuthToken()}`,
        },
        body: JSON.stringify({
          message: inputMessage,
        }),
      });

      if (!response.ok) {
        throw new Error(`Chat API error: ${response.status}`);
      }

      const data = await response.json();

      const assistantMessage: Message = {
        id: Date.now().toString(),
        role: "assistant",
        content: data.response,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, assistantMessage]);

      // Handle any tool calls that were executed
      if (data.tool_calls && Array.isArray(data.tool_calls)) {
        data.tool_calls.forEach((toolCall: any) => {
          try {
            // Process the tool call based on the function name
            switch (toolCall.function?.name) {
              case "add_task":
                if (toolCall.function.arguments) {
                  const args = JSON.parse(toolCall.function.arguments);
                  // Convert to the proper format expected by addTodo
                  addTodo(args.title || "Untitled task");
                }
                break;
              case "complete_task":
                if (toolCall.function.arguments) {
                  const args = JSON.parse(toolCall.function.arguments);
                  toggleTodo(args.task_id);
                }
                break;
              case "delete_task":
                if (toolCall.function.arguments) {
                  const args = JSON.parse(toolCall.function.arguments);
                  deleteTodo(args.task_id);
                }
                break;
              case "update_task":
                if (toolCall.function.arguments) {
                  const args = JSON.parse(toolCall.function.arguments);
                  // Convert to the proper format expected by updateTodo
                  updateTodo(args.task_id, args.title || "Untitled task");
                }
                break;
              case "list_tasks":
                // Just showing the list, no action needed
                break;
            }
          } catch (error) {
            console.error("Error processing tool call:", error);
          }
        });
      }
    } catch (error) {
      console.error("Error sending message:", error);
      const errorMessage: Message = {
        id: Date.now().toString(),
        role: "assistant",
        content: "Sorry, I encountered an error processing your request.",
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="flex flex-col h-full bg-[var(--bg-secondary)] rounded-lg border border-[var(--border-color)] shadow-lg">
      <div className="p-4 border-b border-[var(--border-color)] bg-gradient-to-r from-[var(--pak-green-primary)] to-[var(--pak-green-hover)]">
        <div className="flex items-center space-x-3">
          <div className="relative">
            <div className="w-3 h-3 bg-green-400 rounded-full animate-pulse"></div>
            <div className="absolute top-0 left-0 w-3 h-3 bg-green-400 rounded-full opacity-75 animate-ping"></div>
          </div>
          <h3 className="text-lg font-bold text-white">AI Assistant</h3>
        </div>
        <p className="text-sm text-blue-100 mt-1">Powered by advanced natural language processing</p>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-4 max-h-96 bg-[var(--bg-primary)]">
        {messages.length === 0 ? (
          <div className="text-center py-8 text-[var(--text-secondary)]">
            <div className="flex justify-center mb-4">
              <div className="w-16 h-16 rounded-full bg-gradient-to-r from-[var(--pak-green-primary)] to-[var(--pak-green-hover)] flex items-center justify-center">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-white" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-8-3a1 1 0 00-.867.5 1 1 0 11-1.731-1A3 3 0 0113 8a3.001 3.001 0 01-2 2.83V11a1 1 0 11-2 0v-1a1 1 0 011-1 1 1 0 100-2zm0 8a1 1 0 100-2 1 1 0 000 2z" clipRule="evenodd" />
                </svg>
              </div>
            </div>
            <p className="font-medium text-[var(--text-primary)]">Hello! I'm your AI assistant.</p>
            <p className="mt-2 text-[var(--text-secondary)]">Ask me to manage your tasks naturally</p>
            <div className="mt-4 p-4 bg-[var(--bg-secondary)] rounded-lg">
              <p className="text-sm font-medium text-[var(--text-primary)] mb-2">Try saying:</p>
              <ul className="text-xs space-y-1">
                <li className="flex items-start">
                  <span className="text-[var(--pak-green-primary)] mr-2">•</span>
                  <span className="text-[var(--text-secondary)]">"Add a task to buy groceries"</span>
                </li>
                <li className="flex items-start">
                  <span className="text-[var(--pak-green-primary)] mr-2">•</span>
                  <span className="text-[var(--text-secondary)]">"Mark task 1 as complete"</span>
                </li>
                <li className="flex items-start">
                  <span className="text-[var(--pak-green-primary)] mr-2">•</span>
                  <span className="text-[var(--text-secondary)]">"List all my tasks"</span>
                </li>
                <li className="flex items-start">
                  <span className="text-[var(--pak-green-primary)] mr-2">•</span>
                  <span className="text-[var(--text-secondary)]">"Delete the meeting task"</span>
                </li>
              </ul>
            </div>
          </div>
        ) : (
          messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.role === "user" ? "justify-end" : "justify-start"}`}
            >
              <div
                className={`max-w-xs md:max-w-md px-4 py-3 rounded-2xl ${
                  message.role === "user"
                    ? "bg-gradient-to-r from-[var(--pak-green-primary)] to-[var(--pak-green-hover)] text-white ml-4"
                    : "bg-[var(--bg-primary)] text-[var(--text-primary)] border border-[var(--border-color)] mr-4"
                } shadow-md`}
              >
                <div className="whitespace-pre-wrap break-words">{message.content}</div>
                <div className={`text-xs mt-2 opacity-70 ${message.role === "user" ? "text-blue-100" : "text-gray-500"}`}>
                  {message.timestamp.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
                </div>
              </div>
            </div>
          ))
        )}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-[var(--bg-primary)] text-[var(--text-primary)] border border-[var(--border-color)] px-4 py-3 rounded-2xl mr-4 shadow-md">
              <div className="flex items-center space-x-2">
                <div className="flex space-x-1">
                  <div className="w-2 h-2 bg-[var(--pak-green-primary)] rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-[var(--pak-green-primary)] rounded-full animate-bounce" style={{ animationDelay: "0.2s" }}></div>
                  <div className="w-2 h-2 bg-[var(--pak-green-primary)] rounded-full animate-bounce" style={{ animationDelay: "0.4s" }}></div>
                </div>
                <span className="text-sm">Thinking...</span>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="p-4 border-t border-[var(--border-color)] bg-[var(--bg-primary)]">
        <div className="flex space-x-2">
          <textarea
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask me to manage your tasks..."
            className="flex-1 resize-none border border-[var(--border-color)] rounded-xl px-4 py-3 bg-[var(--bg-secondary)] text-[var(--text-primary)] focus:outline-none focus:ring-2 focus:ring-[var(--pak-green-primary)] focus:ring-offset-2 transition-all duration-200"
            rows={2}
          />
          <button
            onClick={sendMessage}
            disabled={isLoading || !inputMessage.trim() || !user?.id}
            className="px-6 py-3 bg-gradient-to-r from-[var(--pak-green-primary)] to-[var(--pak-green-hover)] text-white rounded-xl hover:from-[var(--pak-green-hover)] hover:to-[var(--pak-green-primary)] disabled:opacity-50 disabled:cursor-not-allowed focus:outline-none focus:ring-2 focus:ring-[var(--pak-green-primary)] focus:ring-offset-2 transition-all duration-200 shadow-md hover:shadow-lg transform hover:-translate-y-0.5"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clipRule="evenodd" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  );
};

export default Chatbot;