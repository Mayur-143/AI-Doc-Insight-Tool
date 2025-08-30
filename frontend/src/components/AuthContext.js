import { createContext, useState } from "react";
import axios from "axios";

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [token, setToken] = useState(localStorage.getItem("token"));

  const login = async (username, password) => {
    const res = await axios.post("http://127.0.0.1:8000/login", new URLSearchParams({
      username, password
    }));
    setToken(res.data.access_token);
    localStorage.setItem("token", res.data.access_token);
  };

  const logout = () => {
    setToken(null);
    localStorage.removeItem("token");
  };

  return (
    <AuthContext.Provider value={{ token, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};
