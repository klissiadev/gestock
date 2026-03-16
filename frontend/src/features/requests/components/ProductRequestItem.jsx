import { Box, Typography, Tooltip } from "@mui/material";
import QuantityStepper from "./QuantityStepper";
import PriorityToggle from "./PriorityToggle";
import RemoveProductButton from "./RemoveProductButton";

const ProductRequestItem = ({
  product,
  onIncrease,
  onDecrease,
  onTogglePriority,
  onRemove,
}) => {
  return (
    <Box
      sx={{
        p: 2,
        borderRadius: 2,
        bgcolor: "grey.50",
        boxShadow: "0 4px 20px rgba(0,0,0,0.08)",
        justifyContent: "space-between",
        display: "flex",
      }}
    >
      <Box
        sx={{
          display: "flex",
          flexDirection: "column",
          maxWidth: 200,
        }}
      >
        <Typography fontWeight={500} fontSize={14}>
          {product.name}
        </Typography>

        <Tooltip title={product.description} arrow>
          <Typography
            fontSize={12}
            color="text.secondary"
            sx={{
              overflow: "hidden",
              textOverflow: "ellipsis",
              whiteSpace: "nowrap",
              cursor: "default",
            }}
          >
            {product.type}
          </Typography>
        </Tooltip>
      </Box>

      <Box
        sx={{
          display: "flex",
          alignItems: "center",
          gap: 2,
        }}
      >
        <QuantityStepper
          value={product.qty}
          onIncrease={() => onIncrease(product.id)}
          onDecrease={() => onDecrease(product.id)}
        />

        <PriorityToggle
          checked={product.priority}
          onChange={() => onTogglePriority(product.id)}
        />

        <RemoveProductButton
          onClick={() => onRemove(product.id)}
        />
      </Box>
    </Box>
  );
};

export default ProductRequestItem;