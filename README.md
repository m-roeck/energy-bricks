<h1 align="center">
	<img
		width="300"
		alt="The Lounge"
		src="assets/visuals/logoo.png">
</h1>

<h3 align="center">
	Measuring wholesale energy market exposure, NEISO
</h3>

<p align="center">
	<strong>
		<a href="https://m.roeck-us.net">App</a>
		•
		<a href="https://www.iso-ne.com/isoexpress/web/charts">Data</a>
		•
		<a href="">Contact</a>
	</strong>
</p>

<p align="center">
	<a href="https://demo.thelounge.chat/"><img
		alt="#thelounge IRC channel on Libera.Chat"
		src="https://img.shields.io/badge/Libera.Chat-%23thelounge-415364.svg?colorA=ff9e18"></a>
	<a href="https://yarn.pm/thelounge"><img
		alt="npm version"
		src="https://img.shields.io/npm/v/thelounge.svg?colorA=333a41&maxAge=3600"></a>
	<a href="https://github.com/thelounge/thelounge/actions"><img
		alt="Build Status"
		src="https://github.com/thelounge/thelounge/workflows/Build/badge.svg"></a>
</p>

<p align="center">
	<img src="assets/visuals/app_capture.png" width="550">
</p>


## Overview
Energy Bricks is a simple framework for analyzing wholesale energy market risk exposure. The tool utilizes day-ahead Locational Marginal Price forecasting to identify hours with high price and market exposure. To-date the tool is built for NEISO, and utilizes several different regression and ML models for forecasting.

Features include:

* Day-Ahead Locational Marginal Pricing, used to inform hourly risk and cost management strategies.
* Visualization of wholesale prices against forecasts, utilizing model validation data.
* Trained regression and machine learning pipelines for nodal price forecasting in NEISO.

## Data Pipeline

The following visual describes the data pipeline utilized for the forecast and consequent risk management visualization.

<p align="center">
	<img src="assets/visuals/data_pipeline.png" width="800">
</p>

In order to address underlying uncertainties in the input data, the framework utilizes multiple forecasts, which in turn produce a range of potential outcomes. In conjuction, the models componesate for different sets of uncertainties, and in combination captures the extreme pricing events which the tool is designed to identify.