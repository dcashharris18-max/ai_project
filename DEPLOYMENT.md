# AI Marketplace - Production Deployment

## Pre-Deployment Checklist

- [ ] Security audit (OWASP Top 10)
- [ ] Load testing (k6, JMeter)
- [ ] Database backup strategy
- [ ] Monitoring setup (Prometheus, Grafana)
- [ ] Alerting configured
- [ ] Incident response plan
- [ ] Legal/compliance review
- [ ] Privacy policy & ToS published
- [ ] Rate limiting & DDoS protection
- [ ] API versioning strategy

## Cloud Deployment Options

### AWS (Recommended)

**Architecture**:
- ECS Fargate for containers
- RDS Postgres for database
- ElastiCache Redis for cache
- S3 for media storage
- CloudFront for CDN
- Route53 for DNS
- WAF for DDoS protection

**Deployment Steps**:
1. Push Docker image to ECR
2. Create ECS cluster and service
3. Configure RDS endpoint
4. Set security groups & VPC
5. Setup CloudFront distribution
6. Configure domain with Route53

**Terraform Example**:
```hcl
resource "aws_ecs_service" "backend" {
  name            = "ai-marketplace-backend"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.backend.arn
  desired_count   = 3
  
  load_balancer {
    target_group_arn = aws_lb_target_group.backend.arn
    container_name   = "backend"
    container_port   = 8000
  }
}
```

### Google Cloud (Alternative)

**Services**:
- Cloud Run for serverless backend
- Cloud SQL for PostgreSQL
- Memorystore for Redis
- Cloud Storage for media
- Cloud CDN for distribution

### Azure (Alternative)

**Services**:
- Container Instances or App Service
- Azure Database for PostgreSQL
- Azure Cache for Redis
- Blob Storage for media
- CDN for distribution

## Environment-Specific Configs

### Production (.env.prod)
```
DATABASE_URL=postgresql://user:strongpass@prod-db.example.com:5432/ai_prod
SECRET_KEY=<generated-strong-key>
ENVIRONMENT=production
DEBUG=false
ALLOWED_HOSTS=api.example.com,www.example.com
STRIPE_API_KEY=sk_live_...
CCXT_EXCHANGE=binance
LOG_LEVEL=INFO
```

### Staging (.env.staging)
```
DATABASE_URL=postgresql://user:pass@staging-db.example.com:5432/ai_staging
SECRET_KEY=<strong-key>
ENVIRONMENT=staging
DEBUG=true
STRIPE_API_KEY=sk_test_...
LOG_LEVEL=DEBUG
```

## CI/CD Pipeline (GitHub Actions Example)

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run tests
        run: |
          cd backend
          pip install -r requirements.txt
          pytest tests/

  build-push:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Build and push Docker image
        run: |
          docker build -t ai-marketplace-backend:${{ github.sha }} ./backend
          docker push ai-marketplace-backend:${{ github.sha }}

  deploy:
    needs: build-push
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to production
        run: |
          # kubectl set image deployment/backend backend=ai-marketplace-backend:${{ github.sha }}
```

## Monitoring & Observability

### Metrics to Track
- API response time (p50, p95, p99)
- Error rate (4xx, 5xx)
- Database query latency
- Wallet transactions volume
- Active users
- Marketplace GMV (Gross Merchandise Volume)

### Logging Strategy
```python
# Example: structured logging
import logging
logger = logging.getLogger(__name__)

logger.info('User login', extra={
    'user_id': user.id,
    'timestamp': datetime.utcnow(),
    'ip': request.client.host
})
```

### Alerting Rules
- Backend response time > 5s
- Error rate > 5%
- Database connection pool exhausted
- Redis cache failures
- Disk space < 10%
- Certificate expiring in 30 days

## Security Hardening

### Network
- Enable VPN for database access
- Use security groups/firewall
- Enable WAF rules
- Rate limiting per IP

### Application
- Input validation & sanitization
- SQL injection prevention (SQLAlchemy ORM)
- XSS protection (React built-in)
- CSRF tokens for state-changing endpoints
- API key rotation strategy
- JWT secret rotation

### Data
- Encrypt sensitive data at rest
- TLS/SSL for all connections
- Database encryption
- Backup encryption
- PII data masking in logs

### Compliance
- GDPR: Data subject requests, right to deletion
- PCI DSS: Credit card handling (use Stripe)
- AML/KYC: Enhanced due diligence
- Audit trails: All transactions logged

## Disaster Recovery

### Backup Strategy
```bash
# Daily database backup
0 2 * * * pg_dump -h prod-db.example.com -U postgres ai_prod | gzip > /backups/ai_prod_$(date +%Y%m%d).sql.gz

# S3 backup
aws s3 sync /backups/ s3://ai-marketplace-backups/ --delete
```

### Recovery Time Objective (RTO): 1 hour
### Recovery Point Objective (RPO): 6 hours

## Scaling Strategy

### Horizontal Scaling
- Load balance backend across 3+ instances
- Database read replicas
- Redis cluster mode for high availability

### Vertical Scaling
- Increase container memory/CPU
- Database instance size
- Cache size

### Performance Optimization
- Database indexing (add on frequently queried columns)
- Query optimization
- Caching strategy (Redis)
- CDN for static assets
- Image optimization

## Cost Estimation (AWS)

| Component | Estimate |
|-----------|----------|
| ECS Fargate (3x 1CPU, 2GB) | $100/month |
| RDS PostgreSQL (2CPU, 20GB) | $200/month |
| ElastiCache Redis (1GB) | $50/month |
| S3 Storage (100GB) | $25/month |
| CloudFront (1TB/month) | $85/month |
| Total | **~$460/month** |

*Adjust based on traffic and requirements*

## Rollout Strategy

### Blue-Green Deployment
1. Deploy new version to "green" environment
2. Run smoke tests
3. Switch traffic to green
4. Keep blue for quick rollback

### Canary Deployment
1. Route 10% traffic to new version
2. Monitor metrics
3. Gradually increase to 100%
4. Roll back if issues detected

## Post-Deployment Verification

```bash
# Health check
curl -s https://api.example.com/health | jq .

# Database connectivity
psql -h prod-db.example.com -U postgres -d ai_prod -c "SELECT VERSION();"

# Cache connectivity
redis-cli -h cache.example.com PING

# SSL certificate
openssl s_client -connect api.example.com:443 -showcerts

# Performance test
ab -n 1000 -c 100 https://api.example.com/
```

## Ongoing Maintenance

- Weekly: Monitor logs for errors
- Monthly: Review metrics and performance
- Quarterly: Security patches and updates
- Annually: Compliance audit and penetration test
