### Configuration
###############################################################################
# Import packages
from multiprocessing import Pool, cpu_count
import re
import time
from typing import Iterable, List


### Patterns

###############################################################################
# TO DO: make this constant, move patterns.py module. create unit test.
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


### Pattern Usage Functions
###############################################################################
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
    
    Parameters
    ----------
    text : str
        The input text.
    start_pattern : re.Pattern
        The starting regex pattern.
    end_pattern : re.Pattern
        The ending regex pattern.
    include_matches : bool
        Whether to include the matched patterns in the returned text.
        
    Returns
    -------
    list
        A list of strings containing the extracted text between the patterns.

    Example Usage
    -------------
    >>> extract_between_patterns("hello [world]!", r"\[", r"\]", include_matches=True)
    ['[world]']
    >>> extract_between_patterns("hello [world]!", r"\[", r"\]", include_matches=False)
    ['world']
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


def is_match(text : str, pattern : re.Pattern):
    """Determine whether a string in it's entirety matches a regex pattern"""
    return pattern.match(text) is not None


def count_matches(text : str, pattern : re.Pattern):
    """Count the number of regex matches in a string"""
    return sum(1 for _ in re.finditer(pattern, text))


def get_matches(text : str, pattern : re.Pattern):
    """Return regex matches in a string"""
    return re.findall(pattern, text)


def contains_match(text : str, pattern : re.Pattern):
    """Determines if a string contains at least 1 occurences of a regex pattern"""
    return re.search(pattern, text) is not None




### Pattern Creation Functions
# TO DO: consider separate module
###############################################################################
def combine_patterns_any(*patterns, case_sensitive=True, use_word_boundaries=False):
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
    >>> combined_pattern = combine_patterns_any(pattern1, pattern2)
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


def combine_patterns_all(*patterns, delimiter=None, case_sensitive=True):
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
    >>> combined_pattern = combine_patterns_all(pattern1, pattern2)
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


def whitespace() -> str:
    """
    Generate a regex pattern to match non-optional whitespace.
    
    Returns
    -------
    str
        The regex pattern to match one or more whitespace characters.
        
    Example Usage
    -------------
    >>> non_optional_whitespace()
    '\\s+'
    """
    return r"\s+"


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


### Multiprocessing Functions
# TO DO: consider separate module
###############################################################################
def contains_match_multi(texts: Iterable[str], pattern: re.Pattern, n_workers: int = None):
    """
    Determines if each string in an iterable contains at least one occurrence of a regex pattern using multiprocessing
    
    Parameters
    ----------
    texts : Iterable[str]
        The iterable of texts to search within
    pattern : re.Pattern
        The compiled regular expression pattern to search for
    n_workers : int, optional
        The number of worker processes to use. Defaults to the number of available CPU cores.
    
    Example Usage
    -------------
    >>> pattern = re.compile(r'\d+')
    >>> texts = ["abc 123", "def", "ghi 789"]
    >>> contains_match_multi(texts, pattern)
    [True, False, True]
    """
    if n_workers is None:
        n_workers = cpu_count()
    
    if len(texts) < n_workers:
        return [contains_match(text, pattern) for text in texts]

    with Pool(n_workers) as pool:
        results = pool.starmap(contains_match, [(text, pattern) for text in texts])
    return results





def is_match_multi(texts: Iterable[str], pattern: re.Pattern, n_workers: int = None):
    """
    Determines if each string in an iterable in it's entirety matches a regex pattern using multiprocessing
    
    Parameters
    ----------
    texts : Iterable[str]
        The iterable of texts to search within
    pattern : re.Pattern
        The compiled regular expression pattern to search for
    n_workers : int, optional
        The number of worker processes to use. Defaults to the number of available CPU cores.
    
    Example Usage
    -------------
    >>> pattern = re.compile(r'\d+')
    >>> texts = ["abc 123", "def", "ghi 789"]
    >>> is_match_multi(texts, pattern)
    [True, False, True]
    """
    if n_workers is None:
        n_workers = cpu_count()
    
    if len(texts) < n_workers:
        return [is_match(text, pattern) for text in texts]
    
    with Pool(n_workers) as pool:
        results = pool.starmap(is_match, [(text, pattern) for text in texts])
    return results


def count_matches_multi(texts: Iterable[str], pattern: re.Pattern, n_workers: int = None):
    """
    Counts the number of regex matches in each string in an iterable using multiprocessing
    
    Parameters
    ----------
    texts : Iterable[str]
        The iterable of texts to search within
    pattern : re.Pattern
        The compiled regular expression pattern to search for
    n_workers : int, optional
        The number of worker processes to use. Defaults to the number of available CPU cores.
    
    Example Usage
    -------------
    >>> pattern = re.compile(r'\d+')
    >>> texts = ["abc 123", "def 456", "ghi 789"]
    >>> count_matches_multi(texts, pattern)
    [1, 1, 1]
    """
    if n_workers is None:
        n_workers = cpu_count()
    
    if len(texts) < n_workers:
        return [count_matches(text, pattern) for text in texts]
    
    with Pool(n_workers) as pool:
        results = pool.starmap(count_matches, [(text, pattern) for text in texts])
    return results


def get_matches_multi(texts: Iterable[str], pattern: re.Pattern, n_workers: int = None):
    """
    Returns regex matches in each string in an iterable using multiprocessing
    
    Parameters
    ----------
    texts : Iterable[str]
        The iterable of texts to search within
    pattern : re.Pattern
        The compiled regular expression pattern to search for
    n_workers : int, optional
        The number of worker processes to use. Defaults to the number of available CPU cores.
    
    Example Usage
    -------------
    >>> pattern = re.compile(r'\d+')
    >>> texts = ["abc 123", "def 456", "ghi 789"]
    >>> get_matches_multi(texts, pattern)
    [['123'], ['456'], ['789']]
    """
    if n_workers is None:
        n_workers = cpu_count()
        
    if len(texts) < n_workers:
        return [get_matches(text, pattern) for text in texts]
    
    with Pool(n_workers) as pool:
        results = pool.starmap(get_matches, [(text, pattern) for text in texts])
    return results








