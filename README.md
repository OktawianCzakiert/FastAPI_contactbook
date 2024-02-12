# Database PostgreSQL
POSTGRES_DB=

POSTGRES_USER=

POSTGRES_PASSWORD=

POSTGRES_PORT=

SQLALCHEMY_DATABASE_URL=postgresql+psycopg2://${POSTGRES_USER}:${POSTGRES_PASSWORD}@localhost:${POSTGRES_PORT}/${POSTGRES_DB}

# JWT authentication
SCHEME=

SECRET_KEY=

ALGORITHM=

# Email service
MAIL_USERNAME=

MAIL_PASSWORD=

MAIL_FROM=

MAIL_PORT=

MAIL_SERVER=

# Redis
REDIS_HOST=

REDIS_PORT=

# Cloud Storage
CLOUDINARY_NAME=

CLOUDINARY_API_KEY=

CLOUDINARY_API_SECRET=




# Start application by below command
docker-compose --project-directory ./src/conf up -d
