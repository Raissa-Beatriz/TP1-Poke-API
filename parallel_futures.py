import requests
import os
import time
from concurrent.futures import ThreadPoolExecutor

os.makedirs("images", exist_ok=True)

def get_and_save(pokemon_id):
    data = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}").json()
    img_url = data["sprites"]["front_default"]
    if img_url:
        img = requests.get(img_url).content
        with open(f"images/{pokemon_id}.png", "wb") as f:
            f.write(img)

def run_futures(total, num_workers):
    times = []
    for run in range(10):
        for f in os.listdir("images"):
            os.remove(f"images/{f}")
        start = time.time()
        with ThreadPoolExecutor(max_workers=num_workers) as executor:
            executor.map(get_and_save, range(1, total + 1))
        elapsed = time.time() - start
        times.append(elapsed)
        print(f"[Futures-{total}-{num_workers}w] Execução {run+1}/10: {elapsed:.2f}s")
    avg = sum(times) / len(times)
    print(f"[Futures-{total}-{num_workers}w] MÉDIA: {avg:.2f}s\n")
    return avg

if __name__ == "__main__":
    for total in [100, 500, 1000]:
        for workers in [2, 4, 8]:
            run_futures(total, workers)