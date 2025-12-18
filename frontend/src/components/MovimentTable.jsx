import { useEffect, useState } from 'react'
import { handleMTable } from '../api/viewApi';
// TO DO: Implementar a tabela de movimentacoes similar a productTable.jsx
// Fazer isso depois de implementar todos os filtros da tabela de produtos

const MovimentTable = () => {
    const [table, setTable] = useState(null);
    const [orderBy, setOrderBy] = useState("id_movimentacao");
    const [isAsc, setIsAsc] = useState(true);
    const [digitado, setDigitado] = useState("");
    const [searchTerm, setSearchTerm] = useState("");

    // Paginacao
    const [currentPage, setCurrentPage] = useState(1);
    const itemsPerPage = 10;

    // Funcao do botao de pesquisar
    const handlePesquisar = () => {
        setSearchTerm(digitado);
    };

    useEffect(() => {
        const carregarDados = async () => {
            try {
                // Busca os dados filtrados do backend
                const dados = await handleMTable(orderBy, isAsc, searchTerm);
                setTable(dados);
                setCurrentPage(1);

            } catch (error) {
                console.error("Erro ao buscar tabela:", error);
                setTable(null);
            }
        };
        carregarDados();

    }, [orderBy, isAsc, searchTerm]);


    if (!table) {
        return (
            <div className="p-10 text-center text-slate-500 animate-pulse">
                <p className="text-lg font-medium">Carregando dados da tabela... ⏳</p>
            </div>
        );
    }

    // Sistema de paginacao
    const indexOfLastItem = currentPage * itemsPerPage;
    const indexOfFirstItem = indexOfLastItem - itemsPerPage;
    const currentItems = table.slice(indexOfFirstItem, indexOfLastItem);
    const totalPages = Math.ceil(table.length / itemsPerPage);

    const colunas = table.length > 0 ? Object.keys(table[0]) : [];

    return (
        // Container principal
        <div className="max-w-6xl mx-auto p-6 bg-white shadow-lg rounded-xl mt-10">

            {/* CABEÇALHO DE CONTROLES*/}
            <div className="flex flex-col md:flex-row justify-between items-start md:items-end gap-6 mb-8 border-b pb-6 border-slate-200">
                {/* BLOCO DE ORDENAÇÃO */}
                <div className="w-full md:w-auto">
                    <h2 className="text-sm font-semibold text-slate-500 uppercase tracking-wider mb-2">Ordenação</h2>
                    <div className="flex gap-2">
                        <select
                            className="w-full md:w-48 bg-slate-50 border border-slate-300 text-slate-700 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2.5"
                            value={orderBy}
                            onChange={(e) => setOrderBy(e.target.value)}
                        >
                            {colunas.map(coluna => (
                                <option key={coluna} value={coluna}>
                                    {coluna.replace('_', ' ')}
                                </option>
                            ))}
                        </select>

                        <button
                            onClick={() => setIsAsc(!isAsc)}
                            className="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg transition-colors border border-slate-300"
                            title={isAsc ? "Ascendente" : "Descendente"}
                        >
                            {isAsc ? "⬇️" : "⬆️"}
                        </button>
                    </div>
                </div>

                {/* BLOCO DE FILTROS E BUSCA */}
                <div className="w-full md:w-auto flex flex-col md:flex-row gap-3">
                    <div className='flex flex-col flex-1'>
                        <label className="text-sm font-semibold text-slate-500 uppercase tracking-wider mb-2">Buscar</label>
                        <div className="flex gap-2">
                            <input
                                type="text"
                                className="bg-slate-50 border border-slate-300 text-slate-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
                                placeholder="Nome do produto..."
                                value={digitado}
                                onChange={(e) => setDigitado(e.target.value)}
                                onKeyDown={(e) => e.key === 'Enter' && handlePesquisar()}
                            />
                            <button
                                type="button"
                                onClick={handlePesquisar}
                                className="text-white bg-blue-600 hover:bg-blue-700 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 transition-all"
                            >
                                Pesquisar
                            </button>
                        </div>
                    </div>
                </div>
            </div>



            {/* TABELA */}
            {table.length > 0 ? (
                <section>
                    <h2 className="text-2xl font-bold text-slate-800 mb-6 text-center">Lista de Movimentação</h2>
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
                                {currentItems.map((item, index) => (
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
                    {/* CONTROLES DE PAGINAÇÃO */}
                    <div className="flex items-center justify-between mt-6 px-2">
                        <span className="text-sm text-slate-600">
                            Mostrando <span className="font-semibold text-slate-800">{indexOfFirstItem + 1}</span> a <span className="font-semibold text-slate-800">{Math.min(indexOfLastItem, table.length)}</span> de <span className="font-semibold text-slate-800">{table.length}</span> registros
                        </span>

                        <div className="inline-flex gap-2">
                            <button
                                onClick={() => setCurrentPage(prev => Math.max(prev - 1, 1))}
                                disabled={currentPage === 1}
                                className="px-4 py-2 text-sm font-medium text-slate-700 bg-white border border-slate-300 rounded-lg hover:bg-slate-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                            >
                                Anterior
                            </button>

                            <div className="flex items-center gap-1 px-4 text-sm font-medium text-slate-700">
                                Página {currentPage} de {totalPages}
                            </div>

                            <button
                                onClick={() => setCurrentPage(prev => Math.min(prev + 1, totalPages))}
                                disabled={currentPage === totalPages}
                                className="px-4 py-2 text-sm font-medium text-slate-700 bg-white border border-slate-300 rounded-lg hover:bg-slate-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                            >
                                Próxima
                            </button>
                        </div>
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
