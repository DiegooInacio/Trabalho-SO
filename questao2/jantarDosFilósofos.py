import threading
import time

# Configurações globais
NUM_FILOSOFOS = 5
TEMPO_LIMITE = 5  # Tempo máximo em segundos para detectar impasse
EXECUCOES = 1000  # Número de execuções para teste

# Função com a solução para evitar deadlock
def jantar_dos_filosofos_com_solucao(resultados, execucao_id):
    # Semáforos para os garfos
    garfos = [threading.Semaphore(1) for _ in range(NUM_FILOSOFOS)]
    estados = [False] * NUM_FILOSOFOS  # True se o filósofo está comendo
    progresso = [0] * NUM_FILOSOFOS  # Conta quantas vezes cada filósofo mudou de estado

    def filosofo(filosofo_id):
        for _ in range(3):  # Cada filósofo tenta comer 3 vezes
            if filosofo_id == NUM_FILOSOFOS - 1:  # Último filósofo pega na ordem inversa
                garfos[(filosofo_id + 1) % NUM_FILOSOFOS].acquire()
                garfos[filosofo_id].acquire()
            else:  # Demais filósofos pegam na ordem direita-esquerda
                garfos[filosofo_id].acquire()
                garfos[(filosofo_id + 1) % NUM_FILOSOFOS].acquire()
            
            # Comendo
            estados[filosofo_id] = True
            progresso[filosofo_id] += 1  # Atualiza progresso
            time.sleep(0.1)  # Simula o tempo comendo
            estados[filosofo_id] = False

            # Libera os garfos
            garfos[filosofo_id].release()
            garfos[(filosofo_id + 1) % NUM_FILOSOFOS].release()

    # Cria e inicia as threads
    threads = []
    for i in range(NUM_FILOSOFOS):
        t = threading.Thread(target=filosofo, args=(i,))
        threads.append(t)
        t.start()

    # Monitoramento para deadlock
    inicio = time.time()
    progresso_anterior = progresso[:]
    while time.time() - inicio < TEMPO_LIMITE:
        time.sleep(0.1)  # Verifica a cada 0.1 segundos
        if not any(estados) and all(p == progresso_anterior[i] for i, p in enumerate(progresso)):
            # Deadlock detectado
            resultados[execucao_id] = "Deadlock"
            for t in threads:
                t.join()  # Aguarda todas as threads terminarem
            return
        progresso_anterior = progresso[:]

    # Se todas as threads finalizarem, não houve deadlock
    for t in threads:
        t.join()  # Aguarda todas as threads terminarem
    resultados[execucao_id] = "Sem Deadlock"

# Loop de 1000 execuções para testar a solução
resultados = {}
for execucao_id in range(EXECUCOES):
    jantar_dos_filosofos_com_solucao(resultados, execucao_id)

# Resumo dos resultados
deadlock_count = sum(1 for r in resultados.values() if r == "Deadlock")
sucesso_count = EXECUCOES - deadlock_count

print(f"Execuções sem deadlock: {sucesso_count}")
print(f"Execuções com deadlock: {deadlock_count}")
