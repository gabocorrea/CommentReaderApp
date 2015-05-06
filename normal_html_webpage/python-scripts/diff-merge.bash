diff web-output-1.csv web-output-2.csv -DVERSION1 > temp-merge
grep -v  '^#if' temp-merge | grep -v '^#endif' > merged.csv
rm temp-merge