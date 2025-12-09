from main.rate_limiter import RateLimiter
import time
from freezegun import freeze_time
class TestRateLimiter:
    def test_initialisation(self):
        limiter = RateLimiter(max_requests=60, period_seconds=60)
        assert limiter.max_requests == 60
        assert limiter.period_seconds == 60
        assert limiter.tokens == 60
    
    def test_single_request_allowed(self):
        limiter = RateLimiter(max_requests=5, period_seconds=60)
        assert limiter.allow_request() is True
        assert limiter.tokens == 5 - 1
    
    def test_tokens_decrease(self):
        limiter = RateLimiter(max_requests=10, period_seconds=60)
        initial_tokens = limiter.tokens
        limiter.allow_request()
        assert limiter.tokens == initial_tokens - 1
    
    def test_multiple_requests(self):
        limiter = RateLimiter(max_requests=3, period_seconds=60)
        for _ in range(3):
            assert limiter.allow_request() is True
    
    def test_request_denied_when_no_tokens(self):
        limiter = RateLimiter(max_requests=2, period_seconds=60)
        limiter.allow_request()
        limiter.allow_request()
        assert limiter.allow_request() is False
    
    @freeze_time("2025-01-01 00:00:00")
    def test_refill_tokens(self):
        limiter = RateLimiter(max_requests=5, period_seconds=60)
        for _ in range(5):
            limiter.allow_request()
        assert limiter.tokens == 0
        with freeze_time("2025-01-01 00:01:01"):
            limiter.refill_tokens()
            assert limiter.tokens == 5
    
    @freeze_time("2025-01-01 00:00:00")
    def test_tokens_dont_exceed_maximum(self):
        limiter = RateLimiter(max_requests=5, period_seconds=60)
        for _ in range(3):
            limiter.allow_request()
        with freeze_time("2025-01-01 00:32:00"):
            limiter.refill_tokens()
            assert limiter.tokens == 5
    
    def test_get_status(self):
        limiter = RateLimiter(max_requests=60, period_seconds=60)
        limiter.allow_request()
        limiter.allow_request()
        status = limiter.get_status()
        assert status["max_requests"] == 60
        assert status["period_seconds"] == 60
        assert status["available_tokens"] == 58
        assert "last_refill" in status

    def test_reset(self):
        limiter = RateLimiter(max_requests=10, period_seconds=60)
        limiter.allow_request()
        limiter.allow_request()
        assert limiter.tokens == 8
        limiter.reset()
        assert limiter.tokens == 10
    
    @freeze_time("2025-01-01 00:00:00")
    def test_gradual_refill(self):
        limiter = RateLimiter(max_requests=60, period_seconds=60)
        for _ in range(60):
            limiter.allow_request()
        with freeze_time("2025-01-01 00:00:10"):
            limiter.refill_tokens()
            assert limiter.tokens == 10
        with freeze_time("2025-01-01 00:00:30"):
            limiter.refill_tokens()
            assert limiter.tokens == 30
    
    # def test_burst_requests(self):
    #  with freeze_time("2025-01-01 00:00:00") as frozen:
    #     limiter = RateLimiter(max_requests=5, period_seconds=60)

    #     for _ in range(5):
    #         assert limiter.allow_request() is True

    #     assert limiter.allow_request() is False

    #     # Move time forward 2 seconds
    #     frozen.tick(2)

    #     assert limiter.allow_request() is True