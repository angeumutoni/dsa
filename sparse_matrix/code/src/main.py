class SparseMatrix:
    """
    A class to represent a sparse matrix using a dictionary.
    Only non-zero elements are stored to save memory.
    """

    def __init__(self, file_path=None, rows=0, cols=0):
        """
        Constructor for SparseMatrix.
        If a file path is provided, the matrix is loaded from the file.
        """
        self.rows = rows
        self.cols = cols
        self.data = {}  # Dictionary to store non-zero elements as {(row, col): value}

        if file_path:
            self.load_from_file(file_path)

    def load_from_file(self, file_path):
        """
        Load matrix from a file.
        The file should follow the format:
        rows=...
        cols=...
        (row, col, value)
        """
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    line = line.strip()
                    if not line:
                        continue  # Skip empty lines

                    if line.startswith("rows="):
                        self.rows = int(line.split("=")[1].strip())
                    elif line.startswith("cols="):
                        self.cols = int(line.split("=")[1].strip())
                    elif line.startswith("(") and line.endswith(")"):
                        parts = line[1:-1].split(',')
                        if len(parts) != 3:
                            raise ValueError("Invalid entry format")
                        row = int(parts[0].strip())
                        col = int(parts[1].strip())
                        val = int(parts[2].strip())
                        self.data[(row, col)] = val
                    else:
                        raise ValueError("Input file has wrong format")
        except Exception:
            raise ValueError("Input file has wrong format")

    def get_element(self, row, col):
        """
        Get the value at a specific (row, col). Returns 0 if not explicitly stored.
        """
        return self.data.get((row, col), 0)

    def set_element(self, row, col, value):
        """
        Set the value at a specific (row, col).
        If value is 0, the entry is removed to keep it sparse.
        """
        if value != 0:
            self.data[(row, col)] = value
        elif (row, col) in self.data:
            del self.data[(row, col)]

    def add(self, other):
        """
        Add two sparse matrices and return a new SparseMatrix.
        """
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrix dimensions must match for addition")

        result = SparseMatrix(rows=self.rows, cols=self.cols)
        result.data = self.data.copy()

        for (row, col), val in other.data.items():
            result.set_element(row, col, result.get_element(row, col) + val)

        return result

    def subtract(self, other):
        """
        Subtract another matrix from the current matrix and return a new SparseMatrix.
        """
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrix dimensions must match for subtraction")

        result = SparseMatrix(rows=self.rows, cols=self.cols)
        result.data = self.data.copy()

        for (row, col), val in other.data.items():
            result.set_element(row, col, result.get_element(row, col) - val)

        return result

    def multiply(self, other):
        """
        Multiply two matrices and return a new SparseMatrix.
        """
        if self.cols != other.rows:
            raise ValueError("Matrix dimensions do not allow multiplication")

        result = SparseMatrix(rows=self.rows, cols=other.cols)

        for (r1, c1), v1 in self.data.items():
            for c2 in range(other.cols):
                v2 = other.get_element(c1, c2)
                if v2 != 0:
                    current_val = result.get_element(r1, c2)
                    result.set_element(r1, c2, current_val + v1 * v2)

        return result

    def to_string(self):
        """
        Convert matrix data to string format for display or saving to file.
        """
        lines = [f"rows={self.rows}", f"cols={self.cols}"]
        for (row, col), val in sorted(self.data.items()):
            lines.append(f"({row}, {col}, {val})")
        return "\n".join(lines)

    def print_matrix(self):
        """
        Print the sparse matrix in readable format.
        """
        print(self.to_string())

    def save_to_file(self, file_path):
        """
        Save the sparse matrix to a file.
        """
        with open(file_path, 'w') as file:
            file.write(self.to_string())


def main():
    """
    Main function to:
    - Ask user for operation
    - Load matrices from files
    - Perform operation
    - Display and save the result
    """
    print("Sparse Matrix Operations")
    print("========================")
    print("1. Add matrices")
    print("2. Subtract matrices")
    print("3. Multiply matrices")
    choice = input("Enter your choice (1/2/3): ")

    # Input file paths — updated to match your actual sample files
    matrix1_path = "../../sample_inputs/easy_sample_02_1.txt"
    matrix2_path = "../../sample_inputs/easy_sample_02_2.txt"

    try:
        # Load matrices from files
        matrix1 = SparseMatrix(matrix1_path)
        matrix2 = SparseMatrix(matrix2_path)

        # Perform selected operation
        if choice == '1':
            result = matrix1.add(matrix2)
            print("\nResult of Addition:")
        elif choice == '2':
            result = matrix1.subtract(matrix2)
            print("\nResult of Subtraction:")
        elif choice == '3':
            result = matrix1.multiply(matrix2)
            print("\nResult of Multiplication:")
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
            return

        # Output result
        result.print_matrix()
        result.save_to_file("result.txt")
        print("\n✅ Result written to 'result.txt'")

    except ValueError as ve:
        print(f"❌ Error: {ve}")
    except FileNotFoundError:
        print("❌ One of the input files was not found.")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")


# Entry point of the script
if __name__ == "__main__":
    main()

