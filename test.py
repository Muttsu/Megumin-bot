def decme(f):
    def wrapped(context, *args, **kwargs):
        # here we can access the context
        print("Before context:", context) 
        cr = f(*args, **kwargs)    # call the underlying function
        print("After")
        return cr
    return wrapped

@decme
def call_me(msg):
    print(msg, context)

context = "kappa"
call_me(context, "keepo")