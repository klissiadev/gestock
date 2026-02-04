import { createContext, useContext, useEffect, useState } from "react";

const ChatSessionContext = createContext();

export function ChatSessionProvider({ children }) {
  const [sessionsByOrigin, setSessionsByOrigin] = useState(() => {
    const saved = localStorage.getItem("chatSessionsByOrigin");
    return saved ? JSON.parse(saved) : {};
  });

  useEffect(() => {
    localStorage.setItem(
      "chatSessionsByOrigin",
      JSON.stringify(sessionsByOrigin)
    );
  }, [sessionsByOrigin]);

  const getSession = (origin) => sessionsByOrigin[origin];

  const setSession = (origin, sessionId) => {
    setSessionsByOrigin((prev) => ({
      ...prev,
      [origin]: sessionId,
    }));
  };

  return (
    <ChatSessionContext.Provider value={{ getSession, setSession }}>
      {children}
    </ChatSessionContext.Provider>
  );
}

export const useChatSession = () => useContext(ChatSessionContext);
