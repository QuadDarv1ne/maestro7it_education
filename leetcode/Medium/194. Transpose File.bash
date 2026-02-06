# Read from the file file.txt and print its transposed content to stdout.
num=$(awk 'END{print NF}' file.txt)
for i in $(seq 1 $num); do
    cut -d ' ' -f $i file.txt | xargs
done