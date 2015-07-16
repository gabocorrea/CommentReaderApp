diff web-output-romain.csv web-output-gabriel.csv -DVERSION1 > temp-merge
grep -v  '^#if' temp-merge | grep -v '^#endif' > WebOutput-merged.csv
rm temp-merge