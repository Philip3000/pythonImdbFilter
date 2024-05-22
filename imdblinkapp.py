import requests
from bs4 import BeautifulSoup
import time



def get_imdb_info():
    print(" ------------------------------------------------------")
    print("Hello and welcome to the movie/imdb application")
    print(" ")
    print("------------------------------------------------------")
    link = input("Insert link of list: ")
    print(" ")
    severity = input("And how severe can it be?: None/Mild/Moderate/Severe: ")
    print(" ")
    print("Okay, thank you. Initiating movie/tv search. This might take a while. Get a coffee or some candy while I work")
    print("------------------------------------------------------------------------------------------------------------")
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br'
        }

        cookies = {
            'COOKIE_NAME': 'COOKIE_VALUE'  # Add any necessary cookies here
        }
        time.sleep(3)
        response = requests.get(link, headers=headers, cookies=cookies)
        html_content = response.content
        soup = BeautifulSoup(html_content, 'html.parser')

        list_without_nudity = []

        tv_show_rows = soup.select_one('#__next > main > div.ipc-page-content-container.ipc-page-content-container--center.sc-a80fc520-0.kpyNQn > div.ipc-page-content-container.ipc-page-content-container--center > section > section > div > section > section > div:nth-child(2) > div > section > div.ipc-page-grid.ipc-page-grid--bias-left.ipc-page-grid__item.ipc-page-grid__item--span-2 > div.ipc-page-grid__item.ipc-page-grid__item--span-2 > ul')
        i = 0
        for row in tv_show_rows:
            title_element = row.select_one('#__next > main > div.ipc-page-content-container.ipc-page-content-container--center.sc-a80fc520-0.kpyNQn > div.ipc-page-content-container.ipc-page-content-container--center > section > section > div > section > section > div:nth-child(2) > div > section > div.ipc-page-grid.ipc-page-grid--bias-left.ipc-page-grid__item.ipc-page-grid__item--span-2 > div.ipc-page-grid__item.ipc-page-grid__item--span-2 > ul > li:nth-child(1) > div > div > div > div.sc-f24f1c5c-3.fRBzBY > div.sc-be6f1408-0.gVGktK > div.ipc-title.ipc-title--base.ipc-title--title.ipc-title-link-no-icon.ipc-title--on-textPrimary.sc-be6f1408-9.srahg.dli-title > a')
            title = title_element.text.strip()
            show_url = title_element['href']
            print(f"Proccessing movie no. :{i} with Title: {title}")
            show_url_now = show_url.split('?')[0]
            i += 1
            parents_guide_link = f"https://www.imdb.com{show_url_now}parentalguide"
            if parents_guide_link:
                print("Entered parents guide")
                print(parents_guide_link)
                parents_guide_response = requests.get(parents_guide_link, headers=headers, cookies=cookies)
                parents_guide_html_content = parents_guide_response.content
                parents_guide_soup = BeautifulSoup(parents_guide_html_content, 'html.parser')

                nudity_element = parents_guide_soup.select_one('#advisory-nudity span')
                if nudity_element == " ":
                    print(f"{title} is yet to release")
                if nudity_element is not None:
                    print(f"Severity: {nudity_element.get_text(strip=True)}")
                    print("debug 3")
                    print(nudity_element)
                    if nudity_element.get_text(strip=True).lower() == severity.lower():
                        print("debug 1")
                        list_without_nudity.append(title)
                        print("debug 2")
                        print(f"Title added to list: {title}")

                print(" ")

            else:
                print("Can't find")
        return list_without_nudity

    except Exception as e:
        print(f"Error: {e}")
        return []


# Call the function and get the list of TV shows without nudity
tv_show_list_without_nudity = get_imdb_info()

# Write the TV show list to a text file
with open('ImdbRandomLink.txt', 'w') as file:
    for show in tv_show_list_without_nudity:
        file.write(show + '\n')

print("Filtered movies/tv shows saved to 'ImdbRandomLink.txt'")
