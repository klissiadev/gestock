import { createContext, useContext, useRef } from "react";

const ChatSessionContext = createContext();

export function ChatSessionProvider({ children }) {
  const sessionsByOrigin = useRef({});

  const getSession = (origin) => sessionsByOrigin.current[origin];
  const setSession = (origin, sessionId) => {
    sessionsByOrigin.current[origin] = sessionId;
  };

  return (
    <ChatSessionContext.Provider value={{ getSession, setSession }}>
      {children}
    </ChatSessionContext.Provider>
  );
}

export const useChatSession = () => useContext(ChatSessionContext);
