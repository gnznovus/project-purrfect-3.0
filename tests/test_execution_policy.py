from core.execution.policy import (
    ExecutionPolicy
)


def test_execution_policy_allows_retry():

    policy = ExecutionPolicy(
        max_retries=3
    )


    assert policy.should_retry(
        0
    ) is True


    assert policy.should_retry(
        2
    ) is True



def test_execution_policy_stops_after_limit():

    policy = ExecutionPolicy(
        max_retries=3
    )


    assert policy.should_retry(
        3
    ) is False