import person_pb2

# Criar uma instância de Person
person = person_pb2.Person()
person.name = "Alice"
person.id = 1234
person.email = "alice@example.com"

# Serializar
data = person.SerializeToString()

# Desserializar
new_person = person_pb2.Person()
new_person.ParseFromString(data)
print(new_person)
