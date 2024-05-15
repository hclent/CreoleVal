## A. Relation Classification
Here, we thoroughly describe our steps to create the relation classification datasets, from data collection, to annotation and verification. This discussion is intended to provide details for exact replication of the work described in the paper, for creating these datasets.
For an overview, our methodology consisted of the following steps:

1. Collecting and cleaning data from Wikipedia dumps, and performing automatic entity linking. 
2. Clustering sentences which belong to the same latent template (i.e., the sentences express the same relation, as evidenced by an exact or near-exact overlap in the text, with the only differences being the entities; more details are provided in section below `Appendix A.2`.
3. Manually verifying and correcting any mistakes from the automatic entity-linking.
4. Manually annotating the relation expressed in the sets of utterances (as grouped by the latent templates) and its associated Property in Wikidata.
5. Validating that the annotated triples indeed exist in Wikidata; sentences where the triples did not exist in Wikidata (due to gaps in the knowledge base) were thrown out.
6. Manually checking the correcting the annotated sentences to ensure that the samples truly reflect real-world usage of the language. 
    - A manual verification of each dataset was performed by a speaker of each Creole. Each sentence was assessed, and speakers made corrections to the grammar or spelling, as they saw fit. Whenever possible, an additional speaker was asked to double-check these changes. 
    - Complementing the above step, a manual verification of the datasets is conducted using published linguistic grammars for the relevant language, to help identify potential issues in the data.
    - A final re-verification of the entity tagging and property labels was conducted, to ensure that any corrected sentences were still properly annotated. 

For steps 1-4, we produced datasets for: Bislama, Chavacano, Haitian Creole, Jamaican Patois, and Pitkern, and Tok Pisin. However at step 5, the triples for Haitian Creole were not validated by the Wikidata and thus this dataset was discarded. Here, simple triples like (apple, is\_a, fruit) were missing from the knowledge graph. Additionally at step 6, the Pitkern samples failed to conform with the description of the language detailed in the grammar, and was also excluded from this work. Ultimately, this resulted in high-quality relation classification evaluation data for 4 of the 9 Creole Wikipedias we started with: Bislama, Chavacano, Jamaican Patois, and Tok Pisin. 

### A.1 Data Collection and Annotation
We first clean the data and perform automatic entity linking and filtering, in order to facilitate the process of manual annotation. First, we preprocess the Wikipedia dumps by removing unnecessary HTML with BeautifulSoup and tokenization with Spacey. We then automatically label entities and link them to Wikidata, a process known as entity linking, first by linking tokens with existing Wikipedia hyperlinks within the text, and then attempt to label any remaining entities without hyperlinks by leveraging OpenTapioca. Before any manual annotation over these examples, we then attempt to automatically group sentences by latent templates, so that sentences can be annotated in groups, allowing us to identify and annotate the correct relationship between the entities, as expressed in the sentences (see “Latent Templates”, below). To this end, we perform automatic clustering over the sentences using first fuzzy string matching with partial token sort ratio, and thereafter affinity propagation, in hopes that utterances sharing templatic spans of text will be clustered together. The result is a large set of clusters, each containing a number of utterances that are at least somewhat similar. In order to refine these clusters further, we first rank the clusters by the longest common string therein, and we then discard clusters below a certain threshold of similarity, as we can assume the sentences do not belong to the same latent template.
Finally, with the highest-scoring clusters of entity-linked sentences, the authors perform a manual annotation of entities and relations. 

### A.2 Latent Templates
In paper `Section 3.2`, we mention the latent templates that the sentences belong to, and how these templates enable more confident manual annotation. To clarify this, we will show some examples of latent templates, and how we map this to Wikidata Properties (i.e. relations) and entities. Note that samples were clustered by latent templates *before* validation and correction by the Creole language speakers, so the provided examples below do not represent the finalized dataset. Consider the following <span style="color:blue">entity-tagged</span> sentences in Bislama:

- <span style="color:blue;">Mongolia</span> i kaontri long <span style="color:blue;">Esia</span>.
- <span style="color:blue;">Fiji</span> hem i wan kaontri long <span style="color:blue;">Pasifik</span>.
- <span style="color:blue;">Jemani</span> i kaontri long <span style="color:blue;">Yurop</span>.
- <span style="color:blue;">Bukina Faso</span> i kaontri long <span style="color:blue;">Afrika</span>.
- <span style="color:blue;">Kanada</span> i wan kaontri blong <span style="color:blue;">Not Amerika</span>.

When we look at these sentences as a group (i.e. a cluster), we can see there is a latent template of <span style="color:gray;">[[ABC]] (hem) i (wan) kaontri (b)long [[XYZ]]</span>. All sentences in the cluster belong to this latent template, albeit with some minor variations, which are later inspected and assessed in detail during the validation stage by a speaker of Bislama, and additionally with a cross-reference against a linguistics grammar documenting the language.

Moving on, for the **entities** themselves, we can identify the Wikidata Qcode in 2 ways:

1. The entities (e.g. <span style="color:blue;">Mongolia</span>, <span style="color:blue;">Pasifik</span>) were already hyperlinked in the Wikipedia article, which means we have a URL, from which we can get the gold entity Q-code.
2. The entities are Named Entities with spelling clearly influenced by English, and we can make an educated guess about the meaning.

Thus from the template and entities, we can now consider the **relation** between the entities:

(<span style="color:blue;">Mongolia</span> is to <span style="color:blue;">Asia</span>) as (<span style="color:blue;">Fiji</span> is to <span style="color:blue;">Pacific</span>) as (<span style="color:blue;">Germany</span> is to <span style="color:blue;">Europe</span>) as (<span style="color:blue;">Canada</span> is to <span style="color:blue;">North America</span>) and (<span style="color:blue;">Burkina Faso</span> is to <span style="color:blue;">Africa</span>).

For all of these entity pairs, to a human annotator, it is clear that the relationship is <span style="color:gray;">[[COUNTRY]] is in [[CONTINENT]]</span>. Thus we can annotate the Wikidata Property as P30: "continent of which the subject is a part".

Finally, we can automatically verify our triples (entity1, Property, entity2) against the Wikidata knowledge graph. We remove any sentences where the triple was not in the knowledge graph. This unfortunately removes correct data points, where there is simply a gap in the knowledge graph; for example, the Haitian dataset was removed for this reason, as Wikidata missed simple cases like (apple, is\_a, fruit). But importantly, it also is a sanity measure of our annotation method performed by the authors, which at times required educated guesswork about the meaning of an entity, as non-native speakers, when the entity was not already hyper-linked.

Presumably, if we incorrectly annotated an entity, the triple will not exist in the knowledge graph, and thus be removed. Imagine that we had incorrectly annotated <span style="color:blue;">Kanada</span> (from the sentence <span style="color:blue;">Kanada</span> i wan kaontri blong <span style="color:blue;">Not Amerika</span>.) to be the language *Kannada* (Q33673), rather than the country *Canada* (Q16). The triple (Kannada_language, "continent of which the subject is a part", North America) would certainly not exist in Wikidata, and thus the entire annotated example would be removed. Yet (Canada, "continent of which the subject is a part", North America) is indeed in the knowledge base, so we can be confident in our annotation. Again, having samples listed together in groups by latent templates also makes us more certain of the meaning.

Here are some more examples of latent templates in the data, and the expressed relations:

**Chavacano**  
Latent template: <span style="color:gray;">[[PERSON]] is a [[SINGER]]</span>.  
Property P106: "occupation of a person"  
Examples:

- <span style="color:blue;">Billie Eilish</span> es un <span style="color:blue;">cantante</span>
- <span style="color:blue;">Sopho Khalvashi</span> es un <span style="color:blue;">cantante</span>
- <span style="color:blue;">Juanes</span> es un <span style="color:blue;">cantante</span> de Colombia de pop.
- <span style="color:blue;">Nina Sublatti</span> (Sulaberidze) es un <span style="color:blue;">cantante</span>
- <span style="color:blue;">Nini Shermadini</span> es un <span style="color:blue;">cantante</span>


**Jamaican Patois**  
Latent template: <span style="color:gray;">[[CITY]] is the capital of [[COUNTRY]]</span>  
Property P1376: "capital of"  
Examples:
- <span style="color:blue;">Sofiya</span> a di kiapital fi <span style="color:blue;">Bulgieria</span>.
- <span style="color:blue;">Broslz</span> a di kiapital fi <span style="color:blue;">Beljiom</span>.
- <span style="color:blue;">Ruom</span> a di kyapital fi <span style="color:blue;">Itali</span>.
- <span style="color:blue;">Masko</span> a di kyapital fi <span style="color:blue;">Rosha</span>.
- <span style="color:blue;">Atenz</span> a di kyapital fi <span style="color:blue;">Griis</span>.


### A.3 Validation and Corrections
After the manual validation of the entity tagging and relation labeling, as well as automatic validation of triples in Wikidata, we work with speakers to further validate and correct the sentences as needed, as sentences sourced from Wikipedia can often be of poor quality for lower-resource languages TODO:\cite{kreutzer-etal-2022-quality}. In conjunction with the validation performed by speakers, we also check published linguistic grammars for these languages, to ensure that our published datasets constitute the up-most quality. 

#### Validation and Corrections by Speakers 
For Bislama, Chavacano, Jamaican Patois, and Tok Pisin, we collaborated with at least one speaker of the language to validate and correct the annotated samples. 
Here, our speakers are either semi-native speakers (i.e., they grew up using the language), or professional linguists who live in the pertinent community and speak the language on a daily basis. Indeed, as many Creoles exist as a lingua-franca in multilingual communities, there are not always ``native speakers'', in the sense that the Creole will be their mother tongue TODO:\cite{lent-etal-2022-creole}. We provide details and discussion on the validation and corrections made for each language below: 

- **Bislama:** the samples were corrected by one speaker. Overall, the speaker found that some sentences were completely correct, fluent Bislama, with minor spelling errors. Almost all sentences were understandable, but many contained specific grammatical errors or contained many spelling errors. Only a few sentences were completely wrong, and corrected accordingly, to capture the meaning of the annotated triple. The major grammatical errors involved missing prepositions, incorrect usage of articles, or incorrect verb tense. 

- **Chavacano:** the samples were corrected by one speaker, and further validated by a second. Here, the sentences in Wikipedia were determined not to be Chavacano, but rather an approximation of Spanish. As the intended meaning of the utterances was still clear, the speaker produced new utterances in Chavacano, to correctly capture the intended meaning with the tagged entities and labeled relation. 

- **Jamaican:** 
*Correction: the samples were sourced from six different speakers to reflect diverse spelling conventions.* (~~the samples were corrected by one speaker, and further validated by six others~~). The spelling and grammar of the Wikipedia sentences was found to be greatly divergent from real-world Jamaican, and thus not representative of the language. Specifically the orthography did not match what is used by Jamaican speakers, and there were a number of grammatical constructions that would not be used by native speakers. To remedy this, the speaker produced new utterances in Jamaican, to correctly capture the intended meaning with the tagged entities and labeled relation. 
  
- **Tok Pisin:** the samples were validated by two speakers, who noted that while the data is correct, it is distinctly representative of the urban variety of the language (*Tok Pisin bilong taun*), which can vary greatly from the rural variety (*Tok Pisin bilong ples*). Thus for future work, collecting and annotating samples that capture a wider spectrum of Tok Pisin will be key for expanding language technology to this language. 

After all manual corrections were made, we conduct an additional round of manual validation, to ensure that the entity tagging and relation labels were still correct. 

One common thread across all languages involved spelling, as many Creoles do not have strictly observed orthography. For example, for lesser-known named entities, there is likely to be great variation across speakers, in whether they default to English spelling, or rather attempt to represent the word according to their pronunciation. This issue highlights an area of future work, for extending Creole language datasets to capture a wider variety of voices and approaches to spelling. To this point, some speakers chose to add limitation variation across their corrections of the data. For example, in the Bislama dataset, there can be found variation in constructions combing the 3person-singular pronoun and the predicate marker *i*. 

Finally, while we did not have funds to pay the speakers for their assistance in this work, the speakers were invited to join the project as co-authors of this work, or otherwise be thanked by name in the Acknowledgements, per their preference. We believe no speakers were harmed in this process, and we are deeply grateful for their collaboration in this work. 

#### Validation through Linguistic Grammars
Full documentation of our grammar check has been submitted as supplementary material alongside this manuscript, for inspection by the reviewers. As we cite directly from published books, copyright prevents us from making our grammar check public. For Bislama we referred to *Crowley (2004)*,
for havacano we referredto *Lipski and Santoro (2007)*, and for JamaicanPatois we primarily referred to *Patrick (2014)*, but also referenced others *(Durrleman, 2008; Patrick,2004; Bailey, 1966)*. For Pitkern we referred to *Mühlhäusler (2020)*, and finally for Tok Pisin wereferred to *Eberl (2019)*. Amongst all of theselanguages, Pitkern was the only case where theWikipedia data failed to meet the description oflanguage, and was thus removed.

## References
- Terry Crowley. 2004. Bislama Reference Grammar. University of Hawaii Press
- John M. Lipski and Maurizio Santoro. 2007. Zamboangueño creole spanish. Comparative CreoleSyntax, pages 373–398.
- Peter L Patrick. 2014. Jamaican creole. Languages and Dialects in the US: Focus on Diversity and Linguistics, pages 126–136.
- Stephanie Durrleman. 2008. The syntax of jamaican creole. The Syntax of Jamaican Creole, pages 1–207
- Peter L Patrick. 2004. Jamaican creole: Morphology and syntax. A Handbook of Varieties of English, 2:407–438.
- Beryl Loftman Bailey. 1966. Jamaican Creole Syntax. Cambridge University Press.
- Peter Mühlhäusler. 2020. Pitkern-Norf’k: The Language of Pitcairn Island and Norfolk Island,volume 17. Walter de Gruyter GmbH & Co KG.
- Martin Eberl. 2019. Innovation and Grammaticalization in the Emergence of Tok  Pisin. Ph.D. Thesis, LMU
- Julia Kreutzer, Isaac Caswell, Lisa Wang, Ahsan Wahab, Daan van Esch, Nasanbayar Ulzii-Orshikh, Allahsera Tapo, Nishant Subramani, Artem Sokolov, Claytone Sikasote,Monang Setyawan, Supheakmungkol Sarin,Sokhar Samb, Benoît Sagot, Clara Rivera, Annette Rios, Isabel Papadimitriou, SalomeyOsei, Pedro Ortiz Suarez, Iroro Orife, KelechiOgueji, Andre Niyongabo Rubungo, Toan Q.Nguyen, Mathias Müller, André Müller, Shamsuddeen Hassan Muhammad, Nanda Muhammad, Ayanda Mnyakeni, Jamshidbek Mirza-khalov, Tapiwanashe Matangira, Colin Leong,Nze Lawson, Sneha Kudugunta, Yacine Jer-nite, Mathias Jenny, Orhan Firat, Bonaven
- Heather Lent, Kelechi Ogueji, Miryam de Lhoneux, Orevaoghene Ahia, and AndersSøgaard. 2022b. What a creole wants, what a creole needs. In Proceedings of the Thirteenth Language Resources and Evaluation Conference, pages 6439–6449, Marseille, France.European Language Resources Association.