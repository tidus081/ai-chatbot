import time
from collections import defaultdict


class UserRateLimiter:
    """
    Rate limiter for users: allows up to `max_calls` per `period` seconds per user.
    Example: max_calls=10, period=3600 (10 calls per hour)
    """

    def __init__(self, max_calls: int, period: int):
        self.max_calls = max_calls
        self.period = period
        self.user_timestamps = defaultdict(list)

    def is_allowed(self, user_id: str) -> bool:
        now = time.time()
        timestamps = self.user_timestamps[user_id]
        # Remove timestamps outside the window
        self.user_timestamps[user_id] = [t for t in timestamps if now - t < self.period]
        if len(self.user_timestamps[user_id]) < self.max_calls:
            self.user_timestamps[user_id].append(now)
            return True
        return False

    def get_remaining(self, user_id: str) -> int:
        now = time.time()
        timestamps = self.user_timestamps[user_id]
        self.user_timestamps[user_id] = [t for t in timestamps if now - t < self.period]
        return max(0, self.max_calls - len(self.user_timestamps[user_id]))


# Example usage:
# limiter = UserRateLimiter(max_calls=10, period=3600)
# if limiter.is_allowed(user_id):
#     # process chat
# else:
#     # reject or warn user
