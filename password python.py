import random
import string

# Define the length of the password
length = 10

# Define the characters to use for the password
characters = string.ascii_letters + string.digits + string.punctuation

# Generate the password
password = ''.join(random.choice(characters) for i in range(length))

# Save the password to a file
with open('passwordPy.txt', 'w') as f:
    f.write(password)