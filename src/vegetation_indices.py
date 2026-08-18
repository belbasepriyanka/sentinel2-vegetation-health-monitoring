def normalized_difference(a,b,eps=1e-12):
    return (a-b)/(a+b+eps)

def ndvi(nir,red): return normalized_difference(nir,red)
def ndre(nir,red_edge): return normalized_difference(nir,red_edge)
def gndvi(nir,green): return normalized_difference(nir,green)
def ndmi(nir,swir1): return normalized_difference(nir,swir1)
