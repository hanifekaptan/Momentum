# Momentum: Zaman Yönetimi ve Verimlilik Uygulaması

Momentum, kullanıcıların görevlerini ve zamanlarını etkin bir şekilde yönetmelerine yardımcı olmak için tasarlanmış kapsamlı bir zaman yönetimi uygulamasıdır. Uygulama, kişisel üretkenliği artırmayı hedefleyen bir görevlendirme ve ajanda mantığı ile çalışır. Ayrıca, popüler Pomodoro Tekniği'ni entegre ederek odaklanmış çalışma süreleri sunar. Python programlama dili ile geliştirilmiş olup, kullanıcı arayüzü için PyQt5, veri depolama için SQLite ve stil için QSS kullanılmıştır.

## Dosya Yapısı

```
momentum-time-manager/
├── src/
│   ├── core/
│   │   ├── databaseManagement
│   │   │   ├── createFakeData.py
│   │   │   ├── crudPomodoro.py
│   │   │   ├── crudSettings.py
│   │   │   └── crudTask.py
│   │   ├── calendar.py
│   │   ├── welcome.py
│   │   ├── editStudy.py
│   │   ├── editTasks.py
│   │   ├── pomodoro.py
│   │   ├── profile.py
│   │   └── tasks.py
│   ├── data/
│   │   ├── momentum_database.db
│   ├── styles/
│   │   ├── calendar.qss
│   │   ├── welcome.qss
│   │   ├── editStudy.qss
│   │   ├── editTasks.qss
│   │   ├── pomodoro.qss
│   │   ├── profile.qss
│   │   └── tasks.qss
│   └── ui/
│       ├── forms/
│       │   ├── calender.ui
│       │   ├── welcome.ui
│       │   ├── editStudy.ui
│       │   ├── editTasks.ui
│       │   ├── pomodoro.ui
│       │   ├── profile.ui
│       │   └── tasks.ui
│       ├── generated/
│       │   ├── calender.py
│       │   ├── welcome.py
│       │   ├── editStudy.py
│       │   ├── editTasks.py
│       │   ├── pomodoro.py
│       │   ├── profile.py
│       │   └── tasks.py
│       └── icons/
│           ├── generated/
│           │   └── icons_rc.py
│           ├── resources/
│           │   ├── calenderDark.png
│           │   ├── calenderBeige.png
│           │   ├── ...
│           │   ├── sort.png
│           │   ├── taskDark.png
│           │   └── taskBeige.png
│           └── icons.qrc
├── main.py
├── README.md
└── requirements.txt
```

## Özellikler

*   **Görev Yönetimi:** Kullanıcılar, görevlerini ekleyebilir, düzenleyebilir, tamamlandı olarak işaretleyebilir ve önceliklerini belirleyebilir. Bu sayede yapılacaklar listeleri her zaman güncel kalır.
*   **Ajanda ve Takvim Entegrasyonu:** Uygulama, görevleri bir takvim ve ajanda görünümünde sergileyerek kullanıcıların programlarını görselleştirmesine yardımcı olur. Belirli tarihlere atanan görevler kolayca takip edilebilir.
*   **Pomodoro Zaman Yönetimi:** Üretkenliği artırmak için Pomodoro Tekniği entegre edilmiştir. Kullanıcılar, odaklanmış çalışma seansları (örneğin 25 dakika) ve kısa molalar (örneğin 5 dakika) arasında geçiş yaparak dikkat dağınıklığını en aza indirebilir ve verimliliklerini artırabilir.
*   **Performans Analizi:** Kullanıcı verilerine dayanarak çalışma düzeni, görev ve başarı oranlarına ilişkin analizler sunarak performansın takip edilip değerlendirilmesine katkı sağlar.
*   **Kullanıcı Dostu Arayüz:** PyQt5 ile geliştirilen modern ve sezgisel arayüz, uygulamanın kolayca kullanılmasını sağlar.
*   **Veri Kalıcılığı:** Tüm görevler, Pomodoro kayıtları ve kullanıcı ayarları, hafif ve güvenilir bir ilişkisel veritabanı olan SQLite üzerinde güvenli bir şekilde saklanır. Bu, verilerin uygulama kapatıldıktan sonra bile korunmasını sağlar.

**Kullanılan Teknolojiler:**

*   **Python:** Uygulamanın ana geliştirme dilidir. Hızlı prototipleme, geniş kütüphane desteği ve okunabilir sözdizimi sayesinde uygulamanın temel mantığı bu dil ile inşa edilmiştir.
*   **PyQt5:** Python için Qt kütüphanesinin bir bağlayıcısıdır. Çapraz platform masaüstü uygulamaları geliştirmek için güçlü ve esnek bir GUI araç takımı sağlar. Momentum'un tüm görsel arayüz elemanları PyQt5 ile tasarlanmıştır.
*   **SQLite:** Uygulama içi veri depolama için kullanılan hafif, sunucusuz bir ilişkisel veritabanı sistemidir. Uygulamanın görevleri, Pomodoro seansları, kullanıcı ayarları gibi tüm verileri `momentum_database.db` dosyasında saklanır.
*   **QSS (Qt Style Sheets):** Qt tabanlı uygulamaların görünümünü CSS benzeri bir sözdizimi ile özelleştirmek için kullanılır. Momentum'un arayüz temaları ve stil özellikleri QSS dosyaları aracılığıyla yönetilir.

## Uygulama Görselleri

![welcome](https://github.com/user-attachments/assets/b52b62d5-24d0-4b64-a3c1-27a1d6bf056c)
![tasks](https://github.com/user-attachments/assets/1b8e22ef-f3a1-439b-903d-799d9d9a7124)
![editTask](https://github.com/user-attachments/assets/fdbf2996-3c3d-4b74-b033-f2d218d67ff4)
![calendar](https://github.com/user-attachments/assets/18f6d44b-fca5-4dbf-987c-653d0936abd5)
![pomodoro](https://github.com/user-attachments/assets/2a76c7c3-6eb8-41e8-9360-18b15b237d48)
![editStudy](https://github.com/user-attachments/assets/d6eac9ae-a787-4444-9a52-ac3ce397e240)
![profile](https://github.com/user-attachments/assets/1bf2b452-732c-458a-969b-8ce5dcb53048)

## Uygulama Kurulumu

Uygulamayı yerel makinenizde çalıştırmak için aşağıdaki adımları izleyin:

1.  **Depoyu Klonlayın:**

    ```bash
    git clone https://github.com/hanifekaptan/momentum-time-manager.git
    cd momentum-time-manager
    ```

2.  **Sanal Ortam Oluşturun:**

    ```bash
    python -m venv momentum
    ```

3.  **Sanal Ortamı Aktive Edin:**

    *   Windows:

        ```bash
        .\momentum\Scripts\activate
        ```

    *   macOS/Linux:

        ```bash
        source momentum/bin/activate
        ```

4.  **Bağımlılıkları Yükleyin:**

    ```bash
    pip install -r requirements.txt
    ```

5.  **Uygulamayı Çalıştırın:**

    ```bash
    python main.py
    ```

## 6. İletişim

Herhangi bir soru, geri bildirim veya işbirliği teklifi için benimle iletişime geçmekten çekinmeyin:

[LinkedIn](https://www.linkedin.com/in/hanifekaptan) [E-Posta](mailto:hanifekaptan.dev@gmail.com) 
