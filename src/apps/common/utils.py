def update_nested_phones(data, instance, model):
    """
    Update nested phones objects
    The method is designed to update multiple phones from a staff
    :param data: update data 
    example: {'id': 1, 'phone': '123456'} 
    :param instance: updating instance
    :param model:  updating model
    example: Phone
    :return: 
    """

    # items for which no changes have occurred (will be deleted)
    old_objects = instance.phones.all()

    # review the data for the update
    while data:
        upd_values = data.pop(0)  # take the data in the first place
        upd_id = upd_values['id']  # expected id of the updatable object
        upd_values['profile'] = instance  # link the phone to the profile
        old_objects = old_objects.exclude(id=upd_id)  # we will not delete the updated object
        created_obj, created = model.objects.update_or_create(id=upd_id,
                                                        defaults=upd_values)
        if created:
            # if a new object is created, add it
            instance.phones.add(created_obj)

    # delete objects that were not encountered in the update that came
    old_objects.delete()
