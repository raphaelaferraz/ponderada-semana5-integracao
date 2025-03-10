
from .integration.google_sheets import save_feedback_to_sheets

# Simulação de um banco de dados em memória
database_feedbacks = []

def save_feedback(motoboy_id: int, response: str, category: str) -> bool:
    """
    Salva um feedback no banco de dados fictício e no Google Sheets.

    :param motoboy_id: ID do entregador que enviou o feedback
    :param response: Texto do feedback enviado pelo entregador
    :param category: Categoria do feedback processado
    :return: True se o feedback foi salvo com sucesso, False caso contrário
    """
    try:
        feedback = {
            "motoboy_id": motoboy_id,
            "response": response,
            "category": category
        }
        database_feedbacks.append(feedback)

        # ✅ Salvar no Google Sheets
        save_feedback_to_sheets(motoboy_id, response, category)

        return True
    except Exception as e:
        print(f"Erro ao salvar feedback: {e}")
        return False

def get_feedbacks() -> list:
  """
  Retorna todos os feedbacks salvos no banco de dados fictício.

  :return: Lista de feedbacks
  """

  return database_feedbacks