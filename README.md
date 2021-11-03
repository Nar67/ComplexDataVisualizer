# ComplexDataVisualizer

This is the work of my bachelor thesis. The goal of the project is to enable the visualization of high dimensional datasets using six different dimensionality reduction methods. It allows the user to upload a dataset and to reduce the dimensionality of it to analyse it. The user can upload either a numerical, categorical or mixed (both numerical and categorical) dataset, as well as managing missing values.

The methods available are:
  - Principal Component Analysis
  - Linear Discriminant Analysis
  - Multiple Correspondence Analysis
  - Kernel Principal Component Analysis
  - t-Distributed Stochastic Neighbor Embedding
  - Multi-Dimensional Scaling

The app is created using [Dash](https://dash.plotly.com/).

# Build


```
docker-compose build
```


# Run

```
docker-compose up
```
