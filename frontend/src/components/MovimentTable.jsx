import { useEffect, useState } from 'react'
import { handleMTable } from '../api/viewApi';
// TO DO: Implementar a tabela de movimentacoes similar a productTable.jsx
// Fazer isso depois de implementar todos os filtros da tabela de produtos

const MovimentTable = () => {
    const [table, setTable] = useState([]);

    useEffect(() => {
            const carregarDados = async () => {
                try {
                    // Busca os dados filtrados do backend
                    const dados = await handleMTable();
                    setTable(dados);
    
                } catch (error) {
                    console.error("Erro ao buscar tabela:", error);
                    setTable([]);
                }
            };
            carregarDados();
    
        }, []);


    if (!table) {
        return (
            <div className="p-10 text-center text-slate-500 animate-pulse">
                <p className="text-lg font-medium">Carregando dados da tabela... ⏳</p>
            </div>
        );
    }

    const colunas = table.length > 0 ? Object.keys(table[0]) : [];

    return (
        // Container principal
        <div className="max-w-6xl mx-auto p-6 bg-white shadow-lg rounded-xl mt-10">

            {/* TABELA */}
            {table.length > 0 ? (
                <section>
                    <h2 className="text-2xl font-bold text-slate-800 mb-6 text-center">Lista de Produtos</h2>
                    <div className="relative overflow-x-auto rounded-lg border border-slate-200">
                        <table className="w-full text-sm text-left text-slate-600">
                            <thead className="text-xs text-slate-700 uppercase bg-slate-100 border-b border-slate-200">
                                <tr>
                                    {colunas.map(coluna => (
                                        <th key={coluna} className="px-6 py-4 font-bold">
                                            {coluna.replace('_', ' ')}
                                        </th>
                                    ))}
                                </tr>
                            </thead>
                            <tbody>
                                {table.map((item, index) => (
                                    <tr
                                        key={index}
                                        className="bg-white border-b hover:bg-slate-50 transition-colors"
                                    >
                                        {colunas.map((coluna) => (
                                            <td key={`${index}-${coluna}`} className="px-6 py-4 whitespace-nowrap">
                                                {item[coluna] ? item[coluna] : <span className="text-slate-400 italic">Indeterminado</span>}
                                            </td>
                                        ))}
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </section>
            ) : (
                <div className="p-10 text-center text-slate-500">
                    <p className="text-lg">Nenhuma movimentação encontrada. 😕</p>
                </div>
            )}



        </div>
    )
}

export default MovimentTable
