# Welcome to `CreoleVal`
CreoleVal is accepted to TACL 2024!

<img src="Appendix/images/landing_page_logo.png" alt="CreoleVal Logo" width="50%"/>


## Overview

This repository includes data (or otherwise download scripts), scripts for training and evaluation, and models for tasks spanning natural language understanding and generation for Creole languages. 

Statistics about the coverage of `CreoleVal` can be found [here](https://github.com/hclent/CreoleVal/tree/main/Appendix), as well as additional analysis of the performance and behaviour over the included tasks. 

If you wish to clone this repository to replicate the results, please remember to initialize the added submodules by using the following command:

```bash
git clone git@github.com:ernlavr/CreoleVal.git --recursive 
```

or if already cloned

```bash
git submodule update --init --recursive
```

### Getting Started
Each of the tasks is contained in a sub-directory where further technical instructions are provided with how to get started in a dedicated `README.md` file.

#### Natural Language Understanding (`./nlu`)
Datasets, training and inference scripts for NLU tasks such as: 
- [Machine Comprehension](nlu/mctest/),
- [Relation Classification](nlu/relation_classification/), 
- [UDPoS](nlu/pos/), 
- [NER](nlu/ner/), 
- [NLI](nlu/nli/), 
- [Sentiment Analysis](nlu/sa/),
- [Tatoeba challenge](nlu/tatoeba_task/).


#### Natural Language Generation (`./nlg`)
Training an inference scripts for Machine Translation task with the MIT-Haiti corpus, KriolMorisiyenMT and bibles. Please note that there is no download script for the set of bibles as the material is copyrighted.

- [Creole-Bible MT](nlg/creolem2m/)
- [KreolMorisien MT](nlg/kreolmorisien_mt)
- [MIT-Ayiti MT](nlg/mit_haiti)
  - Contains monolingual and parallel data for Haitian Creole (hat)


#### Benchmark Overview

Because `CreoleVal` is a composite of new benchmarks and pre-existing ones, there are several different software licenses at play.
For the datasets packed within `CreoleVal` (i.e., the data is actually in the repo, rather than fetched with a download script), we summarize them here, for your convenience. To navigate to a specific dataset, click on the dataset name in the table below.

Note: an `*` indicates a dataset that we have newly introduced in `CreoleVal`:

| **Task** | **Dataset** | **Language (ISO-638-3)** | **License** | **Domain** | **Total Sent.** | **Total words** |
|---|---|---|---|---|---:|---:|
| MC | [CreoleVal MC*](nlu/mctest) | hat-dir, hat-loc, mfe | Microsoft License | Education | 3894 | 32068 |
| RC | [CreoleVal RC*](nlu/relation_classification) | bis, cbk, jam, tpi | CC0 | WikiDump | 785 | 4106 |
| MT | CreoleVal Religious MT* | bzj, bis, cbk, gul,hat, hwc, jam, ktu,kri, mkn, mbf,mfe, djk, pcm,pap, pis, acf, icr,sag, srm, crs, srn,tdt, tpi, tcs | Copyrighted | Religion | 64394 | 811741 |
| MT | [CreoleVal MIT-Haiti*](nlg/mit_haiti) | hat | CC 4.0 | Education | 3164 | 36281 |
| Pretraining data | [CreoleVal MIT-Haiti*](nlg/mit_haiti) | hat | CC 4.0 | Education | 8281 | 116444 |
|||||||
| UDPoS | [Singlish Treebank](nlu/pos) | singlish | MIT | Web Scrape | 1200 | 10989 |
| UDPoS | [UD_Naija-NSC](nlu/pos) | pcm | CC 4.0 | Dialog | 9621 | 150000 |
| NER | [MasakhaNER](nlu/ner) | pcm | Apache 2.0 | BBC News | 3000 | 76063 |
| NER | [WikiAnn](nlu/ner) | bis cbk hat, pih, sgg, tpi, pap | Unspecified | WikiDump | 5877 | 74867 |
| SA | [AfriSenti](nlu/sa) | pcm | CC BY 4.0 | Twitter | 10559 | 235679 |
| SA | [Naija VADER](nlu/sa) | pcm | Unspecified | Twitter | 9576 | 101057 |
| NLI | [JamPatoisNLI](nlu/nli) | jam | Unspecified | Twitter, web | 650 | 2612 |
| SM | [Tatoeba](nlu/tatoeba_task) | cbk, gcf, hat, jam, pap, sag, tpi | CC-BY 2.0 | General web | 49192 | 319719 |
| MT | [KreolMorisienMT](nlg/download_kreolmorisien_mt.sh) | mfe | MIT License | Varied | 6628 | 23554 |
|||||||
|  |  |  |  | New: | 80518 | 1000640 |
|  |  |  |  | Total: | 176821 | 1995180 |

#### Citation
Paper can be found [here](https://arxiv.org/abs/2310.19567).
Please cite us: 

```
@misc{lent2024creoleval,
      title={CreoleVal: Multilingual Multitask Benchmarks for Creoles}, 
      author={Heather Lent and Kushal Tatariya and Raj Dabre and Yiyi Chen and Marcell Fekete and Esther Ploeger and Li Zhou and Ruth-Ann Armstrong and Abee Eijansantos and Catriona Malau and Hans Erik Heje and Ernests Lavrinovics and Diptesh Kanojia and Paul Belony and Marcel Bollmann and Loïc Grobol and Miryam de Lhoneux and Daniel Hershcovich and Michel DeGraff and Anders Søgaard and Johannes Bjerva},
      year={2024},
      eprint={2310.19567},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```
   
