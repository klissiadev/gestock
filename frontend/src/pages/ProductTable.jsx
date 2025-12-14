import React, { useEffect, useState, useRef } from 'react';
import { handlePTable } from '../api/viewApi';
import '../style/productTable.css'
const ProductTable = () => {
    const [table, setTable] = useState(null);

    // Eu tinha notado que tava chamando 2 vezes a API (só pra garantir que isso nao vai acontecer)
    const jaChamou = useRef(false); 
    useEffect(() => {
        if (jaChamou.current) return;
        jaChamou.current = true;
        const carregarDados = async () => {
            try {
                const dados = await handlePTable();
                setTable(dados);
            } catch (error) {
                console.error("Erro ao buscar tabela:", error);
            }
        };
        carregarDados();

    }, []);

    // verificacao dinamica
    if (!table) return <div>Carregando...</div>;
    if (table.length === 0) return <div>Sem dados...</div>;


    // Formatacao da tabela
    const colunas = Object.keys(table[0]);

    // CSS da tabela
    
    return (
        <div className="tabela-container">
            <h2 style={{ textAlign: 'center', color: '#333' }}>Lista de Produtos</h2>
            <table className="styled-table">
                <thead>
                    {colunas.map(coluna => (
                        <th key={coluna}>
                            {coluna.replace('_', ' ')}
                        </th>
                    )
                    )}
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