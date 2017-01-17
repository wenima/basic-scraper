from bs4 import BeautifulSoup
import requests
import sys
import re


#http://info.kingcounty.gov/health/ehs/foodsafety/inspections/Results.aspx?Output=W&Business_Name=&Business_Address=Lake%20City%20Way&Longitude=&Latitude=&City=&Zip_Code=98125&Inspection_Type=All&Inspection_Start=&Inspection_End=&Inspection_Closed_Business=A&Violation_Points=&Violation_Red_Points=&Violation_Descr=&Fuzzy_Search=N&Sort=B
Domain = 'http://info.kingcounty.gov'
Path = '/health/ehs/foodsafety/inspections/Results.aspx?Output=W&'
def get_inspection_page(
Domain, Path, Business_Name='', Business_Address='Lake%20City%20Way',
Longitude='', Latitude='', City='Seattle', Zip_Code='98125', Inspection_Type='All',
Inspection_Start='', Inspection_End='', Inspection_Closed_Business='A',
Violation_Points='', Violation_Red_Points='', Violation_Descr='',
Fuzzy_Search='N', Sort='B'):
    #find out which search params have been passed into the function
    search_params = {arg: v for arg, v in locals().items() if arg not in globals()
    #build a list containing the search params and their values
    params = ['&' + param + '=' + v for param, v in search_params.items()
    #build the url to pass into the request function and replace the && with &
    url = Domain + Path + ''.join(params)
    url_to_parse = url.replace('&&', '&', 1
    # Getting the webpage, creating a Response object, checking for HTTP errors.
    try:
        response = requests.get(url_to_parse)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
        sys.exit(1
        #writing the output to a file
        filename = 'inspection_page.html'
        with open(filename, 'wb') as f:
            f.write(response.content
    return filename

                # filename = get_inspection_page(Domain, Path)

def load_inspection_page():
    return BeautifulSoup(open('inspection_page.html'), 'lxml')

# Extracting the source code of the page.

def parse_source(argv):
    if 'test' in argv
        soup = load_inspection_page()
    else:
        r = get_inspection_page(Domain, Path)
        soup = BeautifulSoup(r, 'lxml')
        import pdb;pdb.set_trace()
    return soup.body

def extract_data_listings(html):
    id_finder = re.compile(r'PR[\d]+~')
    return html.find_all('div', id=id_finder)

def has_two_tds(elem):
    is_tr = elem.name == 'tr'
    td_children = elem.find_all('td', recursive=False)
    has_two = len(td_children) == 2
    return is_tr and has_two

def clean_data(td):
    data = td.string
    try:
        return data.strip(" \n:-")
    except AttributeError:
        return u""


def main(argv):
    body = parse_source(argv)
    listings = extract_data_listings(body)
    for listing in listings:
        metadata_rows = listing.find('tbody').find_all(
            has_two_tds, recursive=False
        )
        for row in metadata_rows:
            for td in row.find_all('td', recursive=False):
                print(repr(clean_data(td)))
            print()
        print()
        print len(metadata_rows)




if __name__ == "__main__":
    main(sys.argv)





# # Passing the source code to Beautiful Soup to create a BeautifulSoup object for it.
#
#
# # Extracting all the <a> tags into a list.
# tags = soup.find_all('a')
#
# # Extracting URLs from the attribute href in the <a> tags.
# for tag in tags:
#     print(tag.get('href'))
