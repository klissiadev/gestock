import { useState, useEffect, useCallback } from 'react';
import { MOVIMENTACAO_HEADER_NAMES, INITIAL_FILTERS } from '../constants/movimentacaoConstant';
import { fetchMovimentacoes } from '../services/movimentService';

export const useMovimentTable = () => {
    const [filters, setFilters] = useState(INITIAL_FILTERS);
    const [rows, setRows] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    // Funcoes de filtro
    const handleFilterChange = useCallback((key, value) => {
      setFilters(prev => ({ ...prev, [key]: value }));
    }, []);

    const resetFilters = useCallback(() => {
      setFilters(INITIAL_FILTERS);
    }, []);

    // Busca de informacoes na tabela
    useEffect(() => {
        const loadData = async () => {
            setLoading(true);
            setError(null);
            
            const response = await fetchMovimentacoes(filters);
            
            if (response.error) {
                setError(response.error);
                setRows([]);
            } else {
                setRows(response);
            }
            setLoading(false);
        };

        loadData();
    }, [filters]);

    const columns = Object.keys(MOVIMENTACAO_HEADER_NAMES).map((key) => ({
        field: key,
        headerName: MOVIMENTACAO_HEADER_NAMES[key],
        flex: 1, 
    }));

    return {
        rows,
        columns,
        loading,
        error,
        filters,
        handleFilterChange,
        resetFilters,
        isFiltered: JSON.stringify(filters) !== JSON.stringify(INITIAL_FILTERS)
    };

};