from bs4 import BeautifulSoup

HTML_FILE = 'templates/porcelanatos.html'

def remove_images():
    try:
        with open(HTML_FILE, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')

        # Find all ambience divs
        ambience_divs = soup.find_all('div', class_='ambience-images')
        count = len(ambience_divs)

        # Remove them
        for div in ambience_divs:
            div.decompose()

        with open(HTML_FILE, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        
        print(f"Successfully removed {count} ambience image sections.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    remove_images()
