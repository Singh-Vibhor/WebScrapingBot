import requests
from bs4 import BeautifulSoup as bs

BASE_URL = {
    'GOOGLE' : "https://www.google.com/search?q={}",
    'GITHUB' : "https://github.com/{}?tab=repositories",
    'YOUTUBE' : "https://www.youtube.com/results?search_query={}"
}

def scrapeGithub(searchText):
    """ Scrapes github for given searchText """
    soup = getRequestContentsParsed(BASE_URL['GITHUB'].format(searchText))
    # Scrape profile image
    profile_image = soup.find('img', {'alt' : 'Avatar'})['src']
    print("Profile Image Link : {}".format(profile_image))

    # Enlist all repository links
    allRepoLinks = soup.find_all('a', {'itemprop': 'name codeRepository'})
    print("-" * 80)

    base_url = "https://github.com/{}"

    soup1=soup

    while( soup1.find('a', {'class': 'next_page'}) ):
        newLink = base_url.format(soup1.find('a', {'class': 'next_page'})['href'])
        soup1 = getRequestContentsParsed(newLink)
        allRepoLinks.extend(soup1.find_all('a', {'itemprop': 'name codeRepository'}))
    

    for link in allRepoLinks:
        print("{:<40s} : {}".format(
            link.get_text().strip(), base_url.format( link['href'] )
        ))

    print("-" * 80)
    print("Total number for repositories : %s\n"%len(allRepoLinks))

def scrapeGoogle(searchText):
    """ Scrapes url for the searchText provided """
    soup = getRequestContentsParsed(BASE_URL['GOOGLE'].format(searchText))
    all_links = soup.find_all('a')

    print("-"*40)
    print("Showing search results for %s"%searchText)
    for link in all_links:
        href = link['href']
        if '/url?q=' in href:
            print("{:<30} : {}\n".format(link.get_text().strip(), href.replace('/url?q=', '')))

    print("-"*40)
    print("\nTotal Number of results : %s\n"%len(all_links))

def scrapeYoutube(searchText):
    soup = getRequestContentsParsed(BASE_URL['YOUTUBE'].format(searchText.replace(" ","+")))
    all_links = soup.find_all('a')

    base_url = 'https://www.youtube.com{}'
    #print(all_links)

    for link in all_links:
        print("{:<40s} : {}".format(
            link.get_text().strip(), base_url.format( link['href'] )
        ))

    

def getRequestContentsParsed(url):
    """ Makes a get request to the url provided """
    r = requests.get(url)
    return bs(r.content, 'html.parser')

def menu():
    """ Diplays menu """
    print("1. Search Google")
    print("2. Search Github")
    print("3. Youtube Search"   )
    print("0. Exit")
    print("-"*50)
    try:
        choice = int(input("Please enter choice : ").strip())
        # print(choice, type(choice))
        if choice in (int(1), int(2), int(3)):
            searchText = input("\nEnter text to be searched : ").strip()
            if choice == int(1):
                scrapeGoogle(searchText)
            elif choice == int(2):
                scrapeGithub(searchText)
            elif choice == int(3):
                scrapeYoutube(searchText)
        elif choice == int(0):
            print("Exiting%s \n*Exited*\n"%("."*30))
            return False
        else:
            print("Please enter a valid choice!")
            print("-"*50)
        return True
    except Exception as e:
        print("Failed with error : %s"%e)
        print("Please Enter a valid choice!")
        print("-"*50)
        return True

flag = True
while flag: 
    flag = menu()
