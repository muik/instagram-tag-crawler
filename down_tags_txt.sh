appcfg.py update_indexes .
rm tags.txt
appcfg.py download_data --url=https://hip-place.appspot.com/_ah/remote_api \
                        --kind=TagText_Sampling \
                        --config_file=bulkloader.yaml \
                        --filename=tags.txt \
                        --batch_size=50 --num_threads=12 \
                        --log_file=/tmp/bulkloader-log
sed -i -- 's/"//g' tags.txt
sed '1d' tags.txt > tags.txt.tmp; mv tags.txt.tmp tags.txt
rm bulkloader-*.sql3
rm tags.txt--
