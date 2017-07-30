"""Inner data class"""
class InnerData(object):
    """Inner data for the problem"""

    def __init__(self, i_d, i_s):
        self.d_value = int(i_d)
        self.s_value = int(i_s)
        self.car_list = []
        self.lines_list = []

    def add_line(self, i_line):
        """Adds a line to data"""

        self.lines_list.append(i_line)

    def add_car(self, i_car):
        """Adds a car to data"""

        self.car_list.append(i_car)

    def get_line_by_id(self, i_line_id):
        """Returns a line by the inner id"""

        for current_line in self.lines_list:
            if current_line.line_id == i_line_id:
                return current_line

        return None

    def get_all_lines_ids(self):
        """Returns all existing lines IDs"""
        result = []

        for current in self.lines_list:
            result.append(current.line_id)

        return result
