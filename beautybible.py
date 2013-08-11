import urllib
import webapp2
import jinja2
import os
import datetime


from google.appengine.ext import db
from google.appengine.api import users

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + "/templates"))

class MainPage(webapp2.RequestHandler):
  """ Front page for those logged in """
  def get(self):
    user = users.get_current_user()
    if user:  # signed in already
      template_values = {
        'user_mail': users.get_current_user().email(),
        'logout': users.create_logout_url(self.request.host_url),
        } 
      template = jinja_environment.get_template('frontuser.html')
      self.response.out.write(template.render(template_values))
    else:
      self.redirect(self.request.host_url)
      
#---------- Datastore definitions--------------------------------------------------------------------------------
class Persons(db.Model):
  """Models a person identified by email"""
  email = db.StringProperty()
  
class Article(db.Model):
  """Models an article with title,category ,date and text"""
  title=db.StringProperty()
  classification=db.StringProperty()
  text=db.StringProperty(multiline=True)
  date = db.DateTimeProperty(auto_now_add=True)

class Product(db.Model):
  """Models a makeup product with name,picture_link ,date and description"""
  name=db.StringProperty()
  picture_link=db.StringProperty()
  description=db.StringProperty(multiline=True)
  date = db.DateTimeProperty(auto_now_add=True)
  
  
class Item(db.Model):
  """Models a DIY experience or sharing information with picture_link,date and description"""
  place=db.StringProperty()
  picture_link=db.StringProperty()
  description=db.StringProperty(multiline=True)
  date = db.DateTimeProperty(auto_now_add=True)
  
#-----------------------------------article(Body beautification , beauty advice)---------------------------------------------------------------------------
class Complete_writing(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()
    if user:  # signed in already
      template_values = {
        'user_mail': users.get_current_user().email(),
        'logout': users.create_logout_url(self.request.host_url),
        } 
      template = jinja_environment.get_template('complete_writing.html')
      self.response.out.write(template.render(template_values))
    else:
      self.redirect(self.request.host_url)
            

          
class Add_article(webapp2.RequestHandler):
  def post(self):
    # Retrieve person
    parent_key = db.Key.from_path('Persons', users.get_current_user().email())
    
   

    article = Article(parent=parent_key)
    article.title = self.request.get('title_article')
    article.classification = self.request.get('classification')
    article.text = self.request.get('text_article')
    
    

    # Only store an item if there is an image
    
    article.put()
    self.redirect('/complete_writing') 
    
    
class TestPost(webapp2.RequestHandler):
  def post(self):
    self.response.write("Test Post")
  def get(self):
    self.response.write("Test Get")
    #for k in self.request.keys():
    #  self.response.write("\t%s = %s\n" % (k,self.request.get(k)))
    
class Display(webapp2.RequestHandler): 
  def get(self):
    # Retrieve person
    user = users.get_current_user()
    if user:  # signed in already

      # Retrieve person
      parent_key = db.Key.from_path('Persons', users.get_current_user().email())
      
      query = db.GqlQuery("SELECT * "
                          "FROM Article "
                          "WHERE ANCESTOR IS :1 "
                          "ORDER BY date DESC",
                          parent_key)

      template_values = {
      'user_mail': users.get_current_user().email(),
      'logout': users.create_logout_url(self.request.host_url),
      'articles': query,
      } 
      template = jinja_environment.get_template('display.html')
      self.response.write(template.render(template_values))



  
  
  
  
class Write_article(webapp2.RequestHandler):
  """ Form for getting article. """
  def get(self):
    user = users.get_current_user()
    if user:  # signed in already

      # Retrieve person
      parent_key = db.Key.from_path('Persons', users.get_current_user().email())

   

      template_values = {
        'user_mail': users.get_current_user().email(),
        'logout': users.create_logout_url(self.request.host_url),
        
        } 

      template = jinja_environment.get_template('write_article.html')
      self.response.out.write(template.render(template_values))
    else:
      self.redirect(self.request.host_url)
      
      
class Delete_article(webapp2.RequestHandler):
 
  
  def post(self):  
    user=users.get_current_user()
     
    if user:

      article_key = self.request.get("article_key")
 
      db.delete(article_key)
      
    self.redirect('/beautybible')
    
#----------------------------------------------------------------------Product---------------------------------------------------------------------------------      
class Post_product(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()
    if user:  # signed in already

      # Retrieve person
      parent_key = db.Key.from_path('Persons', users.get_current_user().email())

      query = db.GqlQuery("SELECT * "
                          "FROM Product "
                          "WHERE ANCESTOR IS :1 "
                          "ORDER BY date DESC",
                          parent_key)

      template_values = {
        'user_mail': users.get_current_user().email(),
        'logout': users.create_logout_url(self.request.host_url),
        'products':query,
        } 

      template = jinja_environment.get_template('post_product.html')
      self.response.out.write(template.render(template_values))
    

class Add_product(webapp2.RequestHandler):
  """ Add a product to the datastore """
  def post(self):
    # Retrieve person
    parent_key = db.Key.from_path('Persons', users.get_current_user().email())
   
 
    product = Product(parent=parent_key)
    product.name = self.request.get('name')
    product.picture_link = self.request.get('image_url')
    product.description = self.request.get('description')

    product.put()
    self.redirect('/post_product') 
class Delete_product(webapp2.RequestHandler):
 
  
  def post(self):  
    user=users.get_current_user()
     
    if user:

      product_key = self.request.get("product_key")
 
      db.delete(product_key)
      
    self.redirect('/beautybible')  

    
#------------------------------------------------------------------------------------------------------------    
class Post_item(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()
    if user:  # signed in already

      # Retrieve person
      parent_key = db.Key.from_path('Persons', users.get_current_user().email())

      query = db.GqlQuery("SELECT * "
                          "FROM Item "
                          "WHERE ANCESTOR IS :1 "
                          "ORDER BY date DESC",
                          parent_key)

      template_values = {
        'user_mail': users.get_current_user().email(),
        'logout': users.create_logout_url(self.request.host_url),
        'items':query,
        } 

      template = jinja_environment.get_template('post_item.html')
      self.response.out.write(template.render(template_values))
        
class Add_item(webapp2.RequestHandler):
  """ Add an item to the datastore """
  def post(self):
    # Retrieve person
    parent_key = db.Key.from_path('Persons', users.get_current_user().email())
   
 
    item = Item(parent=parent_key)
    item.place = self.request.get('name')
    item.picture_link = self.request.get('image_url')
    item.description = self.request.get('description')

    item.put()
    self.redirect('/post_item')
    
class Delete_item(webapp2.RequestHandler):
 
  
  def post(self):  
    user=users.get_current_user()
     
    if user:

      item_key = self.request.get("item_key")
 
      db.delete(item_key)
      
    self.redirect('/beautybible')    
    
#-----------------------------------------------------------------------------------
class Beautyadvice(webapp2.RequestHandler): 
  def get(self):
    # Retrieve person
    user = users.get_current_user()
    if user:  # signed in already
      
      
    
      query = db.GqlQuery("SELECT * "
                          "FROM Article "
                          "WHERE classification='Beauty advice' "
                          "ORDER BY date DESC")
    

      template_values = {
      'user_mail': users.get_current_user().email(),
      'logout': users.create_logout_url(self.request.host_url),
      'articles': query,
      } 
      template = jinja_environment.get_template('display_article.html')
      self.response.write(template.render(template_values))

      
class Bodybeautification(webapp2.RequestHandler): 
  def get(self):
    # Retrieve person
    user = users.get_current_user()
    if user:  # signed in already
      
      
    
      query = db.GqlQuery("SELECT * "
                          "FROM Article "
                          "WHERE classification='Body beautification' "
                          "ORDER BY date DESC")
    

      template_values = {
      'user_mail': users.get_current_user().email(),
      'logout': users.create_logout_url(self.request.host_url),
      'articles': query,
      } 
      template = jinja_environment.get_template('display_article.html')
      self.response.write(template.render(template_values))
      
class Products(webapp2.RequestHandler):
   def get(self):
    user = users.get_current_user()
    if user:  # signed in already

      query = db.GqlQuery("SELECT * "
                          "FROM Product "
                          "ORDER BY date DESC")

      template_values = {
        'user_mail': users.get_current_user().email(),
        'logout': users.create_logout_url(self.request.host_url),
        'products':query,
        } 

      template = jinja_environment.get_template('display_product.html')
      self.response.out.write(template.render(template_values))

      
class Information_sharing(webapp2.RequestHandler):
   def get(self):
    user = users.get_current_user()
    if user:  # signed in already

      query = db.GqlQuery("SELECT * "
                          "FROM Item "
                          "ORDER BY date DESC")

      template_values = {
        'user_mail': users.get_current_user().email(),
        'logout': users.create_logout_url(self.request.host_url),
        'items':query,
        } 

      template = jinja_environment.get_template('display_sharing.html')
      self.response.out.write(template.render(template_values))
#---------------------------------------item(DIY experience or sharing information)----------------  


app = webapp2.WSGIApplication([('/beautybible', MainPage),
                             ('/write_article',Write_article),
                             ('/add_article',Add_article),
                             ('/complete_writing',Complete_writing),
                             ('/display',Display),
                             ('/delete_article',Delete_article),
                             ('/post_product',Post_product),
                             ('/add_product',Add_product),
                             ('/delete_product',Delete_product),
                             ('/test',TestPost),
                              ('/post_item',Post_item),
                              ('/add_item',Add_item),
                              ('/delete_item',Delete_item),
                             ('/body beautification',Bodybeautification),
                             ('/beautyadvice',Beautyadvice),
                             ('/products',Products),
                             ('/information sharing',Information_sharing),
                            
                            ],
                              debug=True)
