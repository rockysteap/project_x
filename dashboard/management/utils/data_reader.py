class DataReader:
    path = 'dashboard/management/repo/'
    data, files = [], [
        'courses.txt',
        'subjects.txt',
        'schedule_grid.txt',
        'men_first_names.txt',
        'men_last_names.txt',
        'women_first_names.txt',
        'women_last_names.txt',
    ]

    def __init__(self):
        (self.courses,
         self.subjects,
         self.schedule_grid,
         self.men_first_names,
         self.men_last_names,
         self.women_first_names,
         self.women_last_names,
         ) = (None for _ in range(len(self.files)))
        self.read_all()

    def read_all(self):
        for file in self.files:
            with open(self.path + file, 'r', encoding='UTF-8') as f:
                file_data = []
                for line in f.readlines():
                    file_data.append(line.strip())
                self.data.append(file_data[:])
        (self.courses,
         self.subjects,
         self.schedule_grid,
         self.men_first_names,
         self.men_last_names,
         self.women_first_names,
         self.women_last_names
         ) = self.data
