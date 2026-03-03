import React, { useState } from 'react';
import TabelaMovimentacao from './pages/TabelaMovimentacao';
import TabelaProduto from './pages/TabelaProduto';

const StockSheets = () => {
    const [productTable, setProductTable] = useState(true);
    const [movimentTable, setMovimentTable] = useState(false);



    // Handle das guias
    const handleProductTable = () => {
        setProductTable(true);
        setMovimentTable(false); 
    }

    const handleMovimentTable = () => {
        setMovimentTable(true); 
        setProductTable(false);
    }

    return (
    // CONTAINER PRINCIPAL: Centralizado, com sombra e fundo branco
    <div>
        {/* BOTOES DE TABELA */}
        <div className="flex justify-center mb-6 space-x-4">
            <button
                className={`px-4 py-2 rounded-lg font-medium ${productTable ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'}`}
                onClick={handleProductTable}
            >
                Tabela de Produtos
            </button>
            <button
                className={`px-4 py-2 rounded-lg font-medium ${movimentTable ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'}`}
                onClick={handleMovimentTable}
            >
                Tabela de Movimentação
            </button>
        </div>

        {/* RENDERIZACAO CONDICIONAL DAS TABELAS */}
        {productTable && <TabelaProduto />}
        {movimentTable && <TabelaMovimentacao />}
    </div>
  );
}

export default StockSheets;