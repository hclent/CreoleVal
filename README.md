# Welcome to `CreoleVal`
<img src="Appendix/images/landing_page_logo.png" alt="CreoleVal Logo" width="50%"/>


## Overview

This repository includes data (or otherwise download scripts), scripts for training and evaluation, and models for tasks spanning natural language understanding and generation for Creole languages. 

Statistics about the coverage of `CreoleVal` can be found [here](https://github.com/hclent/CreoleVal/tree/main/Appendix), as well as additional analysis of the performance and behaviour over the included tasks. 

### This repo is under construction! 

This repository is actively undergoing construction, on a weekly or even daily basis. Our outstanding TODO items include:

* A "Getting Started" guide, to walk you through the data and experiments in this repo. 
* Adding more scripts, so others can easily run `CreoleVal` experiments
* [`nlg/`] Add links and experiments for KriolMorisiyen MT
* [`Appendix/`] Adding more documentation, with analysis of experiments
* Generally, add the scripts to make it clear what data is left over to train CreoleLM's with, without cross-contaminating
* Make sure there are no hard-coded paths


#### Natural Language Understanding (`/nlu`)

Machine comprehension, relation classification, UDPoS, NER, NLI, sentiment analysis, and tatoeba challenge.

#### Natural Language Generation (`/nlg`)

Machine translation with bibles, the MIT-Haiti Corpus, and KriolMorisiyenMT

#### Benchmark Overview

Because `CreoleVal` is a composite of new benchmarks and pre-existing ones, there are several different software licenses at play.
For the datasets packed within `CreoleVal` (i.e., the data is actually in the repo, rather than fetched with a download script), we summarize them here, for your convenience.

Note: an `*` indicates a dataset that we have newly introduced in `CreoleVal`:

| **Task** | **Dataset** | **Language (ISO-638-3)** | **License** | **Domain** | **Total Sent.** | **Total words** |
|---|---|---|---|---|---:|---:|
| MC | [CreoleVal MC*](nlu/mctest) | hat-dir, hat-loc, mfe | Microsoft License | Education | 3894 | 32068 |
| RC | [CreoleVal RC*](nlu/relation_classification/data/relation_extraction) | bis, cbk, jam, tpi | CC0 | WikiDump | 785 | 4106 |
| MT | CreoleVal Religious MT* | bzj, bis, cbk, gul,hat, hwc, jam, ktu,kri, mkn, mbf,mfe, djk, pcm,pap, pis, acf, icr,sag, srm, crs, srn,tdt, tpi, tcs | Copyrighted | Religion | 64394 | 811741 |
| MT | [CreoleVal MIT-Haiti*](nlg/mit_haiti/data) | hat | CC 4.0 | Education | 3164 | 36281 |
| Pretraining data | [CreoleVal MIT-Haiti*](nlg/mit_haiti/data/ht_monolingual.txt) | hat | CC 4.0 | Education | 8281 | 116444 |
|||||||
| UDPoS | [Singlish Treebank](nlu/baselines/download_singlish_upos.sh) | singlish | MIT | Web Scrape | 1200 | 10989 |
| UDPoS | [UD_Naija-NSC](nlu/baselines/download_ud_naija.sh) | pcm | CC 4.0 | Dialog | 9621 | 150000 |
| NER | [MasakhaNER](nlu/baselines/download_masakhaner.sh) | pcm | Apache 2.0 | BBC News | 3000 | 76063 |
| NER | [WikiAnn](nlu/baselines/data/WikiAnn_data) | bis cbk hat, pih, sgg, tpi, pap | Unspecified | WikiDump | 5877 | 74867 |
| SA | [AfriSenti](nlu/baselines/download_afrisenti.sh) | pcm | CC BY 4.0 | Twitter | 10559 | 235679 |
| SA | [Naija VADER](nlu/baselines/data/Oyewusi) | pcm | Unspecified | Twitter | 9576 | 101057 |
| NLI | [JamPatoisNLI](nlu/baselines/download_jampatois_nli.sh) | jam | Unspecified | Twitter, web | 650 | 2612 |
| SM | [Tatoeba](nlu/tatoeba_task) | cbk, gcf, hat, jam, pap, sag, tpi | CC-BY 2.0 | General web | 49192 | 319719 |
| MT | [KreolMorisienMT](nlg/download_kreolmorisien_mt.sh) | mfe | MIT License | Varied | 6628 | 23554 |
|  |  |  |  | New: | 80518 | 1000640 |
|  |  |  |  | Total: | 176821 | 1995180 |

#### Citation

Paper can be found [here](https://arxiv.org/abs/2310.19567).

Please cite us: 

```
@misc{lent2023creoleval,
      title={CreoleVal: Multilingual Multitask Benchmarks for Creoles}, 
      author={Heather Lent and Kushal Tatariya and Raj Dabre and Yiyi Chen and Marcell Fekete and Esther Ploeger and Li Zhou and Hans Erik Heje and Diptesh Kanojia and Paul Belony and Marcel Bollmann and Loïc Grobol and Miryam de Lhoneux and Daniel Hershcovich and Michel DeGraff and Anders Søgaard and Johannes Bjerva},
      year={2023},
      eprint={2310.19567},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```
