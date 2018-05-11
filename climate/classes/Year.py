class Year:
    """
    | Utilities for handling years
    """

    @staticmethod
    def get_months_of_year():
        """
        Get the months of the year
        """
        a = []
        [a.append(i) for i in range(1, 13)]
        return a
