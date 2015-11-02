from django.db.models import Manager
from .to_dict_field_set import ToDictFieldSet


class Dictable(object):

    def to_dict(self, *args):
        """
        Return a dictionary representation of the given instance using a field set
        """

        field_set = ToDictFieldSet(args)
        return self.to_dict_using_field_set(field_set)

    def to_dict_using_field_set(self, field_set):
        """
        Return a dictionary representation of the given instance using a field set
        """

        dict_to_return = {}

        # Add fields from the given field set
        for field in field_set.get_fields():

            # Get the raw value and the field set to apply from it
            initial_value = getattr(self, field, None)
            sub_field_set = field_set.get_sub_field_set(field)

            # Using the sub field set and the raw value get the value we want to store
            dict_to_return[field] = self.__get_final_value_from_initial_value(initial_value, sub_field_set)

        return dict_to_return

    def __get_final_value_from_initial_value(self, initial_value, sub_field_set):
        """
        Grab the final value from the initial value, handling related managers, lists
        and other dictable models
        """

        # If the initial value is a related object manager we have to process each
        # sub value
        if isinstance(initial_value, Manager):
            return self.__get_final_value_from_initial_value(initial_value.all(), sub_field_set)

        # If the initial value is a list we need to process each sub value
        elif hasattr(initial_value, '__iter__'):
            return [self.__get_final_value_from_initial_value(sub_value, sub_field_set) for sub_value in initial_value]

        # If the initial value is a Dictable model we need its dictionary
        # representation
        elif isinstance(initial_value, Dictable):
            return initial_value.to_dict_using_field_set(sub_field_set)

        # Otherwise we can just return the raw value
        else:
            return initial_value
