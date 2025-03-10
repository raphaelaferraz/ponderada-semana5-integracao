import pytest
from src.services.feedback_service.feedback import register_feedback
from src.services.feedback_service.feedback_repository import save_feedback

# Simulação de um banco de dados para testar sem impactar dados reais
def mock_save_feedback(motoboy_id, response, category):
    """Mock para simular o salvamento do feedback no banco de dados."""
    return True 

def mock_save_feedback_fail(motoboy_id, response, category):
    """Mock para simular falha no salvamento do feedback."""
    return False  

@pytest.fixture
def valid_feedback():
    """Retorna um feedback válido para os testes."""
    return {"motoboy_id": 1, "response": "O aplicativo travou várias vezes hoje, precisa de melhorias."}

def test_valid_feedback(valid_feedback, monkeypatch):
    """Teste de sucesso: Feedback válido deve ser armazenado corretamente."""
    monkeypatch.setattr("src.services.feedback_service.feedback_repository.save_feedback", mock_save_feedback)
    
    resultado = register_feedback(valid_feedback["motoboy_id"], valid_feedback["response"])
    
    assert resultado["status"] == "sucesso"
    assert "category" in resultado

def test_mandatory_id():
    """Teste de falha: Deve retornar erro se o ID do entregador estiver ausente."""
    with pytest.raises(ValueError, match="O ID do entregador é obrigatório."):
        register_feedback(None, "O aplicativo travou várias vezes hoje.")

def test_feedback_cannot_be_empty():
    """Teste de falha: Feedback vazio deve retornar erro."""
    with pytest.raises(ValueError, match="O feedback não pode estar vazio!"):
        register_feedback(1, "")

def test_feedback_only_spaces():
    """Teste de falha: Feedback com espaços em branco deve retornar erro."""
    with pytest.raises(ValueError, match="O feedback deve ter pelo menos 20 caracteres."):
        register_feedback(1, "    ")

def test_feedback_less_than_20_characters():
    """Teste de falha: Feedback com menos de 20 caracteres deve retornar erro."""
    with pytest.raises(ValueError, match="O feedback deve ter pelo menos 20 caracteres."):
        register_feedback(1, "Muito ruim!")

def test_feedback_categorization():
    """Teste de sucesso: Verifica se o feedback é categorizado corretamente."""
    resultado = register_feedback(1, "Minha taxa de pagamento foi muito baixa hoje.")
    assert resultado["category"] == "Financeiro"

def test_fail_to_save_feedback(monkeypatch):
    """Teste de falha: Deve gerar erro quando o feedback for inválido (vazio ou menos de 20 caracteres)."""

    invalid_feedback = {
        "motoboy_id": 1,
        "response": "Muito ruim"  
    }

    with pytest.raises(ValueError, match="O feedback deve ter pelo menos 20 caracteres."):
        register_feedback(invalid_feedback["motoboy_id"], invalid_feedback["response"])