import { createContext, useContext, useState, ReactNode } from "react";
import { setAuthToken } from "./queryClient";

interface AuthCtx {
  authed: boolean;
  login: (token: string) => void;
  logout: () => void;
}

const Ctx = createContext<AuthCtx>({
  authed: false,
  login: () => {},
  logout: () => {},
});

export function AuthProvider({ children }: { children: ReactNode }) {
  const [authed, setAuthed] = useState(false);
  return (
    <Ctx.Provider
      value={{
        authed,
        login: (token: string) => {
          setAuthToken(token);
          setAuthed(true);
        },
        logout: () => {
          setAuthToken("");
          setAuthed(false);
        },
      }}
    >
      {children}
    </Ctx.Provider>
  );
}

export function useAuth() {
  return useContext(Ctx);
}
