"""AntData class"""
class AntData(object):
    """Ant data class"""

    def __init__(self, i_ant_id, i_current_car, i_pendindg_dests):
        self.ant_id = i_ant_id
        self.current_car = i_current_car
        self.pendindg_dests = i_pendindg_dests
        self.current_solution = []
        self.current_solution_value = 0
        