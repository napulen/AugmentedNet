import pandas as pd

folds = [
    ".results/wtccrossval/wtcwir-augmentednet-crossval_fold0-210514T135030/54-3.980-0.7878/results.csv",
    ".results/wtccrossval/wirwtc-augmentednet-crossval_fold1-210514T151909/85-9.227-0.7788/results.csv",
    ".results/wtccrossval/wirwtc-augmentednet-crossval_fold2-210514T162835/99-4.326-0.7721/results.csv",
    ".results/wtccrossval/wirwtc-augmentednet-crossval_fold3-210514T172203/76-4.564-0.7464/results.csv",
]

tasks = {
    "LocalKey35": [],
    "Degree": [],
    "Inversion4": [],
    "ChordQuality15": [],
    "RomanNumeral76": [],
    "RomanNumeral": [],
    "AltRomanNumeral": [],
}


for fold in folds:
    df = pd.read_csv(fold)
    for task in tasks:
        tasks[task].append(df[task].mean())


summarydf = pd.DataFrame(tasks)

for task in tasks:
    print(
        f"{task}: {100.0 * summarydf[task].mean().round(3)}, {100.0 * summarydf[task].std().round(3)}"
    )
