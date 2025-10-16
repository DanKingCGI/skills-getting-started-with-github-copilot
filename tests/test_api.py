"""
Test cases for the FastAPI endpoints
"""
import pytest
from fastapi import status


class TestRootEndpoint:
    """Tests for the root endpoint"""
    
    def test_root_redirects_to_static(self, client, reset_activities):
        """Test that root endpoint redirects to static index.html"""
        response = client.get("/", follow_redirects=False)
        assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT
        assert response.headers["location"] == "/static/index.html"


class TestActivitiesEndpoint:
    """Tests for the activities endpoint"""
    
    def test_get_activities_success(self, client, reset_activities):
        """Test getting all activities"""
        response = client.get("/activities")
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert isinstance(data, dict)
        assert "Chess Club" in data
        assert "Programming Class" in data
        
        # Check structure of one activity
        chess_club = data["Chess Club"]
        assert "description" in chess_club
        assert "schedule" in chess_club
        assert "max_participants" in chess_club
        assert "participants" in chess_club
        assert isinstance(chess_club["participants"], list)
    
    def test_activities_contain_expected_data(self, client, reset_activities):
        """Test that activities contain the expected initial data"""
        response = client.get("/activities")
        data = response.json()
        
        # Check Chess Club specifically
        chess_club = data["Chess Club"]
        assert chess_club["max_participants"] == 12
        assert "michael@mergington.edu" in chess_club["participants"]
        assert "daniel@mergington.edu" in chess_club["participants"]


class TestSignupEndpoint:
    """Tests for the signup endpoint"""
    
    def test_signup_success(self, client, reset_activities):
        """Test successful signup for an activity"""
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"
        
        response = client.post(f"/activities/{activity_name}/signup?email={email}")
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]
        
        # Verify the participant was added
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert email in activities_data[activity_name]["participants"]
    
    def test_signup_duplicate_participant(self, client, reset_activities):
        """Test that signing up an already registered participant fails"""
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already registered
        
        response = client.post(f"/activities/{activity_name}/signup?email={email}")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        
        data = response.json()
        assert "detail" in data
        assert "already signed up" in data["detail"].lower()
    
    def test_signup_nonexistent_activity(self, client, reset_activities):
        """Test that signing up for a non-existent activity fails"""
        activity_name = "Nonexistent Activity"
        email = "student@mergington.edu"
        
        response = client.post(f"/activities/{activity_name}/signup?email={email}")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()
    
    def test_signup_url_encoding(self, client, reset_activities):
        """Test signup with URL-encoded activity name"""
        activity_name = "Programming Class"
        email = "newcoder@mergington.edu"
        
        response = client.post(f"/activities/{activity_name.replace(' ', '%20')}/signup?email={email}")
        assert response.status_code == status.HTTP_200_OK
        
        # Verify the participant was added
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert email in activities_data[activity_name]["participants"]


class TestUnregisterEndpoint:
    """Tests for the unregister endpoint"""
    
    def test_unregister_success(self, client, reset_activities):
        """Test successful unregistration from an activity"""
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Existing participant
        
        response = client.delete(f"/activities/{activity_name}/unregister?email={email}")
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]
        
        # Verify the participant was removed
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert email not in activities_data[activity_name]["participants"]
    
    def test_unregister_nonexistent_participant(self, client, reset_activities):
        """Test that unregistering a non-participant fails"""
        activity_name = "Chess Club"
        email = "notregistered@mergington.edu"
        
        response = client.delete(f"/activities/{activity_name}/unregister?email={email}")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        
        data = response.json()
        assert "detail" in data
        assert "not signed up" in data["detail"].lower()
    
    def test_unregister_nonexistent_activity(self, client, reset_activities):
        """Test that unregistering from a non-existent activity fails"""
        activity_name = "Nonexistent Activity"
        email = "student@mergington.edu"
        
        response = client.delete(f"/activities/{activity_name}/unregister?email={email}")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()
    
    def test_unregister_url_encoding(self, client, reset_activities):
        """Test unregister with URL-encoded activity name"""
        activity_name = "Programming Class"
        email = "emma@mergington.edu"  # Existing participant
        
        response = client.delete(f"/activities/{activity_name.replace(' ', '%20')}/unregister?email={email}")
        assert response.status_code == status.HTTP_200_OK
        
        # Verify the participant was removed
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert email not in activities_data[activity_name]["participants"]


class TestIntegrationScenarios:
    """Integration tests that test multiple operations together"""
    
    def test_signup_then_unregister(self, client, reset_activities):
        """Test signing up and then unregistering from an activity"""
        activity_name = "Art Workshop"
        email = "teststudent@mergington.edu"
        
        # First, sign up
        signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")
        assert signup_response.status_code == status.HTTP_200_OK
        
        # Verify signup worked
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert email in activities_data[activity_name]["participants"]
        
        # Then, unregister
        unregister_response = client.delete(f"/activities/{activity_name}/unregister?email={email}")
        assert unregister_response.status_code == status.HTTP_200_OK
        
        # Verify unregister worked
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert email not in activities_data[activity_name]["participants"]
    
    def test_multiple_signups_different_activities(self, client, reset_activities):
        """Test that a student can sign up for multiple different activities"""
        email = "multisport@mergington.edu"
        activities = ["Soccer Team", "Basketball Club", "Art Workshop"]
        
        # Sign up for multiple activities
        for activity in activities:
            response = client.post(f"/activities/{activity}/signup?email={email}")
            assert response.status_code == status.HTTP_200_OK
        
        # Verify all signups worked
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        
        for activity in activities:
            assert email in activities_data[activity]["participants"]
    
    def test_activity_participant_count_changes(self, client, reset_activities):
        """Test that participant counts change correctly with signups/unregisters"""
        activity_name = "Mathletes"
        email = "mathwhiz@mergington.edu"
        
        # Get initial participant count
        initial_response = client.get("/activities")
        initial_data = initial_response.json()
        initial_count = len(initial_data[activity_name]["participants"])
        
        # Sign up
        client.post(f"/activities/{activity_name}/signup?email={email}")
        
        # Check count increased
        after_signup_response = client.get("/activities")
        after_signup_data = after_signup_response.json()
        after_signup_count = len(after_signup_data[activity_name]["participants"])
        assert after_signup_count == initial_count + 1
        
        # Unregister
        client.delete(f"/activities/{activity_name}/unregister?email={email}")
        
        # Check count decreased
        after_unregister_response = client.get("/activities")
        after_unregister_data = after_unregister_response.json()
        after_unregister_count = len(after_unregister_data[activity_name]["participants"])
        assert after_unregister_count == initial_count