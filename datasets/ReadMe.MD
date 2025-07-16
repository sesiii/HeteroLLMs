# Project Dataset Directory Structure

Below is the directory structure for the datasets used in the experiments, organized by domain. The structure includes various domains such as Coding, Finance, General Knowledge, Law, Mathematics, Medical, Research, and Science, with their respective sub-domains.

```plaintext
Domain/
├── Coding
│   ├── test_data-science.json
│   ├── test_java.json
│   └── test_python.json
├── Finance
│   ├── test_accounting.json
│   ├── test_business-overview.json
│   ├── test_corporate-finance.json
│   ├── test_economics.json
│   ├── test_financial-analysis.json
│   └── test_sentiment-analysis.json
├── General-Knowledge
│   ├── test_current.json
│   ├── test_general-knowledge.json
│   ├── test_history.json
│   ├── test_nutrition.json
│   ├── test_science.json
│   ├── test_sexuality.json
│   └── test_us-history.json
├── Law
│   ├── test_global-justice.json
│   ├── test_law.json
│   ├── test_legal-general.json
│   ├── test_property-law.json
│   ├── test_public-relations.json
│   ├── test_security-studies.json
│   └── test_torts.json
├── Mathematics
│   ├── ref.json
│   ├── sample_test.json
│   ├── test_algebra.json
│   ├── test_arithmetic.json
│   ├── test_calculus.json
│   ├── test_combinatorial-probability.json
│   ├── test_combinatorics.json
│   ├── test_complex-numbers.json
│   ├── test_differential-equations.json
│   ├── test_elementary-maths.json
│   ├── test_geometry.json
│   ├── test_logarithms.json
│   ├── test_logical.json
│   ├── test_number-theory.json
│   ├── test_probability.json
│   ├── test_statistics.json
│   └── test_wp.json
├── Medical
│   ├── test_anaesthesia.json
│   ├── test_anatomy.json
│   ├── test_biology.json
│   ├── test_cell-biology.json
│   ├── test_clinical-diagnosis.json
│   ├── test_clinical-medicine.json
│   ├── test_dental.json
│   ├── test_heptalogy.json
│   ├── test_medical-general.json
│   ├── test_microbiology.json
│   ├── test_nephrology.json
│   ├── test_neurology.json
│   ├── test_obstetrics.json
│   ├── test_oncology.json
│   ├── test_orthopedics.json
│   ├── test_orthopedic-surgery.json
│   ├── test_pathophysiology.json
│   ├── test_pediatrics.json
│   ├── test_pharmacology.json
│   ├── test_physiology.json
│   ├── test_social-physcology.json
│   └── test_surgery.json
├── Research
│   ├── test_dataanalysis.json
│   ├── test_ethics.json
│   ├── test_experimental.json
│   ├── test_literature.json
│   ├── test_machine-learning.json
│   ├── test_neural-networks.json
│   └── test_statistical.json
└── Science
    ├── test_astrophysics.json
    ├── test_classical-mechanics.json
    ├── test_condensed-matter-physics.json
    ├── test_electrical-engineering.json
    ├── test_electromagnetism.json
    ├── test_electrostatistics.json
    ├── test_general-chemistry.json
    ├── test_general-physics.json
    ├── test_general-science.json
    ├── test_genetics.json
    ├── test_mechanics.json
    ├── test_medicinal-chemistry.json
    ├── test_molecular-biology.json
    ├── test_nuclear-physics.json
    ├── test_organic-chemistry.json
    ├── test_organic-synthesis.json
    ├── test_physical-chemistry.json
    ├── test_protein-biochemistry.json
    ├── test_quantum-chemistry.json
    ├── test_quantum-mechanics.json
    ├── test_relativistic-mechanics.json
    ├── test_statistical-mechanics.json
    └── test_thermodynamics.json
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

