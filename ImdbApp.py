import requests
from bs4 import BeautifulSoup
import time

def get_imdb_info():
    print(" ------------------------------------------------------")
    print("Hello and welcome to the movie/imdb application")
    print(" ")
    print("------------------------------------------------------")
    movie_or_show = input("Would you like to search for movies or shows?: ").lower()
    if (movie_or_show.__contains__("mov")):
        base_imdb_link = 'https://www.imdb.com/chart/moviemeter/?ref_=nv_mv_mpm'
    elif (movie_or_show.__contains__("show")):
        base_imdb_link = 'https://www.imdb.com/chart/tvmeter/?ref_=nv_tvv_mptv'
    else:
        print("Error - try again")
    print(" ")
    severity = input("And how severe can it be? None/Mild/Moderate/Severe: ")
    print(" ")
    print(f"Okay, thank you. Initiating {movie_or_show} search. This might take a while. Get a coffee or some candy while I work")
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
        time.sleep(2)
        print("1")
        response = requests.get(base_imdb_link, headers=headers, cookies=cookies)
        print("2")
        html_content = response.content
        soup = BeautifulSoup(html_content, 'html.parser')

        list_without_nudity = []
        #print(html_content)
        tv_show_rows = soup.select('ul.ipc-metadata-list.ipc-metadata-list--dividers-between > li')
        i = 0

        for row in tv_show_rows:
            #print("4")sh
            title_element = row.select_one('.ipc-title a')
            title = title_element.text.strip()
            show_url = title_element['href']
            print(f"Proccessing movie no.: {i} - With Title: {title}")
            show_url_now = show_url.split('?')[0]  # Extract the part before the question mark
            i += 1
            # Perform necessary operations with the show URL
            parents_guide_link = f"https://www.imdb.com{show_url_now}parentalguide"
            if parents_guide_link:
                parents_guide_response = requests.get(parents_guide_link, headers=headers, cookies=cookies)
                parents_guide_html_content = parents_guide_response.content
                parents_guide_soup = BeautifulSoup(parents_guide_html_content, 'html.parser')

                nudity_element = parents_guide_soup.select_one('#advisory-nudity span')
                if nudity_element == " ":
                    print(f"{title} is yet to release")
                else:
                    print(f"Severity: {nudity_element.text.strip()}")
                if nudity_element and nudity_element.text.strip().lower() == severity.lower():
                    list_without_nudity.append(f'{title} - No in list: {i}')
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
with open('ImdbTvShowsWithoutNudity.txt', 'w') as file:
    for show in tv_show_list_without_nudity:
        file.write(show + '\n')

print("TV show list without nudity saved to 'ImdbTvShowsWithoutNudity.txt'")
