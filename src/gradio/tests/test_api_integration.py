"""
Tests for the API integration functions in the Gradio app
"""
import pytest
import json
import os
import requests
from unittest.mock import patch, MagicMock

# Import functions to test from app.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import login, get_clients, get_campaigns, get_analytics

class TestAPIIntegration:
    """Tests for the API integration functions in the Gradio app"""
    
    @patch('requests.post')
    def test_login_success(self, mock_post, mock_api_responses):
        """Test successful login"""
        # Setup mock
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_api_responses['login']['success']
        mock_post.return_value = mock_response
        
        # Call function
        result, token = login('test@example.com', 'password123')
        
        # Check results
        assert "Login successful" in result
        assert "Test User" in result
        assert token == 'test-token-123'
        
        # Verify the API was called correctly
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        assert 'auth/login' in args[0]
        assert kwargs['json']['email'] == 'test@example.com'
        assert kwargs['json']['password'] == 'password123'
    
    @patch('requests.post')
    def test_login_failure(self, mock_post, mock_api_responses):
        """Test failed login"""
        # Setup mock
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.json.return_value = mock_api_responses['login']['failure']
        mock_post.return_value = mock_response
        
        # Call function
        result, token = login('bad@example.com', 'wrongpassword')
        
        # Check results
        assert "Login failed" in result
        assert "Invalid credentials" in result
        assert token == ''
    
    @patch('requests.post')
    def test_login_exception(self, mock_post):
        """Test exception handling during login"""
        # Setup mock to raise an exception
        mock_post.side_effect = Exception("Connection error")
        
        # Call function
        result, token = login('test@example.com', 'password123')
        
        # Check results
        assert "Error:" in result
        assert "Connection error" in result
        assert token == ''
    
    @patch('requests.get')
    def test_get_clients_success(self, mock_get, mock_api_responses):
        """Test successfully getting clients"""
        # Setup mock
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_api_responses['clients']['success']
        mock_get.return_value = mock_response
        
        # Call function
        result, clients = get_clients('test-token-123')
        
        # Check results
        assert "Clients retrieved successfully" in result
        assert len(clients) == 2
        assert clients[0]['name'] == 'Client A'
        assert clients[1]['name'] == 'Client B'
        
        # Verify the API was called correctly
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        assert 'clients' in args[0]
        assert kwargs['headers']['Authorization'] == 'Bearer test-token-123'
    
    @patch('requests.get')
    def test_get_clients_no_token(self, mock_get):
        """Test getting clients without a token"""
        # Call function
        result, clients = get_clients('')
        
        # Check results
        assert "Please login first" in result
        assert clients == []
        
        # Verify the API was not called
        mock_get.assert_not_called()
    
    @patch('requests.get')
    def test_get_clients_failure(self, mock_get, mock_api_responses):
        """Test failed client retrieval"""
        # Setup mock
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.json.return_value = mock_api_responses['clients']['failure']
        mock_get.return_value = mock_response
        
        # Call function
        result, clients = get_clients('invalid-token')
        
        # Check results
        assert "Failed to retrieve clients" in result
        assert "Unauthorized" in result
        assert clients == []
    
    @patch('requests.get')
    def test_get_campaigns_success(self, mock_get, mock_api_responses):
        """Test successfully getting campaigns"""
        # Setup mock
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_api_responses['campaigns']['success']
        mock_get.return_value = mock_response
        
        # Call function with client filter
        result, campaigns = get_campaigns('test-token-123', '1')
        
        # Check results
        assert "Campaigns retrieved successfully" in result
        assert len(campaigns) == 2
        assert campaigns[0]['name'] == 'Campaign 1'
        
        # Verify the API was called correctly with client filter
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        assert 'campaigns' in args[0]
        assert 'clientId=1' in args[0]
        assert kwargs['headers']['Authorization'] == 'Bearer test-token-123'
        
        # Reset mock and test without client filter
        mock_get.reset_mock()
        mock_get.return_value = mock_response
        
        result, campaigns = get_campaigns('test-token-123')
        
        # Verify the API was called without client filter
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        assert 'clientId' not in args[0]
    
    @patch('requests.get')
    def test_get_analytics_success(self, mock_get, mock_api_responses):
        """Test successfully getting analytics"""
        # Setup mock
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_api_responses['analytics']['success']
        mock_get.return_value = mock_response
        
        # Call function with campaign filter
        result, analytics = get_analytics('test-token-123', '101')
        
        # Check results
        assert "Analytics retrieved successfully" in result
        assert len(analytics) == 2
        assert analytics[0]['campaign_id'] == '101'
        assert analytics[0]['impressions'] == 10000
        
        # Verify the API was called correctly with campaign filter
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        assert 'analytics' in args[0]
        assert 'campaignId=101' in args[0]
        assert kwargs['headers']['Authorization'] == 'Bearer test-token-123'