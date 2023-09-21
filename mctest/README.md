## MCTest for Mauritian Creole & Haitian Kreyòl

#### Original dataset

Take a look at `./MCTest` for the original dataset, information from the original authors, and Creole translations.

#### Translation

MC160 **.dev** set has been translated into Marutian Creole and Haitian Creole, by professional translators.
This consists of 30 stores pertaining to a total of 120 questions (4 multiple choice questions per story).
Notably, we have **2** distinct translations for Haitian:
The `MCTestHat1/mc160.dev.json` is a direct translation, matching the English. 
The `MCTestHat2/mc160.dev.json` is a localized translation, with names, places, and activities adjusted to be more relevant to Haitian people.

See `./MCTest/CreoleTranslations` for the original `.txt` translations and the `.tsv` file formats as well. 

An **important note**: our translators identified an error with the original English mc160.dev.17 story: namely, in question 3, the correct answer (B) incorrectly says "pink" flowers rather than "yellow" flowers.
We have fixed the English version, included in this repo, and our translations have also been correct to reflect the text of the original story.

**NB: Once this data has been uploaded to the MIT-Ayiti website, we will remove it from the Github, and instead provide a download script to fetch it from the MIT-Ayiti platform**

#### Data Preprocessing
First, we convert the translated `.txt` files into `.tsv` to match the original English `.tsv` files (see `./MCTest/CreoleTranslations`). 
Then we convert these to `.json` format, as we found it more tidy to work with (these are the `./MCTest*X*` directries, where X={160, Hat1, Hat2, Mar, 500}. 
The `./MCTest160` dir is the original train, dev, test data in English. The `Hat1`, `Hat2`, and `Mar` datasets have the translated `mc160.dev.json` files, for **Hait**ian and **Maur**itian. ).
The `./MCTest500` dir is the English MC500 dataset, as json.

Code for this can be found in `preproc.py`, however this code needs a bit of cleaning before its public-ready.
As we provide our json and tsv files, it should be no problem for anyone to plug-and-play with these datasets :-).

#### Baseline Model

We use the Huggingface `AutoModelForMultipleChoice`.
See [here](https://huggingface.co/transformers/v3.3.1/model_doc/auto.html?highlight=automodelformultiplechoice#transformers.AutoModelForMultipleChoice) for details.  
We have sepperate implementations for mbert (`run_mbert.py`) and xlm-r (`run_xlmr.py`), as the latter does not make use of the `token_type_id`'s.  

#### Environment 

As we run our code on a university cluster, we use Singularity to create our python environment.
You can build a Docker or Singularity container from the following docker image: `docker://nvcr.io/nvidia/pytorch:22.08-py3`.

Additionaly/Otherwise, try with our `requirements.txt`.

#### Training 

See `train.sh` for examples. 

#### Evaluation

See `evaluate.sh` for examples.

##### License

As this data is translated from Microsoft's MCTest dataset,
it inherits the same license as the original. Please see `./MCTest/LICENSE.pdf` for details. 