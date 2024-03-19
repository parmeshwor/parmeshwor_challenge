'''


## Requirements

- **Must** transform the schema-less input `JSON file` to the desired output following the transformation criteria.
- **Must** print the output to `stdout`.

### Input

<details>
  <summary>Toggle</summary>

```json
{
  "number_1": {
    "N": "1.50"
  },
  "string_1": {
    "S": "784498 "
  },
  "string_2": {
    "S": "2014-07-16T20:55:46Z"
  },
  "map_1": {
    "M": {
      "bool_1": {
        "BOOL": "truthy"
      },
      "null_1": {
        "NULL ": "true"
      },

      "list_1": {
        "L": [
          {
            "S": ""
          },
          {
            "N": "011"
          },
          {
            "N": "5215s"
          },
          {
            "BOOL": "f"
          },
          {
            "NULL": "0"
          }
        ]
      }
    }
  },
  "list_2": {
    "L": "


    "
  },
  "list_3": {
    "L": [
      "noop"
    ]
  },
  "": {
    "S": "noop"
  }
}
```

</details>

### Output

<details>
  <summary>Toggle</summary>

```json
[
  {
    "map_1": {
      "list_1": [
        11,
        false
      ],
      "null_1": null
    },
    "number_1": 1.5,
    "string_1": "784498",
    "string_2": 1405544146
  }
]
```

</details>

### Transformation

- All `Nth` level values in the input are represented as `Strings` with pertinent data type information.
    - In the example [above](#input), `number_1` will be the field `key`, `"1.50"` would be the associated `value`,
      and **N** denotes the value's data type.
    - Other fields with different data types follow a similar pattern.
        - The `Input` has no schema restrictions other than this.
- Implementation should consider the following conventions for transformation.

#### JSON Field Keys

- **Must** sanitize the keys of trailing and leading whitespace before processing.
- **Must** represent keys with `String` data type.
- **Must** omit fields with empty keys.
- **Must** omit all invalid fields.

##### Data Types

- **S** represents the `String` data type.
    - It stores a `String` value.
    - **Transformation criteria**.
        - **Must** transform value to the `String` data type.
        - **Must** sanitize the value of trailing and leading whitespace before processing.
        - **Must** transform `RFC3339` formatted `Strings` to `Unix Epoch` in `Numeric` data type.
        - **Must** omit fields with empty values.


- **N** represents the `Number` data type.
    - It stores any `Numeric` value (positive, negative, int, float, etc.).
    - **Transformation criteria**.
        - **Must** be transformed to the relevant `Numeric` data type.
        - **Must** sanitize the value of trailing and leading whitespace before processing.
        - **Must** strip the leading zeros.
        - **Must** omit fields with invalid `Numeric` values.


- **BOOL** represents the `Boolean` data type.
    - It stores a `Boolean` value.
    - **Transformation criteria**.
        - **Must** be transformed to the `Boolean` data type.
        - **Must** transform `1`, `t`, `T`, `TRUE`, `true`, or `True` to `true`.
        - **Must** transform `0`, `f`, `F`, `FALSE`, `false`, or `False` to `false`.
        - **Must** sanitize the value of trailing and leading whitespace before processing.
        - **Must** omit fields with invalid `Boolean` values.


- **NULL** represents the `Null` data type.
    - It denotes if a value is supposed to be `Null` using a `Boolean` data type.
    - **Transformation criteria**.
        - **Must** represent a `null` literal when the value is `1`, `t`, `T`, `TRUE`, `true`, or `True`.
        - **Must** omit the field when the value is `0`, `f`, `F`, `FALSE`, `false`, or `False`.
        - **Must** sanitize the value of trailing and leading whitespace before processing.
        - **Must** omit fields with invalid `Boolean` values.


- **L** represents the `List` data type.
    - It stores a `List` of heterogeneous data types except for the `Null`, `List`, or `Map` data types.
    - **Transformation criteria**.
        - **Must** be transformed into the apt data types.
        - **Must** not contain empty `Strings`.
        - **Must** maintain the input order.
        - **Must** omit fields with unsupported data types.
        - **Must** omit fields with empty `List`.
        - The `List` can contain duplicates.


- **M** represents the `Map` data type.
    - It stores the unordered collection of heterogeneous data types including the `Map` data type.
    - **Transformation criteria**.
        - **Must** adhere to all the data type criteria defined in this document.
        - **Must** be lexically sorted.
        - **Must** omit fields with empty `Map`.

### Submission

- **Must** select a language available on [Replit](https://replit.com/templates).
- **Must** select a random name for the repo using the [generator](https://mrsharpoblunto.github.io/foswig.js).
- **Must** host the solution on `GitHub` and import it in `Replit` with the apt language/template.
- **Must** not contain any reference or content from this **confidential** document except the [Input](#input), in part
  or entirety.
- **Must** contain a `README.md` file with `local` execution instructions and `Replit` import/setup and execution
  instructions.
    - A sample [README.md](submission/README.md) is provided in the submission dir.
- **Must** report the implementation processing time.
- **Must** provide the `GitHub` repo link post completion.
- **Must** be prepared for live coding on `Replit` with an invitation link.
- Usage of third-party libraries is highly discouraged.
- Please feel free to submit a **partial solution** with apt justifications.
    - A solution with only the missing data type transformations will be deemed a **partial solution**.
        - E.g., you can skip the `List` or `Map` data type transformations with a justification of being complex to implement.



'''

import json
from pprint import pprint
import re


def process_object(obj):
    if type(obj) is not dict and len(obj) != 1:
        return False
    keys = list(obj.keys())
    valid_keys = ['S', 'N', 'BOOL', 'NULL', 'L', 'M']
    if keys[0].strip() not in valid_keys:
        return False
    if keys[0] == 'S':
        value = obj['S']
        if type(value) is not str:
            return False
        value = value.strip()
        if value == '':
            return False

        # if the string is date in RFC3339 format the string should be converted to unix epoch time
        # next the string must be checked for RFC3339 date time format

        def is_rfc3339_datetime(value):
            pattern = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$'
            return bool(re.match(pattern, value))

        if is_rfc3339_datetime(value):
            # convert to unix epoch time
            from datetime import datetime
            from dateutil import parser
            dt = parser.parse(value)
            value = int(dt.timestamp())
        else:
            pass

        return value
    if keys[0] == 'N':
        value = obj['N']
        if type(value) is not str:
            return False
        value = value.strip()  # remove leading and trailing spaces
        if value == '':
            return False
        # if value[0] == '0' and len(value) > 1:
        #     pass
        # else:
        #     return False
        try:
            value = int(value)
        except:
            try:
                value = float(value)
            except:
                return False
        return value
    if keys[0] == 'BOOL':
        value = obj['BOOL']
        if type(value) is not str:  # check if value is string
            return False
        value = value.strip()  # remove leading and trailing spaces
        if value == '':  # check if value is empty
            return False
        if value in ['1', 't', 'T', 'TRUE', 'true', 'True']:
            return True
        if value in ['0', 'f', 'F', 'FALSE', 'false', 'False']:
            return "false"
        return False
    if keys[0] in ['NULL', 'NULL ']:
        value = obj[keys[0]]
        print("processing null key and value : ", value)
        if type(value) is not str:  # check if value is string
            return False
        value = value.strip()  # remove leading and trailing spaces
        if value == '':  # check if value is empty
            return False
        if value in ['1', 't', 'T', 'TRUE', 'true', 'True']:  # check if value is true
            print("returning a None")
            return "Null"
        return False
    if keys[0] == 'L':
        value = obj['L']  # get list
        if type(value) is not list:  # check if value is list
            print("not a list")
            return False
        if len(value) == 0:  # check if list is empty
            print("empty list")
            return False
        new_list = []  # create new list
        for item in value:
            print("Processing list item : ", item)
            if type(item) is not dict:  # check if item is object
                print("not an object")
                continue
            item = process_object(item)  # process item
            print("Processed item : ", item)
            if item is not None and item is False:  # check if item is valid
                print("invalid item")
                continue
            if item is 'false':
                item = False
            if item is 'Null':
                item = None

            new_list.append(item)  # add item to new list
        if len(new_list) == 0:  # check if new list is empty
            print("empty new list")
            return False
        return new_list
    if keys[0] == 'M':
        print("Processing map")
        value = obj['M']  # get map
        if type(value) is not dict:  # check if value is object
            print("not a dictionary")
            return False
        new_map = {}  # create new map
        for k, v in value.items():
            # process the key
            if type(k) is not str:  # check if key is string
                print("not a string")
                continue
            k = k.strip()  # remove leading and trailing spaces
            if k == '':  # check if key is empty
                print("empty key")
                continue

            print("Processing key : ", k, " value : ", v)
            if type(v) is not dict:  # check if value is object
                continue
            v = process_object(v)  # process value
            print("Processed value : ", v)
            if v is not None and v is False:  # check if value is valid
                continue
            if v is 'false':  # check if value is false
                v = False
            if v is 'Null':
                v = None

            new_map[k] = v  # add value to new map
            print("Processed map level2 : ", new_map)
        print("Processed map  level1: ", new_map)
        return new_map
    return False


def process_json(json):
    if type(json) is not dict:
        print("not a dictionary", json)
        return False
    new_json = {}
    for k, v in json.items():
        # check for key validity and sanitize key
        if type(k) is not str:
            print("not a string", k)
            continue
        k = k.strip()  # remove leading and trailing spaces
        if k == '':
            print("empty key")
            continue
        # process value

        print("Processing key : ", k, " value : ", v)
        if type(v) is not dict:
            print("not a dictionary", v)
            continue
        v = process_object(v)
        print("Processed value : ", v)
        if v is not None and v is False:
            print("invalid value", v)
            continue

        if v is 'false':
            v = False
        if v is 'Null':
            v = None

        new_json[k] = v
        print("Processed json level2 : ", new_json)

    return new_json


def parse_json_file(path):
    with open(path, "r") as file:
        data = json.load(file)
        return data
    return False


if __name__ == '__main__':
    json_path = "input_file_original.json"
    result = parse_json_file(json_path)
    processed_json = process_json(result)

    print("\n Final Output \n")
    pprint(processed_json)

