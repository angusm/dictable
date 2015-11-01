from collections import defaultdict


class ToDictFieldSet(object):
    """
    Used to separate out fields from django__underscored__format
    """

    def __init__(self, fields=None):
        self.fields = defaultdict(ToDictFieldSet)
        if fields is not None:
            field_arrays = ToDictFieldSet.__split_django_fields_into_arrays(fields)
            self.add_fields(field_arrays)

    def add_fields(self, field_arrays):
        """
        Adds fields to the field set
        """
        for field_array in field_arrays:

            # Grab the field that's directly tied to the first model
            direct_field = field_array[0]
            remaining_fields = field_array[1:]

            # Add the remaining fields to the field set tied to the given field
            self.fields[direct_field].add_fields(remaining_fields)

    def get_fields(self):
        return self.fields.keys()

    def get_sub_field_set(self, field):
        """
        Get the sub field set for the given field
        """

        sub_field_set = self.fields[field]
        if sub_field_set.has_fields():
            return sub_field_set
        else:
            return None

    def has_fields(self):
        """
        Returns True/False indicating whether or not the given field set has fields
        """
        return len(self.fields) > 0

    @classmethod
    def __split_django_fields_into_arrays(cls, fields):
        return [cls.__split_django_field_into_array(field) for field in fields]

    @classmethod
    def __split_django_field_into_array(cls, field):
        return field.split('__')