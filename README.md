# Salmon Parentage Assignment Pipeline

Data location: ```/media/hbarton/Data/salmon_parentage_analysis```

Files used: ```SNPgeno_janlaine_IDs_020818.txt```, ```SNPgeno_janlaine_020818.txt```

```bash
ln -s /media/hbarton/Data/salmon_parentage_analysis sal_parentage
```

Columns were adjusted in ID data adding extra column name to correct the header alignment - might not be in the right 
place, but shouldn't matter for this analysis: ```SNPgeno_janlaine_IDs_020818.txt -> SNPgeno_janlaine_IDs_020818_colfix.csv```

Before:

```bash
head -n 5 SNPgeno_janlaine_IDs_020818.txt 
"ID"	"fwd"	"rev"	"run"	"composite"	"age"	"year"	"sexG"	"sexP"	"W"	"L"	"offspring"	"parDam"	"parSire"	"age2"	"age3"
"1"	"Uts_+0y_2012_1"	1	8	"1st"	"1st_1_8"	"0"	2012	"M"	NA	NA	NA	NA	NA	NA	"0"	"0"
"3"	"Uts_+0y_2012_3"	3	8	"1st"	"1st_3_8"	"0"	2012	"M"	NA	NA	NA	NA	NA	NA	"0"	"0"
"4"	"Uts_+0y_2012_4"	4	8	"1st"	"1st_4_8"	"0"	2012	"F"	NA	NA	NA	NA	"Uts_11A_037"	NA	"0"	"0"
"5"	"Uts_+0y_2012_5"	5	8	"1st"	"1st_5_8"	"0"	2012	"M"	NA	NA	NA	NA	NA	NA	"0"	"0"
```

After:

```bash
head -n 5 SNPgeno_janlaine_IDs_020818_colfix.csv 
ID,fwd,unsure,rev,run,composite,age,year,sexG,sexP,W,L,offspring,parDam,parSire,age2,age3
1,Uts_+0y_2012_1,1,8,1st,1st_1_8,0,2012,M,NA,NA,NA,NA,NA,NA,0,0
3,Uts_+0y_2012_3,3,8,1st,1st_3_8,0,2012,M,NA,NA,NA,NA,NA,NA,0,0
4,Uts_+0y_2012_4,4,8,1st,1st_4_8,0,2012,F,NA,NA,NA,NA,Uts_11A_037,NA,0,0
5,Uts_+0y_2012_5,5,8,1st,1st_5_8,0,2012,M,NA,NA,NA,NA,NA,NA,0,0
```

The sequoia input files were prepared as follows:

```bash
./lifehist_prep.py
./create_geno_matrix.py > sal_parentage/sal_geno_matrix_sequoia.csv
```