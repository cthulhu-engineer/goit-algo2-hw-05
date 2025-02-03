import mmh3

class BloomFilter:
    def __init__(self, size, num_hashes):
        self.size = size
        self.num_hashes = num_hashes
        self.bit_array = [0] * size

    def add(self, item):
        """Додає елемент до фільтра Блума"""
        for i in range(self.num_hashes):
            index = mmh3.hash(item, i) % self.size
            self.bit_array[index] = 1

    def check_password_uniqueness(self, items):
        """Перевіряє унікальність паролів у фільтрі Блума"""
        result = {}
        for password in items:
            is_present = all(self.bit_array[mmh3.hash(password, i) % self.size] for i in range(self.num_hashes))
            result[password] = "вже використаний" if is_present else "унікальний"
        return result


if __name__ == "__main__":
    bloom = BloomFilter(size=1000, num_hashes=3)

    existing_passwords = ["password123", "admin123", "qwerty123"]
    for password in existing_passwords:
        bloom.add(password)

    new_passwords_to_check = ["password123", "newpassword", "admin123", "guest"]
    results = bloom.check_password_uniqueness(new_passwords_to_check)

    for password, status in results.items():
        print(f"Пароль '{password}' - {status}.")
