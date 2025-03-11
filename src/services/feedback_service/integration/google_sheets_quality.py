import gspread
import fastapi
import oauth2client
import sys
from oauth2client.service_account import ServiceAccountCredentials
import os
import datetime

# Configuração das credenciais do Google Sheets
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_FILE = os.path.join(BASE_DIR, "credentials-google.json")

# Configuração do Google Sheets API
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
client = gspread.authorize(creds)

# Nome da planilha
SPREADSHEET_NAME = "Feedbacks Entregadores"

# Versões recomendadas (pode ser ajustado conforme necessidade)
VERSIONS_RECOMMENDED = {
    "python": "3.9",  
    "fastapi": "0.95.0",
    "gspread": "5.7.1",
    "oauth2client": "4.1.3",
}

def check_versions():
    """
    Verifica as versões das bibliotecas essenciais e compara com as versões recomendadas.
    """
    current_versions = {
        "python": sys.version.split(" ")[0],
        "fastapi": fastapi.__version__,
        "gspread": gspread.__version__,
        "oauth2client": oauth2client.__version__,
    }

    version_report = {}
    for package, recommended_version in VERSIONS_RECOMMENDED.items():
        current_version = current_versions.get(package, "Desconhecido")
        version_report[package] = {
            "current": current_version,
            "recommended": recommended_version,
            "status": "✔️ Atualizado" if current_version == recommended_version else "⚠️ Desatualizado"
        }

    return version_report

def verify_google_sheets_integration():
    """
    Verifica a qualidade da integração com o Google Sheets, incluindo:
    - Acessibilidade da API
    - Existência da planilha
    - Teste de escrita
    - Controle de versões das dependências
    
    :return: Dicionário com o status da verificação
    """
    verification_result = {
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "api_accessible": False,
        "spreadsheet_found": False,
        "write_test_successful": False,
        "api_version": None,
        "version_report": check_versions()
    }

    try:
        # Testar se a API do Google Sheets está acessível
        spreadsheet = client.open(SPREADSHEET_NAME)
        verification_result["api_accessible"] = True
        verification_result["spreadsheet_found"] = True

        verification_result["api_version"] = gspread.__version__

        worksheet = spreadsheet.worksheet("Verificação de Qualidade")        
        test_data = ["TESTE_VERIFICACAO", "OK", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
        worksheet.append_row(test_data)

        verification_result["write_test_successful"] = True

        print("✅ Verificação da integração com Google Sheets concluída com sucesso!")

    except gspread.exceptions.SpreadsheetNotFound:
        print("❌ Erro: A planilha especificada não foi encontrada.")
    
    except gspread.exceptions.APIError as e:
        print(f"❌ Erro de API do Google Sheets: {e}")
    
    except Exception as e:
        print(f"❌ Erro inesperado na verificação da integração: {e}")

    return verification_result
