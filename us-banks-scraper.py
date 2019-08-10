from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv
import time
import random

baseUrl="https://www.usbanklocations.com"

# with open('stageOne.csv', mode="w") as outputFile:
#     header = ["Bank Name", "Headquarters", "Asset Size", "Income", "Link"]
#     writer = csv.writer(outputFile, delimiter=",", quotechar='"')
#     writer.writerow(header)
#     with urlopen("https://www.usbanklocations.com/bank-rank/total-assets.html") as content:

#         soup = BeautifulSoup(content, "html.parser" )

#         links = []
        
#         for entry in soup.find_all("tr"):
#             bankName = ""
#             assetStr = entry.contents[1].text
#             link = ""
#             if (len(assetStr) is 12 and 'ota' not in assetStr):
#                 assetNum = assetStr[1:4]
#                 if (int(assetNum) > 99 and int(assetNum) < 499):
#                     try:
#                         link = baseUrl + entry.contents[2].contents[0]['href']
#                         bankName = entry.contents[2].contents[0].text
#                         links.append(link)
#                         writer.writerow([bankName, "", assetStr, "", link])
#                     except:
#                         print(entry.contents[2].contents[0])

def randTime():
    return (random.randrange(1000)*(0.001))

with open('stageTwo.csv', mode="w") as outputFile:
    header = ["Bank Name", "Headquarters", "Asset Size", "Income", "Link"]
    writer = csv.writer(outputFile, delimiter=",", quotechar='"')
    writer.writerow(header)
    with open('stageOne.csv') as inputFile:
        reader = csv.reader(inputFile, delimiter=",", quotechar='"')
        countBeforeWeGetBlocked = 0
        for row in reader:
            print("ANOTHER SCRAPE")
            time.sleep(1 + randTime())
            bankName = row[0]
            tempUrl = row[4]
            print("\t" + tempUrl)
            with urlopen(tempUrl) as content:
                soup = BeautifulSoup(content, "html.parser")
                # print("\t" + str(len(soup.select(".panelhead table tr td a"))))
                howManyWithTheSameName = 1
                for candidate in soup.select(".panelhead table tr td a"):
                    # print(candidate['href'])
                    if ("More Information..." in str(candidate.text)):
                        link = baseUrl + candidate['href']
                        if (howManyWithTheSameName is 1):
                            writer.writerow([bankName, "", "", "", link])
                        else:
                            writer.writerow([bankName + " " + str(howManyWithTheSameName), "", "", "", link])
                        howManyWithTheSameName = howManyWithTheSameName + 1
                countBeforeWeGetBlocked = countBeforeWeGetBlocked + 1

# tempUrl = "https://www.usbanklocations.com/first-commerce-bank-locations.htm"
# candidateUrls = []