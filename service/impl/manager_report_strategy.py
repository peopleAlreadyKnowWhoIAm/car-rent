from io import BytesIO
from typing import List

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import calendar

from model.reservation import Reservation, ReservationStatus
from repository.basic_repository import BasicRepository
from service.report_strategy import ReportStrategy
from utils import plot_to_img


class ManagerReportStrategy(ReportStrategy):
    def create_report(self, car_repository: BasicRepository, reservation_repository: BasicRepository):
        reservations = reservation_repository.get_all_entities()
        available_reservations = list(
            filter(lambda reservation: reservation.status != ReservationStatus.CANCELED, reservations))
        completed_reservations = list(
            filter(lambda reservation: reservation.status == ReservationStatus.COMPLETED, reservations))
        return {
            "popular_months": self.__popular_months(available_reservations),
            "top_n_cars_by_reservations": self.__top_n_cars_by_reservations(car_repository, available_reservations,
                                                                            n=10),
            "avg_rental_duration": self.__avg_rental_duration(car_repository, available_reservations),
            "profitability_by_model": self.__profitability_by_model(car_repository, available_reservations),
            "profit_for_last_year": self.__profit_current_year(completed_reservations),
        }

    def __popular_months(self, reservations: List[Reservation]) -> BytesIO:
        data = [res.start_date for res in reservations]
        df = pd.DataFrame(data, columns=['start_date'])
        df['start_date'] = pd.to_datetime(df['start_date'])
        df['month'] = df['start_date'].dt.month
        availability = df.groupby('month').size()

        month_names = [calendar.month_name[i] for i in range(1, 13)]
        availability = availability.reindex(range(1, 13), fill_value=0)

        with sns.axes_style("darkgrid"):
            plt.figure(figsize=(10, 6))
            sns.barplot(x=month_names, y=availability.values, palette='viridis', hue=month_names, legend=False)
            plt.xlabel('Month', fontsize=12, fontweight='bold', color='black')
            plt.ylabel('Number of Reservations', fontsize=12, fontweight='bold', color='black')
            plt.title('Popular months for reserving', fontsize=14, fontweight='bold', color='black')
            plt.xticks(rotation=30)

        buf = plot_to_img(plt)
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

        with sns.axes_style("darkgrid"):
            plt.figure(figsize=(10, 6))
            sns.barplot(data=df_top_n_cars, x='model', y='total_reservations', hue='brand', palette='Set1')
            plt.xlabel('Car Model', fontsize=12, fontweight='bold', color='black')
            plt.ylabel('Number of Reservations', fontsize=12, fontweight='bold', color='black')
            plt.title('Top 10 Cars by Number of Reservations', fontsize=14, fontweight='bold', color='black')
            plt.xticks(rotation=45)

        buf = plot_to_img(plt)
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

        df['model'] = df['car_id'].map(lambda x: " ".join([car_details[x].brand, car_details[x].model]))

        with sns.axes_style("darkgrid"):
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

        df['model'] = df['car_id'].map(lambda x: " ".join([car_details[x].brand, car_details[x].model]))
        profitability = df.groupby('model')['total_profit'].sum().reset_index()

        plt.figure(figsize=(10, 6))
        ax = plt.subplot()
        ax.set_title('Profitability by Car Model', fontsize=14, fontweight='bold', color='black')
        ax.pie(profitability['total_profit'], labels=profitability['model'],
               autopct=lambda x: '{:.0f}$'.format(x * profitability['total_profit'].sum() / 100),
               startangle=140,
               colors=sns.color_palette("rocket", len(profitability)))

        buf = plot_to_img(plt)
        plt.clf()
        return buf

    def __profit_current_year(self, reservations: List[Reservation]):
        data = [(res.start_date, res.expected_profit) for res in reservations]
        df = pd.DataFrame(data, columns=['start_date', 'expected_profit'])
        df['start_date'] = pd.to_datetime(df['start_date'])
        df['month'] = df['start_date'].dt.month

        # Filter data for the current year
        current_year = df[df['start_date'].dt.year == df['start_date'].dt.year.max()]
        profit_by_month = current_year.groupby('month')['expected_profit'].sum()

        # Get month names
        month_names = [calendar.month_name[i] for i in range(1, 13)]
        profit_by_month = profit_by_month.reindex(range(1, 13), fill_value=0)

        with sns.axes_style("darkgrid"):
            plt.figure(figsize=(10, 6))
            sns.lineplot(x=month_names, y=profit_by_month.values, palette='Accent')
            plt.xlabel('Month', fontsize=12, fontweight='bold', color='black')
            plt.ylabel('Profit', fontsize=12, fontweight='bold', color='black')
            plt.title('Profit for Current Year', fontsize=14, fontweight='bold', color='black')
            plt.xticks(rotation=45)  # Rotate x-axis labels for better readability

        buf = plot_to_img(plt)
        plt.clf()
        return buf
