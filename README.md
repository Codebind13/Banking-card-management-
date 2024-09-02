# Banking-card-management-

Developed a Python-based application to simulate and manage a simple bank card system.
Utilized SQLite as a relational database for storing and managing cardholder information, including card numbers, PINs, and account balances. This ensured data persistence and efficient data retrieval.
Implemented core functionalities such as:
Account Creation: Users can generate new bank card accounts, where each card number is generated using a base number prefixed with a random number and validated using the Luhn algorithm to ensure authenticity.
User Authentication: Secure login mechanism that verifies card number and PIN combinations against stored records.
Balance Inquiry: Allows users to check the balance of their accounts.
Adding Funds: Users can add income to their accounts, with updates being immediately reflected in the database.
Money Transfer: Supports transferring money between different card accounts, with real-time balance updates to ensure transaction integrity.
Account Closure: Users can securely close their accounts, with all associated data being removed from the database.
Implemented the Luhn algorithm for card number generation and validation, which is a standard practice in real-world credit card systems to prevent invalid card numbers.
