try:
    from datetime import datetime
except ImportError:
    from datetime import datetime

class constant:

    direction = 0 #down
    time = datetime.utcnow()
