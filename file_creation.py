import csv


def create_csv_files(data):
    with open('maze1.csv', mode='w') as maze_file:
        fieldnames = ['width', 'height', 'start_coord', 'end_coord', 'maze']
        writer = csv.DictWriter(maze_file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerow({
            'width': data['width'],
            'height': data['height'],
            'start_coord': data['start_coord'],
            'end_coord': data['end_coord'],
            'maze': data['maze']
            })
    maze_file.close()

    with open('maze1_stats.csv', mode='w') as stats_file:
        fieldnames = ['algo', 'route', 'steps', 'time']
        writer = csv.DictWriter(stats_file, fieldnames=fieldnames)
        stat_data = data['stats']

        writer.writeheader()
        for row, data in enumerate(stat_data):
            writer.writerow({
                'algo': stat_data[row]['algo'],
                'route': stat_data[row]['route'],
                'steps': stat_data[row]['steps'],
                'time': stat_data[row]['time']
                })