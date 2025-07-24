# Project Dataset Directory Structure

Below is the directory structure for the datasets used in the experiments, organized by domain. The structure includes various domains such as Coding, Finance, General Knowledge, Law, Mathematics, Medical, Research, and Science, with their respective sub-domains.

```plaintext
Domain/
├── Coding
│   ├── test_data-science.json 1000
│   ├── test_java.json 1357
│   └── test_python.json 1138
├── Finance
│   ├── test_accounting.json 7
│   ├── test_business-overview.json 1
│   ├── test_corporate-finance.json 166
│   ├── test_economics.json 45
│   ├── test_financial-analysis.json 901
│   └── test_sentiment-analysis.json 1000
├── General-Knowledge
│   ├── test_current.json 10
│   ├── test_general-knowledge.json 2865
│   ├── test_history.json 13
│   ├── test_nutrition.json 15
│   ├── test_science.json 6
│   ├── test_sexuality.json 10
├── Law
│   ├── test_global-justice.json 2
│   ├── test_law.json 79
│   ├── test_legal-general.json 90
│   ├── test_property-law.json 6
│   ├── test_public-relations.json 3
│   ├── test_security-studies.json 16
│   └── test_torts.json 12
├── Mathematics
│   ├── ref.json
│   ├── sample_test.json
│   ├── test_algebra.json 311
│   ├── test_arithmetic.json 1065
│   ├── test_calculus.json 40
│   ├── test_combinatorial-probability.json 35
│   ├── test_combinatorics.json 12
│   ├── test_complex-numbers.json 1
│   ├── test_differential-equations.json 24
│   ├── test_elementary-maths.json 36
│   ├── test_geometry.json 46
│   ├── test_logarithms.json 2
│   ├── test_logical-reasoning.json 8
│   ├── test_number-theory.json 46
│   ├── test_probability.json 8
│   ├── test_statistics.json 8
│   └── test_wp.json 150
├── Medical
│   ├── test_anaesthesia.json 9
│   ├── test_anatomy.json 43
│   ├── test_biology.json 238
│   ├── test_cell-biology.json 3
│   ├── test_clinical-diagnosis.json 214
│   ├── test_clinical-medicine.json 88
│   ├── test_dental.json 311
│   ├── test_heptalogy.json 1
│   ├── test_medical-general.json 1107
│   ├── test_microbiology.json 49
│   ├── test_nephrology.json 1
│   ├── test_neurology.json 31
│   ├── test_obstetrics.json 62
│   ├── test_oncology.json 3
│   ├── test_orthopedics.json 7
│   ├── test_orthopedic-surgery.json 3
│   ├── test_pathophysiology.json 29
│   ├── test_pediatrics.json 1
│   ├── test_pharmacology.json 271
│   ├── test_physiology.json 54
│   ├── test_social-physcology.json 4
│   └── test_surgery.json 94
├── Research
│   ├── test_dataanalysis.json 9
│   ├── test_ethics.json 6
│   ├── test_experimental.json 6
│   ├── test_literature.json 6
│   ├── test_machine-learning.json 8
│   ├── test_neural-networks.json 2
│   └── test_statistical.json 6
└── Science
    ├── test_astrophysics.json 40
    ├── test_classical-mechanics.json 30
    ├── test_condensed-matter-physics.json 103
    ├── test_electrical-engineering.json 6
    ├── test_electromagnetism.json 1
    ├── test_electrostatistics.json 30
    ├── test_general-chemistry.json 486
    ├── test_general-physics.json 247
    ├── test_general-science.json 659
    ├── test_genetics.json 16
    ├── test_mechanics.json 15
    ├── test_medicinal-chemistry.json 182
    ├── test_molecular-biology.json 62
    ├── test_nuclear-physics.json 1
    ├── test_organic-chemistry.json 200
    ├── test_organic-synthesis.json 106
    ├── test_physical-chemistry.json 13
    ├── test_protein-biochemistry.json 9
    ├── test_quantum-chemistry.json 13
    ├── test_quantum-mechanics.json 78
    ├── test_relativistic-mechanics.json 9
    ├── test_statistical-mechanics.json 4
    └── test_thermodynamics.json 50
```

### Summary:

This collection of JSON files is designed for testing and experimentation across multiple domains. Each file contains structured data tailored to its specific topic, enabling focused research and analysis. The datasets span several key areas:

- **Mathematics**: Includes problems in algebra, arithmetic, calculus, combinatorics, probability, statistics, and more.

- **Coding**: Covers programming challenges in Python, Java, and data science, including datasets like HumanEval, MBPP, CodeXGLUE, and DS-1000, with up to 500 examples per dataset (or 800 for specialized tasks to ensure sufficient coverage).

- **Science**: Encompasses topics such as astrophysics, chemistry, physics, and biology.

- **Medicine**: Includes medical fields like anatomy, clinical diagnosis, pharmacology, and surgery.

- **Finance**: Covers accounting, corporate finance, economics, and financial analysis.

- **Law**: Addresses legal topics including global justice, property law, and security studies.

- **General Knowledge**: Features a wide range of subjects from history to current events.

- **Research**: Focuses on data analysis, ethics, experimental design, and machine learning.

This directory structure offers a well-organized, domain-based framework for evaluating language models across diverse tasks. Each domain and sub-domain contains targeted JSON test files, enabling focused and comprehensive assessment of model performance in specialized areas. The standardized, hierarchical organization ensures easy navigation, efficient experimentation, and supports robust benchmarking for advancing natural language processing research.

