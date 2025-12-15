import React, { useEffect, useState } from 'react';
import { handlePTable } from '../api/viewApi';
import '../style/productTable.css'

const ProductTable = () => {
    const [table, setTable] = useState(null);
    const [orderBy, setOrderBy] = useState("cod_produto");
    const [isAsc, setIsAsc] = useState(true);

    const [digitado, setDigitado] = useState('');
    const [searchTerm, setSearchTerm] = useState("");

    const [categoria, setCategoria] = useState("");
    const [opcoesCategoria, setOpcoesCategoria] = useState([]);

    useEffect(() => {
        const carregarDados = async () => {
            try {
                // Busca os dados filtrados do backend
                const dados = await handlePTable(orderBy, isAsc, searchTerm, categoria);
                setTable(dados);

                // Primeira vez que carrega -> salva as opcoes de categoria pela primeira vez e tals
                setOpcoesCategoria((prevOpcoes) => {
                    if (prevOpcoes.length === 0 && dados && dados.length > 0) {
                        return [...new Set(
                            dados
                                .map(item => item.categoria)
                                .filter(c => c)
                        )].sort();
                    }
                    return prevOpcoes;
                });

            } catch (error) {
                console.error("Erro ao buscar tabela:", error);
                setTable([]);
            }
        };
        carregarDados();

    }, [searchTerm, orderBy, isAsc, categoria]);

    const handlePesquisar = () => {
        setSearchTerm(digitado);
    };

    if (!table) return <div>Carregando...</div>;

    const colunas = table.length > 0 ? Object.keys(table[0]) : [];

    return (
        <div className="tabela-container">
            {/* ... Seletor de ordenação ... */}
            <div className='orderby-container'>
                <h2>Ordenação da tabela</h2>
                <select
                    value={orderBy}
                    onChange={(e) => setOrderBy(e.target.value)}
                >
                    {colunas.map(coluna => (
                        <option key={coluna} value={coluna}>
                            {coluna.replace('_', ' ')}
                        </option>
                    ))}
                </select>
                <button onClick={() => setIsAsc(!isAsc)}>
                    {isAsc ? "⬇️" : "⬆️"}
                </button>
            </div>

            <div className='filter-container'>
                <h2>Busca de produtos</h2>

                <input
                    type="text"
                    placeholder="Digite para buscar..."
                    value={digitado}
                    onChange={(e) => setDigitado(e.target.value)}
                    onKeyDown={(e) => e.key === 'Enter' && handlePesquisar()}
                />
                <button type="button" onClick={handlePesquisar}>
                    Pesquisar
                </button>

                {/* Dropdown das categorias*/}
                <select
                    value={categoria}
                    onChange={(e) => setCategoria(e.target.value)}
                >
                    <option value="">Todas as Categorias</option>
                    {opcoesCategoria.map((cat) => (
                        <option key={cat} value={cat}>
                            {cat}
                        </option>
                    ))}
                </select>
            </div>

            <h2 style={{ textAlign: 'center', color: '#333' }}>Lista de Produtos</h2>

            {/* Verificação visual se não houver dados */}
            {table.length === 0 ? (
                <p style={{ textAlign: 'center' }}>Nenhum produto encontrado.</p>
            ) : (
                <table className="styled-table">
                    <thead>
                        <tr>
                            {colunas.map(coluna => (
                                <th key={coluna}>{coluna.replace('_', ' ')}</th>
                            ))}
                        </tr>
                    </thead>
                    <tbody>
                        {table.map((item, index) => (
                            <tr key={index}>
                                {colunas.map((coluna) => (
                                    <td key={`${index}-${coluna}`}>
                                        {item[coluna] ? item[coluna] : "Indeterminado"}
                                    </td>
                                ))}
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}
        </div>
    );
}

export default ProductTable;