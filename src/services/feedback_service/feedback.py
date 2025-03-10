from .feedback_processor import feedback_process
from .feedback_repository import save_feedback

def register_feedback(motoboy_id: int, response: str):
    """
    Recebe um feedback do entregador, processa e armazena no banco.

    :param motoboy_id: Identificador do entregador
    :param response: Texto do feedback enviado pelo entregador
    :return: Dicionário com o status da operação e a categoria do feedback.
    """

    if not motoboy_id:
        raise ValueError("O ID do entregador é obrigatório.")

    if not response or not isinstance(response, str):
        raise ValueError("O feedback não pode estar vazio!")

    response = response.strip()  
    
    if len(response) < 20:
        raise ValueError("O feedback deve ter pelo menos 20 caracteres.")

    category = feedback_process(response)
    
    success = save_feedback(motoboy_id, response, category)

    return {
        "status": "sucesso" if success else "erro",
        "category": category
    }