import React, { useEffect, useState, useRef } from 'react';
import { handlePTable } from '../api/viewApi';
import '../style/productTable.css'
const ProductTable = () => {
    const [table, setTable] = useState(null);
    const [orderBy, setOrderBy] = useState("cod_produto"); // Hack: garantir que o order by receba alguma coisa que nao seja null
    const [isAsc, setIsAsc] = useState(true);


    // Eu tinha notado que tava chamando 2 vezes a API (só pra garantir que isso nao vai acontecer)
    useEffect(() => {
        const carregarDados = async () => {
            try {
                const dados = await handlePTable(orderBy, isAsc);
                setTable(dados);
            } catch (error) {
                console.error("Erro ao buscar tabela:", error);
            }
        };
        carregarDados();

    }, [orderBy, isAsc]);

    // verificacao dinamica

    if (!table) return <div>Carregando...</div>;
    if (table.length === 0) return <div>Sem dados...</div>;


    // Formatacao da tabela
    const colunas = Object.keys(table[0]);

    return (
        <div className="tabela-container">

            <div className='orderby-container'>
                <h2>Ordenação da tabela</h2>
                {/* Seletor de ordenação */}
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

                {/* Botao para representar ordem crescente e decrescente*/}
                <button
                    value={isAsc}
                    onClick={() => setIsAsc(!isAsc)}
                >
                    {isAsc ? (
                        <svg className="w-6 h-6 text-gray-800 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24">
                            <path stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="m5 15 7-7 7 7" />
                        </svg>
                    ) : (
                        <svg className="w-6 h-6 text-gray-800 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24">
                            <path stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="m19 9-7 7-7-7" />
                        </svg>
                    )}
                </button>

            </div>

            

            {/* Tabela */}
            <h2 style={{ textAlign: 'center', color: '#333' }}>Lista de Produtos</h2>
            <table className="styled-table">
                <thead>
                    <tr>
                        {colunas.map(coluna => (
                            <th key={coluna}>
                                {coluna.replace('_', ' ')}
                            </th>
                        )
                        )}
                    </tr>
                </thead>

                <tbody>
                    {table.map((item, index) => (
                        <tr key={index}>
                            {colunas.map((coluna) => (
                                <td key={`${index}-${coluna}`}>
                                    {item[coluna]}
                                </td>
                            ))}
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

export default ProductTable;