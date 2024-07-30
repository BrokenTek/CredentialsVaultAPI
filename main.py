
import authusers as au
import credentials as cr
from import_credentials import import_credentials
from export_credentials import export_credentials

# STAND IN FOR INTERACTIVE INTERFACE

def print_cred(option, username, password):
    print()  
    try:
        print(f"Credentials for {option}:")
        cred = cr.get_credential(option, username, password)
        print(f"Service: {cred['service']}\nUsername: {cred['username']}\nPassword: {cred['password']}\nNote: {cred['note']}")
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
    
    try:
        print("\n\N{WAVING HAND SIGN} Welcome to the credential manager! -(crappy stand in)-\n\
Enter 'help or 'h' to see possible options.\n\
Enter 'services' or 's' to see a list of available services.\n\
Enter 'import' to import credentials. Asks for db file path.\n\
Enter 'export' to export credentials. Asks for desired json file path/name.\n\
Enter the name of a service to access its credentials.\n\
Enter 'q' to quit at any time.\n")
    except:
        print("\nWelcome to the credential manager! -(crappy stand in)-\n\
Enter 'help or 'h' to see possible options.\n\
Enter 'services' or 's' to see a list of available services.\n\
Enter 'import' to import credentials. Asks for db file path.\n\
Enter 'export' to export credentials. Asks for desired json file path/name.\n\
Enter the name of a service to access its credentials.\n\
Enter 'q' to quit at any time.\n")
    
    option = input("Enter the service name you would like to access credentials for,\nEnter import to import credentials from a JSON file,\nEnter h or help for a list of options,\nOr enter q or quit to exit: ")
    
    while option.strip() != 'q' and option.strip() != 'Q' and option.strip() != 'quit' and option.strip() != 'exit':
        if option.strip() == 'services' or option.strip() == 's' or option.strip() == 'S':
            print_services(username, password)
        elif option.strip() == 'import':
            file_path = input("Enter path to JSON file: ")
            import_credentials(file_path)
            print()
        elif option.strip() == 'export':
            json_path = input("\nEnter path to create JSON file at: ")
            export_credentials(json_path)
            print()
        elif option.strip() == 'help' or option.strip() == 'h' or option.strip() == 'H':
            print("\nOptions:\nEnter 'services' or 's' to see a list of available services.\n\
Enter the name of a service you would like to access credentials for.\n\
Enter 'import' to import credentials. Asks for db file path.\n\
Enter 'export' to export credentials. Asks for desired json file path/name.\n\
Enter 'help' or 'h' to see this message again.\n\
Enter 'q' or 'quit to exit at any time.\n")
        else:
            print_cred(option.strip(), username, password)
            
        option = input("Enter the service name you would like to access credentials for,\nEnter import to import credentials from a JSON file,\nEnter h or help for a list of options,\nOr enter q or quit to exit: ")
        
    print("\nGoodbye!")
    
    # TODO: Implement actual graphical interactive interface
    
if __name__=='__main__':
    main()
