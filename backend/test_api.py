"""Basic tests for ChessViz API"""
import pytest
from fastapi.testclient import TestClient
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from viz_api import app


client = TestClient(app)


class TestHealthCheck:
    """Test API health and basic endpoints"""

    def test_root_endpoint(self):
        """Test that root endpoint returns API info"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "ChessViz API"
        assert "version" in data
        assert "endpoints" in data

    def test_docs_available(self):
        """Test that Swagger docs are accessible"""
        response = client.get("/docs")
        assert response.status_code == 200


class TestUserEndpoints:
    """Test user management endpoints"""

    def test_check_existing_user(self):
        """Test checking if default user exists"""
        response = client.get("/api/check-user/river650")
        assert response.status_code == 200
        data = response.json()
        assert "exists" in data
        assert data["username"] == "river650"

    def test_check_nonexistent_user(self):
        """Test checking non-existent user"""
        response = client.get("/api/check-user/nonexistent_user_12345")
        assert response.status_code == 200
        data = response.json()
        assert data["exists"] == False

    def test_fetch_user_empty_username(self):
        """Test fetching with empty username fails"""
        response = client.post("/api/fetch-user", json={"username": ""})
        assert response.status_code == 400


class TestDataEndpoints:
    """Test data retrieval endpoints (require existing user data)"""

    @pytest.fixture(autouse=True)
    def check_test_data(self):
        """Check if test data exists, skip if not"""
        response = client.get("/api/check-user/river650")
        if not response.json().get("exists"):
            pytest.skip("Test data for river650 not available")

    def test_elo_data_endpoint(self):
        """Test ELO data endpoint"""
        response = client.get("/api/elo-data?username=river650&time_class=rapid&time_control=600")
        assert response.status_code == 200
        data = response.json()
        assert "dates" in data
        assert "elos" in data
        assert data["username"] == "river650"

    def test_wins_data_endpoint(self):
        """Test wins data endpoint"""
        response = client.get("/api/wins-data?username=river650")
        assert response.status_code == 200
        data = response.json()
        assert "months" in data
        assert "wins_white" in data
        assert "wins_black" in data

    def test_opening_stats_endpoint(self):
        """Test opening stats endpoint"""
        response = client.get(
            "/api/opening-stats?username=river650&time_class=rapid&time_control=600&player_color=white"
        )
        assert response.status_code == 200
        data = response.json()
        assert "openings" in data
        assert "win_rates" in data

    def test_time_analysis_endpoint(self):
        """Test time analysis endpoint"""
        response = client.get("/api/time-analysis?username=river650&time_class=rapid&time_control=600")
        assert response.status_code == 200
        data = response.json()
        assert "hours" in data
        assert "hourly_win_rates" in data
        assert "days" in data
        assert "daily_win_rates" in data

    def test_opening_tree_endpoint(self):
        """Test opening tree endpoint"""
        response = client.get(
            "/api/opening-tree?username=river650&time_class=rapid&time_control=600&player_color=white"
        )
        assert response.status_code == 200
        data = response.json()
        assert "tree" in data

    def test_player_stats_endpoint(self):
        """Test player stats endpoint"""
        response = client.get("/api/player-stats/river650")
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "river650"
        assert "total_games" in data
        assert "time_classes" in data


class TestErrorHandling:
    """Test error handling"""

    def test_invalid_user_stats(self):
        """Test that invalid user returns 404"""
        response = client.get("/api/player-stats/nonexistent_user_12345")
        assert response.status_code == 404

    def test_invalid_elo_request(self):
        """Test ELO data with invalid user"""
        response = client.get("/api/elo-data?username=nonexistent_user_12345")
        assert response.status_code == 404


class TestLegacyEndpoint:
    """Test backwards compatibility"""

    def test_legacy_get_plot_option3(self):
        """Test legacy get-plot endpoint for tree"""
        response = client.get("/get-plot?option=Option%203")
        assert response.status_code == 200
        data = response.json()
        assert "tree" in data

    def test_legacy_invalid_option(self):
        """Test legacy endpoint with invalid option"""
        response = client.get("/get-plot?option=Invalid")
        assert response.status_code == 400


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
