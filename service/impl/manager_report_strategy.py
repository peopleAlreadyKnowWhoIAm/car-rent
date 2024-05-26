from io import BytesIO
from typing import List

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from model.reservation import Reservation
from repository.basic_repository import BasicRepository
from service.report_strategy import ReportStrategy
from utils import plot_to_img


class ManagerReportStrategy(ReportStrategy):
    def create_report(self, car_repository: BasicRepository, reservation_repository: BasicRepository):
        reservations = reservation_repository.get_all_entities()
        return {
            "car_availability": self.__car_availability(car_repository, reservations),
            "top_n_cars_by_reservations": self.__top_n_cars_by_reservations(car_repository, reservations, n=10),
            "avg_rental_duration": self.__avg_rental_duration(car_repository, reservations),
            "profitability_by_model": self.__profitability_by_model(car_repository, reservations),
        }

    def __car_availability(self, car_repository: BasicRepository, reservations: List[Reservation]) -> BytesIO:
        data = [(res.car_id, res.start_date) for res in reservations]
        df = pd.DataFrame(data, columns=['car_id', 'start_date'])

        df['start_date'] = pd.to_datetime(df['start_date'])
        df['month'] = df['start_date'].dt.to_period('M')

        availability = df.groupby(['car_id', 'month']).size().unstack(fill_value=0)

        car_brands = {}
        for car_id in availability.index:
            car = car_repository.get_entity_by_id(car_id)
            if car:
                car_brands[car_id] = car.brand

        availability['brand'] = availability.index.map(car_brands.get)
        availability = availability.groupby('brand').sum()

        plt.figure(figsize=(10, 6))
        sns.barplot(data=availability.T, palette='coolwarm')
        plt.xlabel('Month', fontsize=12, fontweight='bold', color='black')
        plt.ylabel('Number of Reservations', fontsize=12, fontweight='bold', color='black')
        plt.title('Car Availability Over Time by Brand', fontsize=14, fontweight='bold', color='black')

        buf = plot_to_img(plt)
        plt.show()
        plt.clf()
        return buf

    def __top_n_cars_by_reservations(self, car_repository: BasicRepository, reservations: List[Reservation], n: int):
        data = [(res.car_id, res.start_date) for res in reservations]
        df = pd.DataFrame(data, columns=['car_id', 'start_date'])

        df['start_date'] = pd.to_datetime(df['start_date'])
        df['month'] = df['start_date'].dt.to_period('M')

        availability = df.groupby(['car_id', 'month']).size().unstack(fill_value=0)
        availability['total_reservations'] = availability.sum(axis=1)

        top_n_cars = availability['total_reservations'].nlargest(n)

        top_n_car_details = {}
        for car_id in top_n_cars.index:
            car = car_repository.get_entity_by_id(car_id)
            if car:
                top_n_car_details[car_id] = car

        top_n_cars_data = [(car.model, car.brand, top_n_cars[car_id]) for car_id, car in top_n_car_details.items()]
        df_top_n_cars = pd.DataFrame(top_n_cars_data, columns=['model', 'brand', 'total_reservations'])

        plt.figure(figsize=(10, 6))
        sns.barplot(data=df_top_n_cars, x='model', y='total_reservations', hue='brand', palette='Set1')
        plt.xlabel('Car Model', fontsize=12, fontweight='bold', color='black')
        plt.ylabel('Number of Reservations', fontsize=12, fontweight='bold', color='black')
        plt.title('Top 10 Cars by Number of Reservations', fontsize=14, fontweight='bold', color='black')
        plt.xticks(rotation=45)

        buf = plot_to_img(plt)
        plt.show()
        plt.clf()
        return buf

    def __avg_rental_duration(self, car_repository: BasicRepository, reservations: List[Reservation]):
        data = [(res.car_id, res.start_date, res.end_date) for res in reservations]
        df = pd.DataFrame(data, columns=['car_id', 'start_date', 'end_date'])
        df['start_date'] = pd.to_datetime(df['start_date'])
        df['end_date'] = pd.to_datetime(df['end_date'])
        df['rental_duration'] = (df['end_date'] - df['start_date']).dt.days

        car_details = {}
        for car_id in df['car_id']:
            car = car_repository.get_entity_by_id(car_id)
            if car:
                car_details[car_id] = car

        df['model'] = df['car_id'].map(lambda x: car_details[x].model)

        plt.figure(figsize=(10, 6))
        avg_duration = df.groupby('model')['rental_duration'].mean()
        sns.barplot(x=avg_duration.index, y=avg_duration.values, palette='spring', hue=avg_duration.index, legend=False)
        plt.xlabel('Car Model', fontsize=12, fontweight='bold', color='black')
        plt.ylabel('Average Rental Duration, days', fontsize=12, fontweight='bold', color='black')
        plt.title('Average Rental Duration by Car Model', fontsize=14, fontweight='bold', color='black')

        buf = plot_to_img(plt)
        plt.clf()
        return buf

    def __profitability_by_model(self, car_repository: BasicRepository, reservations: List[Reservation]):
        data = [(res.car_id, res.expected_profit) for res in reservations]
        df = pd.DataFrame(data, columns=['car_id', 'expected_profit'])
        df['total_profit'] = df['expected_profit'].groupby(df['car_id']).transform('sum')

        car_details = {}
        for car_id in df['car_id']:
            car = car_repository.get_entity_by_id(car_id)
            if car:
                car_details[car_id] = car

        df['model'] = df['car_id'].map(lambda x: car_details[x].model)

        plt.figure(figsize=(10, 6))
        profitability = df.groupby('model')['total_profit'].sum()
        sns.barplot(x=profitability.index, y=profitability.values, palette='husl', hue=profitability.index,
                    legend=False)
        plt.xlabel('Car Model', fontsize=12, fontweight='bold', color='black')
        plt.ylabel('Total Profit, $', fontsize=12, fontweight='bold', color='black')
        plt.title('Profitability by Car Model', fontsize=14, fontweight='bold', color='black')

        buf = plot_to_img(plt)
        plt.clf()
        return buf
