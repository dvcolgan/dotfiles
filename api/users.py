import pwd


def get_linux_users():
    """Get all Linux users on the system."""
    users = []
    try:
        for user in pwd.getpwall():
            # Include only real users (typically UID >= 1000)
            if (
                user.pw_uid >= 1000
                and user.pw_shell != "/usr/sbin/nologin"
                and user.pw_shell != "/bin/false"
            ):
                users.append(
                    {
                        "username": user.pw_name,
                        "uid": user.pw_uid,
                        "home_dir": user.pw_dir,
                        "shell": user.pw_shell,
                    }
                )
    except ImportError:
        # Handle case when pwd is not available (e.g., on Windows)
        pass
    return users
