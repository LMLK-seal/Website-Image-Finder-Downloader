<h1>Advanced Image Chooser & Downloader</h1>
This Python application allows you to fetch and download large images from any website, including those loaded dynamically with JavaScript. It uses a combination of requests, BeautifulSoup, and Selenium to scrape the website and find sizable images. The user can preview the images and select one to download to their local machine.
<h2>Features</h2>
<ul>
<li>Fetch large images from any website URL</li>
<li>Support for JavaScript-loaded images using Selenium</li>
<li>Preview images before downloading</li>
<li>Save images in various formats (JPEG, PNG, etc.)</li>
<li>User-friendly GUI interface</li>
</ul>
<h2>Prerequisites</h2>
Before running the application, you'll need to have the following Python libraries installed:
<ul>
<li>tkinter (usually pre-installed with Python)</li>
<li>requests</li>
<li>beautifulsoup4</li>
<li>selenium</li>
<li>webdriver-manager</li>
<li>pillow</li>
</ul>
You can install these libraries using pip:
Copy code: pip install requests beautifulsoup4 selenium webdriver-manager pillow
Additionally, you'll need to have a compatible web browser (e.g., Google Chrome) installed on your system for Selenium to work correctly.
<h2>Usage</h2>
<ol>
<li>Clone or download the repository to your local machine.</li>
<li>Navigate to the project directory in your terminal or command prompt.</li>
<li>Run the <code>run.py</code> script:</li>
</ol>
Copy codepython run.py
<ol start="4">
<li>The application window will open. Enter the website URL you want to fetch images from in the provided text field.</li>
<li>Click the <b>"Fetch Images"</b> button to start the image scraping process.</li>
<li>Once the scraping is complete, a list of large images found on the website will be displayed.</li>
<li>Select an image from the list to preview it.</li>
<li>Click the <b>"Download Selected Image"</b> button to save the currently previewed image to your local machine.</li>
<li>Choose a file location and name for the downloaded image.</li>
</ol>
<h2>Contributing</h2>
Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.
<h2>License</h2>
This project is licensed under the MIT License.
