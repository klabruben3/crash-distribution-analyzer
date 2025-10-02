import random

# --- Welcome Banner ---
print("\n" + "-"*40)
print("🎲 Welcome to the Random Number Generator 🎲")
print("-"*40 + "\n")

# --- Get initial limit with validation ---
def input_maxVal():
    while True:
            try:
                limit = int(input("Enter new maximum value: "))
                if limit <= 0:
                    print("⚠️  Limit must be positive.")
                    continue
                print(f"✅ Limit updated to {limit}")
                return limit
            except ValueError:
                print("⚠️  Please enter a valid integer.")

limit = input_maxVal()

# --- Main loop ---
history = []
while True:
    print("\nCommands: [y] generate | [u] update limit | [h] show history | [n] quit")
    command = input("Your choice: ").lower()

    if command == 'n':
        print("\nThanks for using the Random Number Generator! Goodbye! 👋")
        break
    elif command == 'y':
        number = random.random() * limit
        history.append(number)
        print(f"\033[92mGenerated: {number:.2f}\033[0m (0 - {limit})")
    elif command == 'u':
        limit = input_maxVal()
    elif command == 'h':
        if not history:
            print("No numbers generated yet.")
        else:
            print("\n--- Generated Numbers History ---")
            for i, num in enumerate(history, 1):
                print(f"{i}: {num:.2f}")
            print("-------------------------------")
    else:
        print("⚠️  Invalid input. Use y, n, u, or h.")
