# Salmon Parentage Assignment Pipeline

Data location: ```/media/hbarton/Data/salmon_parentage_analysis```

```bash
ln -s /media/hbarton/Data/salmon_parentage_analysis sal_parentage
```

Columns were adjusted in ID data adding extra column name to correct the header alignment - might not be in the right 
place: ```SNPgeno_janlaine_IDs_020818.txt -> SNPgeno_janlaine_IDs_020818_colfix.csv```

Preparing the input files:

```bash
./lifehist_prep.py

```