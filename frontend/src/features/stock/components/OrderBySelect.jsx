import OrderSelector from "./OrderSelector";

const OrderBySelect = ({ orderBy, isAsc, onChange }) => {
  const options = [
    { value: "nome|asc", label: "Nome ↑" },
    { value: "nome|desc", label: "Nome ↓" },
    { value: "estoque_atual|asc", label: "Quantidade ↑" },
    { value: "estoque_atual|desc", label: "Quantidade ↓" },
    { value: "data_validade|asc", label: "Vencimento ↑" },
    { value: "data_validade|desc", label: "Vencimento ↓" },
  ];

  const isDefault = !orderBy || orderBy === "id";

  // Sincronizado: usando o mesmo pipe "|" que as options
  const currentValue = isDefault
    ? ""
    : `${orderBy}|${isAsc ? "asc" : "desc"}`;

  const handleChange = (e, combinedValue) => {
    // Alguns componentes passam o valor no evento (e.target.value), 
    // outros como segundo argumento. Garanta que pegamos o correto:
    const val = combinedValue || e.target.value;

    if (!val) return;

    const [field, direction] = val.split("|");

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