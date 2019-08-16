from urllib.request import urlopen
from bs4 import BeautifulSoup, NavigableString, Tag
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

# with open('stageTwo.csv', mode="w") as outputFile:
#     header = ["Bank Name", "Headquarters", "Asset Size", "Income", "Link"]
#     writer = csv.writer(outputFile, delimiter=",", quotechar='"')
#     writer.writerow(header)
#     with open('stageOne.csv') as inputFile:
#         reader = csv.reader(inputFile, delimiter=",", quotechar='"')
#         countBeforeWeGetBlocked = 0
#         shouldStart = False
#         for row in reader:
#             if ("irst Northern Bank of Wyomin" in row[0]):
#                 shouldStart = True
#             if (shouldStart):
#                 print(str(countBeforeWeGetBlocked) + " SCRAPE")
#                 time.sleep(0.4 + randTime())
#                 bankName = row[0]
#                 tempUrl = row[4]
#                 print("\t" + tempUrl)
#                 with urlopen(tempUrl) as content:
#                     soup = BeautifulSoup(content, "html.parser")
#                     # print("\t" + str(len(soup.select(".panelhead table tr td a"))))
#                     howManyWithTheSameName = 1
#                     for candidate in soup.select(".panelhead table tr td a"):
#                         # print(candidate['href'])
#                         if ("More Information..." in str(candidate.text)):
#                             link = baseUrl + candidate['href']
#                             if (howManyWithTheSameName is 1):
#                                 writer.writerow([bankName, "", "", "", link])
#                             else:
#                                 writer.writerow([bankName + " " + str(howManyWithTheSameName), "", "", "", link])
#                             howManyWithTheSameName = howManyWithTheSameName + 1
#                     countBeforeWeGetBlocked = countBeforeWeGetBlocked + 1
#             else:
#                 print("DON'T SCRAPE")

def scrapSingleBank(bankName, usbankUrl):
    with urlopen(usbankUrl) as content:
        soup = BeautifulSoup(content, "html.parser")
        streetAddress = soup.select_one('span[property="v:street-address"]').text
        town = soup.select_one('span[property="v:locality"]').text
        state = soup.select_one('span[property="v:region"]').text
        zip = soup.select_one('span[property="v:postal-code"]').text

        address = streetAddress + ', ' + town + ', ' + state + ' ' + zip

        website = ''
        possibleWebsites = soup.select('b')
        for candidate in possibleWebsites:
            if ("ebsite" in candidate.text):
                if (type (candidate.parent.next_sibling.contents[0]) is Tag):
                    website = candidate.parent.next_sibling.contents[0].text
                elif (type (candidate.parent.next_sibling.contents[0]) is NavigableString):
                    website = candidate.parent.next_sibling.contents[0]
                else:
                    website = "No website" + str(type (candidate.parent.next_sibling.contents[0]))

        assetSize = ''
        possibleAssetSizes = soup.select('b')
        for candidate in possibleAssetSizes:
            if ("otal Assets" in candidate.text):
                assetSize = candidate.parent.next_sibling.contents[0].text
        
        income = ''
        possibleIncomes = soup.select('b')
        for candidate in possibleIncomes:
            if ("et Income" in candidate.text and "uarterly" not in candidate.text):
                income = candidate.parent.next_sibling.contents[0].text
    return [bankName, address, assetSize, income, usbankUrl, website]


with open('stageThree.csv', mode="w") as outputFile:
    writer = csv.writer(outputFile, delimiter=",", quotechar='"')
    header = ["Bank Name", "Headquarters", "Asset Size", "Income", "USBANK Link", "Website"]
    writer.writerow(header)
    with open('stageTwo.csv', mode="r") as inputFile:
        reader = csv.reader(inputFile, delimiter=",", quotechar='"')
        isFirstRow = True
        count = 0
        for row in reader:
            count = count + 1
            if (not isFirstRow and count > 485 and count < 2222):
                print(str(count) + " " + row[0])
                time.sleep(0.4 + randTime())
                writer.writerow(scrapSingleBank(row[0], row[4]))
            else:
                print("skip" + row[0])
            isFirstRow = False

