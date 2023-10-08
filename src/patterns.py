### Configuration
###############################################################################
# Import packages
import re


### Patterns
###############################################################################
phone_number = re.compile(r'^(?=(?:[^\d]*\d){7,})(?:\+?\d{1,4}\s?)?(?:\((\d{1,4})\)|\d{1,4})[-.\s]?(\d{1,4}(?:[-.\s]\d{1,4}){0,2}|\d{7,10})$')
dollar_amount = re.compile(r'(?:(?:USD\s*)?[-(]?\$(?:\d+(?:,\d{3})*(?:\.\d{1,2})?|\d+\.\d{1,2})(?:\s?[kKmMbBtT]| million| billion| trillion)?[)]?)|(?:\d+(?:,\d{3})*(?:\.\d{1,2})?(?:\s?[kKmMbBtT]| million| billion| trillion)?\s*(USD|dollars))$', re.IGNORECASE)

