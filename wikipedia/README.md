# Relation Extraction

## Generated Datasets:
`wikipedia/data/relation_extraction/final-01-09-2023`


## List of Properties in the Generated Datasets:
ID: _LABEL_, Description
* __P106__ : _occupation_, occupation of a person; see also "field of work" (Property:P101), "position held" (Property:P39)	
* __P131__ : _located in the administrative territorial entity_ , the item is located on the territory of the following administrative entity. Use P276 (location) for specifying locations that are non-administrative places and for items about events	
* __P17__ : _country_,	sovereign state of this item; don't use on humans
* __P30__ : _continent_, continent of which the subject is a part
* __P31__ : _instance of_,	that class of which this subject is a particular example and member
* __P36__ : _capital_,	primary city of a country, province, state or other type of administrative territorial entity
* __P37__ : _official language_, language designated as official by this item
* __P39__ : _position held_, subject currently or formerly holds the object position or public office
* __P495__ : _country of origin_, 	country of origin of this item (creative work, food, phrase, product, etc.)
* __P1376__ : _capital of country_ , state, department, canton or other administrative division of which the municipality is the governmental seat
* __P2341__ : _indigenous to_,	area or ethnic group that a language, folk dance, cooking style, food or other cultural expression is found (or was originally found)
* __P2936__ : _language used_,	language widely used (spoken or written) in this place or at this event
* __P361__ : _part of_,	object of which the subject is a part (if this subject is already part of object A which is a part of object B, then please only make the subject part of object A). Inverse property of "has part" (P527, see also "has parts of the class" (P2670)).


## ZS_BERT


- selected `data/relation_extraction/selected`
- #1.output files from zs-bert `data/relation_extraction/zs-output`

- use the selected json files to run inference again. 
` python inference.py ../../data/relation_extraction/selected/tpi.json ../../data/relation_extraction/selected/properties/tpi.json ../output/01`

