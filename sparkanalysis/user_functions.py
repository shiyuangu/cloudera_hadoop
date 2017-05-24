def fix_user(line):
  (id, gender, age, occupation, zip) = line.strip().split("\t")
  # Normalize all genders (m, M, f or F) to uppercase (M or F)
  gender = gender.upper()

  # Convert any ZIP+4 codes (12345-6789) to the
  # five-digit representation (12345).
  if len(zip) > 5:
     zip = zip[:5] # First 5 characters

  # Here we cast the age to an integer so we can check 
  # its value numerically
  age = int(age)

  # Convert all ages to absolute (positive) values 
  age = abs(age)

  # print the corrected line to standard output
  return "%s\t%s\t%s\t%s\t%s" % (id, gender, str(age), occupation, zip)
