from wtforms import Form, StringField, validators, SubmitField, FileField
import shelve
import uuid

recipes = shelve.open('recipes')

class createRecipe(Form):
    title = StringField('Recipe Name')
    body = StringField('Body')
    image = FileField('Upload')
    submit = SubmitField('Create')

class Recipe:
    def __init__(self, id):
        self.id = id
        self.title = ''
        self.body = ''
        self.image = 0

def create_recipe(title, body, image):
    id = str(uuid.uuid4())
    recipe = Recipe(id)
    recipe.title = title
    recipe.body = body
    recipe.image = image
    recipes[id] = recipe

def update_recipe(blog):
    recipes[blog.id] = blog

def delete_recipe(id):
    if id in recipes:
        del recipes[id]

def get_recipes():
    x = []
    for i in recipes:
        x.append(recipes[i])
    return x

def get_recipe(id):
    if id in recipes:
        return recipes[id]
