class DataPoint:
    """
    This Class will contain variable information like name, value, id, group id
    Object will be used to update values in graphical interface
    """

    def __init__(self, id, group_id, name, value):
        self.id = id
        self.group_id = group_id
        self.__name = name
        self.value = value

    def __repr__(self):
        return "{} has id {}, is in group {} and have value {}".format(self.__name, self.id, self.group_id, self.value)
    
