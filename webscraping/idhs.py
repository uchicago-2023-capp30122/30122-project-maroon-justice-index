import sys
import json
import lxml.html

def scrape_idhs_page():
    """
    Takes the url of the Illinois Department of Human Services and returns a
    dictionary of the name, type, address, contact info (phone, TTY, website),
    and description of IDHS offices and service providers by county

    Parameters:
        * url:  a URL for the IDHS offices and service providers locator page

    Returns:
        A dictionary of office names mapped to the following keys:
            * name:         the name of the office
            * office_type:  the type of office (Early Intervention, Family Case Management, etc.)
            * address:      the address of the office
            * contact:      the phone number, TTY number, fax number, and url for the office
            * note:         the note for the office
    """

    d = {}

    with open("webscraping/idhs_page.html.aspx") as fh:
        html = fh.read()
    
    elem = lxml.html.fromstring(html_text)

    office_list = elem[1].xpath("//ol[@id='OfficeList']")[0]

    for li in office_list:
        name = li[0].text_content()
        office_type = li[1].text_content()
        address = li[2].text_content()
        phones = li[3].text_content()
        try:
            note = li[4].text_content()
        except ValueError:
            note = ""

        d[name] = {"Name": name,
                   "Type": office_type,
                   "Address": address,
                   "Contact": phones,
                   "Note": note}
    
    return d



