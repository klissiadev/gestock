import { createContext, useContext, useState } from "react";

const HeaderContext = createContext();

export function HeaderProvider({ children }) {
  const [headerConfig, setHeaderConfig] = useState({});

  return (
    <HeaderContext.Provider value={{ headerConfig, setHeaderConfig }}>
      {children}
    </HeaderContext.Provider>
  );
}

export function useHeader() {
  return useContext(HeaderContext);
}
