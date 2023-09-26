# Relation Extraction 





## Sorokin & Gurevych 
### Introduction
Taks: to each occurrence of the target entity pair `<e_1, e_2>` in some sentence `s` one has to assign a relation type `r` from a given set `R`.

A triple `<e_1, r, e_2>` is called a _relation instance_ and a refer to the relation of the target entity pair as _target relation_.

In order to correctly identify the relation type between the movie `e_1` and the director `e_2`, it is important to separate out the `INSTANCE_OF` relation between the movie and its type `e_3`:

(1) [`e_1` __Star Wars VII__] is an American [`e_3` __space opera epic film__] directed by [`e_2` __J. J. Abrams__].


`context relations`: other relations in the sentence as a context for predicting the label of the target relation.



### Related Works
* create relation extraction datasets for a large-scale KB:
Mintz et al. 2009, Riedel et al. 2010 - distant supervision approach. However, only include target relations.


### Data Generation with Wikidata
Wikidata is a KB that encodes knowledge in a form of binary relation instances
- CAPITAL:P36 (Hawaii:Q782, Honolulu:Q18094)

It contains more than 28 million entities and 160 million relation instances.


1. use complete English Wikipedia Corpus to generate training and evalaution data.
wikipedia-> wikidata 1-1 mapping

__INPUT__ Born in `[[Honolulu|Honolulu, Hawaii]]`, Obama is a graduate of `[[Columbia University]]`.
__LINKS to Wikidata Ids__ Honolulu`|->` Q18094, `Columbia_University |-> Q49088`

2. filter out sentences that contain fewer than 3 annotated entities

3. extract named entities and noun chunks from the input sentences with the Stanford CoreNLP toolkit to identify entities that are not covered by the Wikipedia annotations. -> retrieve IDs for these entities by searching through entity labels in Wikidata.
use HeidelTime to extract dates.

4. For each pair of entities, we query Wikidata for relation types that connect them. We disgard an occurrence of an entity pair if the relation is ambiguous, i.e. multiple relation types were retrieved.

The entity pairs that have no relation in the knowledge base are stored as negative instances.


- assess the quality of the distant supervision set-up on 200 manually verified sentences from the training set:
79.5% of relations in those sentences were correctly labeled with distant supervision.







