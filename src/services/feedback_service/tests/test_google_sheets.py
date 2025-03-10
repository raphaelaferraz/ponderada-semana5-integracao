import pytest
from unittest.mock import patch, MagicMock
from src.services.feedback_service.integration.google_sheets import save_feedback_to_sheets

@pytest.fixture
def feedback_data():
    """Retorna um feedback válido para os testes."""
    return {"motoboy_id": 10, "response": "Entrega atrasada, muito ruim", "category": "Problemas na Entrega"}

### **✅ Cenário Positivo: Feedback salvo com sucesso**
def test_save_feedback_success(feedback_data):
    """Testa se o feedback é salvo corretamente no Google Sheets."""

    # Mock do cliente do Google Sheets e da planilha
    with patch("src.services.feedback_service.integration.google_sheets.client") as mock_client:
        mock_worksheet = MagicMock()
        mock_client.open.return_value.sheet1 = mock_worksheet 
        mock_worksheet.append_row.return_value = True  

        # Executa a função
        result = save_feedback_to_sheets(
            feedback_data["motoboy_id"],
            feedback_data["response"],
            feedback_data["category"]
        )

        # Verificações
        assert result is True  # Deve retornar True
        mock_worksheet.append_row.assert_called_once()  
        print("✅ Teste de sucesso: Feedback salvo corretamente no Google Sheets.")

### **❌ Cenário Negativo: Erro ao salvar no Google Sheets**
def test_save_feedback_failure(feedback_data):
    """Testa se a função lida corretamente com um erro ao salvar no Google Sheets."""

    # Mock do cliente do Google Sheets para simular um erro
    with patch("src.services.feedback_service.integration.google_sheets.client") as mock_client:
        mock_worksheet = MagicMock()
        mock_client.open.return_value.sheet1 = mock_worksheet  
        mock_worksheet.append_row.side_effect = Exception("Erro ao salvar no Google Sheets")  # Simula erro

        # Executa a função
        result = save_feedback_to_sheets(
            feedback_data["motoboy_id"],
            feedback_data["response"],
            feedback_data["category"]
        )

        # Verificações
        assert result is False  
        print("❌ Teste de falha: Erro tratado corretamente ao salvar no Google Sheets.")

### **❌ Cenário Negativo: Erro quando envia feedback vazio 
def test_empty_feedback(feedback_data):
    """Testa se a função lida corretamente com um feedback vazio."""

    # Executa a função com feedback vazio
    result = save_feedback_to_sheets(
        feedback_data["motoboy_id"],
        "",
        feedback_data["category"]
    )

    # Verificações
    assert result is False  
    print("❌ Teste de falha: Erro tratado corretamente ao enviar feedback vazio.")