from flask import abort

from common.logger.logging import logger


def db_saver_helper(db, model_instance) -> "model_instance":

    for _ in range(4):
        db.session.add(model_instance)

        try:
            db.session.commit()
        except:
            db.session.rollback()
            logger.critical(f"An error occurred while trying to save the data belonging to user")
        else:
            return model_instance
    abort(500)
