"""
tests/test_suite.py
Suite completa con marcadores smoke, regression y performance.
API: https: // jsonplaceholder.typicode.com — Sin registro, sin API key.
"""
import pytest
import requests

BASE_URL = "https://jsonplaceholder.typicode.com"

# ── Fixtures ──────────────────────────────────────────────────────────────────


@pytest.fixture(scope="session")
def api():
    """Sesión HTTP compartida para toda la suite."""
    session = requests.Session()
    session.headers.update({"Content-Type": "application/json"})
    yield session
    session.close()

# ── Posts ─────────────────────────────────────────────────────────────────────


class TestPosts:

    @pytest.mark.smoke
    def test_get_posts_returns_200(self, api):
        r = api.get(f"{BASE_URL}/posts")
        assert r.status_code == 200

    @pytest.mark.smoke
    def test_get_posts_is_list(self, api):
        r = api.get(f"{BASE_URL}/posts")
        assert isinstance(r.json(), list)

    @pytest.mark.smoke
    def test_get_posts_total_100(self, api):
        r = api.get(f"{BASE_URL}/posts")
        assert len(r.json()) == 100

    @pytest.mark.smoke
    def test_get_single_post_200(self, api):
        r = api.get(f"{BASE_URL}/posts/1")
        assert r.status_code == 200

    @pytest.mark.smoke
    def test_get_single_post_fields(self, api):
        r = api.get(f"{BASE_URL}/posts/1")
        post = r.json()
        for field in ["userId", "id", "title", "body"]:
            assert field in post, f"Falta campo '{field}'"

    @pytest.mark.regression
    def test_get_post_not_found(self, api):
        r = api.get(f"{BASE_URL}/posts/9999")
        assert r.status_code == 404

    @pytest.mark.regression
    def test_get_single_post_correct_id(self, api):
        r = api.get(f"{BASE_URL}/posts/1")
        assert r.json()["id"] == 1

    @pytest.mark.regression
    @pytest.mark.parametrize("post_id", [1, 2, 5, 10, 50, 100])
    def test_get_post_by_various_ids(self, api, post_id):
        r = api.get(f"{BASE_URL}/posts/{post_id}")
        assert r.status_code == 200
        assert r.json()["id"] == post_id

    @pytest.mark.regression
    def test_filter_posts_by_user(self, api):
        r = api.get(f"{BASE_URL}/posts", params={"userId": 1})
        assert r.status_code == 200
        data = r.json()
        assert len(data) > 0
        for post in data:
            assert post["userId"] == 1

    @pytest.mark.regression
    def test_create_post_201(self, api):
        r = api.post(f"{BASE_URL}/posts",
                     json={"title": "QA Post", "body": "Test body", "userId": 1})
        assert r.status_code == 201

    @pytest.mark.regression
    def test_create_post_returns_id(self, api):
        r = api.post(f"{BASE_URL}/posts",
                     json={"title": "QA Post", "body": "Test body", "userId": 1})
        assert "id" in r.json()

    @pytest.mark.regression
    def test_create_post_data_matches(self, api):
        payload = {"title": "Mi Post", "body": "Mi Body", "userId": 1}
        r = api.post(f"{BASE_URL}/posts", json=payload)
        data = r.json()
        assert data["title"] == "Mi Post"
        assert data["body"] == "Mi Body"
        assert data["userId"] == 1

    @pytest.mark.regression
    def test_update_post_put_200(self, api):
        r = api.put(f"{BASE_URL}/posts/1",
                    json={"id": 1, "title": "Updated", "body": "Updated body", "userId": 1})
        assert r.status_code == 200

    @pytest.mark.regression
    def test_update_post_put_data_matches(self, api):
        r = api.put(f"{BASE_URL}/posts/1",
                    json={"id": 1, "title": "Título PUT", "body": "B", "userId": 1})
        assert r.json()["title"] == "Título PUT"

    @pytest.mark.regression
    def test_update_post_patch_200(self, api):
        r = api.patch(f"{BASE_URL}/posts/1", json={"title": "Título PATCH"})
        assert r.status_code == 200

    @pytest.mark.regression
    def test_update_post_patch_data_matches(self, api):
        r = api.patch(f"{BASE_URL}/posts/1", json={"title": "PATCH OK"})
        assert r.json()["title"] == "PATCH OK"

    @pytest.mark.regression
    def test_delete_post_200(self, api):
        r = api.delete(f"{BASE_URL}/posts/1")
        assert r.status_code == 200

    @pytest.mark.regression
    def test_delete_post_empty_response(self, api):
        r = api.delete(f"{BASE_URL}/posts/1")
        assert r.json() == {}

# ── Users ─────────────────────────────────────────────────────────────────────


class TestUsers:

    @pytest.mark.smoke
    def test_get_users_200(self, api):
        r = api.get(f"{BASE_URL}/users")
        assert r.status_code == 200

    @pytest.mark.smoke
    def test_get_users_total_10(self, api):
        r = api.get(f"{BASE_URL}/users")
        assert len(r.json()) == 10

    @pytest.mark.smoke
    def test_get_single_user_200(self, api):
        r = api.get(f"{BASE_URL}/users/1")
        assert r.status_code == 200

    @pytest.mark.smoke
    def test_get_single_user_fields(self, api):
        r = api.get(f"{BASE_URL}/users/1")
        user = r.json()
        for field in ["id", "name", "username", "email"]:
            assert field in user

    @pytest.mark.regression
    def test_get_user_not_found(self, api):
        r = api.get(f"{BASE_URL}/users/9999")
        assert r.status_code == 404

    @pytest.mark.regression
    def test_get_user_posts(self, api):
        r = api.get(f"{BASE_URL}/users/1/posts")
        assert r.status_code == 200
        assert len(r.json()) > 0

    @pytest.mark.regression
    def test_create_user_201(self, api):
        r = api.post(f"{BASE_URL}/users",
                     json={"name": "Jenifer QA", "username": "jeniferqa", "email": "j@qa.com"})
        assert r.status_code == 201

    @pytest.mark.regression
    def test_update_user_put_200(self, api):
        r = api.put(f"{BASE_URL}/users/1",
                    json={"name": "Updated", "username": "updated", "email": "u@qa.com"})
        assert r.status_code == 200

    @pytest.mark.regression
    def test_update_user_patch_200(self, api):
        r = api.patch(f"{BASE_URL}/users/1", json={"email": "new@qa.com"})
        assert r.status_code == 200

    @pytest.mark.regression
    def test_delete_user_200(self, api):
        r = api.delete(f"{BASE_URL}/users/1")
        assert r.status_code == 200

# ── Comments ──────────────────────────────────────────────────────────────────


class TestComments:

    @pytest.mark.smoke
    def test_get_comments_200(self, api):
        r = api.get(f"{BASE_URL}/comments")
        assert r.status_code == 200

    @pytest.mark.smoke
    def test_get_comment_by_id_200(self, api):
        r = api.get(f"{BASE_URL}/comments/1")
        assert r.status_code == 200

    @pytest.mark.smoke
    def test_get_comment_fields(self, api):
        r = api.get(f"{BASE_URL}/comments/1")
        comment = r.json()
        for field in ["postId", "id", "name", "email", "body"]:
            assert field in comment

    @pytest.mark.regression
    def test_get_comment_email_format(self, api):
        r = api.get(f"{BASE_URL}/comments/1")
        assert "@" in r.json()["email"]

    @pytest.mark.regression
    def test_filter_comments_by_post(self, api):
        r = api.get(f"{BASE_URL}/comments", params={"postId": 1})
        assert r.status_code == 200
        data = r.json()
        assert len(data) > 0
        for comment in data:
            assert comment["postId"] == 1

    @pytest.mark.regression
    def test_get_comment_not_found(self, api):
        r = api.get(f"{BASE_URL}/comments/9999")
        assert r.status_code == 404

    @pytest.mark.regression
    def test_create_comment_201(self, api):
        r = api.post(f"{BASE_URL}/comments", json={
            "postId": 1, "name": "QA Comment",
            "email": "jenifer@qa.com", "body": "Prueba automatizada"
        })
        assert r.status_code == 201

# ── Todos ─────────────────────────────────────────────────────────────────────


class TestTodos:

    @pytest.mark.smoke
    def test_get_todos_200(self, api):
        r = api.get(f"{BASE_URL}/todos")
        assert r.status_code == 200

    @pytest.mark.smoke
    def test_get_todo_by_id_200(self, api):
        r = api.get(f"{BASE_URL}/todos/1")
        assert r.status_code == 200

    @pytest.mark.smoke
    def test_get_todo_fields(self, api):
        r = api.get(f"{BASE_URL}/todos/1")
        todo = r.json()
        for field in ["userId", "id", "title", "completed"]:
            assert field in todo

    @pytest.mark.regression
    def test_get_todo_completed_is_bool(self, api):
        r = api.get(f"{BASE_URL}/todos/1")
        assert isinstance(r.json()["completed"], bool)

    @pytest.mark.regression
    def test_get_todo_not_found(self, api):
        r = api.get(f"{BASE_URL}/todos/9999")
        assert r.status_code == 404

    @pytest.mark.regression
    def test_filter_todos_by_user(self, api):
        r = api.get(f"{BASE_URL}/todos", params={"userId": 1})
        assert r.status_code == 200
        data = r.json()
        assert len(data) > 0
        for todo in data:
            assert todo["userId"] == 1


# ── Performance ───────────────────────────────────────────────────────────────

class TestPerformance:

    @pytest.mark.performance
    @pytest.mark.parametrize("endpoint", [
        "/posts",
        "/posts/1",
        "/users",
        "/users/1",
        "/comments/1",
        "/todos/1",
    ])
    def test_response_time_under_3s(self, api, endpoint):
        r = api.get(f"{BASE_URL}{endpoint}")
        elapsed = r.elapsed.total_seconds()
        assert elapsed < 3.0, f"Respuesta lenta: {elapsed:.3f}s para {endpoint}"
