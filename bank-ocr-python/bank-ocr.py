import copy

pattern_raw_digits = [
  [' _ ',
   '| |',
   '|_|'],
  ['   ',
   '  |',
   '  |'],
  [' _ ',
   ' _|',
   '|_ '],
  [' _ ',
   ' _|',
   ' _|'],
  ['   ',
   '|_|',
   '  |'],
  [' _ ',
   '|_ ',
   ' _|'],
  [' _ ',
   '|_ ',
   '|_|'],
  [' _ ',
   '  |',
   '  |'],
  [' _ ',
   '|_|',
   '|_|'],
  [' _ ',
   '|_|',
   ' _|']] 

def read_raw_number(file):
  raw_number = []
  for row in range(3):
    line = file.readline()
    if line == "":
      return None
    line = line.rstrip('\n')
    raw_number.append(line)
  file.readline()
  return raw_number

def print_raw_number(raw_number):
  for i in range(3):
    print(raw_number[i])

def read_expected_result(file):
    return file.readline().rstrip('\n')

def parse_raw_digit(raw_digit):
  for digit in range(10):
    if pattern_raw_digits[digit] == raw_digit:
      return str(digit)
  return '?'

def parse_raw_number(raw_number):
  number = ''
  for digit_index in range(9):
    raw_digit = []
    for row in range(3):
      start = digit_index * 3
      end = start + 3
      raw_digit_line = raw_number[row][start:end]
      raw_digit.append(raw_digit_line)
    digit = parse_raw_digit(raw_digit)
    number += digit
  return number

def is_valid(number):
  if len(number) != 9:
    return False
  for i in range(9):
    digit = number[i]
    if not digit in "0123456789":
      return False
  return True

# assumes number is valid
def is_checksum_ok(number):
  total = 0
  for i in range(9):
    digit = number[i]
    total += int(digit) * (9 - i)
  return (total % 11) == 0

def classify_number(number):
  if is_valid(number):
    if is_checksum_ok(number):
      return ""
    else:
      return " ERR"
  else:
    return " ILL"

def change_one_char(raw_number, row, col, new_char):
  new_raw_number = copy.copy(raw_number)
  new_raw_number[row] = raw_number[row][:col] + new_char + raw_number[row][col+1:]
  return new_raw_number

def find_all_guesses(raw_number):
  guesses = []
  for row in range(3):
    for col in range(27):
      char = raw_number[row][col]
      if (char == '_') or (char == '|'):
        guess_raw_number = change_one_char(raw_number, row, col, ' ')
        guess_number = parse_raw_number(guess_raw_number)
        if classify_number(guess_number) == "":
          guesses.append(guess_number)
      elif (char == ' '):
        guess_raw_number = change_one_char(raw_number, row, col, '|')
        guess_number = parse_raw_number(guess_raw_number)
        if classify_number(guess_number) == "":
          guesses.append(guess_number)
        guess_raw_number = change_one_char(raw_number, row, col, '_')
        guess_number = parse_raw_number(guess_raw_number)
        if classify_number(guess_number) == "":
          guesses.append(guess_number)
  print(guesses)
  return guesses

def parse_and_classify_raw_number(raw_number):
  number = parse_raw_number(raw_number)
  classify = classify_number(number)
  if classify != "":
    guesses = find_all_guesses(raw_number)
    if len(guesses) == 1:
      number = guesses[0]
      classify = classify_number(number)
    elif len(guesses) > 1:
      classify = " AMB " + str(sorted(guesses))
  return number + classify

def run_all_test_cases():
  file = open('test-data.txt')
  fail_count = 0
  while True:
    raw_number = read_raw_number(file)
    if raw_number == None:
      break
    result = parse_and_classify_raw_number(raw_number)
    expected_result = read_expected_result(file)
    print_raw_number(raw_number)
    print('expected result:', expected_result)
    print('result         :', result)
    if result == expected_result:
      print('pass')
    else:
      print('fail')
      fail_count += 1
    print()
  if fail_count == 0:
    print("ALL PASS")
  else:
    print(fail_count, "FAILURE(S)")
  file.close()

run_all_test_cases()
                           
