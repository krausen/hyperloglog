# HyperLogLog vs Set

Check the error of redis HyperLogLog when it is used to compute the cardinality (number of elements in a set) when given a multiset (set that might contain duplicates) of ip addresses.
Also compare memory usage of HyperLogLog and a regular set in.

## Results

|  | Accuracy | Memory Usage|
| --- | ----------- |--|
| HyperLogLog | 99.89% | 14KB |
| Set | 100% | 617725KB|

## Run

```bash
pip install -r requirements.txt
./run.sh  # Will kill redis docker container and start a new one
```