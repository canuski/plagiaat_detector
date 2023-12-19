from jinja2 import Environment, FileSystemLoader, select_autoescape
import os
import re

# Sample list of author names
author_names = ["Author1", "Author2", "Author3"]

# Initialize an empty matrix using a dictionary comprehension
matrix = {author: {other_author: [] for other_author in author_names}
          for author in author_names}

# Print the matrix for verification
print(matrix)


# Configure Jinja environment
env = Environment(
    loader=FileSystemLoader("."),
    autoescape=select_autoescape()
)

# Sample data for rendering
data = {
    "matrix": matrix,
    "author_aliases": {"Author1": "student_1", "Author2": "student_2", "Author3": "student_3"}
}

# Render HTML using Jinja template
# Correct the template filename
template = env.get_template("output_template.html")
html_output = template.render(data)

# Get the output file name from the user
output_file_name = 'test.html'

# Write the rendered HTML to the output file
with open(output_file_name, "w") as output_file:
    output_file.write(html_output)


def extract_comments(file_content):
    """
    Extract single-line comments from the file content using regular expressions.
    """
    # Use a regular expression to match single-line comments
    pattern = re.compile(r'#(.*)')
    comments = pattern.findall(file_content)
    return comments


def compare_comments(file1, file2):
    """
    Compare comments in two files and return True if they are identical.
    """
    comments1 = extract_comments(file1)
    comments2 = extract_comments(file2)

    return set(comments1) == set(comments2)


def process_directory(directory_path):
    """
    Process files in the given directory and update the matrix.
    """
    author_files = {}

    # Iterate through files in the directory
    for author in os.listdir(directory_path):
        author_path = os.path.join(directory_path, author)

        # Skip non-directory entries
        if not os.path.isdir(author_path):
            continue

        # Collect all Python files in the author's directory
        author_files[author] = [f for f in os.listdir(
            author_path) if f.endswith(".py")]

    # Compare files and update the matrix
    for author1, files1 in author_files.items():
        for author2, files2 in author_files.items():
            if author1 != author2:
                for file1 in files1:
                    for file2 in files2:
                        file1_path = os.path.join(
                            directory_path, author1, file1)
                        file2_path = os.path.join(
                            directory_path, author2, file2)

                        # Compare comments and update the matrix
                        if compare_comments(open(file1_path).read(), open(file2_path).read()):
                            matrix[author1][author2].append(
                                f"Identical comments in {file1} and {file2}")


# Test the function with a sample directory path
process_directory("E:\\School\\Python advanced\\Plagiaat_detector\\test_dir")

# Print the updated matrix
print(matrix)
