class UserActivityChoices:
    USER_LOGGED_IN = 'USER_LOGGED_IN'
    USER_REGISTERED = 'USER_REGISTERED'
    USER_RESET_PASSWORD = 'USER_RESET_PASSWORD'
    RESET_PASSWORD_REQUESTED = 'RESET_PASSWORD_REQUESTED'
    USER_UPDATED = 'USER_UPDATED'

    EVENT_CHOICES = (
        (USER_LOGGED_IN, 'User logged id'),
        (USER_REGISTERED, 'User registered'),
        (USER_RESET_PASSWORD, 'User reset password'),
        (RESET_PASSWORD_REQUESTED, 'Reset password requested'),
        (USER_UPDATED, 'User updated'),
    )

    EVENT_BODIES = {
        USER_LOGGED_IN: 'User logged in with the next attributes:\n First name - {first_name},\n Last name - {last_name}\n',
        USER_REGISTERED: 'New user registered with the next attributes:\n First name - {first_name},\n Last name - {last_name}\n',
        USER_RESET_PASSWORD: 'User reset password',
        RESET_PASSWORD_REQUESTED: 'User requested reset password instructions',
        USER_UPDATED: 'User updated with the next attributes:\n First name - {first_name},\n Last name - {last_name},\n Email - {email}\n',
    }
