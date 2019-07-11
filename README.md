# Salmon Parentage Assignment Pipeline

Data location: ```/home/DATA/salmon_parentage_analysis```

Files used: ``` GenoScoreNUM_Annukka_set3_NextSeq-20190619.txt```, ```GenoScoreNUM_NextSeq-20190416.txt```

```bash
ln -s /home/DATA/salmon_parentage_analysis sal_parentage
```

The data was prepared with:

```bash
python snp_data_prep.py
```

The raw data from Kenyon was preprocessed to extract UTS samples and male controls. Loci with more than 40% 'NA's were 
removed, along with the SDY locus, list of removed loci: [removed_loci.csv](removed_loci.csv). Individuals with more than
60% missing genotypes were also removed: [removed_indivs.csv](removed_indivs.csv). The male controls were used to estimate
a per locus error rate: [marker_summary.csv](marker_summary.csv). The cleaned data was written to: 
[uts_sal_allruns.filtered.csv](uts_sal_allruns.filtered.csv).