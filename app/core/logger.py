import logging


class LocationFilter(logging.Filter):
    def filter(self, record):
        record.location = f"{record.name}:{record.lineno}"
        return True


def setup_logging():
    file_handler = logging.FileHandler("app.log", encoding="utf-8")
    stream_handler = logging.StreamHandler()
    location_filter = LocationFilter()
    file_handler.addFilter(location_filter)
    stream_handler.addFilter(location_filter)
    logging.basicConfig(
        level=logging.DEBUG,
        datefmt="%Y-%m-%d %H:%M:%S",
        format=(
            "[%(asctime)s.%(msecs)03d] - "
            "%(location)-30s - "
            "%(levelname)-8s - "
            "%(message)s"
        ),
        handlers=[file_handler, stream_handler]
    )
