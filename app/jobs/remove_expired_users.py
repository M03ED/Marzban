from config import USER_AUTODELETE_INCLUDE_LIMITED_ACCOUNTS
from app import scheduler, logger
from app.db import GetDB, crud
from app.utils.report import user_deleted


# TODO: Send notifications
def remove_expired_users():
    with GetDB() as db:
        deleted_users = crud.delete_all_expired_users(db, USER_AUTODELETE_INCLUDE_LIMITED_ACCOUNTS)

        for user in deleted_users:
            logger.info("Expired user %s deleted." % user.username)
            user_deleted(username=user.username, user_admin=user.admin)


scheduler.add_job(remove_expired_users, 'interval', coalesce=True, hours=6, max_instances=1)
