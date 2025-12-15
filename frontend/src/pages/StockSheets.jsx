import React, { useState } from 'react';
import ProductTable from '../components/ProductTable';
import MovimentTable from '../components/MovimentTable';

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
    <div className="max-w-6xl mx-auto p-6 bg-white shadow-lg rounded-xl mt-10">

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
        {productTable && <ProductTable />}
        {movimentTable && <MovimentTable />}
    </div>
  );
}

export default StockSheets;