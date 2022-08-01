from libgravatar import Gravatar


def get_user_gravatar_image(user_email):
    g = Gravatar(user_email)
    return g.get_image()
