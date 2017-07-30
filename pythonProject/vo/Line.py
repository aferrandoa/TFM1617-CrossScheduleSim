"""Line class"""
class Line(object):
    """Line information"""

    def __init__(self, i_line_id):
        self.line_id = i_line_id
        self.non_confl_lines = []

    def add_non_conflict(self, i_non_conflict):
        """Add a non conflicted line"""
        self.non_confl_lines.append(i_non_conflict)
