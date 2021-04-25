def argument_exception_message(name, instance_of, value):
    return f'Expected argument {name} to be instance of {instance_of} got {type(value)} instead'
