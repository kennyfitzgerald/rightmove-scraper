from numpy import rec
from rightmove_webscraper import RightmoveData
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from os.path import exists

def write_urls(df):

    urls = list(df['url'])

    textfile = open("seen_urls.txt", "w")
    for element in urls:
        textfile.write(element + "\n")
    textfile.close()

def read_urls():

    if exists("seen_urls.txt"):
        textfile = open("seen_urls.txt", "r")
        urls = textfile.read()
        urls_list = urls.split('\n')
        textfile.close()
        return urls_list

    else:
        return list()

def get_rightmove_data(url, max_price_pp):

    seen_urls = read_urls()
    rm = RightmoveData(url)
    results = rm.get_results
    results['price_pp'] = round(results['price']/results['number_bedrooms'])
    results = results.query(f'(price_pp <= {max_price_pp}) & ~(url in {seen_urls})')
    write_urls(results)

    return results

def build_html(df):

    results = []

    for row in range(0, len(df)):
        link = f"<p><a href=\"{df.iloc[row]['url']}\">{df.iloc[row]['number_bedrooms']} Bed, {round(df.iloc[row]['price_pp'])} PP, {df.iloc[row]['address']}</a></p>"
        results.append(link)

    return '\n'.join(results)

def send_mail(body, sender, receivers, password):

    message = MIMEMultipart()
    message['Subject'] = 'New Rightmove Search Results'
    message['From'] = sender
    message['To'] = receivers

    body_content = body
    message.attach(MIMEText(body_content, "html"))
    msg_body = message.as_string()

    server = SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(message['From'], password)
    server.sendmail(message['From'], message['To'], msg_body)
    server.quit()

def send_results(url, max_price_pp, sender, receivers, password):

    rightmove_data = get_rightmove_data(url, max_price_pp)
    if len(rightmove_data) == 0:
        return "No new results."
        pass
    output = build_html(rightmove_data)
    send_mail(output, sender, receivers, password)
    return "Mail sent successfully."
