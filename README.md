# regex_helper: A Python package for simplifying regular expression use.

## Overview
Almost everyone hates writing regular expressions. The regex_helper package is an easier-to-use wrapper around Python's built-in re module. 

The goal of the package is to break down regular expressions into more manageable pieces that can be combined in an easier way. Here's an example where you want to extract Maple Lane and Cherry Lane addresses from text:

```python
from src import regex_helper as rh

lane_or_ln = rh.combine_patterns_any(
    'lane',
    'ln',
     case_sensitive = False
)

maple_or_cherry = rh.combine_patterns_any(
    'maple',
    'cherry',
     case_sensitive = False
)


maple_or_cherry_lane_address = rh.combine_patterns_all(
    rh.up_to_n_digits(3),
    rh.whitespace(),
    maple_or_cherry,
    rh.whitespace(),
    lane_or_ln,
    case_sensitive = False
)

my_str = """
This will match: '123 MAPLE LN'
So will this -> '5 maple lane'
14 ChERrY lAnE will too
"""

rh.get_matches(my_str, maple_or_cherry_lane_address)

# Returns:
# ['123 MAPLE LN', '5 maple lane', '14 ChERrY lAnE']
```

This is significantly more verbose than the regular expression itself, but it's easier to write.

```python
re.compile(r'\d{1,3}\s+(?:(?i:maple)|(?i:cherry))\s+(?:(?i:lane)|(?i:ln))',
re.IGNORECASE|re.UNICODE)
```



## Features

### Create compiled re.Pattern objects
combine_patterns_any: Combine multiple regex patterns to capture any one of them.
combine_patterns_all: Combine multiple regex patterns to capture all of them consecutively.
is_valid_pattern: Validate if a given regex pattern is syntactically correct.
n_digits: Generate a regex pattern to match exactly N digits.
up_to_n_digits: Generate a regex pattern to match up to N digits.
optional_whitespace: Generate a regex pattern to match optional whitespace.
optional_word: Create a regex pattern for an optional word.
make_optional: Make a given regex pattern optional.


### Using patterns
get_words_before_pattern: Get N words before a regex pattern match in a string.
extract_between_patterns: Extract text between two regex patterns.
is_match: Check if a string matches a regex pattern entirely.
count_matches: Count the number of regex matches in a string.
get_matches: Return all regex matches in a string.
contains_match: Check if a string contains at least one occurrence of a regex pattern.















