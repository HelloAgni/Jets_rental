from pathlib import Path
from datetime import datetime


def fake_email_send(
        user_id,
        user_email,
        user_first_name,
        user_last_name,
        token):
    """Fake email.
    /auth/request-verify-token  -> get token
    /auth/verify  -> verify user by token
    """
    curr_dir = Path(__file__).parent.resolve()
    new_file = curr_dir / 'verify_token.txt'

    cur_date = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
    # 22.07.2023 17:59:39
    with new_file.open('a+', encoding='utf-8') as file:
        file.write('---To verify use token---\n'
                   f'date: {cur_date}\n'
                   f'User.id: {user_id}\n'
                   f'User.fullname: {user_first_name} {user_last_name}\n'
                   f'User.email: {user_email}\n'
                   f'Token: {token}\n')
