from werkzeug.security import generate_password_hash

password = "jorgeadmin"
hash_generado = generate_password_hash(password)

print(hash_generado)