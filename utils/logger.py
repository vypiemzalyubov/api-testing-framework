import logging


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def log(response, request_body=None):
    logger.info(f"REQUEST METHOD: {response.request.method}")
    logger.info(f"REQUEST URL: {response.url}")
    logger.info(f"REQUEST HEADERS: {response.request.headers}")
    logger.info(f"REQUEST BODY: {request_body}\n")
    logger.info(f"RESPONSE STATUS CODE: {response.status_code}")
    logger.info(f"RESPONSE TIME: {response.elapsed.total_seconds() * 1000:.0f} ms")
    logger.info(f"RESPONSE HEADERS: {response.headers}")
    logger.info(f"RESPONSE COOKIES: {response.cookies}")
    logger.info(f"RESPONSE BODY: {response.text}\n.")
