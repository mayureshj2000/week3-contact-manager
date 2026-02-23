# Contact Manager System

The application acts like a digital address book where each contact has a name, phone number, email, address, and group (Friends, Work, Family, Other). It runs in a loop with a menu, so the user can repeatedly choose operations like adding new contacts, searching by name, editing details, or exporting data to CSV. All contacts are stored in a Python dictionary in memory and are saved to a JSON file on disk so that data is not lost when the program closes.

## Core data structure and persistence

Contacts are stored in a single dictionary where:
- Keys are contact names (as entered by the user, preserving original case).
- Values are nested dictionaries with fields like "phone", "email", "address", "group", "created_at", and "updated_at".
This dictionary is loaded from contacts_data.json when the program starts and saved back to the same file (with a backup in contacts_backup.json) after operations that modify data. JSON is used because it is human-readable, easy to parse with the json module, and suitable for small to medium datasets in beginner projects.

## Validation and case-insensitive behavior

The system validates phone numbers by stripping non-digit characters and checking that the resulting string has between 10 and 11 digits, which keeps input flexible while enforcing basic correctness. Email addresses are validated using a regular expression that ensures a standard format (user@domain.tld).
For user experience, name handling is case-insensitive in all key operations:
- Searching uses lowercase comparison, so "john", "John", or "JOHN" all match the same stored name.
- Adding a contact checks for duplicates in a case-insensitive way, preventing separate entries like "John Doe" and "john doe".
- Updating and deleting contacts also look up the name without case sensitivity, using a helper function that finds the correct key while preserving the original stored spelling.

## Functional features (CRUD, search, export, stats)

The program implements full CRUD and additional utilities:
- Add contact: prompts for name, phone, email, address, group, validates inputs, and saves a new contact with timestamps.
- Search contacts: performs partial, case-insensitive matching on names and prints formatted results with phone, email, address, and group.
- Update contact: locates a contact by name (case-insensitive), then allows optional changes to phone, email, address, and group while updating the updated_at timestamp.
- Delete contact: confirms before removing a contact from the dictionary, again using case-insensitive name matching.
- Display all contacts: shows all stored contacts in a clean, multi-line format including timestamps.
- Export to CSV: writes all contacts to contacts_export.csv with headers, which is useful for viewing in Excel or Google Sheets.
- View statistics: prints the total number of contacts, counts by group, and how many were updated in the last seven days, giving the user a quick overview of their contact data.

## Menu-driven user interface and learning outcomes

Interaction is implemented as a looped menu (options 1–8) so that users can repeatedly perform operations until they choose Exit, at which point contacts are saved and a closing message is displayed. Each menu choice routes to a specific function, which keeps the code modular and easier to maintain.

By building this system, we practice:
- Functions for clean separation of logic (validation, CRUD, UI).
- Dictionaries and nested dictionaries for structured data storage.
- String methods and regular expressions for cleaning and validating input.
- File handling with JSON and CSV for persistence and data exchange.
- Error handling and user input validation to make the app robust.
- Designing a user-friendly, menu-driven CLI workflow that resembles real-world utility tools.
