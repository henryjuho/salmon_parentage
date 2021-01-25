# Salmon Parentage Assignment Pipeline

Data file: UtsSNPMasterDataKM_20.09.09.csv

## Data prep

Linked loci were identified:

```shell script
Rscript id_linked_markers.R UtsSNPMasterDataKM_20.09.09.csv
```

Output:
```
                  Locus1             Locus2         r
30276           AKAP11_4 c25_684F_713R_SACa 0.6717277
30451           AKAP11_4 c25_684F_713R_SACb 0.6717277
352        UtagF_SS_147a      UtagF_SS_148c 0.8592247
702        UtagF_SS_147a       c25_1441_SAC 0.6866607
703        UtagF_SS_148c       c25_1441_SAC 0.8377466
25413              X21_1             TN_301 0.6286910
30624 c25_684F_713R_SACa c25_684F_713R_SACb 0.9997091
```

Second column markers flagged for removal

```shell script
printf 'c25_684F_713R_SACa\nc25_684F_713R_SACb\nUtagF_SS_148c\nc25_1441_SAC\nTN_301\n' > linked_markers_toremove.txt
```

The data was then prepared with:

```bash
python snp_data_prep.py
python lifehist_prep.py
```

The data from Kenyon was preprocessed to remove loci with more than 40% 'NA's, and those identified above, 
list of removed loci: [removed_loci.csv](removed_loci.csv). Individuals with more than
50% missing genotypes were also removed: [removed_indivs.csv](removed_indivs.csv). A list of all samples processed: 
[all_samples_process.txt](all_samples_process.txt). The cleaned data was written to: 
[uts_sal_allruns.filtered.csv](uts_sal_allruns.filtered.csv).

<!---
The male controls were used to estimate a per locus error rate: [marker_summary.csv](marker_summary.csv). The cleaned data was written to: 
[uts_sal_allruns.filtered.csv](uts_sal_allruns.filtered.csv).
--->

Failed samples were summarised:

```bash
python sample_success_summary.py > sample_success_data.csv
Rscript sample_success_heatmap.R 
```
<img src="sample_heatmap.png" width=500 height=600>


## Generating main input file and running sequoia

```bash
python recode_geno_rm_sdy.py -geno uts_sal_allruns.filtered.csv > uts_sal_allruns.filtered.nosdy.recode.csv
```