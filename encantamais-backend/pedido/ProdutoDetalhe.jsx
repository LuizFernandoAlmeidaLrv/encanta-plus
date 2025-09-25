import React, { useState, useEffect } from 'react';

function ProdutoDetalhe({ produtoId }) {
  const [produto, setProduto] = useState(null);

  useEffect(() => {
    const fetchProduto = async () => {
      const response = await fetch(`http://127.0.0.1:8000/api/produtos/${produtoId}/`);
      const data = await response.json();
      setProduto(data);
    };

    fetchProduto();
  }, [produtoId]);

  if (!produto) return <div>Carregando...</div>;

  return (
    <div>
      <h1>{produto.nome}</h1>
      <p>{produto.descricao}</p>
      <h2>Ingredientes:</h2>
      <ul>
        {produto.ingredientes.length > 0 ? (
          produto.ingredientes.map((ingrediente, index) => (
            <li key={index}>{ingrediente}</li>
          ))
        ) : (
          <p>Não há ingredientes disponíveis para este produto.</p>
        )}
      </ul>
    </div>
  );
}

export default ProdutoDetalhe;
