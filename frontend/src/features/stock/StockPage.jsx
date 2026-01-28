import React from 'react'
import { products } from './mocks/productTable.mock'
import { DataGrid } from '@mui/x-data-grid/DataGrid';
import { Box, Pagination } from '@mui/material'


const StockPage = () => {

    // Gerador de colunas (um dicionario com os campos: field e headerName)
    const columns = Object.keys(products[0])
        .map(
            key => (
                {
                    field: key,
                    headerName: key.replace("_", " ").toLowerCase(),
                    flex: 1,
                    sortable: false

                }
            )
        )


    const rows = products.map(
        p => ({
            id: p.nome_produto,
            ...p,
        })
    );

    /* 
    Map -> percorre em todos os itens do array
    a cada item P => ele vai criar um novo objeto em que

    id = nome do produto
    ...p => copia todos os outros campos
    */

    const [paginationModel, setPaginationModel] = React.useState({
        page: 0,
        pageSize: 10,
    });





    return (
        <Box sx={{
            backgroundColor: 'white',
            width: '100%',
            height: '100%',
            padding: 10
        }}>

            <DataGrid
                columns={columns}
                rows={rows}

                // Setup do sistema de paginacao externo
                pagination
                paginationMode="client"
                paginationModel={paginationModel}
                onPaginationModelChange={setPaginationModel}
                pageSizeOptions={[paginationModel.pageSize]}
                hideFooterPagination // Esconder o footer de paginacao

                autoHeight
                disableColumnMenu
                disableColumnSorting
                disableColumnFilter
                disableRowSelectionOnClick

                sx={{
                    // root
                    backgroundColor: (theme) => theme.palette.background.default,
                    padding: 1,
                    borderRadius: 5,

                    // Bloco de coluna
                    '& .MuiDataGrid-columnHeader': {
                        backgroundColor: (theme) => theme.palette.background.default,
                        justifyContent: 'center'

                    },

                    // container do título
                    '& .MuiDataGrid-columnHeaderTitleContainer': {
                        justifyContent: 'center',
                    },

                    // Texto da coluna
                    '& .MuiDataGrid-columnHeaderTitle': {
                        textAlign: 'center',
                        width: '100%',
                    }
                }}


            />

            <Pagination
                count={Math.ceil(rows.length / paginationModel.pageSize)}
                page={paginationModel.page + 1}
                onChange={(e, value) =>
                    setPaginationModel((prev) => ({
                        ...prev,
                        page: value - 1,
                    }))
                }
                color="secondary"
                variant="outlined"
                shape="rounded"
            />


        </Box>
    )
}

export default StockPage
