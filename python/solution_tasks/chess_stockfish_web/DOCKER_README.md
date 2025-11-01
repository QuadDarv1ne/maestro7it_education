# Chess Stockfish Web - Docker Setup

This document explains how to run the Chess Stockfish Web application using Docker.

## Prerequisites

- Docker Engine 20.10+ installed
- Docker Compose 1.29+ installed

## Quick Start

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd chess_stockfish_web
   ```

2. Build and run the application:
   ```bash
   docker-compose up --build
   ```

3. Access the application at http://localhost:5001

## Services Overview

The docker-compose.yml file defines the following services:

1. **chess-app**: The main Flask application
2. **postgres**: PostgreSQL database for user and game data
3. **redis**: Redis cache for performance optimization

## Configuration

### Environment Variables

The application can be configured using environment variables:

- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string
- `SECRET_KEY`: Flask secret key for sessions

### Volumes

Data is persisted in named volumes:

- `postgres_data`: PostgreSQL data
- `redis_data`: Redis data

## Development Workflow

1. Make changes to the code
2. Rebuild the application:
   ```bash
   docker-compose build
   ```
3. Restart services:
   ```bash
   docker-compose up
   ```

## Production Deployment

For production deployment:

1. Update the docker-compose.yml file with production settings
2. Set secure passwords for database and Redis
3. Configure SSL termination (nginx, traefik, etc.)
4. Add monitoring and logging solutions

## Troubleshooting

### Common Issues

1. **Port already in use**: Change the port mapping in docker-compose.yml
2. **Insufficient permissions**: Ensure Docker has necessary permissions
3. **Build failures**: Check Dockerfile and requirements.txt

### Useful Commands

- View logs: `docker-compose logs -f`
- Stop services: `docker-compose down`
- Restart services: `docker-compose restart`
- Access container shell: `docker-compose exec chess-app sh`

## Data Management

### Backup

To backup the database:
```bash
docker-compose exec postgres pg_dump -U chessuser chessdb > backup.sql
```

### Restore

To restore the database:
```bash
docker-compose exec -T postgres psql -U chessuser chessdb < backup.sql
```

## Scaling

To scale the application:
```bash
docker-compose up --scale chess-app=3
```

Note: You'll need to add a load balancer for proper scaling.

## Customization

### Adding Dependencies

1. Add new packages to requirements.txt
2. Rebuild the image: `docker-compose build`

### Customizing the Database

1. Modify the postgres service in docker-compose.yml
2. Update environment variables as needed

## Security Considerations

1. Change default passwords in docker-compose.yml
2. Use Docker secrets for sensitive data in production
3. Keep base images updated
4. Scan images for vulnerabilities