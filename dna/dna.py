import csv
import sys

def main():

    if len(sys.argv) != 3:
        print("Usage: python dna.py data.csv sequence.txt")
        sys.exit(1)

    # Store filenames
    database_file = sys.argv[1]
    sequence_file = sys.argv[2]

    # TODO: Read database file into a variable
    people = []
    with open(database_file) as file:
        reader = csv.DictReader(file)
        # Extract list of STRs (all columns except the first one)
        str_list = reader.fieldnames[1:]
        # Convert each row into a dictionary and store
        for row in reader:
            people.append(row)

    # TODO: Read DNA sequence file into a variable
    with open(sequence_file) as file:
        sequence = file.read()

    # TODO: Find longest match of each STR in DNA sequence
    # Build a dictionary with counts for each STR
    str_counts = {}
    for STR in str_list:
        str_counts[STR] = longest_match(sequence, STR)

    # TODO: Check database for matching profiles
    for person in people:
        match = True
        for STR in str_list:
            # Compare STR counts, converting CSV values to int
            if int(person[STR]) != str_counts[STR]:
                match = False
                break
        if match:
            print(person['name'])
            return

    # If no matches found
    print("No match")
    return

def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        count = 0

        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in sequence, return longest run found
    return longest_run

main()


