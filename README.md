# Heat Acclimatisation Analysis

Does regular training in hot weather improve heart rate efficiency over
time compared to training in cool conditions?

Analysis of the EndoMondo fitness dataset (Ni, Muhlstein & McAuley, 2019)
using Python, pandas and Dask across 38,988 workouts from 855 users.

## Findings

- 95.8% of hot-weather trainers improved heart rate efficiency over their
  workout history, versus 77.8% of cool-weather trainers.
- 94 users improved specifically in hot weather but not cool, against only
  15 the other way — a 6:1 ratio.
- Frequent itemset mining showed most users train in both conditions, so
  the comparison is largely within-subject rather than between two
  different populations.

Full write-up: [MaxBlockley_DATA301_Project.pdf](report.pdf)

## Method

Heart rate efficiency = `avg_speed / avg_heart_rate`. Higher means more
speed per unit of cardiac effort.

1. Preprocessing — parse gzipped JSON line by line, drop workouts with
   no weather data, compute per-workout efficiency, filter outliers.
2. Cleaning — merge bike/bike-transport, keep run/bike/walk, drop users
   with fewer than 20 workouts per sport, label each workout hot or cool
   from AccuWeather condition codes.
3. Frequent itemsets — Dask Bag `map`/`flatten`/`frequencies` to find
   common sport-weather pairs per user.
4. Rolling averages — Dask `map_partitions` for a 10-workout rolling
   mean of efficiency per user.
5. Clustering — users grouped as hot, mixed or cool trainers by their
   proportion of hot-weather workouts.
6. Set operations — union, intersection and difference over the sets of
   users who improved in each condition.

## Data

Requires `endomondoMeta.json.gz` and `endomondoHR.json.gz` from the
[EndoMondo dataset](https://cseweb.ucsd.edu/~jmcauley/pdfs/www19.pdf).
Not included here due to size. 

## Running

```bash
pip install -r requirements.txt
python preprocess.py     # writes meta_cleaned.csv and hr_cleaned.csv
jupyter notebook project.ipynb
```

Preprocessing takes roughly an hour on the raw files — it only needs to be
run once. The notebook reads the cleaned CSVs.



## Limitations

Weather is collapsed into two categories, so a mild sunny day and an
extreme one are treated identically; actual temperature values would allow
a graded analysis. Rolling averages are computed across all workouts rather
than separately per weather condition, meaning a user's score reflects
overall fitness rather than condition-specific fitness. Workout intensity
and duration are not controlled for.

## References

Ni, J., Muhlstein, L., & McAuley, J. (2019). *Modeling heart rate and
activity data for personalized fitness recommendation.* WWW.

Périard, J. D., Racinais, S., & Sawka, M. N. (2015). *Adaptations and
mechanisms of human heat acclimatization.* Scand J Med Sci Sports, 25(S1).
