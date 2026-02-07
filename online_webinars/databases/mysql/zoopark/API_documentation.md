# API Documentation for Zoo Animals Database

## Overview

This RESTful API provides programmatic access to the zoo animals database, allowing external applications to interact with animal records, feeding schedules, medical records, and other related data.

## Base URL

```
https://api.zoopark.example.com/v1
```

## Authentication

All API requests require an API key to be sent in the header:

```
Authorization: Bearer {your_api_key}
```

## Common Headers

- `Content-Type: application/json`
- `Accept: application/json`

## Error Responses

All error responses follow the same format:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": "Additional error details if available"
  }
}
```

## Endpoints

### Animals

#### Get all animals

```
GET /animals
```

**Parameters:**
- `limit` (optional): Number of records to return (default: 50, max: 100)
- `offset` (optional): Number of records to skip (default: 0)
- `species` (optional): Filter by species name
- `enclosure` (optional): Filter by enclosure name
- `health_status` (optional): Filter by health status

**Response:**
```json
{
  "data": [
    {
      "id": 1,
      "name": "Simba",
      "species": "Lion",
      "latin_name": "Panthera leo",
      "class": "Mammal",
      "conservation_status": "VU",
      "gender": "male",
      "birth_date": "2019-06-15",
      "age_years": 4,
      "health_status": "healthy",
      "arrival_date": "2020-03-10",
      "enclosure_name": "Lion Enclosure",
      "enclosure_type": "Outdoor with shelters"
    }
  ],
  "pagination": {
    "total": 15,
    "limit": 50,
    "offset": 0
  }
}
```

#### Get specific animal by ID

```
GET /animals/{id}
```

**Response:**
```json
{
  "data": {
    "id": 1,
    "name": "Simba",
    "species": "Lion",
    "latin_name": "Panthera leo",
    "class": "Mammal",
    "conservation_status": "VU",
    "gender": "male",
    "birth_date": "2019-06-15",
    "age_years": 4,
    "health_status": "healthy",
    "arrival_date": "2020-03-10",
    "enclosure_name": "Lion Enclosure",
    "enclosure_type": "Outdoor with shelters",
    "mother_name": null,
    "father_name": null,
    "last_feeding_date": "2024-02-07",
    "last_medical_check": "2024-01-15"
  }
}
```

#### Add new animal

```
POST /animals
```

**Request body:**
```json
{
  "name": "New Animal Name",
  "species_id": 1,
  "birth_date": "2024-01-01",
  "gender": "male",
  "health_status": "healthy",
  "arrival_date": "2024-02-01",
  "enclosure_id": 1,
  "mother_id": null,
  "father_id": null
}
```

**Response:**
```json
{
  "data": {
    "id": 16,
    "name": "New Animal Name",
    "species_id": 1,
    "birth_date": "2024-01-01",
    "gender": "male",
    "health_status": "healthy",
    "arrival_date": "2024-02-01",
    "enclosure_id": 1,
    "mother_id": null,
    "father_id": null
  },
  "message": "Animal created successfully"
}
```

### Species

#### Get all species

```
GET /species
```

**Response:**
```json
{
  "data": [
    {
      "id": 1,
      "name": "Lion",
      "latin_name": "Panthera leo",
      "class": "Mammal",
      "conservation_status": "VU",
      "description": "Large cat living in prides"
    }
  ]
}
```

### Enclosures

#### Get all enclosures

```
GET /enclosures
```

**Response:**
```json
{
  "data": [
    {
      "id": 1,
      "name": "Lion Enclosure",
      "type": "Outdoor with shelters",
      "area": 600.00,
      "capacity": 6,
      "temperature_range": "+15°C to +30°C",
      "humidity_range": "30-50%",
      "current_animals": 2,
      "species_list": "Lion",
      "responsible_employee": "Alexey Kozlov",
      "position": "Keeper"
    }
  ]
}
```

### Feedings

#### Get today's feeding schedule

```
GET /feedings/today
```

**Response:**
```json
{
  "data": [
    {
      "id": 1,
      "animal_name": "Simba",
      "species": "Lion",
      "feeding_time": "09:00:00",
      "food_type": "Meat, chicken, vitamins",
      "quantity": "5 kg",
      "employee_name": "Ivan Petrov",
      "position": "Zookeeper",
      "notes": "Main feeding"
    }
  ]
}
```

#### Add feeding record

```
POST /feedings
```

**Request body:**
```json
{
  "animal_id": 1,
  "employee_id": 1,
  "food_type": "Special diet",
  "quantity": "2 kg",
  "feeding_time": "10:30:00",
  "feeding_date": "2024-02-07",
  "notes": "Following dietary restrictions"
}
```

### Medical Records

#### Get animal's medical history

```
GET /medical-history/{animal_id}
```

**Response:**
```json
{
  "data": [
    {
      "id": 1,
      "animal_name": "Simba",
      "species": "Lion",
      "record_date": "2024-01-15",
      "diagnosis": "Routine checkup",
      "treatment": "Vaccination, dental check",
      "medication": "Rabies vaccine",
      "next_checkup": "2024-07-15",
      "veterinarian": "Maria Sidorova",
      "position": "Veterinary doctor"
    }
  ]
}
```

### Vaccinations

#### Get vaccination due list

```
GET /vaccinations/due
```

**Response:**
```json
{
  "data": [
    {
      "animal_name": "Simba",
      "species": "Lion",
      "vaccine_name": "Rabies vaccine",
      "vaccination_date": "2023-10-15",
      "expiration_date": "2024-10-15",
      "status": "DUE SOON"
    }
  ]
}
```

### Health Reports

#### Get daily health report

```
GET /reports/daily-health
```

**Response:**
```json
{
  "data": [
    {
      "animal_name": "Simba",
      "species": "Lion",
      "health_status": "healthy",
      "last_checkup": "2024-01-15",
      "last_vaccination_expiry": "2024-10-15",
      "status_comment": "NORMAL"
    }
  ]
}
```

## Status Codes

- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Resource Not Found
- `500` - Internal Server Error

## Rate Limiting

API requests are limited to 1000 requests per hour per API key. Exceeding this limit will result in a `429 Too Many Requests` response.

## Versioning

This API uses versioning in the URL path. Current version is v1. Future versions will be released as `/v2`, `/v3`, etc. with appropriate migration guides.