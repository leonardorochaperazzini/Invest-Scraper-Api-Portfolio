import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class Base():
   def __init__(self, model):
      self.model = model
      conn = f"postgresql://{os.getenv('DATABASE_USER')}:{os.getenv('DATABASE_PASSWORD')}@{os.getenv('DATABASE_HOST')}/{os.getenv('DATABASE_NAME')}"
      engine = create_engine(conn)
      self.conn_session = sessionmaker(bind=engine)
      self.session = self.conn_session()

   def all(self, limit = 10, offset = 0, filter = None):
      query = self.session.query(self.model)
      if filter:
         query = query.filter_by(**filter)
      return query.limit(limit).offset(offset).all()
   
   def create(self, data):
      new_record = self.model(**data)
      self.session.add(new_record)
      self.session.commit()
      return new_record
   
   def update(self, id, data):
      record = self.session.query(self.model).get(id)
      for key, value in data.items():
         setattr(record, key, value)
      self.session.commit()
      return record
      
   def get_current_date(self):
      return 'NOW()'

   def __del__(self):
      if self.session:
         self.session.close()