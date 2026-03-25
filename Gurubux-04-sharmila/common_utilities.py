"""Common utilities for the FitBuddy program."""

def create_if_missing(fname, header):
    """If the file doesn't exist, create it and add the header row."""
    try:
        temp_f = open(fname, "r")
        temp_f.close()
    except FileNotFoundError:
        temp_f = open(fname, "w")
        temp_f.write(header + "\n")
        temp_f.close()


def get_all_rows(fname):
    """Returns a list of all rows in the file, except the header."""
    temp_f = open(fname, "r")
    lines = temp_f.readlines()
    temp_f.close()

    rows = []
    i = 0
    for line in lines:
        if i == 0:
            i = i + 1
            continue
        clean = line.strip()
        if clean != "":
            rows.append(clean)
        i = i + 1
    return rows


def save_row(fname, row_data):
    """Appends a row to the end of the file."""
    temp_f = open(fname, "a")
    temp_f.write(row_data + "\n")
    temp_f.close()


def replace_file(fname, header, new_rows):
    """Replaces the file with the new rows, and adds the header back."""
    temp_f = open(fname, "w")
    temp_f.write(header + "\n")
    for row in new_rows:
        temp_f.write(row + "\n")
    temp_f.close()
