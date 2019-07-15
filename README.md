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

A ```.dat``` file for colony was generated as follows:

```bash
python create_dat_file.py -geno uts_sal_allruns.filtered.csv -marks marker_summary.csv > uts_salmon.dat
python create_dat_file.py -geno uts_sal_allruns.filtered.csv -marks marker_summary.csv > uts_salmon_mediumrun.dat
```

Colony2 was run as follows:

```bash
mkdir sal_parentage/colony_out
cd sal_parentage/colony_out/
mpirun -np 7 ~/colony2/colony2p.ifort.impi2015.out IFN:/home/hbarton/salmon_parentage/uts_salmon.dat &> uts_sal_colony.log.txt &
```