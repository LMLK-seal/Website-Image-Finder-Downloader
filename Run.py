import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin
import ssl
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from io import BytesIO
from PIL import Image, ImageTk

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def get_image_size(url, headers):
    try:
        img_response = requests.head(url, headers=headers, verify=False)
        size = int(img_response.headers.get('content-length', 0))
    except:
        try:
            img_response = requests.get(url, headers=headers, verify=False)
            size = len(img_response.content)
        except:
            size = 0
    return size

def find_large_images(soup, base_url, headers, min_size=30000):
    img_tags = soup.find_all('img')
    large_images = []

    for img in img_tags:
        src = img.get('src') or img.get('data-src')
        if src:
            full_url = urljoin(base_url, src)
            size = get_image_size(full_url, headers)
            if size > min_size:
                title = img.get('alt') or img.get('title') or os.path.basename(src)
                large_images.append((title, full_url, size))
    
    return sorted(large_images, key=lambda x: x[2], reverse=True)

def show_image_preview(img_url):
    try:
        response = requests.get(img_url, headers=headers, verify=False)
        img_data = BytesIO(response.content)
        img = Image.open(img_data)
        img.thumbnail((200, 200))
        photo = ImageTk.PhotoImage(img)
        preview_label.config(image=photo)
        preview_label.image = photo
    except:
        preview_label.config(image=None, text="Preview failed")

def on_image_select(event):
    selected_item = image_list.selection()[0]
    img_url = image_list.item(selected_item)['values'][1]
    show_image_preview(img_url)

def download_selected_image():
    selected_items = image_list.selection()
    if not selected_items:
        messagebox.showwarning("Warning", "Please select an image to download.")
        return

    selected_item = selected_items[0]
    img_url = image_list.item(selected_item)['values'][1]
    
    save_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("All files", "*.*")])
    if save_path:
        img_data = requests.get(img_url, headers=headers, verify=False).content
        with open(save_path, 'wb') as f:
            f.write(img_data)
        messagebox.showinfo("Success", f"Image saved to {save_path}")
    else:
        messagebox.showwarning("Warning", "No file location selected. Image not saved.")

def fetch_images():
    url = url_entry.get()
    if not url:
        messagebox.showerror("Error", "Please enter a website URL.")
        return

    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    global headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        update_status("Connecting to the website...")
        
        # First, try with requests
        response = requests.get(url, headers=headers, verify=False)
        soup = BeautifulSoup(response.text, 'html.parser')
        images = find_large_images(soup, url, headers)
        
        # If no suitable images found, try with Selenium
        if not images:
            update_status("No images found in HTML. Trying with JavaScript...")
            driver = setup_driver()
            driver.get(url)
            
            time.sleep(5)  # Wait for JavaScript to load content
            
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "img")))
            except:
                pass  # Continue even if the wait times out
            
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            images = find_large_images(soup, url, headers)
            driver.quit()
        
        if images:
            update_status(f"Found {len(images)} large images. Select one to download.")
            for item in image_list.get_children():
                image_list.delete(item)
            for i, (title, url, size) in enumerate(images, 1):
                image_list.insert("", "end", text=str(i), values=(title, url, f"{size / 1024:.1f} KB"))
            image_list.selection_set(image_list.get_children()[0])
            show_image_preview(images[0][1])
        else:
            messagebox.showwarning("Warning", "No suitable images found on the webpage.")
            update_status("No suitable images found.")

    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Failed to connect to the website: {str(e)}")
        update_status("Connection error. Check URL and internet.")
    except Exception as e:
        messagebox.showerror("Error", str(e))
        update_status("An error occurred.")

# Create main window
root = tk.Tk()
root.title("Advanced Image Chooser & Downloader")

window_width = 800
window_height = 600
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# URL entry and fetch button
url_frame = tk.Frame(root)
url_frame.pack(pady=10, padx=10, fill=tk.X)

url_label = tk.Label(url_frame, text="Enter Website URL:", font=("Arial", 12))
url_label.pack(side=tk.LEFT, padx=5)

url_entry = tk.Entry(url_frame, width=50, font=("Arial", 10))
url_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
url_entry.focus()

fetch_button = tk.Button(url_frame, text="Fetch Images", command=fetch_images, font=("Arial", 10), bg="#4CAF50", fg="white")
fetch_button.pack(side=tk.LEFT, padx=5)

# Image list and preview
content_frame = tk.Frame(root)
content_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

image_list_frame = tk.Frame(content_frame)
image_list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

image_list = ttk.Treeview(image_list_frame, columns=("Title", "URL", "Size"), show="headings")
image_list.heading("Title", text="Title")
image_list.heading("URL", text="URL")
image_list.heading("Size", text="Size")
image_list.column("Title", width=200)
image_list.column("URL", width=300)
image_list.column("Size", width=100)
image_list.pack(fill=tk.BOTH, expand=True)
image_list.bind("<<TreeviewSelect>>", on_image_select)

preview_frame = tk.Frame(content_frame)
preview_frame.pack(side=tk.RIGHT, padx=10)

preview_label = tk.Label(preview_frame, text="Image Preview", compound=tk.TOP)
preview_label.pack()

# Download button
download_button = tk.Button(root, text="Download Selected Image", command=download_selected_image, font=("Arial", 12), bg="#008CBA", fg="white")
download_button.pack(pady=10)

# Status label
status_label = tk.Label(root, text="", font=("Arial", 10), fg="#333333")
status_label.pack(pady=5)

def update_status(message):
    status_label.config(text=message)
    root.update_idletasks()

# Help text
help_text = """
1. Enter the full website URL (e.g., https://www.example.com).
2. Click 'Fetch Images' to search for large images.
3. Select an image from the list to preview it.
4. Click 'Download Selected Image' to save it.

Note: This tool can find images loaded by JavaScript!
It looks for all sizable images, not just the largest one.

Created by: LMLK - Imperial Seal.
"""

help_label = tk.Label(root, text=help_text, justify=tk.LEFT, fg="#555555", font=("Arial", 8))
help_label.pack(pady=10, padx=20, anchor="w")

# Global headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Run the GUI
root.mainloop()
