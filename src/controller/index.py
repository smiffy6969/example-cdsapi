from fastapi import FastAPI
from src.router import Route
import cdsapi
# import pygrib
import xarray;
import sqlite3
import numpy as np

def controller(app: FastAPI, route: Route):	
	@app.get(route.path)
	def get():
		conn = sqlite3.connect('temps.db')
		c = conn.cursor()
		c.execute('SELECT time, center_lat, center_lon, north, south, east, west, center FROM grid_temps ORDER BY time')
		rows = c.fetchall()
		conn.close()
		# Format as a list of dicts for JSON response
		result = [{
			"time": row[0],
			"center_lat": row[1],
			"center_lon": row[2],
			"north": row[3],
			"south": row[4],
			"east": row[5],
			"west": row[6],
			"center": row[7]
		} for row in rows]
		return result
	
	@app.post(route.path)
	def post():
		client = cdsapi.Client()
		
		dataset = 'reanalysis-era5-single-levels'
		request ={
			'product_type': 'reanalysis',
			'variable': '2m_temperature',
			'year': ['2025'],
			'month': ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'],
			'day': ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31'],
			'time': [
				'00:00', '01:00', '02:00', '03:00', '04:00', '05:00',
				'06:00', '07:00', '08:00', '09:00', '10:00', '11:00',
				'12:00', '13:00', '14:00', '15:00', '16:00', '17:00',
				'18:00', '19:00', '20:00', '21:00', '22:00', '23:00'
			],
			'format': 'grib',
			'area': [52, -1, 51, 0],  # [North, West, South, East]
		}
		
		target = 'download.grib'
		client.retrieve(dataset, request, target)

		ds = xarray.open_dataset('download.grib', engine='cfgrib')
		data_dict = ds.to_dict()
		store_grid_temps(data_dict)

	def store_grid_temps(data_dict, db_path='temps.db'):
		# Extract times, temperature data, and coordinates
		times = data_dict['coords']['time']['data']  # List of time strings
		temps = data_dict['data_vars']['t2m']['data']  # 3D list: [time][lat][lon]
		lats = data_dict['coords']['latitude']['data']  # List of latitude values
		lons = data_dict['coords']['longitude']['data']  # List of longitude values

		# Store in SQLite
		conn = sqlite3.connect(db_path)
		c = conn.cursor()
		c.execute('''
			CREATE TABLE IF NOT EXISTS grid_temps (
				time TEXT PRIMARY KEY,
				center_lat REAL,
				center_lon REAL,
				north REAL,
				south REAL,
				east REAL,
				west REAL,
				center REAL
			)
		''')

		# Insert each time's 5 temperature values with center coordinates
		for t_idx, temp_grid in enumerate(temps):
			c.execute('''
				INSERT OR REPLACE INTO grid_temps (
					time, center_lat, center_lon, north, south, east, west, center
				) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
			''', (
				times[t_idx],
				float(lats[4]),  # center latitude (middle of the 5x5 grid)
				float(lons[4]),  # center longitude (middle of the 5x5 grid)
				float(temp_grid[0][2]),  # north
				float(temp_grid[4][2]),  # south
				float(temp_grid[2][4]),  # east
				float(temp_grid[2][0]),  # west
				float(temp_grid[2][2])   # center
			))

		conn.commit()
		conn.close()

		return {"message": "data updated"};