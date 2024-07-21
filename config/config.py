class Config:
    DEBUG = False
    TYPE = 'production'
    URI = 'mongodb+srv://ryandoesnothing1:0wt60G4Vv2e3fv0u@firstvisionary.06rzakp.mongodb.net/?retryWrites=true&w=majority&appName=FirstVisionary'
    DB_NAME = 'main'
    CATEGORY_COLL = 'categories'
    QUESTIONS_COLL = 'questions'

class ProductionConfig(Config):
    DEBUG = False
    TYPE = 'production'
    URI = 'mongodb+srv://ryandoesnothing1:0wt60G4Vv2e3fv0u@firstvisionary.06rzakp.mongodb.net/?retryWrites=true&w=majority&appName=FirstVisionary'
    DB_NAME = 'main'
    CATEGORY_COLL = 'categories'
    QUESTIONS_COLL = 'questions'

def get_config():
    return ProductionConfig()