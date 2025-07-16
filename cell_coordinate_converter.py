class CellCoordinateConverter:

    @staticmethod
    def int_to_excel_col(int):
        int += 1
        col_alpha = []
        while int > 0:
            int -= 1
            remainder = int % 26
            col_alpha.append(chr(ord("A") + remainder))
            int = int // 26
        return ''.join(reversed(col_alpha))

    def to_excel_coord(row, col):
        col_str = CellCoordinateConverter.int_to_excel_col(row)
        row_str = str(col + 1)
        return f"{col_str}{row_str}"

# Export the following to a unit test
# print(CellCoordinateConverter.int_to_excel_col(0))
# print(CellCoordinateConverter.int_to_excel_col(25))
# print(CellCoordinateConverter.int_to_excel_col(26))
#
# print(CellCoordinateConverter.to_excel_coord(0, 0))  # Should print "A1"
