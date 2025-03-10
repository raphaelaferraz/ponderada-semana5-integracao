import time
import asyncio
from ..feedback_repository import save_feedback 
from ..feedback_processor import feedback_process  

# Estados possíveis do Circuit Breaker
CLOSED = "closed"
OPEN = "open"
HALF_OPEN = "half-open"

circuit_state = CLOSED
time_opened = 0
open_duration = 3

# Controle de falhas baseado no tempo de processamento dos feedbacks
max_processing_time = 10
time_error_occurred = None

async def circuit_breaker_process_feedback(motoboy_id, response):
    """
    Circuit Breaker adaptado para processar feedbacks.
    Fecha o circuito se o tempo de processamento for maior que max_processing_time.
    Após o processamento, categoriza e salva o feedback.
    """
    global circuit_state, time_opened

    current_time = time.time()

    # Se o circuito estiver OPEN, verifica se já pode testar de novo
    if circuit_state == OPEN:
        if (current_time - time_opened) >= open_duration:
            circuit_state = HALF_OPEN
            print("🔄 Circuit Breaker em HALF_OPEN - Testando requisição...")
        else:
            print("❌ Circuit Breaker está OPEN - Rejeitando requisição")
            raise Exception("Circuit Breaker is OPEN - Temporarily blocking requests")

    try:
        result = await process_feedback(motoboy_id, response)
    except Exception as e:
        circuit_state = OPEN
        time_opened = time.time()
        print(f"❌ Circuit Breaker voltou para OPEN devido a erro: {e}")
        raise e

    # Se o tempo de processamento estiver dentro do limite, o circuito volta para CLOSED
    if result["processing_time"] <= max_processing_time:
        circuit_state = CLOSED
        print("✅ Circuit Breaker voltou para CLOSED!")
    else:
        circuit_state = OPEN
        time_opened = time.time()
        print("❌ Circuit Breaker voltou para OPEN!")

    # Após o processamento, categorize o feedback e salve-o no "banco de dados"
    category = feedback_process(response)
    saved = save_feedback(motoboy_id, response, category)
    result["saved"] = saved
    result["category"] = category

    return result


async def process_feedback(motoboy_id, response):
    """
    Simula o processamento do feedback com tempo variável.
    Se demorar mais que max_processing_time, o Circuit Breaker abrirá.
    """
    global time_error_occurred

    start_time = time.time()
    processing_time = min(10, max(2, start_time % 10))
    
    if processing_time > max_processing_time:
        time_error_occurred = time.time()
        print(f"⚠️ Feedback processing exceeded {max_processing_time}s - Triggering Circuit Breaker")
        raise Exception(f"Processing time exceeded {max_processing_time}s")

    await asyncio.sleep(processing_time)
    print(f"✅ Feedback processed in {processing_time:.2f}s")

    return {
        "message": f"Feedback processed in {processing_time:.2f}s",
        "processing_time": processing_time,
        "circuit_state": circuit_state
    }
