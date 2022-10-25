# datagen
 Generate test data based on data schema


## Project description:

Imagine that you have a data pipeline and you need some test data to check correctness of data transformations and validations on this data pipeline. You need to generate different input data. Datagen is a console utility that will generate our data for us. Data schema have to be in JSON format.

Random data generation depends on field type and data schema. Described in detail in “Data Schema Parse” point.

## Data Schema Parse:

**Example of data schema:**

`{"date": "timestamp:", "name": "str:rand", "type": "int:[1, 2, 3]", "age": "int:rand(1, 90)"}`

**All values support special notation “type**:what_to_generate”:

“:” in value indicates that the left part of the value is a type.

**Type could be:** timestamp, str and int.

For example, “str:rand” means that the value of this key must be a str type and it’s generated randomly.

**For right part of values with “:” notation, possible 5 options:**

1. **rand** - random generation, if on the left there is “str” type, for generation uuid4 is used. If on the left there is “int” type, random.randint(0, 10000) is used.
2. **list with values [].** For example, ”str:[‘client’, ‘partner’, ‘government’]” or “int:[0, 9, 10, 4]”. Generator takes a random value from a list for each generated data line.
3. **rand(from, to)** - random generation for int values in the prescribed range. Possible to use only with “int” type.
4. **Stand alone value.** If in schema after “:” a value is written, which has a type corresponding with the left part, and the word “rand” is not reserved, use it on each line of generated data. For example, “name”: “str:cat”. So script generates data where in each line attr “name”:”cat” will be. But if in schema there is “age”:”int:head”, it is an error, because “head” could not be converted to int type.
5. **Empty value.** It’s normal for any type. If type “int” is with empty value, None is used in value, if type “str”, empty string - “” is used.

**Timestamp type** ignores all values after “:”. Timestamp does not support any values and it will be ignored. **Value for timestamp is always the current unix timestamp.**

## List of input params for CU:
| Name | Description |
| ----------- | ----------- |
| path | path to save files, "." for cwd |
| count | files count, ==0: print output to console |
| filename | with no suffix, full filename="filename.jsonl" |
| suffix | filename suffix when files count is more than 1, full filename="filename_suffix.jsonl |
| schema | path to json file or json string |
| lines | number of lines in each file |
| clear | whether to delete all files in path that match filename |
| multiprocessing | number of processes used to create files |

Default values of params can be changed in `default.ini` file.
