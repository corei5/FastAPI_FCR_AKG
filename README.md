# FastAPI for the FCR_AKG project

The main goal of this research is to support the Fact-checkers to find relevant facts and arguments related to the COVID-19 information. 


## Installation


### Dependencies


1. [requirements.txt]()


## How to run

Open your Linux terminal inside the APIs folder. 
1. To find the transformer-based text similarity : uvicorn Transformers:app --reload
2. To find the vectorizer-based text similarity : uvicorn Vectorizer:app --reload 

1. Example text:
2. Example Output:

## Fastapi swagger

*** add image for the example input and output ****


## Dataset: 

We utilize the Covid-on-the-Web Dataset (https://github.com/Wimmics/CovidOnTheWeb), especially the CORD-19 Argumentative Knowledge Graph (CORD19-AKG) for COVID-19 related facts and arguments.

## CORD-19 Argumentative Knowledge Graph (CORD19-AKG)

To extract argumentative components (claims and evidences) and PICO elements, They used the [Argumentative Clinical Trial Analysis](http://ns.inria.fr/acta/) platform (ACTA) [2].

Argumentative components and PICO elements were extracted from the articles' abstracts.

| | ACTA |
| ------------- | ---------: |
| No. argumentative components | 119,053 |
| No. PICO elements linked to UMLS concepts | 515,590 |
| No. unique UMLS concepts | 31,841 |

## Documentation

*** Need to update ***
- [Transformer based COVID-19 facts similarity]()
- [TF-IDF vectorizer and Count vectorizer based COVID-19 facts similarity]()

## Funding

This work is financially supported in part by the Countering Creative Information Manipulation with Explainable AI [CIMPLE] (https://www.chistera.eu/projects/cimple)  project. 

## References

[1] Franck Michel, Fabien Gandon, Valentin Ah-Kane, Anna Bobasheva, Elena Cabrio, Olivier Corby, Raphaël Gazzotti, Alain Giboin, Santiago Marro, Tobias Mayer, Mathieu Simon, Serena Villata, Marco Winckler. Covid-on-the-Web: Knowledge Graph and Services to Advance COVID-19 Research. International Semantic Web Conference (ISWC), Nov 2020, Athens, Greece. [PDF](https://hal.archives-ouvertes.fr/hal-02939363/file/article-cam-ready.pdf)
