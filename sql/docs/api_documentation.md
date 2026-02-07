# API Documentation for SQL Learning Platform

## Overview
The SQL Learning Platform provides programmatic access to educational SQL resources, database management, and learning analytics.

## Base URL
```
https://api.sql-learning-platform.com/v1
```

## Authentication
```bash
# API Key authentication
curl -H "Authorization: Bearer YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     https://api.sql-learning-platform.com/v1/databases
```

## Endpoints

### Database Management

#### List Available Databases
```http
GET /databases
```

**Response:**
```json
{
  "databases": [
    {
      "id": "chinook",
      "name": "Chinook Music Store",
      "description": "Music store database with artists, albums, tracks",
      "size": "1.2 MB",
      "tables": 11,
      "download_url": "https://example.com/chinook.db"
    },
    {
      "id": "northwind",
      "name": "Northwind Business",
      "description": "Classic business database with suppliers, products",
      "size": "800 KB",
      "tables": 13,
      "download_url": "https://example.com/northwind.db"
    }
  ]
}
```

#### Download Database
```http
POST /databases/{database_id}/download
```

**Request:**
```json
{
  "format": "sqlite",  // sqlite, csv, json
  "include_sample_data": true
}
```

**Response:**
```json
{
  "status": "success",
  "download_url": "https://storage.example.com/downloads/chinook_20231015.db",
  "expires_in": 3600
}
```

### Query Execution

#### Execute SQL Query
```http
POST /query/execute
```

**Request:**
```json
{
  "database_id": "chinook",
  "query": "SELECT name FROM Artist LIMIT 5;",
  "timeout": 30
}
```

**Response:**
```json
{
  "results": [
    {"name": "AC/DC"},
    {"name": "Accept"},
    {"name": "Aerosmith"},
    {"name": "Alanis Morissette"},
    {"name": "Alice In Chains"}
  ],
  "execution_time": 0.005,
  "rows_affected": 5
}
```

#### Query Validation
```http
POST /query/validate
```

**Response:**
```json
{
  "valid": true,
  "errors": [],
  "suggestions": [
    "Consider adding LIMIT clause for large tables",
    "Index on Artist.Name column recommended"
  ]
}
```

### Learning Analytics

#### Track Learning Progress
```http
POST /learning/progress
```

**Request:**
```json
{
  "user_id": "user123",
  "database_id": "chinook",
  "query": "SELECT * FROM Artist;",
  "time_spent": 120,
  "attempts": 3,
  "success": true
}
```

**Response:**
```json
{
  "progress_updated": true,
  "current_level": "intermediate",
  "next_recommendation": "Try using JOIN operations"
}
```

#### Get Learning Recommendations
```http
GET /learning/recommendations?user_id=user123&level=beginner
```

**Response:**
```json
{
  "recommendations": [
    {
      "topic": "Basic SELECT Statements",
      "exercises": 5,
      "estimated_time": 30,
      "prerequisites": []
    },
    {
      "topic": "Filtering with WHERE",
      "exercises": 8,
      "estimated_time": 45,
      "prerequisites": ["Basic SELECT Statements"]
    }
  ]
}
```

### Exercise Management

#### Get Exercise
```http
GET /exercises/{exercise_id}
```

**Response:**
```json
{
  "id": "ex001",
  "title": "Find Artists Starting with 'A'",
  "description": "Write a query to find all artists whose names start with the letter 'A'",
  "database": "chinook",
  "difficulty": "beginner",
  "solution_template": "SELECT name FROM Artist WHERE name LIKE 'A%';",
  "test_cases": [
    {
      "input": "A%",
      "expected_count": 3
    }
  ]
}
```

#### Submit Exercise Solution
```http
POST /exercises/{exercise_id}/submit
```

**Request:**
```json
{
  "user_id": "user123",
  "solution": "SELECT name FROM Artist WHERE name LIKE 'A%';",
  "execution_time": 2.5
}
```

**Response:**
```json
{
  "correct": true,
  "feedback": "Perfect! Your query returns the correct results.",
  "performance_score": 95,
  "next_exercise": "ex002"
}
```

## WebSocket API

### Real-time Query Execution
```javascript
const ws = new WebSocket('wss://api.sql-learning-platform.com/v1/ws');

ws.onopen = function() {
  ws.send(JSON.stringify({
    type: 'execute_query',
    database: 'chinook',
    query: 'SELECT COUNT(*) FROM Track;'
  }));
};

ws.onmessage = function(event) {
  const response = JSON.parse(event.data);
  console.log('Results:', response.results);
};
```

## Rate Limits

- **Anonymous users**: 100 requests/hour
- **Authenticated users**: 1000 requests/hour
- **Query execution**: 50 queries/hour
- **Database downloads**: 10 downloads/day

## Error Handling

### Common Error Responses

```json
{
  "error": {
    "code": "INVALID_QUERY",
    "message": "SQL syntax error near 'SELCT'",
    "details": "Did you mean SELECT?",
    "suggested_fix": "Check your SQL syntax"
  }
}
```

```json
{
  "error": {
    "code": "DATABASE_NOT_FOUND",
    "message": "Database 'nonexistent' not found",
    "available_databases": ["chinook", "northwind", "basketball"]
  }
}
```

## SDK Examples

### Python SDK
```python
from sql_learning_sdk import SQLClient

client = SQLClient(api_key="your_api_key")

# Execute query
results = client.execute_query(
    database="chinook",
    query="SELECT name FROM Artist LIMIT 5;"
)

# Get recommendations
recommendations = client.get_recommendations(
    user_id="user123",
    level="beginner"
)
```

### JavaScript SDK
```javascript
import { SQLClient } from '@sql-learning/sdk';

const client = new SQLClient({ apiKey: 'your_api_key' });

// Execute query
const results = await client.executeQuery({
  database: 'chinook',
  query: 'SELECT name FROM Artist LIMIT 5;'
});

// Track progress
await client.trackProgress({
  userId: 'user123',
  databaseId: 'chinook',
  query: 'SELECT * FROM Artist;',
  success: true
});
```

## Webhooks

### Progress Updates
```http
POST https://your-endpoint.com/sql-progress
```

**Payload:**
```json
{
  "event": "user_progress_updated",
  "user_id": "user123",
  "database_id": "chinook",
  "level_achieved": "intermediate",
  "timestamp": "2023-10-15T14:30:00Z"
}
```

## Support and Documentation

- **API Documentation**: https://docs.sql-learning-platform.com
- **Support**: support@sql-learning-platform.com
- **Status Page**: status.sql-learning-platform.com