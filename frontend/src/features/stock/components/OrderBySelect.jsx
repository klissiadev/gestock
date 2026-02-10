import OrderSelector from "./OrderSelector";

const OrderBySelect = ({ orderBy, isAsc, onChange }) => {
  const options = [
    { value: "nome_asc", label: "Nome ↑" },
    { value: "nome_desc", label: "Nome ↓" },

    { value: "estoque_atual_asc", label: "Quantidade ↑" },
    { value: "estoque_atual_desc", label: "Quantidade ↓" },

    { value: "data_validade_asc", label: "Vencimento ↑" },
    { value: "data_validade_desc", label: "Vencimento ↓" },
  ];

  const isDefault =
  !orderBy || orderBy === "id"; // seu startingPoint real

  const currentValue = isDefault
  ? ""
  : `${orderBy}_${isAsc ? "asc" : "desc"}`;

  const handleChange = (_, combinedValue) => {
    const [field, direction] = combinedValue.split("_");

    onChange("orderBy", field);
    onChange("isAsc", direction === "asc");
  };

  return (
    <OrderSelector
      name="orderCombined"
      value={currentValue}
      onChange={handleChange}
      placeholder="Ordenar"
      options={options}
      startingPoint=""
    />
  );
};

export default OrderBySelect;
