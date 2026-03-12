import { Box, Typography, Button } from "@mui/material";

const SearchProductList = ({ products, onRequestProduct }) => {
  return (
    <Box
      sx={{
        width: "100%",
        mt: 3,
        display: "flex",
        flexDirection: "column",
        gap: 1.5,
        maxHeight: 340, 
        overflowY: "auto", 
      }}
    >
      {products.map((product) => (
        <Box
          key={product.id}
          sx={{
            p: 1,
            borderRadius: 2,
            bgcolor: "grey.50",
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
          }}
        >
          <Box>
            <Typography fontSize={14} fontWeight={500}>
              {product.name}
            </Typography>

            <Typography
              fontSize={12}
              color="text.secondary"
              sx={{
                maxWidth: 220,
                overflow: "hidden",
                textOverflow: "ellipsis",
                whiteSpace: "nowrap",
              }}
            >
              {product.description}
            </Typography>
          </Box>
          <Box>
          <Button
            variant="contained"
            onClick={() => onRequestProduct(product)}
            sx={{
                borderRadius: "6px",
                textTransform: "none",
                flex: 1,
                width: 70,
                height: 36,
                fontFamily: (theme) => theme.typography.fontFamily,
                fontWeight: (theme) => theme.typography.fontWeightLight,
                color: theme => theme.palette.common.white,
                backgroundColor: (theme) => theme.palette.uploadBox.button,
                "&:hover": {
                    backgroundColor: (theme) => theme.palette.button.hover,
                    color: theme => theme.palette.common.black,
                },
            }}
        >
            Pedir
        </Button>
        </Box>
        </Box>
      ))}
    </Box>
  );
};

export default SearchProductList;