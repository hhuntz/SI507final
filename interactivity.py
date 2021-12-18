import rent_and_restaurants
import analysis
from time import sleep

def get_restaurant():
    '''
    prompts user for address and cuisins, prints nearest restaurant
    '''
    print('Please enter an address without punctuation to find nearby restaurants.\nExample: 105 S State St Ann Arbor MI')
    address = input('?: ')
    print('Please enter a category or cuisine (i.e., "Chinese," "Indian," "Sushi," or "Pizza")')
    category = input('?: ')
    try:
        restaurant_dict = rent_and_restaurants.get_restaurants(address, category)
        name = restaurant_dict['name']
        num = int(restaurant_dict['distance'])
        miles = round(num*0.000621371,2) # converts meters to miles
        distance = str(miles) 
        ratings = restaurant_dict['review_count']
        avg = restaurant_dict['rating']
    except:
        print("Hmm...that didn't work. Enter 'quit' to exit or anything else to try again.")
        query = input('?: ')
        if query.lower == 'quit':
            quit()
        else:
            get_restaurant()
    print(f"The nearest {category} restaurant to {address} is:")
    print(f"{name}, which is {distance} away.")
    print(f"They have {ratings} ratings with an average of {avg} stars.")

    sleep(10)

def rent_prices():
    '''
    Prompts user for address, and displays avg. rent prices nearby
    '''        
    print('Please enter an address without punctuation to find rent prices nearby.\nExample: 105 S State St Ann Arbor MI')
    address = input('?: ')
    rent = rent_and_restaurants.get_rent(address)
    print(f'Based on 2019 US Census data, the average rent near {address} is:')
    if rent != 'unknown':
        print(f'${rent}/month.')
    else:
        print('f{rent}')

    sleep(10)

if __name__ == "__main__":
    rent_and_restaurants.cache_setup()

    while True:
        print('Hello and welcome!\nThis is a tool for looking at rent prices, nearby restaurants, and the relationships between them.')
        print('Here are your options:')
        print('1. You can enter "find restaurant" or "1" to see the closest restaurant to a given address in a given category')
        print('2. You can enter "rent prices" or "2" to see the average rent prices near a given address.')
        print('3. You can enter "analysis" or "3" to look at some interesting plots showing the relationships between rent prices and restaurants')
        print('4. You can enter "tree" or "4" to see my implementation of a binary search tree.')
        print('5. You can enter "quit" or "5" to exit this program.')
        print('Enter one of these options to proceed.')
        user = input('?: ')

        if user.lower == "find restaurant" or user == "1":
            print('OK!')
            get_restaurant()
        
        elif user.lower == "rent prices" or user == "2":
            print('OK!')
            rent_prices()

        elif user.lower == "analysis" or user == "3":
            print('OK!')
            bst = analysis.tree()
            analysis.analyze(bst)

        elif user.lower == "tree" or user == "4":
            print('OK!')
            bst = analysis.tree()
            analysis.print_tree(bst.root)

        elif user.lower == 'quit' or user == '5':
            print('Thank you! Quitting now.')
            quit()
        
        else:
            print("I'm sorry, I didn't get that. Please try again.")