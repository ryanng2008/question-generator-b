import databases.categorydb as cdb

def get_category(cid):
    for category in cdb.categories:
        print(category)
        if str(category.get('id')) == cid:
            return category
        else:
            return f"No Category with ID {cid}"

def get_all_categories():
    return cdb.categories