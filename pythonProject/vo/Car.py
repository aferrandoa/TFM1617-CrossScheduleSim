"""Car class"""
class Car(object):
    """Car information"""

    def __init__(self, i_car_id, i_line_id, i_arrival_time):
        self.line_id = i_line_id
        self.car_id = i_car_id
        self.arrival_time = int(i_arrival_time)

    def get_car_def(self):
        """Returns the definition of the car like: 'line_id-car_id'"""
        return str(self.line_id) + '-' + str(self.car_id)
