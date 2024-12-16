import threading
import time

# Número de filósofos
NUM_FILOSOFOS = 5

# Semáforos para os garfos
garfos = [threading.Semaphore(1) for _ in range(NUM_FILOSOFOS)]

# Função para representar a ação de um filósofo
def filosofo(id):
    while True:
        # Pensar
        print(f"Filósofo {id} está pensando.")
        time.sleep(1)

        # Tentar pegar os garfos
        print(f"Filósofo {id} está tentando pegar o garfo direito.")
        garfos[(id + 1) % NUM_FILOSOFOS].acquire()  # Pega o garfo à direita
        print(f"Filósofo {id} pegou o garfo direito.")

        print(f"Filósofo {id} está tentando pegar o garfo esquerdo.")
        garfos[id].acquire()  # Pega o garfo à esquerda
        print(f"Filósofo {id} pegou o garfo esquerdo.")

        # Comer
        print(f"Filósofo {id} está comendo.")
        time.sleep(2)

        # Devolver os garfos
        print(f"Filósofo {id} terminou de comer e está devolvendo os garfos.")
        garfos[(id + 1) % NUM_FILOSOFOS].release()  # Devolve o garfo à direita
        garfos[id].release()  # Devolve o garfo à esquerda

# Criar e iniciar threads para os filósofos
threads = []
for i in range(NUM_FILOSOFOS):
    t = threading.Thread(target=filosofo, args=(i,))
    threads.append(t)
    t.start()

# Manter o programa rodando
for t in threads:
    t.join()
