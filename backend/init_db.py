from database import engine, Base
import models

print("Creating database tables...")
# Yeh line automatically saari classes ko dhund kar DB mein tables bana degi
Base.metadata.create_all(bind=engine)
print("Tables created successfully!")