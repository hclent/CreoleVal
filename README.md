# Welcome to `CreoleVal`


## Overview

This repository includes data (or otherwise download scripts), scripts for training and evaluation, and models for tasks spanning natural language understanding and generation for Creole languages. 

Statistics about the coverage of `CreoleVal` can be found [here](https://github.com/hclent/CreoleVal/tree/main/Appendix), as well as additional analysis of the performance and behaviour over the included tasks. 

#### This repo is under construction! 

This repository is actively undergoing construction, on a weekly or even daily basis. Our outstanding TODO items include:

* [documentation] finish the "License Overview"
* [`nlg/creolem2m`] Add details for train-dev-test creation
* [`nlg/`] Add links and experiments for KriolMorisiyen MT
* [`Appendix/relation_classification`] Add examples of the latent templates
* [`Appendix`] add pictures of data stats
* much more ... 

#### Natural Language Understanding (`/nlu`)

Machine comprehension, relation classification, UDPoS, NER, NLI, sentiment analysis, and tatoeba challenge.

#### Natural Language Generation (`/nlg`)

Machine translation with bibles, the MIT-Haiti Corpus, and KriolMorisiyenMT

## License Overview

Because `CreoleVal` is a compossit of new benchmarks and pre-existing ones, there are several different licesnes at play.
We summarize them here, for your convenience. A `*` indicates a dataset that we have newly introduced in `CreoleVal`:

| Dataset           | Task                    | Languages                       |                                         Source                                          | Domain                 |                            License | 
|:------------------|:------------------------|:--------------------------------|:---------------------------------------------------------------------------------------:|:-----------------------|-----------------------------------:|
| MCTest            | machine comprehension   | eng, hat*, mfe*                 |           [original](https://github.com/mcobzarenco/mctest/tree/master/data)            | short stories for kids | MSR-LA: Microsoft Research License | 
| CreoleRC          | relation classification | bi*, cbk-zam*, jam*, phi*, tpi* |                                        Wikipedia                                        | Wikipedia              |                       CC-BY-SA 4.0 |
| MIT-Haiti Corpus  | machine translation     | hat*, eng*, es*, fr*            |                       [Platform MIT-Haiti](https://mit-ayiti.net/)                      | education              |                       CC-BY-SA 4.0 |
| Singlish Treebank | universal dependencies  | singlish                        |                                                                                         |                        |                       CC-BY-SA 4.0 |
| UD_Naija-NSC      | universal dependencies  | pcm                             |                                                                                         |                        |                       CC-BY-SA 4.0 |
|                   |                         |                                 |                                                                                         |                        |                       CC-BY-SA 4.0 |
|                   |                         |                                 |                                                                                         |                        |                       CC-BY-SA 4.0 |
|                   |                         |                                 |                                                                                         |                        |                       CC-BY-SA 4.0 | 
|                   |                         |                                 |                                                                                         |                        |                       CC-BY-SA 4.0 |


Paper can be found here

Please cite us: `{...}`
