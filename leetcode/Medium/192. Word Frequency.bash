# Read from the file words.txt and output the word frequency list to stdout.
#!/bin/bash
# Read the file, replace spaces with newlines, sort, count unique words, 
# then sort by count (descending) and word (descending for ties)

cat words.txt | tr -s ' ' '\n' | sort | uniq -c | sort -rn | awk '{print $2, $1}'