# Ithome Data Transfer Tools

# MongoDB tool

## Get Data
```
python3 mongo_client.py [--collection|-c] {{ MONGO_COLLECTION }} to-csv \
    [--csv-file-path|-csv] {{ FILE_PATH }} \
    [--skip-column|-s] {{ SKIP_COLUMN_NAME }}
```
Example
```
python3 mongo_client.py -c content_info to-csv \
    --csv-file-path ./tmp.csv \
    --skip-column _id \
    --skip-column text
```

## Conunt Data
```
python3 mongo_client.py [--collection|-c] {{ MONGO_COLLECTION }} count-data --contain-header
```
Example
```
python3 mongo_client.py -c user_info count-data --contain-header
>> 29
python3 mongo_client.py -c user_info count-data
>> 28
```

## Housekeeping
```
python3 mongo_client.py [--collection|-c] {{ MONGO_COLLECTION }} housekeeping
```
Example
```
python3 mongo_client.py -c user_info housekeeping
```


# Data Quality 

## content_info
```
python3 mongo_client.py -c content_info to-csv --csv-file-path ./output/content_info/content_info.csv

cd ./output/content_info
piperider run --skip-recommend 
# check if test failed

piperider run --skip-recommend  |grep "\[FAILED\]"
if [ $? -ne 0 ]; then echo "success"; else echo "failed"; fi  # piperider version 0.9.0
```

## user_info
```
python3 mongo_client.py -c user_info to-csv --csv-file-path ./output/user_info/user_info.csv

cd ./output/user_info
piperider run --skip-recommend 
# check if test failed

piperider run --skip-recommend  |grep "\[FAILED\]"
if [ $? -ne 0 ]; then echo "success"; else echo "failed"; fi  # piperider version 0.9.0
```