from flask import Flask, render_template, request, redirect
import requests
from bs4 import BeautifulSoup
import os

app = Flask(__name__)

def get_download_links(url):
    try:
        # Send a HEAD request to check if the URL is a direct file link
        response = requests.head(url, allow_redirects=True)
        content_type = response.headers.get('Content-Type', '')
        if 'application/' in content_type or 'video/' in content_type or 'audio/' in content_type:
            return [url]  # Return the direct link if it's a valid file
        else:
            # If not a direct link, parse HTML for downloadable links
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            links = []
            for a_tag in soup.find_all('a', href=True):
                href = a_tag['href']
                if href.endswith(('mkv', 'mp4', 'avi', 'zip', 'rar', '7z', 'pdf', 'exe')):
                    links.append(requests.compat.urljoin(url, href))
            return links
    except Exception as e:
        print(f"Error fetching links: {e}")
        return []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    links = get_download_links(url)
    if not links:
        return "No valid download links found. Please check the URL and try again."

    # Redirect to the first downloadable link
    return redirect(links[0])

if __name__ == '__main__':
    import os
    port = int(os.getenv('PORT', 5000))  # Use PORT environment variable or default to 5000
    app.run(host='0.0.0.0', port=port)
