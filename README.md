# Weather Location API

A FastAPI-based service that provides weather information based on IP addresses. The service integrates with IP geolocation and weather data providers to deliver accurate weather forecasts.

## Features

- IP-based location detection
- Weather forecasting
- Rate limiting
- Response caching
- Comprehensive error handling
- Health monitoring
- Docker support

## Prerequisites

- Python 3.8+
- Docker (optional)
- Git

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
WEATHER_API_KEY=your_weather_api_key
REDIS_URL=redis://localhost:6379
LOG_LEVEL=INFO
RATE_LIMIT_PER_MINUTE=60
```

## API Documentation

### Endpoints

#### GET /api/v1/weather/{ip}

Get weather information for a specific IP address.

**Parameters:**
- `ip` (string, required): Valid IPv4 or IPv6 address

**Response Format:**
```

json:README.md
{
"location": {
"city": "New York",
"country": "United States"
},
"weather": {
"temperature": 20.5,
"condition": "Clear",
"humidity": 65
}
}

json
{
"status": "healthy",
"timestamp": "2024-03-14T12:00:00Z",
"version": "1.0.0"
}
</rewritten_file>