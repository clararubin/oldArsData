import datetime
import time

def get_date_string():
    #example output: '2017-01-23__23-12'
    return str(datetime.date.today()) + '__' +str(time.strftime("%H-%M-%S"))

def generate_pdf_name(temp_name, index):
    #example inputs: 'psych update 2016 ARS', 1
    #example output: 'psych update 2016 ARS__2017-01-23__23-12__part1.pdf'
    pdf_title = "__".join((temp_name, get_date_string(), "part"+str(index)))
    return pdf_title + ".pdf"