import os

def display_directory_structure(directory, prefix=''):
    try:
        items = os.listdir(directory)
    except PermissionError as e:
        print(f"PermissionError: {e}")
        return
    
    for i, item in enumerate(items):
        item_path = os.path.join(directory, item)
        is_last = (i == len(items) - 1)
        arrow = '└── ' if is_last else '├── '
        
        print(prefix + arrow + item)
        
        if os.path.isdir(item_path):
            new_prefix = prefix + ('    ' if is_last else '│   ')
            display_directory_structure(item_path, new_prefix)

def save_to_file(content, file_path):
    try:
        with open(file_path, 'w') as file:
            file.write(content)
        print(f"Directory structure saved to {file_path}")
    except Exception as e:
        print(f"Error: {e}")

while True:
    user_input = input("Enter the full path to the folder or 'exit' to quit: ")
    
    if user_input.lower() == 'exit':
        break
    
    if not os.path.exists(user_input):
        print("Error: The specified path does not exist.")
    elif not os.path.isdir(user_input):
        print("Error: The specified path is not a directory.")
    else:
        print("\nFolder structure:")
        display_directory_structure(user_input)
        print("\n")

        save_option = input("Do you want to save the directory structure to a text file? (yes/no): ")
        if save_option.lower() == 'yes':
            file_path = input("Enter the full path for the text file (including filename): ")
            save_to_file('\n'.join([item for item in os.listdir(user_input)]), file_path)
        elif save_option.lower() == 'no':
            continue
        else:
            print("Invalid option. Please enter 'yes' or 'no'.")
