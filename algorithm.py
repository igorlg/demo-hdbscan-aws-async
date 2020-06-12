def calculate_cluster(data, n_points, algo='OPTICS'):
    print('Filtering {} points of data'.format(n_points))
    coords = data.loc[1:n_points, ['Latitude', 'Longitude']].values

    print('Starting {} algo object', algo)
    if algo == 'OPTICS':
        clustering = OPTICS(min_samples=5)
    elif algo == 'HDBSCAN':
        clustering = HDBSCAN(algorithm='best',
                             alpha=1.0, leaf_size=40,
                             min_cluster_size=5, min_samples=5, p=None,
                             approx_min_span_tree=True, gen_min_span_tree=True,
                             metric='haversine'
                             )
    else:
        clustering = None

    print('Running fit_predict on {} data points with algo {}'.format(n_points, algo))
    clustering.fit_predict(coords)
    put_metric(algo, 'fit_predict', n_points, int(L.ts() - L.lastop))

    print('Getting labels from clustering')
    cluster_labels = clustering.labels_

    print('Getting # of Clusters')
    num_clusters = len(set(cluster_labels))

    print('Generating data series w/ Pandas for {} clusters'.format(num_clusters))
    clusters = pd.Series([coords[cluster_labels == n] for n in range(num_clusters)])

    print('Filtering out clusters with len <= 0')
    clusters = clusters[clusters.apply(len) > 0]

    print('Generating map of clusters')
    clmap = clusters.map(get_centermost_point)
    return clmap


def gen_results(centermost_points, csv_file, title):
    print('gen_image_file(): csv_file={}'.format(csv_file))
    print('Getting lats, lons')
    lats, lons = zip(*centermost_points)

    print('Getting Pandas DataFrame')
    rep_points = pd.DataFrame({'lon': lons, 'lat': lats})

    print('Splitting points into Lat/Lon')
    rs = rep_points.apply(lambda row: df[(df['Latitude'] == row['lat']) & (df['Longitude'] == row['lon'])].iloc[0], axis=1)

    print('Saving result points to {}'.format(csv_file))
    rs.to_csv(csv_file, encoding='utf-8')
