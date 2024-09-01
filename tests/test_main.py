import pytest
import github_activity


@pytest.fixture
def username():
    return "EdmilsonRodrigues"


@pytest.mark.asyncio(loop_scope="session")
async def test_fail_get_github_activity():
    github_activity.argv = ["github_activity"]
    with pytest.raises(SystemError):
        assert await github_activity.get_activity() is not None


@pytest.mark.asyncio(loop_scope="session")
async def test_fail_get_github_activity_2():
    github_activity.argv = ["github_activity", "username", "wrong"]
    with pytest.raises(SystemError):
        assert await github_activity.get_activity() is not None


@pytest.mark.asyncio(loop_scope="session")
async def test_get_github_activity(username):
    github_activity.argv = ["github_activity", username]
    assert await github_activity.get_activity() is not None
    assert list((await github_activity.get_activity()).keys()) == ["others", "commits", "issue"]


"""
  +     'id',
  +     'type',
  +     'actor',
  +     'repo',
  +     'payload',
  +     'public',
  +     'created_at',
"""
