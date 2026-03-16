import { useEffect, useState } from "react";
import { fetchProdutos } from "../../stock/services/produtctService";

export const useProductSearch = (search) => {

  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {

    const loadProducts = async () => {

      if (!search) {
        setProducts([]);
        return;
      }

      setLoading(true);

      const response = await fetchProdutos({
        searchTerm: search,
        orderBy: "id",
        isAsc: true,
        categoria: "",
        isBaixoEstoque: false,
        isVencido: false
      });

      if (!response.error) {
        setProducts(response);
      }

      setLoading(false);
    };

    loadProducts();

  }, [search]);

  return { products, loading };
};