import datetime
import time

def get_date_string():
    """
    Gets date.

    :returns: string representing date (e.g. '2017-01-23__23-12')
    """
    return str(datetime.date.today()) + '__' +str(time.strftime("%H-%M-%S"))

def generate_pdf_name(temp_name, index):
    """
    Constructs name for output file.
    
    :param temp_name: name of event/series (e.g. 'psych update 2016')
    :param index:     section number (e.g. 1)
    :returns:         name for pdf output (e.g. 'psych update 2016 ARS__2017-01-23__23-12__part1.pdf')

    """
    pdf_title = "__".join((temp_name, get_date_string(), "part"+str(index)))
    return pdf_title + ".pdf"