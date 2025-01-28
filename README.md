# Repository File Description

- **kag**: Main logic code
  - **builder**: Knowledge graph construction code. Builds knowledge graphs from various data sources such as PDFs, Markdown files, CSVs, etc.
  - **common**: General-purpose logic code, including graph data storage, evaluation functions, retrievers, vectorization functions, entity-relation extraction, etc.
  - **interface**: Backend interface code.
  - **medicine**: Project code. Multiple projects can be created here.
  - **solver**: Parser code.
- **rdata**: Traditional Chinese Medicine (TCM) entity objects and datasets. The complete UCMLS knowledge graph will be updated in future versions.
  - **dataset**
    - **CCMR**: Chinese clinical medical Reasoning, effective multi-round tracking of medical records
    - **CMSD**: Chinese medical syndrome differentiation.
    - **clinicalQa**: TCM question-answering dataset, Short dialogue for diagnosis.
  - **medicalRule**: Sample TCM rule data. *The complete version will be updated later.*
    - **termsDictionary**: TCM entity dictionary.
