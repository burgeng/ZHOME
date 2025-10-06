# Zillow Housing Overview and Market Explorer (ZHOME)
Easily explore housing market data from [Zillow](https://www.zillow.com/research/data/).

## Try the app at [zhome.casa](https://www.zhome.casa)

### Zillow Home Value Index
<img src="react-flask-app/public/zhvi.gif" width="750" alt="Demo GIF">

### Zillow Home Value Forecast
<img src="react-flask-app/public/zhvf.gif" width="750" alt="Demo GIF">

## Implementation
Frontend: React (create-react-app), Chart.js \
Backend: Python (Flask, Gunicorn) \
Database: MySQL (AWS RDS) \
Infrastructure: Nginx reverse proxy, Let’s Encrypt SSL, Ubuntu 22.04 on AWS EC2 \
DevOps: GitHub Actions CI/CD, Certbot for auto-renewal \
