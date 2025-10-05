from flask_login import AnonymousUserMixin
from app import login_manager
from .user import User

class Anonymous(AnonymousUserMixin):
    def can(self, perm):
        return False
    
    def is_administrator(self):
        return False
    
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))