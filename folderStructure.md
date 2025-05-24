# Momentum Projesi Dosya Yapısı

Bu belge, Momentum uygulamasının klasör ve dosya yapısını özetlemektedir.

```
momentum/
├── docs/                           # Proje belgeleri
├── src/                            # Kaynak kodlar
│   ├── core/                       # Ana uygulama mantığı
│   │   ├── databaseManagement      # DB CRUD işlemleri barındırır
│   │   │   ├── createFakeData.py   # veritabanına fake veriler ekler
│   │   │   ├── crudPomodoro.py     # pomodoro bilgileri için db crud işlemleri
│   │   │   ├── crudSettings.py     # kullanıcı bilgileri için db crud işlemleri
│   │   │   └── crudTask.py         # task tablosu için db crud işlemleri
│   │   ├── calendar.py
│   │   ├── welcome.py
│   │   ├── editStudy.py
│   │   ├── editTasks.py
│   │   ├── pomodoro.py
│   │   ├── profile.py
│   │   └── tasks.py
│   ├── data/                       # Uygulama verileri
│   │   ├── momentum_database.db    # SQLite veritabanı
│   ├── styles/                     # QSS stil dosyaları
│   │   ├── calendar.qss
│   │   ├── welcome.qss
│   │   ├── editStudy.qss
│   │   ├── editTasks.qss
│   │   ├── pomodoro.qss
│   │   ├── profile.qss
│   │   └── tasks.qss
│   └── ui/                         # Kullanıcı arayüzü ile ilgili dosyalar
│       ├── forms/                  # PyQt Designer ile oluşturulan .ui dosyaları
│       │   ├── calender.ui
│       │   ├── welcome.ui
│       │   ├── editStudy.ui
│       │   ├── editTasks.ui
│       │   ├── pomodoro.ui
│       │   ├── profile.ui
│       │   └── tasks.ui
│       ├── generated/              # .ui dosyalarından otomatik oluşturulan .py dosyaları
│       │   ├── calender.py
│       │   ├── welcome.py
│       │   ├── editStudy.py
│       │   ├── editTasks.py
│       │   ├── pomodoro.py
│       │   ├── profile.py
│       │   └── tasks.py
│       └── icons/                  # İkonlar ve kaynak dosyaları
│           ├── generated/          # .qrc dosyasından otomatik oluşturulan Python modülü
│           │   └── icons_rc.py
│           ├── resources/          # İkon png dosyaları
│           │   ├── calenderDark.png
│           │   ├── calenderBeige.png
│           │   ├── ...
│           │   ├── sort.png
│           │   ├── taskDark.png
│           │   └── taskBeige.png
│           └── icons.qrc           # Qt Kaynak Dosyası (ikonları derlemek için)
├── main.py                         # Uygulamanın ana giriş noktası
├── README.md                       # Proje hakkında genel bilgiler
└── requirements.txt                # Proje bağımlılıkları
``` 