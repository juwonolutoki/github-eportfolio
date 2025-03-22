from pymongo import MongoClient
from bson.objectid import ObjectId
from pymongo.errors import ConnectionFailure


def update(key, value):
    for i in range(1):
        key = "animal_type"
        value = "Dog"
        return True
    else:
        return False


class AnimalShelter(object):
    """CRUD operations for animals collection"""

    def __init__(self, username, password):
        # Initializing the MongoClient to access MongoDB databases and collections
        try:
            self.client = MongoClient('mongodb://%s:%s@localhost:27017/' % (username, password))
            self.database = self.client['AAC']
            print("Connected to MongoDB")
        except ConnectionFailure as e:
            print(f"Could not connect to MongoDB: {e}")

    def create(self, data):
        """Insert new animal data into the collection"""
        if data is not None:
            self.database.animals.insert_one(data)  # data should be a dictionary
            return True
        else:
            raise Exception("Nothing to save, because data parameter is empty")
            return False

    def read(self, data=None):
        """Retrieve animal data from the collection, either filtered or all"""
        if data is not None:
            data = self.database.animals.find(data, {"_id": False})
        else:
            data = self.database.animals.find({}, {"_id": False})
        return data

    def readAll(self, data):
        """Retrieve all animals based on filter criteria"""
        data_read = self.database.animals.find(data, {"_id": False})
        return data_read

    def delete(self, data):
        """Delete an animal from the collection based on the provided criteria"""
        if data is not None:
            self.database.animals.delete_one(data)
            return True
        else:
            raise Exception("Nothing to delete because data parameter is invalid")

    def search(self, **criteria):
        """Search and filter animals based on multiple criteria"""
        query = {}
        
        # Add criteria to the query dictionary
        for key, value in criteria.items():
            query[key] = value
        
        # Execute the search query
        data = self.database.animals.find(query, {"_id": False})
        
        # Return the filtered data
        return data


# Example usage:
if __name__ == "__main__":
    shelter = AnimalShelter("AACuser", "Juwon")

    # Create some sample data
    shelter.create({"animal_type": "Dog", "name": "Buddy", "age": 3, "color": "Brown"})
    shelter.create({"animal_type": "Cat", "name": "Tom", "age": 5, "color": "Black"})
    shelter.create({"animal_type": "Dog", "name": "Rex", "age": 4, "color": "Golden"})

    # Read all animals
    animals = shelter.read()
    print("All animals:", list(animals))

    # Read animals by specific filter (for example, animals of type "Dog")
    dog_filter = {"animal_type": "Dog"}
    dogs = shelter.read(dog_filter)
    print("Dogs:", list(dogs))

    # Delete a specific animal (e.g., delete the animal with name "Tom")
    shelter.delete({"name": "Tom"})
    print("Deleted 'Tom'. Remaining animals:")
    remaining_animals = shelter.read()
    print(list(remaining_animals))

    # Search for animals of type "Dog" and color "Golden"
    search_criteria = {"animal_type": "Dog", "color": "Golden"}
    found_animals = shelter.search(**search_criteria)
    print("Found animals:", list(found_animals))
