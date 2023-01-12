from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
import re
from flask_app.models import user_model
# EMAIL_REGEX = re.compile(r'[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+')


class Recipe:
  def __init__(self,data):
    self.id = data['id']
    self.name = data['name']
    self.description = data['description']
    self.instructions = data['instructions']
    self.date_made = data['date_made']
    self.under = data['under']
    self.created_at = data['created_at']
    self.updated_at = data['updated_at']
    self.user_id = data['user_id']

  # VERY IMP.=============
# this is getting all the recipes from my database============

  @classmethod
  def get_all(cls):
    query = """
    SELECT * FROM recipes
    JOIN users ON recipes.user_id = users.id
    """
    results = connectToMySQL(DATABASE).query_db(query)
    all_recipes =[]
    if results:
      for row in results:
        this_recipe = cls(row)
        user_data = {
          **row,
          'id': row['users.id'],
          'created_at': row['users.created_at'],
          'updated_at': row['users.updated_at']
        }
        this_user = user_model.User(user_data)
        this_recipe.planner = this_user
        all_recipes.append(this_recipe)
      return all_recipes

  @classmethod
  def save_recipe(cls, data):
      query = """
      INSERT INTO recipes (name, description, instructions, date_made, under, user_id)
      VALUES (%(name)s, %(description)s, %(instructions)s, %(date_made)s, %(under)s, %(user_id)s);
      """
      return connectToMySQL(DATABASE).query_db(query, data)

  @classmethod 
  def get_by_id(cls,data):
      query = """
      SELECT * FROM recipes JOIN users ON recipes.user_id = users.id
      WHERE recipes.id = %(id)s
      """
      results = connectToMySQL(DATABASE).query_db(query, data)
      if results:
        this_recipe = cls(results[0])
        row = results[0]
        user_data = {
          **row,
          'id': row['users.id'],
          'created_at': row['users.created_at'],
          'updated_at': row['users.updated_at']
        }
        this_user = user_model.User(user_data)
        this_recipe.writer = this_user
        return this_recipe
      return False
      
  @classmethod
  def update_recipe(cls, data):
      query = """
      UPDATE recipes SET name=%(name)s, description=%(description)s, 
      instructions=%(instructions)s, date_made=%(date_made)s, under=%(under)s
      WHERE id = %(id)s
      """
      return connectToMySQL(DATABASE).query_db(query, data)

  @classmethod
  def delete_recipe(cls,data):
    query ="""
    DELETE FROM recipes WHERE id = %(id)s;
    """
    return connectToMySQL(DATABASE).query_db(query,data)

  @staticmethod
  def validator(form_data):
    is_valid = True

    # this is validation for  name
    if len(form_data['name']) < 3:
      flash('Name must be atleast 3 characters')
      is_valid = False

      # validation for last name
    if len(form_data['description']) < 3:
      flash('descriptions must be atleast 3 characters')  
      is_valid = False

  # validation for instructions
    if len(form_data['instructions']) < 3:
      flash('instructions must be atleast 3 characters')
      is_valid= False

      # validation for the date
    if len(form_data['date_made']) < 1:
      flash('Insert date')
      is_valid = False

  # this validates the radio buttons
    # if int(form_data['under']) < 0:
    #   flash('select yes or no')
    #   is_valid = False
    
    return is_valid
