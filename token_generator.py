#!/usr/bin/env python
# For SHA32 - token_gen(32)
# Format also can be changed - token_gen('32', 'abc123')
import random
import string


def token_gen(size=6, chars=string.ascii_uppercase + string.digits):
    """Generate uniq token"""
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(size))
