def flt2per(num):
    """Convert float number to percent"""
    return int(100*num)

def per2flt(num):
    """Convert percent to float number"""
    return float(num / 100)

def random_pair(max_value):
    from numpy.random import default_rng
    rng = default_rng()
    idx = rng.choice(max_value, 2, replace=False)
    return idx[0], idx[1]