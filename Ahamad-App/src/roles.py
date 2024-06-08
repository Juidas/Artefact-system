"""Module for roles and permissions."""

class Role:
    """Base class for different roles."""
    def __init__(self, role_name):
        self.role_name = role_name

    def can_create(self):
        return False

    def can_read(self):
        return False

    def can_update(self):
        return False

    def can_delete(self):
        return False

class AdminRole(Role):
    """Admin role with all permissions."""
    def __init__(self):
        super().__init__('admin')

    def can_create(self):
        return True

    def can_read(self):
        return True

    def can_update(self):
        return True

    def can_delete(self):
        return True

class UserRole(Role):
    """User role with permissions to manage their own artefacts."""
    def __init__(self):
        super().__init__('user')

    def can_create(self):
        return True

    def can_read(self):
        return True

    def can_update(self, artefact, user):
        return artefact['created_by'] == user

    def can_delete(self, artefact, user):
        return artefact['created_by'] == user

def get_role(role_name):
    """
    Get the role instance based on role name.

    Args:
        role_name (str): The name of the role.

    Returns:
        Role: The role instance.
    """
    roles = {
        'admin': AdminRole(),
        'user': UserRole()
    }
    return roles.get(role_name, Role(role_name))

# Example usage
if __name__ == "__main__":
    admin = get_role('admin')
    user = get_role('user')
    print(f"Admin can create: {admin.can_create()}")
    print(f"User can create: {user.can_create()}")
