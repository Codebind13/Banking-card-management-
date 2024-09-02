import random
import sys
import sqlite3


random.seed()


connection = sqlite3.connect('user_cards.db')
cursor = connection.cursor()


cursor.execute("""
    CREATE TABLE IF NOT EXISTS card(
        id INTEGER PRIMARY KEY,
        number TEXT,
        pin TEXT,
        balance INTEGER DEFAULT 0
    );
""")
connection.commit()

class BankCard:

    def __init__(self):
        self.card_number = ''
        self.pin_number = ''
        self.logged_in_card = ''
        self.logged_in_pin = ''
        self.account_details = []
        self.current_balance = 0
        self.target_balance = 0

    def create_new_account(self):
        print("Your account has been created successfully!")
        print("Your new card number is:")
        self.card_number = '400000' + str(random.randint(100000000, 999999999))
        print(self.generate_valid_card_number())
        print("Your new card PIN is:")
        self.pin_number = str(random.randint(1000, 9999))
        print(self.pin_number)
        cursor.execute(f"""
            INSERT INTO card (number, pin) VALUES ({self.card_number}, {self.pin_number});
        """)
        connection.commit()

    def user_login(self):
        self.logged_in_card = input("Please enter your card number:\n")
        self.logged_in_pin = input("Please enter your PIN:\n")

        cursor.execute(f"""
            SELECT
                id,
                number,
                pin,
                balance
            FROM 
                card
            WHERE
                number = {self.logged_in_card}
                AND pin = {self.logged_in_pin};
        """)

        self.account_details = cursor.fetchone()
        if self.account_details:
            self.current_balance = self.account_details[3]
            print('\nLogin successful!')
            self.account_dashboard()
        else:
            print("Invalid card number or PIN.")

    def account_dashboard(self):
        while True:
            print("""
                1. View Balance
                2. Add Funds
                3. Transfer Money
                4. Close Account
                5. Log Out
                0. Exit
            """)
            choice = int(input())
            if choice == 1:
                print('\nYour current balance is: ', self.current_balance)
            elif choice == 2:
                print('\nEnter the amount to add:')
                amount = int(input())
                self.current_balance += amount
                cursor.execute(f"""
                    UPDATE card SET balance = {self.current_balance} WHERE number = {self.logged_in_card};
                """)
                connection.commit()
                print('Funds added successfully!')
            elif choice == 3:
                print('\nEnter the recipient card number:')
                recipient_card = input()
                cursor.execute(f"""
                    SELECT id, number, pin, balance FROM card WHERE number = {recipient_card};
                """)

                if not self.is_valid_card_number(recipient_card):
                    print('Invalid card number format. Please try again.')
                elif not cursor.fetchone():
                    print('Recipient card does not exist.')
                else:
                    transfer_amount = int(input("Enter the amount to transfer:\n"))
                    if transfer_amount > self.current_balance:
                        print("Insufficient funds!")
                    else:
                        self.current_balance -= transfer_amount
                        cursor.execute(f"""
                            UPDATE card SET balance = {self.current_balance} WHERE number = {self.logged_in_card};
                        """)
                        self.target_balance += transfer_amount
                        cursor.execute(f"""
                            UPDATE card SET balance = {self.target_balance} WHERE number = {recipient_card};
                        """)
                        print("Transfer completed successfully!")
                        connection.commit()

            elif choice == 4:
                cursor.execute(f"DELETE FROM card WHERE number = {self.logged_in_card}")
                connection.commit()
                print('\nYour account has been closed.')
                break
            elif choice == 5:
                print("\nYou have logged out successfully!")
                break
            elif choice == 0:
                print("\nGoodbye!")
                connection.close()
                sys.exit()

    def is_valid_card_number(self, card_number):
        reversed_digits = card_number[::-1]
        digit_list = [int(x) for x in reversed_digits]
        odd_sum = sum(digit_list[::2])
        for i in range(len(digit_list)):
            if i % 2 != 0:
                digit_list[i] *= 2
        for i in range(len(digit_list)):
            if digit_list[i] > 9:
                digit_list[i] -= 9
        even_sum = sum(digit_list[1::2])

        return (odd_sum + even_sum) % 10 == 0

    def generate_valid_card_number(self):
        digits = [int(x) for x in self.card_number]
        for i in range(len(digits)):
            if i % 2 == 0:
                digits[i] *= 2
            if digits[i] > 9:
                digits[i] -= 9
        total_sum = sum(digits)
        check_digit = (10 - (total_sum % 10)) % 10
        self.card_number += str(check_digit)
        return self.card_number

    def main_menu(self):
        while True:
            print("""
                1. Create a new account
                2. Login to your account
                0. Exit
            """)
            action = int(input())
            if action == 1:
                self.create_new_account()
            elif action == 2:
                self.user_login()
            elif action == 0:
                connection.close()
                print("\nThank you for using our service!")
                break
            else:
                print("Invalid option. Please try again.")


user_card = BankCard()
user_card.main_menu()
