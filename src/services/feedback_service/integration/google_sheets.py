import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

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

def save_feedback_to_sheets(motoboy_id: int, response: str, category: str):
    """
    Salva o feedback na planilha do Google Sheets.

    :param motoboy_id: ID do entregador
    :param response: Texto do feedback
    :param category: Categoria classificada do feedback
    """
    try:
        worksheet.append_row([motoboy_id, response, category])
        print("✅ Feedback salvo no Google Sheets com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao salvar no Google Sheets: {e}")