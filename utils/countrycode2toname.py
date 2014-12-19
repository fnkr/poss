import pycountry

def countrycode2toname(countrycode2):
    try:
        return pycountry.countries.get(alpha2=countrycode2).name
    except KeyError:
        return countrycode2
