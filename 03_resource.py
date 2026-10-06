"""
Resource wo data hota hai jo AI padhta hai (read_only) and wo koi changes nahi kar sakta like AI want to read reeturn policy so it use resource
"""
# @app.resource("policy://return")              now here we use @app.resource and in brackets we make a name like url
# def get_return_policy() -> str:                it reads only so no arguments needed
#     """Store's return policy document"""       docstring
#     return "Returns accepted within 7 days with receipt."
