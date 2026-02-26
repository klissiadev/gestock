import { createContext, useContext, useState, useEffect, useCallback } from "react";
import { sendCredencials, registerUser } from "./api/loginService";

const AuthContext = createContext({});

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const isAdmin = true;


    // Da um ping pra verificar sessão e pega informacoes basicas do usuario
    const verificarSessao = useCallback(async (token) => {
        try {
            const response = await fetch('http://127.0.0.1:8000/auth/me', {
                method: 'GET',
                headers: { 'Authorization': `Bearer ${token}` }
            });

            if (response.ok) {
                const dadosUsuario = await response.json();
                setUser(dadosUsuario);
                console.log("Sessão verificada, usuário:", dadosUsuario);
            } else {
                localStorage.removeItem('token');
                setUser(null);
            }
        } catch (err) {
            console.error("Erro na conexão:", err);
            setUser(null);
        } finally {
            setLoading(false);
        }
    }, []);

    // Pela primeira vez, verifica se está com token e se ele funciona
    useEffect(() => {
        const token = localStorage.getItem('token');
        if (token) {
            verificarSessao(token);
        } else {
            setLoading(false);
        }
    }, []);

    // lida com o login
    const login = async (email, password) => {
        setError(null);
        setLoading(true);
        try {
            const dados = await sendCredencials(email, password);
            if (dados.access_token) {
                localStorage.setItem('token', dados.access_token);
                await verificarSessao(dados.access_token);
                return true;
            }
        } catch (err) {
            setError("E-mail ou senha inválidos");
            throw err;
        } finally {
            setLoading(false);
        }
    };

    // Da logout
    const logout = () => {
        localStorage.removeItem('token');
        setUser(null);
    };

    // Responsavel pelo registro do usuario
    const register = async (nome, email, password, papel) => {
        setError(null);
        setLoading(true);
        try {
            //const token = localStorage.getItem('token');
            const resposta = await registerUser(nome, email, password, papel);
            // Geralmente redirecionamos para o login ou exibimos uma mensagem verde.
            console.log("Usuário registrado:", resposta.message);
            return { success: true };
        } catch (err) {
            setError(err.message);
            return { success: false, error: err.message };
        } finally {
            setLoading(false);
        }
    };

    // Resetando a senha: pega nova senha e cadastra la
    const resetPassword = async (token, newPassword) => {
        try {
            const response = await fetch('http://127.0.0.1:8000/auth/reset-password', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ token, new_password: newPassword }) // Bate com o seu backend Python
            });
            return response.ok;
        } catch (err) {
            alert("Erro: ", err);
        }
    };

    // enviando email de recuperacao
    const sendRecoveryEmail = async (email) => {
        setLoading(true);
        setError(null);
        try {
            const response = await fetch('http://127.0.0.1:8000/auth/forgot-password', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email })
            });

            if (!response.ok) {
                const data = await response.json();
                throw new Error(data.detail || "E-mail não encontrado.");
            }

            return true; // Sucesso
        } catch (err) {
            setError(err.message);
            return false;
        } finally {
            setLoading(false);
        }
    };


    return (
        <AuthContext.Provider value={{ user, loading, error, login, logout, register, resetPassword, sendRecoveryEmail, isAdmin}}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);