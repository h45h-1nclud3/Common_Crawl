#!/usr/bin/python
import gzip
import sys
import requests
import json
### -----------------------
### Searches the Common Crawl Index for a domain.
### -----------------------
#Searches the Common Crawl Index for a domain.
def search_domain(domain):
    record_list = []
    index_list = ['2019-22', '2019-18', '2019-13', '2019-09', '2019-04', '2018-51', '2018-47', '2018-43', '2018-39', '2018-34', '2018-30', '2018-26', '2018-22', '2018-17', '2018-13', '2018-09', '2018-05', '2017-51', '2017-47', '2017-43', '2017-39', '2017-34', '2017-30', '2017-26', '2017-22', '2017-17', '2017-13', '2017-09', '2017-04', '2016-50', '2016-44', '2016-40', '2016-36', '2016-30', '2016-26', '2016-22', '2016-18', '2016-07', '2015-48', '2015-40', '2015-35', '2015-32', '2015-27', '2015-22', '2015-18', '2015-14', '2015-11', '2015-06', '2014-52', '2014-49', '2014-42', '2014-41', '2014-35', '2014-23', '2014-15', '2014-10', '2013-48', '2013-20', '2012', '2009-2010', '2008-2009']
    print "[*] Trying target domain: %s" % domain
    for index in index_list:
        print "[*] Trying index %s" % index
        cc_url  = "http://index.commoncrawl.org/CC-MAIN-%s-index?" % index
        cc_url += "url=%s&matchType=domain&output=json" % domain
        response = requests.get(cc_url)
        if response.status_code == 200:
            records = response.content.splitlines()
            for record in records:
                record_list.append(json.loads(record))  
            print "[*] Added %d results." % len(records)
    print "[*] Found a total of %d hits." % len(record_list)
    return record_list



def download_page(record):

    offset, length = int(record['offset']), int(record['length'])
    offset_end = offset + length - 1

    # We'll get the file via HTTPS so we don't need to worry about S3 credentials
    # Getting the file on S3 is equivalent however - you can request a Range
    prefix = 'https://commoncrawl.s3.amazonaws.com/'

    # We can then use the Range header to ask for just this set of bytes
    resp = requests.get(prefix + record['filename'], headers={'Range': 'bytes={}-{}'.format(offset, offset_end)})

    # The page is stored compressed (gzip) to save space
    # We can extract it using the GZIP library
    raw_data = StringIO.StringIO(resp.content)
    f = gzip.GzipFile(fileobj=raw_data)

    # What we have now is just the WARC response, formatted:
    data = f.read()

    response = ""

    if len(data):
        try:
            warc, header, response = data.strip().split('\r\n\r\n', 2)
        except:
            pass

    return response


record_list = search_domain(sys.argv[1])

for record in record_list:
	result = download_page(record)
	with open(record+".html", "w") as f:
		f.write(result)

