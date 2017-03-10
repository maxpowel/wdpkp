import model
import database

model.Base.metadata.create_all(database.engine)
print("Database created!")