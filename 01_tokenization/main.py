import tiktoken 
enc = tiktoken.encoding_for_model("gpt-4o")

text = "Hey there! My name is Muskan"
tokens = enc.encode(text)
print("tokens", tokens) 
decoded = enc.decode([25216, 1354, 0, 3673, 1308, 382, 6619, 4482])

print("decoded", decoded)