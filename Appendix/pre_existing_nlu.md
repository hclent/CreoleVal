## Pre-Existing NLU Tasks

Here, we breifly describe the datasets/tasks we are working with, and provide statistics and analysis where relevant.


### UDPoS Tagging

To our knowledge, the two Creoles with existing UD datasets are [Singlish](https://aclanthology.org/P17-1159/) and [Nigerian Pidgin](https://aclanthology.org/W19-7803/). 

### Named Entity Recognition 

Nigerian Pidgin (pcm) is among the 10 African languages composing the [MasakhaNER dataset](https://github.com/masakhane-io/masakhane-ner/tree/main/MasakhaNER2.0). 
The Nigerian Pidgin subset of this data lies within the news domain, and has `train/dev/test` splits with `2100/ 300/ 600` sentences, respectively. 
Of the total 76,063 tokens, 13.25% are part of a named entity. 

In contrast with MasakhaNER, [WikiAnn](https://aclanthology.org/P17-1178/) is a *"silver standard"* dataset, with NER labels automatically generated over sentences for Wikipedia, for 282 languages. 
Among these languages are 7 Creoles, with varying degrees of data available, depending on the size of the Wikipedia. 
We were unable to find the official data splits released with the dataset, so we rather constructed our own train/dev/test sets, stratified by utterance length, to ensure that one split did not over-represent short or long utterances. 

Here are some statistics on our WikiAnn datasplits for Creoles, presented in `CreoleVal`:

| Language | Train/Dev/Test            | LOC  | PER | ORG | % of Entities | # of Tokens |
|:---------|:--------------------------|:-----|:---:|----:|--------------:|------------:|
| bi       | 263/38/76                 | 418  | 30  |   5 |          14.5 |        3.7K |
| cbk-zam  | 1736/248/497              | 3800 | 152 | 186 |          13.5 |         45K |
| ht       | 171/25/50                 | 265  | 59  |  24 |          48.2 |        1.6K |
| pap      | 871/125/250               | 1285 | 78  |  80 |          11.5 |         18K |
| pih      | 259/37/75                 | 433  |  6  |  13 |          15.5 |        3.8K |
| sg       | 147/21/43                 | 208  |  1  |   2 |          21.4 |        1.9K |
| tpi      | 654/94/187                | 962  | 14  |  14 |          25.8 |        6.6K |

Above, you can see the size of the dataset splits, the number of entities in each label type (LOC, PER, ORG), the proportion of named entities amongst all tokens, and the total number of tokens in the entire dataset.
Notably, most named entities fall under the LOC category. As silver standard data generated over Wikipedia data, this is perhaps not surprising. 

### Sentiment Analysis for Nigerian Pidgin 

We work with the Nigerian Pidgin portion of [AfriSenti](https://aclanthology.org/2023.semeval-1.315/) from SemEval2023.
This dataset expands on the previous [NaijaSenti](https://aclanthology.org/2022.lrec-1.63/) dataset.
The Nigerian Pidgin portion of AfriSenti has a `train/dev/test` split of `5122 / 1282 / 4155 `.

Another Sentiment Analysis dataset for Nigerian Pidgin was introduced by [Oyewusi et al. 2020](https://arxiv.org/abs/2003.12450).
This dataset was specifically designed to fit within the VADER paradigm, a rule-based Sentiment Analysis approach, which leverages a lexicon of terms weighted for their sentiment. 
We have made our own 70-10-20 split for train, dev, and test, for this data, as we did not find information about the splits in the [original repo](https://github.com/sharonibejih/Research-Papers-by-Data-Science-Nigeria/tree/develop/Semantic%20Enrichment%20of%20Nigerian%20Pidgin%20English%20for%20Contextual%20Sentiment%20Classification).

### NLI for Jamacan Patois

The `JamPatoisNLI` dataset by [Armstrong et al. 2022](https://aclanthology.org/2022.findings-emnlp.389/) is a small dataset intended for few-shot learning and adapting English-based NLI systems for Jamaican Patois 
We follow the authors' protocol by first finetuning on the [GLUE MNLI dataset](https://aclanthology.org/N18-1101/) and then do few-shot learning on JamPatoisNLI. 
The `JamPatoisNLI` has a total of 250 examples, evenly distributed across each label type (entailment, contradiction, neutral).

### Tatoeba

The [Tatoeba](https://aclanthology.org/Q19-1038/) task is a multilingual sentence similarity search task.
It involves finding the nearest neighbours across bilingual sentence pairs using cosine similarity between their representations.
Performance is evaluated using accuracy.
Following previous benchmarks using the Tatoeba task -- see [XTREME](https://arxiv.org/abs/2003.11080) and [XTREME-R](https://aclanthology.org/2021.emnlp-main.802/) -- we do not carry out task-specific fine-tuning, instead creating sentence embeddings by pooling the subword token embeddings of the pretrained LMs.

## TODO: table with data sizes 

In order to obtain coverage of at least a subset of our Creole languages, we derive data from the [Tatoeba Translation Challenge dataset](https://aclanthology.org/2020.wmt-1.139/) that covers over 557 languages.
After the original implementation of the task, we aim to create test sets of 1,000 sentence pairs with English and, where possible, a related language -- this took place in the case of two French-related Creoles, gcf and hat.
Due to dataset sizes, test sets are considerably smaller for `jam-eng` (146 sentence pairs) and `gcf-eng` (102 sentence pairs).
Another limitation comes from the fact that the datasets are not parallel across languages, which might significantly impact the difficulty of the task across languages.
To control for this, **when the dataset sizes allowed, we sampled from the source data three times** and compared results.

#### Full Results for Tatoeba

We compare accuracy scores on the Creole source sentence - English (and/or another ancestor language) target sentence pairs with a random baseline and with scores achieved on high-resource languages all observed during the training of the LMs: German, French, and Norwegian.

Here are the Creoles, paired with English, and German/French/Norwegian with English as a comparisson. 
These scores reflect accuracy: 

 Pair        | mBERT       | XLM-R      |   mT5    |           Random |
|:------------|:------------|:-----------|:--------:|-----------------:|
  | cbk-eng     | **15.9**    | 3.9        |   6.5    |              0.0 |  
 | gcf-eng     | **12.8**    | 4.9        |   6.9    |              0.0 |
 | hat-eng     | 23.9        | 18.5       | **37.9** |              0.0 | 
 | jam-eng     | **19.9**    | 9.6        |   10.3   |              0.7 |
 | pap-eng     | **22.4**    | 6.1        |   15.9   |              0.1 |
 | sag-eng     | 5.7         | 2.1        | **7.3**  |              0.2 |
 | tpi-eng     | 7.2         | 3.3        | **7.6**  |              0.1 |
| :--------:  | :---------: | :--------: |:--------:| :--------------: |
| deu-eng     | **55.7**    | 44.2       |   29.4   |              0.2 |  
| fra-eng     | **49.4**    | 33.7       |   32.3   |              0.1 |
| nor-eng     | **60.8**    | 47.7       |   30.7   |              0.0 | 

Generally low accuracy scores landing between 2-38 out of 100 for Creole-English sentence pairs, falling behind accuracy scores on languages in the training data.

For Creoles not genealogically related to English, we also look at the `<Creole>`--`<ancestor>` scenario.
Tatoeba accuracy with French-based Creoles (`gfc` and `hat`) and the Spanish-based Chavacano (`cbk`): 

  | Pair    | mBERT       | XLM-R   |   mT5    |  Random | 
  |:--------|:------------|:--------|:--------:|--------:|
  | cbk-eng | **15.9**    | 3.9     |  6.5     |     0.0 |
  | cbk-spa | **54.8**    | 23.1    |   18.3   |     0.1 | 
  | gcf-eng | **12.8**    | 4.9     |   6.9    |     0.0 |
  | gcf-fra | **2.4**     | 1.8     |   2.1    |     0.1 |
  | hat-eng | 23.9        | 18.5    | **37.9** |     0.0 |
  | hat-fra | 31.0        | 12.9    | **43.4** |     0.0 |

#### Discussion of Tatoeba Results

All LMs perform better on high-resource languages seen in the pretraining data.
This is especially clear with the highest performance achieved on Creoles -- by mT5 on `hat`, which is included in its pretraining data.
Despite mBERT containing the least number of parameters (180M), the accuracy scores it achieves on most languages surpass both mT5 (300M) and especially XLM-R (270M).
We hypothesise that this performance benefit is achieved due to mBERT being the only LM trained on a sentence-level objective, next sentence prediction.
On the other hand, mT5 is trained using a span-level language modelling objective while XLM-R is only trained on subword-level masked language modelling.

Accuracy on the Tatoeba task increases when pairing `hat` and `cbk` with their lexifiers, French and Spanish, respectively. 
While in the case of `cbk` this is true across the board, with the case of `hat`, this is only for mBERT and mT5, the two LMs that perform better on the Tatoeba task.
The opposite is true for `gcf`, which is geneaologically related to French: all three LMs perform significantly better on the `gcf-eng` language pair.
However, it is important to remember that the *size* of the `gcf-eng` dataset is a tenth (102 sentence pairs) of the size of the `gcf-fra` one.
This might be behind the abysmal performance of the latter.
The size of the `cbk-spa` dataset is also 102 sentences, meaning that the models underperform on the smaller datasets.
Further investigation would be necessary to assess more generally whether sentence similarity search is more successful when pairing Creoles with their lexifier.

#### Tatoeba analysis

Inspired by [ExplainaBoard](https://aclanthology.org/2021.acl-demo.34/), we carry out a more in-depth analysis of our results.
We measure the subword token overlap ratio between source and target languages, as well as the source sentence fertility of the source sentence as candidate factors that we suspect might affect performance on the Tatoeba task.
Source sentence fertility, following \citealp{acs-etal-2019-exploring} is defined as the ratio of subword tokens to words in a sentence.
We hypothesise that source sentence fertility might correlate with how well a given LM captures the linguistic elements of a sentence.
Subword overlap, on the other hand, is an important measure to control for how much the presence of the same subword tokens impacts LM judgement.
If subword overlap correlates a lot with the accuracy on the Tatoeba task, it begs the question whether the LMs do anything more than pairing identical spans across sentences.

We bin sentences based on the two factors in categories such as 'very low', 'medium low', 'medium high', and 'very high', plotting average accuracy scores across the individual categories.
We find that subword overlap contributes to the most increase in accuracy on the Tatoeba task.
Somewhat felicitously, however, the increase is most significant when the overall accuracy on a language pair is already above 10, indicating that the LMs do something more than just matching identical spans.
Fertility seems to correlate less with accuracy, and the correlation is less obvious across languages.
Nevertheless, a sort of u-pattern is observable with a large subset of languages where performance on source sentences with either 'very low' or 'very high' fertility is higher than on mid-level categories.

## TODO: put the graphs here 