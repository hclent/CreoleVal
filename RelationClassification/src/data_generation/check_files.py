import os
import json
import glob

import plac
import jsonlines
import pandas as pd


def get_the_idle_lines(lang):
    wikidump_folder = os.path.join("wikidumps", lang)
    wikidump_files = [x for x in os.listdir(os.path.join(wikidump_folder, "AA"))]
    print(wikidump_files)

    pattern = f"wikipedia/output/{lang}*.jsonl"
    filepaths = glob.glob(pattern, recursive=False)
    print(filepaths)

    crawled_idxs = []
    writer = jsonlines.open(os.path.join(wikidump_folder, "idle.jsonlines"), mode="w")

    for filenpath in filepaths:
        with open(filenpath) as f:
            for line in f:
                line_ = json.loads(line)
                idx = line_["id"]
                crawled_idxs.append(idx)
    print(f"crawled data lines {lang} -> {len(crawled_idxs)}")

    # get the ids of the wikidump data, to cross-examine with crawled data

    wikidump_idx = []
    for filename in wikidump_files:
        if filename.startswith("wiki_"):
            filepath = os.path.join(wikidump_folder, "AA", filename)

            print(f"open file {filepath}")

            with open(filepath) as f:
                for line in f:
                    line_ = json.loads(line)
                    idx = line_["id"]
                    if idx not in crawled_idxs:
                        print(f"{line_} not written")
                        writer.write(line_)
                    wikidump_idx.append(idx)

    writer.close()
    print(f"wikidump {lang}-> {len(wikidump_idx)}")
    print(len(list(set(wikidump_idx))) == len(list(set(crawled_idxs))))


def compact_files(lang):
    outputfolder = "wikipedia/data/annotated_wikidumps"

    pattern = f"wikipedia/output/{lang}*.jsonl"
    filepaths = glob.glob(pattern, recursive=False)
    print(filepaths)

    # line_writer = jsonlines.open(os.path.join(outputfolder, f"{lang}.jsonl"), mode="w")

    lines = []
    for filenpath in filepaths:
        with open(filenpath) as f:
            for line in f:
                try:
                    line_ = json.loads(line)
                    lines.append(line_)
                except ValueError:
                    print(f)

    # deduplicate dictionaries in the list
    lines = [dict(t) for t in {tuple(d.items()) for d in lines}]
    print(f"crawled data lines {lang} -> {len(lines)}")

    with open(os.path.join(outputfolder, f"{lang}.jsonl"), "w", encoding="utf-8-sig") as outfile:
        outfile.write("\n".join(map(json.dumps, lines)))

    pattern_ = f"wikipedia/output/{lang}_annos*.csv"
    filepaths_ = glob.glob(pattern_, recursive=False)
    print(filepaths_)
    df_list = []
    for filepath in filepaths_:
        try:
            df = pd.read_csv(filepath, sep="\t")
            print(df.head())
            df_list.append(df)
        except Exception as msg:
            print(f"{filepath} -> msg")
            continue

    if len(df_list) > 0:
        df_concat = pd.concat(df_list)
        df_concat = df_concat.drop_duplicates()
        df_concat.to_csv(os.path.join(outputfolder, f"{lang}_anno.csv"), index=False)
        print(f"annotated entities {lang} -> {len(df_concat)}")
    print("*" * 40)


def main():
    creoles = ["ht", "gcr", "pap", "jam", "tpi", "bi", "pih", "sg", "cbk-zam"]
    for lang in creoles:
        # get_the_idle_lines(lang)
        compact_files(lang)


if __name__ == '__main__':
    main()
