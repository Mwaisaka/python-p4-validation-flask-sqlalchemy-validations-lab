from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'
    
    # Add validators 
    @validates('name')
    def validate_name(self,key,name):
        if not name:
            raise ValueError("Name is required.")
        author=db.session.query(Author.id).filter_by(name=name).first()
        if author is not None:
            raise ValueError('Name must be unique.')
        return name
        
    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if len(phone_number) != 10 or not phone_number.isdigit():
            raise ValueError("Phone number must be 10 digits.")
        return phone_number
    
class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates('title')
    def validate_title(self,key,title):
        if not title:
            ValueError("Title is required.")
        clickbait = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(substring in title for substring in clickbait):
            raise ValueError("No clickbait found")
        return title
    
    @validates('content','summary')
    def validate_content(self,key,post):
        if(key=="content"):
            if len(post)<250:
                raise ValueError("Post content must be greater than 250 characters long.")
            return post       
        
        if(key=="summary"):
            if len(post)>250:
                raise ValueError("Post summary must be less than or equal 250 characters long.")
            return post
        
    @validates('category')
    def validate_category(self, key,category):
        if category!='Fiction' and category!='Non-Fiction':
            raise ValueError('Post category must be Fiction or Non-Fiction')
        return category
        
    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'

