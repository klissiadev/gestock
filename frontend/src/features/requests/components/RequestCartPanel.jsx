import { Box } from "@mui/material";
import ShoppingSvg from "../../../assets/icon/iconShop.svg?react";
import ProductRequestItem from "./ProductRequestItem";
import RequestForm from "./RequestForm";
import ChatSvg from "../../../assets/icon/iconChat.svg?react";
import ExpandableIconButton from "../../../components/ui/ExpandableIconButton.jsx";

const RequestCartPanel = ({ products, setProducts, setRequestSent }) => {

  const increaseQty = (id) => {
    setProducts((prev) =>
      prev.map((p) =>
        p.id === id ? { ...p, qty: p.qty + 1 } : p
      )
    );
  };

  const decreaseQty = (id) => {
    setProducts((prev) =>
      prev.map((p) =>
        p.id === id && p.qty > 1
          ? { ...p, qty: p.qty - 1 }
          : p
      )
    );
  };

  const togglePriority = (id) => {
    setProducts((prev) =>
      prev.map((p) =>
        p.id === id
          ? { ...p, priority: !p.priority }
          : p
      )
    );
  };

  const removeProduct = (id) => {
    setProducts((prev) =>
      prev.filter((p) => p.id !== id)
    );
  };

  return (
    <Box
      sx={{
        width: 400,
        borderRadius: 3,
        display: "flex",
        flexDirection: "column",
        overflow: "hidden",
        bgcolor: "grey.50",
      }}
    >
      {/* HEADER */}
      <Box
        sx={{
          display: "flex",
          justifyContent: "space-between",
          p: 2,
        }}
      >
        <ShoppingSvg width={22} height={22} />

        <ExpandableIconButton
          icon={<ChatSvg width={16} height={16} />}
          origin="requests"
          initialMessage="Olá Minerva, me ajude com uma nova requisição."
        />
      </Box>

      {/* LISTA */}
      <Box
        sx={{
          flex: 1,
          overflowY: "auto",
          px: 2,
          display: "flex",
          flexDirection: "column",
          gap: 1,
        }}
      >
        {products.map((product) => (
          <ProductRequestItem
            key={product.id}
            product={product}
            onIncrease={increaseQty}
            onDecrease={decreaseQty}
            onTogglePriority={togglePriority}
            onRemove={removeProduct}
          />
        ))}
      </Box>

      <RequestForm products={products} setRequestSent={setRequestSent}/>
    </Box>
  );
};

export default RequestCartPanel;