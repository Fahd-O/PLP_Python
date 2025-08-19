# file_read_write.py

# Step 1: Open the input file in read mode
with open("input.txt", "r") as infile:
    content = infile.read()

# Step 2: Modify the content (for demo, let's make everything uppercase)
modified_content = content.upper()

# Step 3: Write the modified content to a new file
with open("output.txt", "w") as outfile:
    outfile.write(modified_content)

print("File has successfully been read, modified, and written to output.txt ✅")
