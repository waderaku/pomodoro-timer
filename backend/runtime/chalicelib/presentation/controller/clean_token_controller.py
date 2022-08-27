import logging

from chalicelib.usecase.service.crean_token_service import crean_token_service


def crean_token(event: dict):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.info("期限切れのトークンを探索します")
    expired_token_list = crean_token_service()
    if not expired_token_list:
        logger.info("期限切れのトークンは存在しませんでした")
    else:
        logger.info("期限切れのトークンが存在しました。以下のトークンを削除します")
        logger.info(expired_token_list)

    logger.info("処理を終了します")
