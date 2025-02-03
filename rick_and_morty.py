# We only need two libraries:
# 'requests' to fetch data from the internet
# 'csv' to create the CSV file
import requests
import csv

# This is the website address where we'll get our character information
api_url = "https://rickandmortyapi.com/api/character"

# Step 1: Get all characters from the API
def get_characters():
    # Create an empty list to store all our characters
    all_characters = []
    
    # Start with the first page
    current_page = api_url
    
    # Keep getting more characters while there are more pages
    while current_page:
        # Get data from the current page
        response = requests.get(current_page)
        data = response.json()
        
        # Add the characters from this page to our list
        all_characters.extend(data['results'])
        
        # Move to the next page (if there is one)
        current_page = data['info']['next']
    
    return all_characters

# Step 2: Filter characters based on our requirements
def filter_characters(characters):
    # Create a list of characters that match our conditions
    filtered_list = []
    
    # Check each character
    for character in characters:
        # Only keep the character if they match ALL our conditions
        if (character['species'] == 'Human' and           # Must be Human
            character['status'] == 'Alive' and            # Must be Alive
            'earth' in character['origin']['name'].lower()):      # Must be from Earth
            
            # Create a simple dictionary with just the info we need
            character_info = {
                'Name': character['name'],
                'Origin': character['origin']['name'],
                'Location': character['location']['name'],
                'Image': character['image']
            }
            
            # Add this character to our filtered list
            filtered_list.append(character_info)
    
    return filtered_list

# Step 3: Save our results to a CSV file
def save_to_csv(characters):
    # Open a new file named 'characters.csv'
    with open('characters.csv', 'w', newline='', encoding='utf-8') as file:
        # Define the column headers
        fieldnames = ['Name', 'Origin', 'Location', 'Image']
        
        # Create a CSV writer
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        # Write the headers
        writer.writeheader()
        
        # Write each character's information
        writer.writerows(characters)

# Main program
def main():
    # Step 1: Get all characters
    print("Getting characters from the Rick and Morty API...")
    all_characters = get_characters()
    
    # Step 2: Filter the characters
    print("Filtering characters...")
    filtered_characters = filter_characters(all_characters)
    
    # Step 3: Save to CSV
    print("Saving characters to CSV file...")
    save_to_csv(filtered_characters)
    
    print(f"Done! Found {len(filtered_characters)} characters matching your criteria.")

# Run the program
if __name__ == "__main__":
    main()