import os
import sys
from dotenv import load_dotenv
from lib.google_search_results import GoogleSearchResults
from difflib import SequenceMatcher
load_dotenv()

companyName = str(sys.argv[1])
print(companyName)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

collect = []
commonDomains = [".com ", ".ai ", ".net ", ". io", ".org "]

searchParams = {
    "engine": "google",
    "q": companyName + " crunchbase contact info",
    "google_domain": "google.com",
    "gl": "us",
    "hl": "en",
    "api_key": SERPAPI_API_KEY,
}
client = GoogleSearchResults(searchParams)
results = client.get_dict()

def verifyResult(result):
    # testing url
    if ("https://www.crunchbase.com/organization" not in result["link"]):
        return False
    return True

def getSimilarity(result):
    crunchbaseName = result["link"][40:]
    crunchbaseName.replace('-', ' ')
    similarity = SequenceMatcher(None, crunchbaseName.lower(), companyName.lower()).ratio()
    return similarity

def extractContact(result):
    final = "not found"
    p1 = result["snippet"].find("Contact Email")
    if (p1 is not -1):
        final = result["snippet"][(p1 + 14):]
        print(final)
        p2 = final.find(". ")
        final = final[:p2]
        if ("Phone Number" in final):
            final = final[:((final.find("Phone Number")))]
    return final

def sortConfidence(companyObject):
    return companyObject['confidence']

for result in results['organic_results']:
    verifyResult(result)
    if (verifyResult(result)):
        collect.append({
            "companyName": companyName,
            "companyEmail": extractContact(result),
            "confidence": getSimilarity(result),
        })

collect.sort(key = sortConfidence, reverse = True)

for entry in collect:
    print(entry["companyName"])
    print("\t" + entry["companyEmail"])
    print("\t" + str(entry["confidence"]))



