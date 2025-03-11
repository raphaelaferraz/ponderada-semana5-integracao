import pytest
from unittest.mock import patch, MagicMock
from src.services.feedback_service.integration.google_sheets import save_feedback_to_sheets
from src.services.feedback_service.integration.google_sheets_quality import verify_google_sheets_integration


@pytest.fixture
def feedback_data():
    """Retorna um feedback válido para os testes."""
    return {"motoboy_id": 10, "response": "Entrega atrasada, muito ruim", "category": "Problemas na Entrega"}

### ✅ Cenário Positivo: Feedback salvo com sucesso
def test_save_feedback_success(feedback_data):
    """Testa se o feedback é salvo corretamente no Google Sheets."""

    with patch("src.services.feedback_service.integration.google_sheets.client") as mock_client:
        mock_worksheet = MagicMock()
        mock_client.open.return_value.sheet1 = mock_worksheet 
        mock_worksheet.append_row.return_value = True  

        result = save_feedback_to_sheets(
            feedback_data["motoboy_id"],
            feedback_data["response"],
            feedback_data["category"]
        )

        assert result is True  
        mock_worksheet.append_row.assert_called_once()  
        print("✅ Teste de sucesso: Feedback salvo corretamente no Google Sheets.")

### ❌ Cenário Negativo: Erro ao salvar no Google Sheets
def test_save_feedback_failure(feedback_data):
    """Testa se a função lida corretamente com um erro ao salvar no Google Sheets."""

    with patch("src.services.feedback_service.integration.google_sheets.client") as mock_client:
        mock_worksheet = MagicMock()
        mock_client.open.return_value.sheet1 = mock_worksheet  
        mock_worksheet.append_row.side_effect = Exception("Erro ao salvar no Google Sheets")  

        result = save_feedback_to_sheets(
            feedback_data["motoboy_id"],
            feedback_data["response"],
            feedback_data["category"]
        )

        assert result is False  
        print("❌ Teste de falha: Erro tratado corretamente ao salvar no Google Sheets.")

### ❌ Cenário Negativo: Erro quando envia feedback vazio 
def test_empty_feedback(feedback_data):
    """Testa se a função lida corretamente com um feedback vazio."""

    result = save_feedback_to_sheets(
        feedback_data["motoboy_id"],
        "",
        feedback_data["category"]
    )

    assert result is False  
    print("❌ Teste de falha: Erro tratado corretamente ao enviar feedback vazio.")

### ✅ Cenário Positivo: Conexão com o Google Sheets ocorreu com sucesso
def test_quality_google_sheets():
    """Testa a verificação da integração e a gravação na aba de qualidade"""

    with patch("src.services.feedback_service.integration.google_sheets_quality.client") as mock_client:
        mock_spreadsheet = MagicMock()
        mock_worksheet = MagicMock()

        mock_client.open.return_value = mock_spreadsheet  
        mock_spreadsheet.worksheet.return_value = mock_worksheet  
        mock_worksheet.append_row.return_value = True  

        result = verify_google_sheets_integration()

        assert result["api_accessible"] is True
        assert result["spreadsheet_found"] is True
        assert result["write_test_successful"] is True
        assert isinstance(result["api_version"], str)

        print("✅ Teste de verificação de qualidade com Google Sheets passou com sucesso!")

### ❌ Cenário Negativo: Erro com a conexão com o Google Sheets
def test_quality_google_sheets_failure():
    """Testa a verificação da integração e a gravação na aba de qualidade com falha"""

    with patch("src.services.feedback_service.integration.google_sheets_quality.client") as mock_client:
        mock_spreadsheet = MagicMock()
        mock_worksheet = MagicMock()

        mock_client.open.return_value = mock_spreadsheet  
        mock_spreadsheet.worksheet.return_value = mock_worksheet  
        mock_worksheet.append_row.side_effect = Exception("Erro ao salvar na planilha")  

        result = verify_google_sheets_integration()

        assert result["api_accessible"] is True
        assert result["spreadsheet_found"] is True
        assert result["write_test_successful"] is False
        assert isinstance(result["api_version"], str)

        print("❌ Teste de verificação de qualidade com Google Sheets falhou corretamente!")