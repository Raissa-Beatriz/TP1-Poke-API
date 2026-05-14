import requests, os, time, threading, csv
from multiprocessing import Pool
from concurrent.futures import ThreadPoolExecutor

os.makedirs("images", exist_ok=True)

def get_and_save(pokemon_id):
    try:
        data = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}", timeout=10).json()
        img_url = data["sprites"]["front_default"]
        if img_url:
            img = requests.get(img_url, timeout=10).content
            with open(f"images/{pokemon_id}.png", "wb") as f:
                f.write(img)
    except Exception as e:
        print(f"Erro no pokémon {pokemon_id}: {e}")

def clear():
    for f in os.listdir("images"):
        os.remove(f"images/{f}")

def measure(fn, runs=10):
    times = []
    for _ in range(runs):
        clear()
        start = time.time()
        fn()
        times.append(time.time() - start)
    return round(sum(times) / len(times), 2)

TOTALS = [100, 500, 1000]
WORKERS = [2, 4, 8]
results = []

for total in TOTALS:
    ids = range(1, total + 1)
    print(f"\n=== {total} pokémons ===")

    avg = measure(lambda: [get_and_save(i) for i in ids])
    results.append({"abordagem": "Sequential", "workers": "-", "total": total, "media_s": avg})
    print(f"  Sequential: {avg}s")

    for w in WORKERS:
        def run_t(ids=ids, w=w):
            threads = []
            for i in ids:
                t = threading.Thread(target=get_and_save, args=(i,))
                threads.append(t); t.start()
                if len(threads) >= w:
                    for th in threads: th.join()
                    threads = []
            for th in threads: th.join()
        avg = measure(run_t)
        results.append({"abordagem": "Threading", "workers": w, "total": total, "media_s": avg})
        print(f"  Threading-{w}: {avg}s")

    for w in WORKERS:
        def run_mp(ids=ids, w=w):
            with Pool(processes=w) as pool: pool.map(get_and_save, ids)
        avg = measure(run_mp)
        results.append({"abordagem": "Multiprocessing", "workers": w, "total": total, "media_s": avg})
        print(f"  Multiprocessing-{w}: {avg}s")

    for w in WORKERS:
        def run_f(ids=ids, w=w):
            with ThreadPoolExecutor(max_workers=w) as ex: ex.map(get_and_save, ids)
        avg = measure(run_f)
        results.append({"abordagem": "concurrent.futures", "workers": w, "total": total, "media_s": avg})
        print(f"  Futures-{w}: {avg}s")

with open("results.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["abordagem","workers","total","media_s"])
    writer.writeheader()
    writer.writerows(results)

print("\n\n=== RESULTADO FINAL ===")
print(f"{'Abordagem':<22} {'Workers':<10} {'Total':<8} {'Média (s)'}")
print("-"*55)
for r in results:
    print(f"{r['abordagem']:<22} {str(r['workers']):<10} {r['total']:<8} {r['media_s']}")
print("\nSalvo em results.csv")