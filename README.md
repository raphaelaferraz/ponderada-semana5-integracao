# Ingteraação - Armazenagem do Feedback do Entregador com Google Sheets

## 1 - Estrutura da Integração (Camadas, Módulos, Componentes, Serviços, Hardware, Software, Processos)

A integração implementada consiste em armazenar os feedbacks coletados na API diretamente no Google Sheets, permitindo acesso em tempo real aos dados para análise. Para visualizar melhor, abaixo há um resumo da estrutura da integração:

```
┌──────────────────────────────┐
│    Entregador (usuário)      │
│  - Envia feedback na API     │
└─────────────▲────────────────┘
              │
┌─────────────┴──────────────┐
│        FastAPI (API)       │
│  - Recebe os feedbacks     │
│  - Processa a categoria    │
│  - Envia para Google Sheets│
└─────────────▲──────────────┘
              │
┌─────────────┴──────────────┐
│  Google Sheets API         │
│  - Armazena feedbacks      │
│  - Permite acesso e análise│
└────────────────────────────┘
```

**Camadas e Módulos:**
| **Camada**          | **Módulo**                 | **Descrição**                                  |
|---------------------|---------------------------|----------------------------------------------|
| **API**            | `api.py`                   | Gerencia requisições HTTP, recebe feedbacks e chama `register_feedback()` |
| **Processamento**  | `feedback_processor.py`    | Classifica os feedbacks em categorias       |
| **Banco de Dados** | `feedback_repository.py`   | Simula um banco de dados local e envia feedbacks ao Google Sheets |
| **Integração**     | `google_sheets.py`         | Envia feedbacks para uma planilha no Google Sheets via API |
| **Circuit Breaker**| `circuit_breaker.py`       | Gerencia falhas e evita sobrecarga na API   |

**Serviços e Tecnologias Utilizadas:**
| **Componente**      | **Tecnologia**                | **Descrição**                                  |
|---------------------|-----------------------------|----------------------------------------------|
| **API Web**        | FastAPI                      | Framework para desenvolvimento da API       |
| **Banco de Dados** | Simulação em memória         | Feedbacks armazenados localmente e no Google Sheets |
| **Integração Externa** | Google Sheets API      | Serviço externo para armazenar feedbacks    |
| **Autenticação**   | Google Service Account       | Permissão para escrita no Google Sheets     |
| **Monitoramento**  | Circuit Breaker              | Evita sobrecarga caso a API do Google Sheets falhe |
| **Desempenho**     | `asyncio`                    | Processamento assíncrono para melhor eficiência |

## 2 - Aferição de Qualidade (Tempos, Protocolos, Versões e Tratamento de Exceções)

A qualidade dessa integração foi medida com base nos seguintes critérios:
- **Tempo de processamento:** O tempo de processamento de um feedback foi medido em 10 segundos, considerando a classificação e envio para o Google Sheets. Isso significa que tal tempo não pode ultrapassar 10 segundos.
- **Protocolos de comunicação:** A comunicação entre a API e o Google Sheets foi feita via HTTP, garantindo a integridade dos dados e a segurança da informação. Além disso, há também a utilização de JSON, para o envio do feedback, para o resgate do feedback e para a conexão entre a API de Feedback e o Google Sheets.
- **Versões utilizadas:** 
  - FastAPI 0.95.0
  - gspread 5.7.1
  - oauth2client 4.1.3

- **Tratamento de Exceções**
| **Possível Falha**                                  | **Motivo**                                          | **Solução Implementada**                                   |
|-----------------------------------------------------|-----------------------------------------------------|-----------------------------------------------------------|
| **Falha na autenticação com o Google Sheets**      | Credenciais incorretas ou chave de API inválida    | Verificação da existência do arquivo de credenciais e logs informativos |
| **Planilha não encontrada**                         | O nome da planilha pode ter sido alterado manualmente | Tratamento de erro específico para verificar a existência da planilha |
| **Erro de conexão com a API do Google Sheets**     | Problemas na rede ou indisponibilidade da API      | Implementação de um retry automático e logs de erro      |
| **Falha ao escrever na planilha**                  | Ocorre quando a API do Google bloqueia requisições temporariamente | Circuit Breaker impede sobrecarga e reenvia feedbacks posteriormente |

Essas exceções foram implementadas no código para garantir a integridade dos dados e a confiabilidade da integração. E, para que eles de fato funcionem, foram adotados os seguintes mecanismos de tratamento de exceções:
- Tratamento de erros no acesso às credenciais:
  - O código verifica se o arquivo credentials-google.json existe antes de tentar autenticar. Caso contrário, ele exibe um log de erro informativo.

- Reconexão Automática
	- Caso a autenticação falhe, o código tenta reconectar automaticamente ao Google Sheets.

- Retries com Delay
  - Se houver um erro temporário na API do Google Sheets, o código espera alguns segundos e tenta novamente.
	- O número de tentativas é configurável (padrão: 3 tentativas, com 2 segundos de intervalo).

- Circuit Breaker para prevenir sobrecarga
	- Se muitas falhas consecutivas ocorrerem, o Circuit Breaker pode bloquear novas requisições temporariamente para evitar que a API fique sobrecarregada.