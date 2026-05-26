from werkzeug.security import generate_password_hash

password = "admin"
hash_generado = generate_password_hash(password)

print(hash_generado)