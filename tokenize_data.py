import re
import string

def generate_substitution_table(key):
    key = key.lower()
    available_chars = list(string.ascii_lowercase)
    used_chars = set()
    substitution_table = {}

    for k in key:
        if not available_chars:
            break
        if k not in used_chars:
            substitution_table[available_chars.pop(0)] = k
            used_chars.add(k)
            if k in available_chars:
                available_chars.remove(k)

    for c in available_chars:
        substitution_table[c] = c

    return substitution_table

def substitute_chars(value, substitution_table):
    return ''.join([substitution_table[c] if c in substitution_table else c for c in value.lower()])

def mask_email(email, substitution_table):
    username, domain = email.split("@")
    domain_name, domain_extension = domain.split(".")
    return f"{substitute_chars(username, substitution_table)}@{substitute_chars(domain_name, substitution_table)}.{domain_extension}"

def mask_phone(phone, substitution_table):
    return re.sub(r'\d', lambda match: substitute_chars(match.group(0), substitution_table), ''.join(re.findall(r'\d', phone)))

def mask_name(name, substitution_table):
    first, last = name.split(" ")
    return f"{substitute_chars(first, substitution_table)} {substitute_chars(last, substitution_table)}"

def tokenize_and_mask_data(file_path, key):
    substitution_table = generate_substitution_table(key)
    
    with open(file_path, 'r') as file:
        data = file.readlines()

    masked_data = []
    for line in data:
        key, value = line.strip().split(": ")
        if key == "Name":
            masked_data.append(f"{key}: {mask_name(value, substitution_table)}")
        elif key == "Email":
            masked_data.append(f"{key}: {mask_email(value, substitution_table)}")
        elif key == "Phone":
            masked_data.append(f"{key}: {mask_phone(value, substitution_table)}")
        else:
            masked_data.append(line.strip())

    return masked_data

if __name__ == "__main__":
    file_path = "data.txt"
    key = "5aLNDuGa0HlpRhINCmWRInIgjjG6xuatcEaI6GufjnwzxUMYVbptvtFwK0RpPKGKOQFXksso2jL+Pv4ozFUm+2dpeYIjxzN0785lM5loKHJsU+/FCj6cDoqINWnotK3oBQ5E20kgcBVgOu5MY/wx8P2Yv2Afln6rjRZaj/o9Xt3qMKmbMP0ExQaHLcEMfJlqzOyxwzKPTgEj3peWwLJPO2K6RS+htEMwjvbUvROTyWYTjwXy44eqdfYmYJDI3HP2czhz53XotxS5Zw2+PZlmNiwSttdl0EE0Eu4qpeOz5W+I6vQUFocnGhhZ8vSdbvMg3IgMbmGfpnfFnlwwDQHK295Qnwyuq1gd9XqrIha9BvgdU1lmVS1hHt5PUtAXQe45FOwhL8YqZG+Q2zIyMhycKxmDzUkST7/+loppTO0ZwjRz1gzKVb"
    masked_data = tokenize_and_mask_data(file_path, key)
    for line in masked_data:
        print(line)