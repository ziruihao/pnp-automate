from difflib import SequenceMatcher
import csv

with open('../ventures-sourcing/output.csv', mode = 'r', ) as listOfStartupsAndDomains:
    reader = csv.reader(listOfStartupsAndDomains, delimiter=',', quotechar='"')
    for row in reader:
        startupName = str(row[0])
        startupEmail = row[1]
        if ("Not Found" not in startupEmail):
            p = startupEmail.find('@')
            startupDomainFull = startupEmail[(p + 1):]
            p2 = startupDomainFull.find('.')
            startupDomain = startupDomainFull[:p2]
            similarity = SequenceMatcher(None, startupName.lower(), startupDomain.lower()).ratio()
            if (".com" not in startupDomainFull):
                print(startupDomainFull)
                # print(startupName.lower() + " v. " + startupDomain.lower())
                # print('\t' + str(similarity))

