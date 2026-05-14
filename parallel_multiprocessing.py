import requests
import os
import time
from multiprocessing import Pool

os.makedirs("images", exist_ok=True)

def get_and_save(pokemon_id):
    data = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}").json()
    img_url = data["sprites"]["front_default"]
    if img_url:
        img = requests.get(img_url).content
        with open(f"images/{pokemon_id}.png", "wb") as f:
            f.write(img)

def run_multiprocessing(total, num_processes):
    times = []
    for run in range(10):
        for f in os.listdir("images"):
            os.remove(f"images/{f}")
        start = time.time()
        with Pool(processes=num_processes) as pool:
            pool.map(get_and_save, range(1, total + 1))
        elapsed = time.time() - start
        times.append(elapsed)
        print(f"[Multiprocessing-{total}-{num_processes}p] Execução {run+1}/10: {elapsed:.2f}s")
    avg = sum(times) / len(times)
    print(f"[Multiprocessing-{total}-{num_processes}p] MÉDIA: {avg:.2f}s\n")
    return avg

if __name__ == "__main__":
    for total in [100, 500, 1000]:
        for procs in [2, 4, 8]:
            run_multiprocessing(total, procs)