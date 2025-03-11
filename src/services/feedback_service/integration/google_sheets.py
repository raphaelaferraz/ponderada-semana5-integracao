import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
from .google_sheets_quality import verify_google_sheets_integration


# Define o caminho absoluto para o arquivo JSON
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  
CREDENTIALS_FILE = os.path.join(BASE_DIR, "credentials-google.json")  

print(f"🔍 Carregando credenciais do Google Sheets de: {CREDENTIALS_FILE}")  

# Nome da planilha no Google Sheets
SPREADSHEET_NAME = "Feedbacks Entregadores"

# Configurar o acesso ao Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
client = gspread.authorize(creds)

# Abrir a planilha pelo nome
spreadsheet = client.open(SPREADSHEET_NAME)

# Selecionar a primeira aba da planilha
worksheet = spreadsheet.sheet1

# Função para reconectar caso a API falhe
def reconnect_to_google_sheets():
    global client
    try:
        client = gspread.authorize(creds)
        print("✅ Reconexão com Google Sheets bem-sucedida!")
    except Exception as e:
        print(f"❌ Erro ao reconectar ao Google Sheets: {e}")

def save_feedback_to_sheets(motoboy_id: int, response: str, category: str, retries=3, delay=2):
    """
    Salva um feedback na planilha do Google Sheets e implementa tentativas em caso de falha.

    :param motoboy_id: ID do entregador
    :param response: Texto do feedback
    :param category: Categoria classificada do feedback
    :param retries: Número máximo de tentativas antes de desistir
    :param delay: Tempo de espera entre tentativas (segundos)
    :return: True se o feedback foi salvo com sucesso, False caso contrário.
    """

    verification_result = verify_google_sheets_integration()
    print(f"🔍 Verificação do Google Sheets: {verification_result}")

    if not verification_result["api_accessible"] or not verification_result["write_test_successful"]:
        print("❌ A integração com Google Sheets falhou! Feedback não será salvo.")
        return False

    if not response.strip():
        print("❌ Erro: Feedback vazio não pode ser salvo!")
        return False

    for attempt in range(retries):
        try:
            spreadsheet = client.open(SPREADSHEET_NAME)
            worksheet = spreadsheet.sheet1

            worksheet.append_row([motoboy_id, response, category])
            print("✅ Feedback salvo no Google Sheets com sucesso!")
            return True
        
        except gspread.exceptions.APIError as e:
            print(f"⚠️ Erro ao salvar no Google Sheets: {e}")
            
            if attempt < retries - 1:
                print(f"🔄 Tentando novamente... (Tentativa {attempt + 2}/{retries})")
                time.sleep(delay)
                reconnect_to_google_sheets()
            else:
                print("❌ Todas as tentativas falharam. Feedback não salvo.")
                return False

        except Exception as e:
            print(f"❌ Erro inesperado ao salvar no Google Sheets: {e}")
            return False