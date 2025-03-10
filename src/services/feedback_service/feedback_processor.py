# Dicionário de palavras-chave para categorização automática
CATEGORIES = {
  "recompensa": "Recompensas",
  "pagamento": "Financeiro",
  "atraso": "Problemas na Entrega",
  "aplicativo": "Problemas Técnicos",
  "suporte": "Atendimento",
  "erro": "Problemas Técnicos",
  "taxa": "Financeiro",
  "bônus": "Recompensas"
}

def feedback_process(response: str) -> str:
  """
  Classifica um feedback com base em palavras-chave predefinidas.

  :param response: Texto do feedback enviado pelo entregador
  :return: Categoria correspondente ao feedback
  """

  lower_response = response.lower()

  for words, category in CATEGORIES.items():
    if words in lower_response:
      return category

  return "Outros" 

