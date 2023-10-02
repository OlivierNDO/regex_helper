# -*- coding: utf-8 -*-
"""
Created on Sat Sep 16 15:31:54 2023

@author: user
"""

import re


def dollar_amount_pattern():
    """
    Generate a regex pattern to match various dollar amount formats.

    Returns
    -------
    re.Pattern
        A compiled regex pattern for matching dollar amounts.

    Example Usage
    -------------
    >>> pattern = dollar_amount_pattern()
    >>> bool(pattern.match("$1,000.50"))
    True
    """
    
    # The pattern is broken down as follows:
    # (?:USD\s*)?: Matches optional "USD" with possible spaces.
    # [-(]?: Matches optional negative sign or opening parenthesis for negative amounts.
    # \$: Matches the dollar sign.
    # \d+(?:,\d{3})*: Matches numbers with commas (e.g., 1,000 or 20,000).
    # |\d*: Matches numbers without commas (e.g., 2500).
    # (\.\d{1,2})?: Matches optional decimal values (e.g., .50 or .05).
    # (?:k|m|mm|b)?: Matches optional 'k' for thousand, 'm' or 'mm' for million, 'b' for billion.
    # [)]?: Matches optional closing parenthesis for negative amounts.
    # (?:\s*USD)?: Matches optional "USD" with possible spaces after the amount.
    pattern = r"(?:USD\s*)?[-(]?\$(?:\d+(?:,\d{3})*(?:\.\d{1,2})?|\d*(?:\.\d{1,2})?)(?:k|m|mm|b)?[)]?(?:\s*USD)?"   
    return re.compile(pattern, re.IGNORECASE)



    
def phone_number_pattern():
    """
    Generate a regex pattern to match various phone number formats.

    Returns
    -------
    re.Pattern
        A compiled regex pattern for matching phone numbers.

    Example Usage
    -------------
    >>> pattern = phone_number_pattern()
    >>> bool(pattern.match("+1 (555) 555-5555"))
    True
    """
    
    # The pattern is broken down as follows:
    # ^: Matches the start of the string.
    # (?:...): Non-capturing group.
    # \+?: Matches an optional '+' at the start.
    # \d{0,4}: Matches up to 4 digits (for country code).
    # \s?: Matches an optional space.
    # \(?: Matches an optional opening parenthesis.
    # \d{1,4}: Matches 1 to 4 digits (for area code).
    # \)?: Matches an optional closing parenthesis.
    # [-.\s]?: Matches an optional hyphen, dot, or space.
    # \d{1,4}: Matches 1 to 4 digits.
    # (?:[-.\s]\d{1,4}){1,3}: Matches groups of up to 4 digits, separated by hyphens, dots, or spaces, repeated 1 to 3 times.
    # $: Matches the end of the string.
    pattern = r"(?:\+?\d{0,4}\s?)?\(?(?:\d{1,4})\)?[-.\s]?\d{1,4}(?:[-.\s]\d{1,4}){1,3}"
    return re.compile(pattern)



def email_regex_pattern(username_chars=None, domain_chars=None, tld_length=None):
    """
    Generate an email regex pattern based on provided constraints.

    Parameters
    ----------
    username_chars : str, optional
        Allowed characters in the username part of the email. 
        Default includes common special characters.
    domain_chars : str, optional
        Allowed characters in the domain part of the email. Default is a-zA-Z0-9.-.
    tld_length : int, optional
        Length of the top-level domain (like com, org). Default is 2 or more.

    Returns
    -------
    re.Pattern
        A compiled regex pattern.

    Example Usage
    -------------
    >>> pattern = email_regex_pattern()
    >>> bool(pattern.match("test.user@example.com"))
    True
    """
    
    # Default values
    if username_chars is None:
        username_chars = r"a-zA-Z0-9.!#$%&'*+-/=?^_`{|}~"
    if domain_chars is None:
        domain_chars = "a-zA-Z0-9.-"
    if tld_length is None:
        tld_length = "{2,}"
    else:
        tld_length = f"{{{tld_length}}}"

    # Using f-string to format the regex pattern without the ^ and $ anchors
    pattern = f"[{username_chars}]+@[{domain_chars}]+\\.[a-zA-Z]{tld_length}"
    compiled_pattern = re.compile(pattern, re.UNICODE)
    return compiled_pattern


def get_words_before_pattern(text : str, pattern : re.Pattern, n : int, include_match=True):
    """
    Get the N words before a regex pattern match.

    Parameters
    ----------
    text : str
        The input text.
    pattern : re.Pattern
        The regex pattern to search for.
    n : int
        The number of words to capture before the pattern.
    include_match : bool, optional
        Whether to include the matched pattern in the returned string. Default is True.

    Returns
    -------
    list[str]
        A list of strings, each containing N words before each match (and the match itself if include_match is True).

    Example Usage
    -------------
    >>> pattern = re.compile(r"fox")
    >>> get_words_before_pattern("The quick brown fox jumps over the lazy dog.", pattern, 3)
    ['The quick brown fox']
    """
    
    # Convert pattern to string if it's a compiled regex pattern
    if isinstance(pattern, re.Pattern):
        use_pattern = pattern.pattern
    else:
        use_pattern = pattern
    
    # If include_match is True, add the pattern to the capturing group.
    # Otherwise, just use a positive lookahead to ensure the pattern exists ahead.
    if include_match:
        n_words_pattern = r"\b(\S+(?:\s+\S+){0," + str(n-1) + r"}\s+" + use_pattern + r")"
    else:
        n_words_pattern = r"\b(\S+(?:\s+\S+){0," + str(n-1) + r"})(?=\s+" + use_pattern + r")"
    
    return re.findall(n_words_pattern, text)



def extract_between_patterns(text : str,
                             start_pattern : re.Pattern,
                             end_pattern : re.Pattern,
                             include_matches = False):
    """
    Extract the text between two regex patterns.
    
    :param text: The input text.
    :param start_pattern: The starting regex pattern.
    :param end_pattern: The ending regex pattern.
    :param include_matches: Whether to include the matched patterns in the returned text.
    :return: A list of strings containing the extracted text between the patterns.
    """
    
    # Convert patterns to string if they're compiled regex patterns
    if isinstance(start_pattern, re.Pattern):
        start_pattern = start_pattern.pattern
    if isinstance(end_pattern, re.Pattern):
        end_pattern = end_pattern.pattern

    # Construct the regex pattern based on the include_matches parameter
    if include_matches:
        pattern = start_pattern + r'(.*?' + end_pattern + r')'
    else:
        pattern = start_pattern + r'(.*?)' + end_pattern

    # Use re.DOTALL to make sure the . character matches newline characters as well
    matches = re.findall(pattern, text, re.DOTALL)
    return matches




def is_pattern(text : str, pattern : re.Pattern):
    """Determine whether a string in it's entirety matches a regex pattern"""
    return pattern.match(text) is not None


def count_patterns(text : str, pattern : re.Pattern):
    """Count the number of regex matches in a string"""
    return sum(1 for _ in re.finditer(pattern, text))


def get_patterns(text : str, pattern : re.Pattern):
    """Return regex matches in a string"""
    return re.findall(pattern, text)


def has_pattern(text : str, pattern : re.Pattern):
    """Determines if a string contains at least 1 occurences of a regex pattern"""
    return re.search(pattern, text) is not None


def DEPRECATED_combine_patterns_with_or(patterns : list,
                             case_sensitive = True):
    """
    Combine an arbitrary number of regex patterns to capture any one of them.
    
    Parameters
    ----------
    patterns : list
        The regex patterns to combine.
    case_sensitive : bool
        Whether or not to compile the returned regex using re.IGNORECASE.
        Default is True (which does not include re.IGNORECASE).

    Returns
    -------
    re.Pattern
        A compiled regex pattern that matches any of the provided patterns.

    Example Usage
    -------------
    >>> pattern1 = re.compile(r"fox")
    >>> pattern2 = re.compile(r"dog")
    >>> combined_pattern = combine_patterns_with_or([pattern1, pattern2])
    >>> bool(combined_pattern.match("The quick brown fox."))
    True
    """
    
    patterns_str = []
    for pattern in patterns:
        if isinstance(pattern, re.Pattern):
            patterns_str.append(pattern.pattern)
        elif isinstance(pattern, str):
            patterns_str.append(pattern)
        else:
            terr = f"All inputs to be re.Pattern or str, not {type(pattern).__name__}"
            raise TypeError(terr)
    
    combined_str = '|'.join(patterns_str)
    out_str = fr'\b(?:{combined_str})'
    if case_sensitive:
        out_pattern = re.compile(out_str)
    else:
        out_pattern = re.compile(out_str, re.IGNORECASE)
    return out_pattern




def DEPRECATED_combine_patterns_with_and(*patterns : list, delimiter=r'\s*', case_sensitive = True):
    """
    Combine an arbitrary number of regex patterns to capture all of them consecutively, separated by an optional delimiter.
    
    Parameters
    ----------
    patterns : list
        The regex patterns to combine sequentially.
    delimiter : str, optional
        The delimiter regex pattern that might appear between each regex pattern. Default is whitespace (which can include spaces, tabs, and line breaks).
    case_sensitive : bool
        Whether or not to compile the returned regex using re.IGNORECASE.
        Default is True (which does not include re.IGNORECASE).

    Returns
    -------
    re.Pattern
        A compiled regex pattern that matches all provided patterns in sequence.

    Example Usage
    -------------
    >>> pattern1 = re.compile(r"fox")
    >>> pattern2 = re.compile(r"dog")
    >>> combined_pattern = combine_patterns_with_and([pattern1, pattern2])
    >>> bool(combined_pattern.match("The quick brown fox      \n   dog."))
    True
    """
    patterns_str = []
    for p in patterns:
        if isinstance(p, re.Pattern):
            patterns_str.append(p.pattern)
        elif isinstance(p, str):
            patterns_str.append(p)
        else:
            terr = f"All inputs to be re.Pattern or str, not {type(p).__name__}"
            raise TypeError(terr)
    combined_str = delimiter.join(patterns_str)
    if case_sensitive:
        out_pattern = re.compile(combined_str)
    else:
        out_pattern = re.compile(combined_str, re.IGNORECASE)
    return out_pattern


def DEPRECATED_combine_patterns_with_or(*patterns,
                             case_sensitive = True):
    """
    Combine an arbitrary number of regex patterns to capture any one of them.
    
    Parameters
    ----------
    patterns
        The regex patterns to combine.
    case_sensitive : bool
        Whether or not to compile the returned regex using re.IGNORECASE.
        Default is True (which does not include re.IGNORECASE).

    Returns
    -------
    re.Pattern
        A compiled regex pattern that matches any of the provided patterns.

    Example Usage
    -------------
    >>> pattern1 = re.compile(r"fox")
    >>> pattern2 = re.compile(r"dog")
    >>> combined_pattern = combine_patterns_with_or([pattern1, pattern2])
    >>> bool(combined_pattern.match("The quick brown fox."))
    True
    """
    
    patterns_str = []
    for pattern in patterns:
        if isinstance(pattern, re.Pattern):
            patterns_str.append(pattern.pattern)
        elif isinstance(pattern, str):
            patterns_str.append(pattern)
        else:
            terr = f"All inputs to be re.Pattern or str, not {type(pattern).__name__}"
            raise TypeError(terr)
    
    combined_str = '|'.join(patterns_str)
    out_str = fr'\b(?:{combined_str})'
    if case_sensitive:
        out_pattern = re.compile(out_str)
    else:
        out_pattern = re.compile(out_str, re.IGNORECASE)
    return out_pattern



def combine_patterns_with_or(*patterns, case_sensitive=True, use_word_boundaries=False):
    """
    Combine an arbitrary number of regex patterns to capture any one of them.
    
    Parameters
    ----------
    *patterns : re.Pattern or str
        The regex patterns to combine.
    case_sensitive : bool, optional
        Whether or not to compile the returned regex using re.IGNORECASE.
        Default is True (which does not include re.IGNORECASE).
    use_word_boundaries : bool, optional
        Whether or not to include word boundaries in the regex pattern.
        Default is True.

    Returns
    -------
    re.Pattern
        A compiled regex pattern that matches any of the provided patterns.

    Example Usage
    -------------
    >>> pattern1 = re.compile(r"fox")
    >>> pattern2 = re.compile(r"dog")
    >>> combined_pattern = combine_patterns_with_or(pattern1, pattern2)
    >>> bool(combined_pattern.match("The quick brown fox."))
    True
    """
    patterns_str = []
    for pattern in patterns:
        if isinstance(pattern, re.Pattern):
            patterns_str.append(f'(?i:{pattern.pattern})' if not case_sensitive else pattern.pattern)
        elif isinstance(pattern, str):
            patterns_str.append(f'(?i:{pattern})' if not case_sensitive else pattern)
        else:
            terr = f"All inputs to be re.Pattern or str, not {type(pattern).__name__}"
            raise TypeError(terr)
    
    combined_str = '|'.join(patterns_str)
    if use_word_boundaries:
        out_str = fr'\b(?:{combined_str})\b'
    else:
        out_str = fr'(?:{combined_str})'
        
    if case_sensitive:
        out_pattern = re.compile(out_str)
    else:
        out_pattern = re.compile(out_str, re.IGNORECASE)
    return out_pattern






def combine_patterns_with_and(*patterns, delimiter=None, case_sensitive=True):
    """
    Combine an arbitrary number of regex patterns to capture all of them consecutively, separated by an optional delimiter.
    
    Parameters
    ----------
    *patterns : re.Pattern or str
        The regex patterns to combine sequentially.
    delimiter : str, optional
        The delimiter regex pattern that might appear between each regex pattern. Default is None (which means no delimiter).
    case_sensitive : bool, optional
        Whether or not to compile the returned regex using re.IGNORECASE.
        Default is True (which does not include re.IGNORECASE).

    Returns
    -------
    re.Pattern
        A compiled regex pattern that matches all provided patterns in sequence.

    Example Usage
    -------------
    >>> pattern1 = re.compile(r"fox")
    >>> pattern2 = re.compile(r"dog")
    >>> combined_pattern = combine_patterns_with_and(pattern1, pattern2)
    >>> bool(combined_pattern.match("The quick brown foxdog."))
    True
    """
    if delimiter is None:
        delimiter = ''
        
    patterns_str = []
    for p in patterns:
        if isinstance(p, re.Pattern):
            patterns_str.append(p.pattern)
        elif isinstance(p, str):
            patterns_str.append(p)
        else:
            terr = f"All inputs to be re.Pattern or str, not {type(p).__name__}"
            raise TypeError(terr)
            
    combined_str = delimiter.join(patterns_str)
    if case_sensitive:
        out_pattern = re.compile(combined_str)
    else:
        out_pattern = re.compile(combined_str, re.IGNORECASE)
    return out_pattern




def is_valid_pattern(pattern: str) -> bool:
    """
    Validate if a given regex pattern is syntactically correct.
    
    Parameters
    ----------
    pattern : str
        The regex pattern to validate.
        
    Returns
    -------
    bool
        True if the pattern is valid, False otherwise.
        
    Example Usage
    -------------
    >>> is_valid_pattern(r"\d{3}-\d{2}-\d{4}")
    True
    
    >>> is_valid_pattern(r"\d{3-")
    False
    """
    try:
        re.compile(pattern)
        return True
    except re.error:
        return False
    
    
def n_digits(n: int) -> str:
    """
    Generate a regex pattern to match exactly n digits.
    
    Parameters
    ----------
    n : int
        The number of digits to match.
        
    Returns
    -------
    str
        The regex pattern to match exactly n digits.
        
    Example Usage
    -------------
    >>> n_digits(3)
    '\\d{3}'
    """
    return f"\\d{{{n}}}"

def up_to_n_digits(n: int) -> str:
    """
    Generate a regex pattern to match up to n digits.
    
    Parameters
    ----------
    n : int
        The maximum number of digits to match.
        
    Returns
    -------
    str
        The regex pattern to match up to n digits.
        
    Example Usage
    -------------
    >>> up_to_n_digits(4)
    '\\d{1,4}'
    """
    return f"\\d{{1,{n}}}"


def optional_whitespace() -> str:
    """
    Generate a regex pattern to match optional whitespace.
    
    Returns
    -------
    str
        The regex pattern to match zero or more whitespace characters.
        
    Example Usage
    -------------
    >>> optional_whitespace()
    '\\s*'
    """
    return r"\s*"
    

def optional_word(word: str, use_word_boundaries: bool = False):
    """
    Create a regex pattern for an optional word.
    
    Parameters
    ----------
    word : str
        The word to make optional in the regex pattern.
    use_word_boundaries : bool, optional
        Whether or not to include word boundaries in the regex pattern.
        Default is False.

    Returns
    -------
    str
        A regex pattern string that matches the optional word.

    Example Usage
    -------------
    >>> optional_word("is")
    '(?:\\bis\\b)?'
    >>> optional_word("is", use_word_boundaries=False)
    '(?:is)?'
    """
    if use_word_boundaries:
        return fr'(?:\b{word}\b)?'
    else:
        return fr'(?:{word})?'


def make_optional(pattern):
    """
    Make a given regex pattern optional.
    
    Parameters
    ----------
    pattern : re.Pattern or str
        The regex pattern to make optional.

    Returns
    -------
    re.Pattern
        A compiled regex pattern that makes the original pattern optional.

    Example Usage
    -------------
    >>> make_optional(re.compile(r"\d{3}"))
    re.compile(r'(?:\d{3})?')
    >>> make_optional(r"\d{3}")
    re.compile(r'(?:\d{3})?')
    """
    if isinstance(pattern, re.Pattern):
        pattern_str = pattern.pattern
    elif isinstance(pattern, str):
        pattern_str = pattern
    else:
        raise TypeError(f"Input must be re.Pattern or str, not {type(pattern).__name__}")

    optional_pattern_str = fr'(?:{pattern_str})?'
    return re.compile(optional_pattern_str)



### Example Usage
#################################################################################
# Area code
area_code_pattern = combine_patterns_with_and(
    'area code',
    optional_whitespace(),
    optional_word('is'),
    optional_whitespace(),
    n_digits(3)
)
    
area_code_pattern

my_str = """
The area code 504 is New Orleans
My area code is 210
"""
    
get_patterns(my_str, area_code_pattern)


# Date
end_word_pattern = combine_patterns_with_or(
    'End Date',
    'Final Date',
    'Last Date',
    case_sensitive = False
)

is_was_will_be_pattern = combine_patterns_with_or(
    'is',
    'was',
    'will be',
    case_sensitive = False
)

optional_is_was_will_be_pattern = make_optional(is_was_will_be_pattern)


end_date_pattern = combine_patterns_with_and(
    end_word_pattern,
    optional_whitespace(),
    optional_is_was_will_be_pattern,
    optional_whitespace(),
    optional_word(':'),
    optional_whitespace(),
    n_digits(4),
    '-',
    n_digits(2),
    '-',
    n_digits(2),
    case_sensitive = False
)

print(end_date_pattern)


# re.compile('(?:(?i:End Date)|(?i:Final Date)|(?i:Last Date))\\s*(?:\\bis\\b)?\\s*(?:\\b:\\b)?\\s*\\d{4}-\\d{2}-\\d{2}', re.IGNORECASE)





my_str_list = ['tournament end date: 2023-04-12',
               'the last date is 2022-12-31',
               'my final date will be 2019-01-02',
               'my birthday is 2024-01-04']


for s in my_str_list:
    print(has_pattern(s, end_date_pattern))



# returns: re.compile(r'area code\s*\s*\s*(?:\bis\b)?\s*\s*\s*\d{3}', re.UNICODE)
    
    
    
    
    
    



pattern_digits = r'(?=\d)'
pattern_opt_space = r' ?'
pattern_opt_whitespace = r'\s*'
pattern_ssn = r'\b\d{3}-\d{2}-\d{4}\b'
pattern_phone_number = r"(?:\+?\d{0,4}\s?)?\(?(?:\d{1,4})\)?[-.\s]?\d{1,4}(?:[-.\s]\d{1,4}){1,3}"
#pattern_email = email_regex_pattern()
pattern_email = r'\b[\w.-]+@[\w.-]+\.\w+\b'
pattern_date_written = r'(?:\d{1,2}[-/th|st|nd|rd\s]*)?(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)?[a-z\s,.]*(?:\d{1,2}[-/th|st|nd|rd)\s,]*)+(?:\d{2,4})+'
pattern_date_yyyy_mm_dd_dash = '(\d{4})-(\d{1,2})-(\d{1,2})'
pattern_date_yyyy_mm_dd_slash = '(\d{4})/(\d{1,2})/(\d{1,2})'
pattern_date_mm_dd_yyyy_slash = r'(\d{1,2})/(\d{1,2})/(\d{4})'
pattern_date_mm_dd_yyyy_dash = r'(\d{1,2})-(\d{1,2})-(\d{4})'
pattern_date_dd_mm_yyyy_slash = r'(\d{1,2})/(\d{1,2})/(\d{4})'
pattern_date_dd_mm_yyyy_dash = r'(\d{1,2})-(\d{1,2})-(\d{4})'
pattern_date_dd_mmm_yyyy = r'(\d{1,2})-(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)-(\d{4})'
pattern_date_mmm_dd_yyyy = r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) (\d{1,2}), (\d{4})'

pattern_all_dates = combine_patterns_with_or([pattern_date_written,
                                              pattern_date_yyyy_mm_dd_dash,
                                              pattern_date_yyyy_mm_dd_slash,
                                              pattern_date_mm_dd_yyyy_slash,
                                              pattern_date_mm_dd_yyyy_dash,
                                              pattern_date_dd_mm_yyyy_slash,
                                              pattern_date_dd_mm_yyyy_dash,
                                              pattern_date_dd_mmm_yyyy,
                                              pattern_date_mmm_dd_yyyy])




date_string = """
Date formats:
2023-09-17 (YYYY-MM-DD)
09/17/2023 (MM/DD/YYYY)
17-09-2023 (DD-MM-YYYY)
2023/09/17 (YYYY/MM/DD)
17-Sep-2023 (DD-MMM-YYYY)
Sep 17, 2023 (MMM DD, YYYY)
1/9/2023 (Optional leading zeros in DD/MM/YYYY)


Mar 25 2023

"""



get_patterns(date_string, pattern_all_dates)






pattern_date_mm_dd_yyyy = r'(\d{1,2})/(\d{1,2})/(\d{4})'
text = 'this one 10/1/2002 and also this one 10/01/2002'
get_patterns(text, pattern_date_mm_dd_yyyy)





pii_pattern = combine_patterns_with_or([pattern_ssn, pattern_phone_number, pattern_email])




my_text = 'My ssn is 111-11-1111 and my phone number is (555) 555-5555. Oh and my email is fake_email@yahoo.com'


re.sub(pii_pattern, '__REDACTED__', my_text)




good_pattern = combine_patterns_with_or(['good', 'great', 'fantastic', 'delicious'])


meal_pattern = combine_patterns_with_or(['breakfast', 'lunch', 'dinner', 'meal'])

good_meal_pattern = combine_patterns_with_and([good_pattern, optional_whitespace, meal_pattern])



date_formats = ['(\d{4})-(\d{2})-(\d{2})', # YYYY-MM-DD
                '(\d{4})-(\d{2})-(\d{2})'




re.search('(\d{4})-(\d{2})-(\d{2})', 'the date is 2023-09-17')





import re

pattern_date_written = r'(?:\d{1,2}[-/th|st|nd|rd\s]*)?(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)?[a-z\s,.]*(?:\d{1,2}[-/th|st|nd|rd)\s,]*)+(?:\d{2,4})+'





dateEntries = "04-20-2009; 04/20/09; 4/20/09; 4/3/09; Mar 20, 2009; March 20, 2009; Mar. 20, 2009; Mar 20 2009; 20 Mar 2009; 20 March 2009; 2 Mar. 2009; 20 March, 2009; Mar 20th, 2009; Mar 21st, 2009; Mar 22nd, 2009; Feb 2009; Sep 2009; Oct 2010; 6/2008; 12/2009; 2009; 2010"
result = re.findall(regEx, dateEntries)
print(result)




txt_list = (
    'I forgot to have breakfast today, but I had a good lunch',
    'I had a fantastic meal at the restaurant.',
    'Hope you had a good dinner',
    'Chicken for dinner, cool?'    
)

for t in txt_list:
    print(get_patterns(t, good_meal_pattern))


get_patterns('Chicken for dinner, cool?', good_meal_pattern)


text = 'I had a good breakfast today'
has_pattern(text, good_meal_pattern)

get_patterns(text, good_meal_pattern)


import re

text = "I had a great dinner and it was great!"

pattern = re.compile(r'\b(?:good|great|awesome)\s*(?:breakfast|lunch|dinner|meal)', re.UNICODE | re.IGNORECASE)

matches = pattern.findall(text)

print(matches)




import re

text = "Chicken for good dinner, cool?"

pattern = re.compile(r'\bgood\s*(?:breakfast|lunch|dinner|meal)', re.UNICODE | re.IGNORECASE)

matches = pattern.findall(text)

print(matches)








import re

string = "I love Python3 and Python2"
pattern = r'Python(?=\d)'

matches = re.findall(pattern, string)

print(matches)  
# Output: ['Python', 'Python']



import re

string = "I love Python 3 and Python 2"
pattern = r'Python ?(?=\d)'

matches = re.findall(pattern, string)

print(matches)








def negative_lookahead(pattern : str, lookahead : list):
    
    if isinstance(pattern, re.Pattern):
        pattern_str = pattern.pattern
    elif isinstance(pattern, str):
        pattern_str = pattern
    else:
        terr = f"pattern argument must be re.Pattern or str, not {type(pattern).__name__}"
        raise TypeError(terr)
        
    if isinstance(lookbehind, re.Pattern):
        lookbehind_str = lookbehind.pattern
    elif isinstance(lookbehind, str):
        lookbehind_str = lookbehind
    else:
        terr = f"lookbehind argument must be re.Pattern or str, not {type(lookbehind).__name__}"
        raise TypeError(terr)
    
    new_pattern = fr'({lookbehind_str})([^ \|,]+ ){{0,{n_words-1}}}({pattern_str})'
    return re.compile(new_pattern)







import re

text = "I had a banana with my lunch. My apples ran out yesterday. It's almost time for dinner."

pattern = re.compile(r'(?:(?!(?:banana|apple)(?:\s+\w+){0,4})(?:\w+\s+){0,4})(breakfast|lunch|dinner|meal)', re.UNICODE | re.IGNORECASE)

matches = pattern.findall(text)
print(matches)

import re

text = "I had a banana with my lunch. My apples ran out yesterday. It's almost time for dinner."

pattern = re.compile(r'(?:\b(?!apple|banana))([^ \|,]+ ){0,4}(breakfast|lunch|dinner|meal)', re.UNICODE | re.IGNORECASE)

matches = pattern.findall(text)
print(matches)





def add_lookbehind(pattern : str, lookbehind : str, n_words : int, positive = True, delimiter='\s+'):
    
    if isinstance(pattern, re.Pattern):
        pattern_str = pattern.pattern
    elif isinstance(pattern, str):
        pattern_str = pattern
    else:
        terr = f"pattern argument must be re.Pattern or str, not {type(pattern).__name__}"
        raise TypeError(terr)
        
    if isinstance(lookbehind, re.Pattern):
        lookbehind_str = lookbehind.pattern
    elif isinstance(lookbehind, str):
        lookbehind_str = lookbehind
    else:
        terr = f"lookbehind argument must be re.Pattern or str, not {type(lookbehind).__name__}"
        raise TypeError(terr)
    
    new_pattern = fr'({lookbehind_str})([^ \|,]+ ){{0,{n_words-1}}}({pattern_str})'
    return re.compile(new_pattern)



def add_lookbehind(pattern : str, lookbehind : str, n_words : int, positive = True, delimiter='\s+'):
    
    if isinstance(pattern, re.Pattern):
        pattern_str = pattern.pattern
    elif isinstance(pattern, str):
        pattern_str = pattern
    else:
        terr = f"pattern argument must be re.Pattern or str, not {type(pattern).__name__}"
        raise TypeError(terr)
        
    if isinstance(lookbehind, re.Pattern):
        lookbehind_str = lookbehind.pattern
    elif isinstance(lookbehind, str):
        lookbehind_str = lookbehind
    else:
        terr = f"lookbehind argument must be re.Pattern or str, not {type(lookbehind).__name__}"
        raise TypeError(terr)
    
    new_pattern = fr'({lookbehind_str})(?! [^ \|,]+ ){{0,{n_words-1}}}({pattern_str})'
    return re.compile(new_pattern)



fruit_pattern = combine_patterns_with_or(['banana', 'apple'])
meal_pattern = combine_patterns_with_or(['breakfast', 'lunch', 'dinner', 'meal'])
fruit_before_meal_pattern = add_lookbehind(pattern = meal_pattern,
                                           lookbehind = fruit_pattern,
                                           n_words = 5)

text = "I had a banana with my lunch. My apples ran out yesterday. It's almost time for dinner."
re.findall(fruit_before_meal_pattern, text)

# expected output: "banana with my lunch"










import re

def add_lookbehind(pattern: str, lookbehind: str, n_words: int, positive=True, delimiter='\s+'):
    if isinstance(pattern, re.Pattern):
        pattern_str = pattern.pattern
    elif isinstance(pattern, str):
        pattern_str = pattern
    else:
        terr = f"pattern argument must be re.Pattern or str, not {type(pattern).__name__}"
        raise TypeError(terr)

    if isinstance(lookbehind, re.Pattern):
        lookbehind_str = lookbehind.pattern
    elif isinstance(lookbehind, str):
        lookbehind_str = lookbehind
    else:
        terr = f"lookbehind argument must be re.Pattern or str, not {type(lookbehind).__name__}"
        raise TypeError(terr)

    if positive:
        new_pattern = fr'(?<={lookbehind_str})(\s+\w+){0,{n_words-1}}\s+({pattern_str})'
    else:
        new_pattern = fr'(?<!{lookbehind_str})(\s+\w+){0,{n_words-1}}\s+({pattern_str})'
    
    return re.compile(new_pattern)

# Define combine_patterns_with_or function or import it if necessary

fruit_pattern = re.compile(r'(banana|apple)')
meal_pattern = re.compile(r'(breakfast|lunch|dinner|meal)')
fruit_before_meal_pattern = add_lookbehind(pattern=meal_pattern, lookbehind=fruit_pattern, n_words=5)

text = "I had a banana with my lunch. My apples ran out yesterday. It's almost time for dinner."
matches = re.findall(fruit_before_meal_pattern, text)

print(matches)





import re

# Define a regular expression pattern using re.compile
fruit_before_meal_pattern = re.compile(r'(?:banana|apple ((?:\w+\s+){0,4}))(?:breakfast|lunch|dinner|meal)', re.UNICODE)

# Sample text
text = 'I had a banana with my lunch'

# Use re.findall to find and extract matches
matches = re.findall(fruit_before_meal_pattern, text)

print(matches)


get_matches(text, fruit_before_meal_pattern)





n_words = 5
lookbehind = r'never'
pattern = r'worked'
use_pattern = fr'{lookbehind} ([^ \|,]+ ){{0,{n_words-1}}}{pattern}'



# Example usage:
text = "it was said that his approach never would have worked"
matches = re.findall(use_pattern, text)

print(matches)



# Use re.findall to find and extract matches
matches = re.findall(pattern, text)

# Display the matches
for match in matches:
    print(match)











import re

def add_lookbehind(pattern, lookbehind, n_characters=20, positive=True):
    """
    Add a lookbehind to an existing regex pattern based on the number of characters.
    """
    if positive:
        full_pattern = f"(?<=.{{0,{n_characters}}}{re.escape(lookbehind)})(?!{re.escape(lookbehind)}).*{pattern}"
    else:
        full_pattern = f"(?<=.{{0,{n_characters}}}{re.escape(lookbehind)})(?={re.escape(lookbehind)}).*{pattern}"

    return re.compile(full_pattern)

text = "The water is always good but always ensure water is clean."
pattern_lookbehind = add_lookbehind(r"\bwater\b", "always", n_characters=20, positive=False)
print(re.findall(pattern_lookbehind, text))





import re

# Define the regex pattern with "black" within 1 to 5 preceding words before "fox"
pattern = r"((?:\w+\s+){0,5}\bblack\b)(\s*fox)"


pattern = r'((?:\w+\s+){1,5})(black)'


def add_lookbehind(pattern : str, lookbehind : str, n_words : int, positive = True, delimiter='\s+'):
    
    new_pattern = f"((?:\w+\s+){{1,{n_words}}})({lookbehind}){delimiter}({pattern})"
    return re.compile(new_pattern)


black_fox_pattern = add_lookbehind('fox', 'black', 5)


# Sample text
text = "This is a black-haired fox."


black_fox_pattern = re.compile(r'((?:\w+\s+){1,5})(black)\s+(fox)', re.UNICODE)



black_fox_pattern = r'((?:\w+ ?){0,5})(black)\W+(fox)'

text = "This is a black-haired fox."
matches = re.findall(black_fox_pattern, text)
print(matches)



x = "NEG_IND ([^ \|,]+ ){0,3}KEYWORD"





# Display the matches
for match in matches:
    words_before = match[0].strip()  # Trim any leading/trailing spaces
    fox_in_parentheses = match[1]
    words_after = match[3].strip()   # Trim any leading/trailing spaces
    print(f"Words before: {words_before}")
    print(f"Word in parentheses: {fox_in_parentheses}")
    print(f"Words after: {words_after}")
    print("---")

























import re

def add_lookbehind(pattern, lookbehind, n_characters=20, positive=True):
    """
    Add a lookbehind to an existing regex pattern based on the number of characters.
    
    Parameters
    ----------
    pattern : re.Pattern or str
        The original regex pattern.
    lookbehind : str
        The lookbehind pattern.
    n_characters : int
        Number of characters to look back.
    positive : bool, optional
        Whether to add a positive lookbehind (True) or negative lookbehind (False).
    
    Returns
    -------
    re.Pattern
        A compiled regex pattern with the lookbehind.
    """
    if positive:
        full_pattern = f"(?<=.{{{0,{n_characters}}}}{re.escape(lookbehind)}).{pattern}"
    else:
        full_pattern = f"(?<!.{{{0,{n_characters}}}}{re.escape(lookbehind)}).{pattern}"

    return re.compile(full_pattern)

def add_lookahead(pattern, lookahead, n_characters=20, positive=True):
    """
    Add a lookahead to an existing regex pattern based on the number of characters.
    
    Parameters
    ----------
    pattern : re.Pattern or str
        The original regex pattern.
    lookahead : str
        The lookahead pattern.
    n_characters : int
        Number of characters to look forward.
    positive : bool, optional
        Whether to add a positive lookahead (True) or negative lookahead (False).
    
    Returns
    -------
    re.Pattern
        A compiled regex pattern with the lookahead.
    """
    if positive:
        full_pattern = f"{pattern}(?={re.escape(lookahead)}.{{0,{n_characters}}})"
    else:
        full_pattern = f"{pattern}(?!{re.escape(lookahead)}.{{0,{n_characters}}})"
    
    return re.compile(full_pattern)



text = "I will always choose water over soda."
pattern = add_lookbehind(r"\bwater\b", "always", n_characters=20, positive=True)
print(re.findall(pattern, text))  # Expected output: ['water']

pattern = add_lookahead(r"\bwater\b", "soda", n_characters=20, positive=True)
print(re.findall(pattern, text))  # Expected output: ['water']





def add_lookbehind(pattern, lookbehind, n_characters=20, positive=True):
    """
    Add a lookbehind to an existing regex pattern based on the number of characters.
    """
    base_pattern = f"{pattern}"
    
    # Create patterns with varying lookbehind widths
    patterns = [f"(?<=.{i}{re.escape(lookbehind)}){base_pattern}" for i in range(n_characters + 1)]
    
    if not positive:
        # For negative lookbehinds
        patterns = [f"(?<!.{i}{re.escape(lookbehind)}){base_pattern}" for i in range(n_characters + 1)]

    combined_pattern = "|".join(patterns)
    
    return re.compile(combined_pattern)



def add_lookahead(pattern, lookahead, n_characters=20, positive=True):
    """
    Add a lookahead to an existing regex pattern based on the number of characters.
    """
    if positive:
        full_pattern = f"{pattern}(?=.{{0,{n_characters}}}{re.escape(lookahead)})"
    else:
        full_pattern = f"{pattern}(?!=.{{0,{n_characters}}}{re.escape(lookahead)})"
    
    return re.compile(full_pattern)

text = "I will always choose water over soda."
pattern_lookbehind = add_lookbehind(r"\bwater\b", "always", n_characters=20, positive=True)
print(re.findall(pattern_lookbehind, text))  # Expected output: ['water']

pattern_lookahead = add_lookahead(r"\bwater\b", "soda", n_characters=20, positive=True)
print(re.findall(pattern_lookahead, text))  # Expected output: ['water']




import re

text = """
The subtotal amount is $50. However, the total amount due is $100. 
Please ensure the total is paid by the due date. Subtotal is $30 and 
the total after tax is $110. total $50.
"""

# Base pattern to match dollar amounts
amount_pattern = re.compile(r'\$\d+')

# Add a positive lookbehind to ensure the amount is preceded by the word "total" (case-insensitive)
# but not "subtotal"
modified_pattern = add_lookbehind(amount_pattern, r"(?i)\btotal\b")

# Find all matches in the text
matches = modified_pattern.findall(text)

print(matches)  # Expected output: ['$100', '$110']








# Example usage:
email_pattern = email_regex_pattern()
phone_pattern = phone_number_pattern()
phone_or_email_pattern = combine_patterns_with_or([email_pattern, phone_pattern])
phone_plus_email_pattern = combine_patterns_with_and([phone_pattern, email_pattern])


t = "My email is first_last@yahoo.com. My dog's contact info is (500) 123-4567 woof@gmail.com."

get_patterns(t, phone_or_email_pattern)
# ['first_last@yahoo.com', ' (500) 123-4567', 'woof@gmail.com']


get_patterns(t, phone_plus_email_pattern)
# [' (500) 123-4567 woof@gmail.com']




# Test
original_pattern = r"\d+"
pattern_with_lookahead = add_lookahead(original_pattern, r"\sUSD")
pattern_with_lookbehind = add_lookbehind(original_pattern, r"\$")

print(pattern_with_lookahead.findall("100 USD, 200 EUR, 300 USD"))  # Outputs: ['100', '300']
print(pattern_with_lookbehind.findall("$100, €200, £300"))          # Outputs: ['100']










get_patterns(t, phone_or_email_pattern)





x = 'first_last@yahoo.com'

y = 'something else'



is_pattern(x, email_pattern)

is_pattern(y, email_pattern)

count_patterns(t, email_pattern)



get_patterns(t, email_pattern)


has_pattern(t, email_pattern)

has_pattern(y, email_pattern)

get_words_before_pattern(t, email_pattern, 2)


extract_between_patterns(t, email_pattern, email_pattern)


import re

            

# Test
pattern1 = re.compile(r"fox")
pattern2 = re.compile(r"dog")
combined_pattern = combine_patterns_with_and([pattern1, pattern2])
print(bool(combined_pattern.search("The quick brown fox      \n   dog.")))  # Expected True






combined_str = delimiter.join([patterns_str])

TypeError: sequence item 0: expected str instance, list found




pattern1.pattern


    combined_str = delimiter.join([patterns_str])
    return re.compile(combined_str)
    
    
    
    
    # Convert patterns to string, ensuring they're escaped in case the delimiter is a special regex character.
    patterns_str = [
        pattern.pattern if isinstance(pattern, re.Pattern) else pattern 
        for pattern in patterns
    ]
    combined_pattern_str = delimiter.join(patterns_str)
    
    return re.compile(combined_pattern_str)

# Test
pattern1 = re.compile(r"fox")
pattern2 = re.compile(r"dog")
combined_pattern = combine_patterns_with_and(pattern1, pattern2)
print(bool(combined_pattern.search("The quick brown fox      \n   dog.")))  # Expected True


pattern1.pattern



