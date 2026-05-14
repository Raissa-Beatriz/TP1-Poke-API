# <img src="./icons/pokeball.png" width="32"/> TP1 — PokéAPI: Sistemas Paralelos e Distribuídos

> Comparação de desempenho entre abordagens **sequencial** e **paralelas** para download de imagens da PokéAPI.

**Instituto Federal de Pernambuco — IFPE Campus Belo Jardim**  
Disciplina: Sistemas Paralelos e Distribuídos  
Aluna: Raíssa Beatriz Marinho dos Santos

***

## <img src="./icons/pikachu.png" width="28"/> Sobre o projeto

Este projeto realiza requisições à [PokéAPI](https://pokeapi.co/) para coletar imagens de Pokémon e armazená-las em disco, comparando o tempo de execução entre quatro abordagens:

| Abordagem | Biblioteca | Descrição |
|---|---|---|
| Sequential | — | Um Pokémon por vez, sem paralelismo |
| Threading | `threading` | Múltiplas threads no mesmo processo |
| Multiprocessing | `multiprocessing` | Múltiplos processos independentes |
| concurrent.futures | `concurrent.futures` | API moderna de alto nível para paralelismo |

***

## <img src="./icons/snorlax.png" width="28"/> Estrutura do projeto

```
TP1---Poke-API/
├── sequential.py                # Abordagem sequencial
├── parallel_threading.py        # Abordagem com threading
├── parallel_multiprocessing.py  # Abordagem com multiprocessing
├── parallel_futures.py          # Abordagem com concurrent.futures
├── benchmark.py                 # Script principal — roda tudo e gera results.csv
├── requirements.txt             # Dependências do projeto
├── images/                      # Pasta onde as imagens são salvas (gerada automaticamente)
└── README.md                    # Este arquivo
```

***

## <img src="./icons/jigglypuff.png" width="28"/> Configurações testadas

- **Número de Pokémons:** 100, 500 e 1.000
- **Workers / Threads / Processos:** 2, 4 e 8
- **Repetições por abordagem:** 10 execuções (média calculada ao final)

***

## <img src="./icons/gengar.png" width="28"/> Como executar

### 1. Clone o repositório

```bash
git clone https://github.com/Raissa-Beatriz/TP1-Poke-API.git
cd TP1---Poke-API
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

### 3. Execute o benchmark completo

```bash
python benchmark.py
```

> ⚠️ O benchmark completo pode demorar bastante (1.000 Pokémons × 10 execuções).  
> Para testar rapidamente, edite a linha `TOTALS = [100, 500, 1000]` em `benchmark.py` e use `TOTALS = [10]`.

### 4. Execute cada abordagem individualmente

```bash
python sequential.py
python parallel_threading.py
python parallel_multiprocessing.py
python parallel_futures.py
```

***

## <img src="./icons/pikachu.png" width="28"/> Resultados

Após rodar o `benchmark.py`, um arquivo `results.csv` será gerado com os tempos médios de cada abordagem. Esses resultados são utilizados nas tabelas e gráficos do relatório final em LaTeX.

***

## <img src="./icons/pokeball.png" width="28"/> API utilizada

**PokéAPI** — [https://pokeapi.co](https://pokeapi.co)

- Endpoint base: `https://pokeapi.co/api/v2/pokemon/{id}`
- Campo de imagem: `sprites → front_default`
- Formato de resposta: JSON
- Autenticação: não necessária