# Opening a file to read
with open('example.txt', 'r') as file:
    content = file.read()
    print("File Content:")
    print(content)

# Writing to a file
with open('output.txt', 'w') as file:
    file.write("This is an example of writing to a text file.\n")
    file.write("Adding another line to the file.")

print("\nData has been written to 'output.txt'.")
