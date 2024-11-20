class NumberSet:
  def __init__(self):
    self.numbers = set(range(1, 101))
    self.extracted_number = None

  def extract(self, number):
    if number not in self.numbers:
      raise ValueError("El número no está en el conjunto o ya ha sido extraído.")
    self.numbers.remove(number)
    self.extracted_number = number

  def find_missing_number(self):
    if self.extracted_number is None:
      raise ValueError("No se ha extraído ningún número.")
    return self.extracted_number
      

      