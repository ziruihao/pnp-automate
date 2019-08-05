from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv

baseUrl="https://www.usbanklocations.com"

with open('output.csv', mode="w") as outputFile:
    header = ["Bank Name", "Headquarters", "Asset Size", "Income", "Link"]
    writer = csv.writer(outputFile, delimiter=",", quotechar='"')
    writer.writerow(header)
    with urlopen("https://www.usbanklocations.com/bank-rank/total-assets.html") as content:

        soup = BeautifulSoup(content, "html.parser" )

        links = []
        
        for entry in soup.find_all("tr"):
            bankName = ""
            assetStr = entry.contents[1].text
            link = ""
            if (len(assetStr) is 12 and 'ota' not in assetStr):
                assetNum = assetStr[1:4]
                if (int(assetNum) > 99 and int(assetNum) < 499):
                    try:
                        link = baseUrl + entry.contents[2].contents[0]['href']
                        bankName = entry.contents[2].contents[0].text
                        print(link)
                        links.append(link)
                        writer.writerow([bankName, "", assetStr, "", link])
                    except:
                        print(entry.contents[2].contents[0])

