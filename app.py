from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    ingredients = request.form.get('ingredients').split(',')
    # Add your web scraping logic here to fetch recipe details based on ingredients
    # You can use the BeautifulSoup code from the previous example
    # Extract recipe name, URL, and image
    base_url = "https://food.ndtv.com/recipes/indian-recipes"
    
    # Send an HTTP GET request to the website
    response = requests.get(base_url)
    
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Find all recipe URLs on the page
    recipe_links = soup.find_all("a", class_="crd_img")
    
    # List to store matching recipes
    matching_recipes = []
    
    # Loop through each recipe link and check if it contains the ingredients
    for link in recipe_links:
        recipe_url = link["href"]
        recipe_response = requests.get(recipe_url)
        recipe_soup = BeautifulSoup(recipe_response.text, "html.parser")
        
        # Extract ingredients and recipe name
        recipe_ingredients = [ingredient.text.strip() for ingredient in recipe_soup.find_all("li", class_="RcpIngd-tp_li")]
        recipe_name = recipe_soup.find("h1", class_="sp-ttl").text.strip()
        
        # Check if all user-provided ingredients are in the recipe
        if all(ingredient.lower() in " ".join(recipe_ingredients).lower() for ingredient in ingredients):
            matching_recipes.append({'name': recipe_name, 'url': recipe_url})

    
    return render_template('results.html', matching_recipes=matching_recipes)

if __name__ == '__main__':
    app.run(debug=True, port=3000)