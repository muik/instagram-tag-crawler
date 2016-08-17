# for login
appcfg.py update_indexes .

# remove existed file
rm tags.txt

# download data
appcfg.py download_data --url=https://hip-place.appspot.com/_ah/remote_api \
                        --kind=TagText_Sampling2 \
                        --config_file=bulkloader.yaml \
                        --filename=tags.txt \
                        --batch_size=50 --num_threads=12 \
                        --log_file=/tmp/bulkloader-log
# remove logs
rm bulkloader-*.sql3

# remove useless characters
sed -i '' 's/"//g' tags.txt
sed -i '' '1d' tags.txt

# remove duplicated media
sort tags.txt | uniq > tags.tmp; mv tags.tmp tags.txt
sed -i '' 's/^[^ ]* //' tags.txt

# remove duplicated user tags
sort tags.txt | uniq > tags.tmp; mv tags.tmp tags.txt
sed -i '' 's/^[0-9]* //' tags.txt
