from rightmoveScraper import *
import os

url = 'https://www.rightmove.co.uk/property-to-rent/find.html?minBedrooms=3&maxBedrooms=5&keywords=&sortType=2&viewType=LIST&channel=RENT&index=0&maxPrice=3000&radius=0.0&maxDaysSinceAdded=1&locationIdentifier=USERDEFINEDAREA%5E%7B%22polylines%22%3A%22yynyH%7CgXymDxeAa%7BAhC%7EBs%60B_KqaAin%40m%60A__Atf%40_QhRuQqViFsqAh%5CiCi%40qVhlAdBi%40yh%40am%40sGsO%7DLiBgo%40u%5Ba%5DtIqs%40rSal%40Sg_F%7CPe_%40%7E%5EuIjTtIhDho%40iFrW_E%7E%5B%3FfQ%3FpGkN%7Ej%40iXhCTpqA%7Eh%40dm%40tM%60%40%7EF%7Cx%40_Uhp%40hj%40tH%7EBijB_G_k%40jtC%7B%7CD_gAkkBk%60%40rGuKg%7D%40t_%40st%40%60a%40mEtYnd%40hNyw%40jlAbAlrAzaCbeAzxKcuA%7EqI%22%7D'
max_price_pp = 900

sender = os.environ.get('EMAIL_SENDER')
receivers = os.environ.get('EMAIL_RECEIVERS')
password = os.environ.get('EMAIL_PASS')

send_results(url, max_price_pp, sender, receivers, password)