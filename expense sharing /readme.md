Certainly! Here's a README file for your SQLite-based sharing app.

---

# Sharing App

This Sharing App is a Python-based application that helps users manage shared expenses, lending, and borrowing money among friends. The app uses SQLite for data storage and allows users to add, display, delete data, split bills, and save data to Excel files.

## Features

1. **Add User**: Create a new user and associated database table.
2. **Add Data**: Add expense or transaction data for a user.
3. **Display User**: Display all users in the database.
4. **Display Data**: Display all data for a specific user.
5. **Delete Data**: Delete specific data from a user's table.
6. **Delete User**: Delete a user and their associated table.
7. **Split Bill**: Split a bill among multiple users.
8. **Lend or Borrow Money**: Record lending or borrowing transactions between users.
9. **Save Data to Excel**: Export user data to an Excel file.
10. **Exit**: Exit the application.

## Prerequisites

- Python 3.x
- `sqlite3` library (included in Python standard library)
- `pandas` library
- `openpyxl` library

You can install the required libraries using:
```sh
pip install pandas openpyxl
```

## How to Run

1. Clone this repository or download the script file.
2. Ensure you have the required libraries installed.
3. Run the script using Python:
```sh
python sharing_app.py
```

## Usage

Upon running the script, you will be presented with a menu of options. You can choose an option by entering the corresponding number.

### Add User

This option allows you to create a new user and their associated database table.

### Add Data

This option allows you to add expense or transaction data for a user. You will be prompted to enter the user name (table name), item name, category, and amount.

### Display User

This option displays all the users (tables) in the database.

### Display Data

This option allows you to display all data for a specific user. You will be prompted to enter the user name (table name).

### Delete Data

This option allows you to delete specific data from a user's table. You can choose to delete by row ID or by criteria.

### Delete User

This option allows you to delete a user and their associated table. You will be prompted to enter the user name (table name).

### Split Bill

This option allows you to split a bill among multiple users. You will be prompted to enter the names of the friends and the total bill amount. The bill amount can be split equally or you can specify a custom amount for each friend.

### Lend or Borrow Money

This option allows you to record lending or borrowing transactions between users. You will be prompted to enter the user who is lending money, the user who is borrowing money, and the amount.

### Save Data to Excel

This option allows you to export user data to an Excel file. You will be prompted to enter the user name (table name) and the file name.

### Exit

This option exits the application.

## Example

Below is an example of how the app might be used:

1. Run the script:
```sh
python sharing_app.py
```

2. Select option 1 to add a user:
```
Enter the option from above: 1
Enter the user name: Alice
```

3. Select option 2 to add data:
```
Enter the option from above: 2
Enter the user name (table name): Alice
Enter the name of the item: Dinner
Enter the category: Food
Enter the amount: 150
```

4. Select option 3 to display users:
```
Enter the option from above: 3
Tables in app.db:
Alice
```

5. Select option 4 to display data for a user:
```
Enter the option from above: 4
Enter the table name to display: Alice
  NAME  CATEGORY       DATE     TIME  AMOUNT
0  Dinner     Food  09-07-2024  12:34:56     150
```

6. Select option 10 to exit:
```
Enter the option from above: 10
Exiting the application.
```

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Acknowledgments

This app uses:
- SQLite for database management
- Pandas for data manipulation
- Openpyxl for Excel file creation

---

Feel free to customize this README file further to better fit your needs!
