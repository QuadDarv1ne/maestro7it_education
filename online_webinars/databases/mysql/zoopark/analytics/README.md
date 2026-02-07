# 📊 Advanced Analytics

This folder contains advanced analytical views and reports for the zoopark database system.

## 📁 Contents

- `advanced_analytics.sql` - Complex analytical views for business intelligence

## 📈 Available Analytics Views

### 1. animal_popularity_metrics
Provides metrics on animal popularity based on staff interactions (feeding frequency, medical visits).

### 2. employee_performance_metrics  
Analyzes employee performance based on their interactions with animals.

### 3. enclosure_utilization
Shows enclosure occupancy rates and species distribution.

### 4. cost_analysis
Provides cost estimates for animal care based on food consumption and medical procedures.

### 5. breeding_and_survival
Tracks breeding statistics and survival rates across species.

## 🔧 Usage

Execute the SQL file to create the analytical views:

```bash
mysql -u username -p animals_db < analytics/advanced_analytics.sql
```

Then query the views as needed for reporting and analysis.