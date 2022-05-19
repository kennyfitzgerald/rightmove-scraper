from rightmoveScraper import *
import os

url = 'https://www.rightmove.co.uk/property-to-rent/find.html?locationIdentifier=USERDEFINEDAREA%5E%7B%22polylines%22%3A%22yynyH%7CgXymDxeAa%7BAhC~Bs%60B_KqaAin%40m%60A__Atf%40_QhRuQqViFsqAh%5CiCi%40qVhlAdBi%40yh%40am%40sGsO%7DLiBgo%40u%5Ba%5DtIqs%40rSal%40Sg_F%7CPe_%40~%5EuIjTtIhDho%40iFrW_E~%5B%3FfQ%3FpGkN~j%40iXhCTpqA~h%40dm%40tM%60%40~F%7Cx%40_Uhp%40hj%40tH~BijB_G_k%40jtC%7B%7CD_gAkkBk%60%40rGuKg%7D%40t_%40st%40%60a%40mEtYnd%40hNyw%40jlAbAlrAzaCbeAzxKcuA~qI%22%7D&maxBedrooms=5&minBedrooms=3&maxPrice=3000&propertyTypes=&maxDaysSinceAdded=1&mustHave=&dontShow=&furnishTypes=&keywords='
max_price_pp = 900

sender = os.environ.get('EMAIL_SENDER')
receivers = os.environ.get('EMAIL_RECEIVERS')
password = os.environ.get('EMAIL_PASS')

send_results(url, max_price_pp, sender, receivers, password)