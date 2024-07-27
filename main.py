
import authusers as au
import credentials as cr

# STAND IN FOR INTERACTIVE INTERFACE

def print_cred(option, username, password):
    print()  
    try:
        print(f"Credentials for {option}:")
        cred = cr.get_credential(option, username, password)
        print(f"Service: {cred['service']}\nUsername: {cred['username']}\nPassword: {cred['password']}")
    except:
        pass
    print() 
    
def print_services(username, password):
    services = cr.get_services(username, password)
    print()
    for service in services:
        print(service)
    print()  

def main():
    # Get user auth creds
    username, password = au.load_config()
    
    print("Welcome to the credential manager! (crappy stand in)\n\
Enter 'services' or 's' to see a list of available services.\n\
Enter 'q' to quit at any time.\n")
    
    option = input("Enter the service you would like to access credentials for: ")
    
    while option.strip() != 'q':
        if option.strip() == 'services' or option.strip() == 's':
            print_services(username, password)
        else:
            print_cred(option.strip(), username, password)
            
        option = input("Enter the service you would like to access credentials for: ")
        
    print("\nGoodbye!")
    
    # TODO: Implement actual graphical interactive interface
    
if __name__=='__main__':
    main()
