import os
import csv
import json
import requests
import http.client

#gets the current working directory
cwd = os.getcwd()

#maps path to the new urls csv
new_urls_csv_path = os.path.join(cwd, "new_urls.csv")

#maps paths to both deny-lists for Palo Alto
denylist_POP_path = r"path\to\file"
denylist_COC_path = r"\pat\to\file"

#creates empty list for current Palo Alto urls
denylist_POP_content = []
denylist_COC_content = []

#creates empty list of netksope and PaloAlto urls
netskope_urls = []
paloalto_urls = []


def get_content_of_paloalto_lists():
    with open (denylist_POP_path) as f:
        pop_content = csv.reader(f)
        for row in pop_content:
            url = row [0]
            denylist_POP_content.append(url)

    with open (denylist_COC_path) as f:
        coc_content = csv.reader(f)
        for row in coc_content:
            url = row[0]
            denylist_COC_content.append(url)

#opens the new_urls csv and appends contents into the netskope urls list
#also appends the urls to the Palo Alto text files
def create_url_lists():

    global netskope_api_formatted_urls

    #opens csv file with proper encoding format
    try:
        with open("new_urls.csv", encoding="utf-8-sig") as f:
            #uses reader class to parse the data
            new_urls_csv_opened = csv.reader(f)

            #for loop to create netksope urls and append to list
            for row in new_urls_csv_opened:
                #define the first row of the csv
                url = row[0].strip() #remove the leading/trailing whitespace
                
                #append urls to netskope list
                netskope_urls.append(url)
                netskope_urls.append(f"*.{url}")

                #append urls to Palo Alto list
                paloalto_urls.append(url)


    except Exception as error:
        print (f"Error: {error}")

#takes the new_urls csv and adds all urls from it to the Palo Alto urls IF NOT already in there
def add_urls_to_palo_alto():

    #opens the deny lists for POP so we can append to it
    with open (denylist_POP_path, 'a') as f:

        f.write("\n")

        #write contents of Palo Alto list to txt file
        for url in paloalto_urls:

            if url not in denylist_POP_content:
                f.write(url + "\n")
            else:
                print (f"{url} is already in the POP Palo Alto Deny-List")

    with open (denylist_COC_path, 'a') as f:

        f.write("\n")

        #write contents of Palo Alto list to txt file
        for url in paloalto_urls:

            if url not in denylist_COC_content:
                f.write(url + "\n")
            else:
                print (f"{url} is already in the  COC Palo Alto Deny-List")

#runs API patch call to NetSkope to append URL list with new_urls
def netskope_api_patch():

    url = "https://url.goskope.com/api/v2/policy/urllist/5/append"

    headers = {
        'Content-Type': 'application/json',
        'Netskope-Api-Token': 'token123'
    }

    payload = json.dumps({
        "name": "AnthonyTestList",
        "data": {
            "urls": paloalto_urls,
            "type": "exact"
        }
    })

    #encode the payload as bytes
    payload_bytes = payload.encode('utf-8')

    conn = http.client.HTTPSConnection("sandiegocounty.goskope.com")
    conn.request("PATCH", "/api/v2/policy/urllist/5/append", payload_bytes, headers)
    response = conn.getresponse()

    print(response.read().decode('utf-8'))
    conn.close()


#run function to get the current content of the Palo Alto url deny lists
get_content_of_paloalto_lists()

#runs function to create new netskope and Palo Alto url lists
create_url_lists()

#runs function to add urls to Palo Alto deny lists
add_urls_to_palo_alto()

netskope_api_patch()
