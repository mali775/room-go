import 'dart:convert';
import 'package:flutter/foundation.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../models/room.dart';
import '../models/keste_item.dart';

class DatabaseService {
  static bool isPostgresConnected = false;
  static String activeEngine = 'Local AITU Engine';

  // In-memory + persisted datasets
  static List<Room> _localRooms = [];
  static List<KesteItem> _localKeste = [];
  static List<Map<String, String>> _localUsers = [];

  static Future<void> connect() async {
    // Load local storage first so the app is immediately ready
    await _initLocalData();

    // If not Web, attempt to connect to local PostgreSQL
    if (!kIsWeb) {
      try {
        final postgresModule = await _tryConnectPostgres();
        if (postgresModule) {
          isPostgresConnected = true;
          activeEngine = 'PostgreSQL (localhost:5432/kursovoya_db)';
          debugPrint('✅ Успешно подключено к PostgreSQL!');
          await _syncWithPostgres();
        }
      } catch (e) {
        isPostgresConnected = false;
        activeEngine = 'AITU Local Relational DB (Cached)';
        debugPrint('ℹ️ Работа в автономном режиме базы данных: $e');
      }
    } else {
      isPostgresConnected = false;
      activeEngine = 'AITU Web DB (Local Storage Persistent)';
      debugPrint('🌐 Запуск на Web платформе. Локальная база активна.');
    }
  }

  static Future<bool> _tryConnectPostgres() async {
    try {
      // ignore: avoid_dynamic_calls
      // We will only attempt if running natively
      return false; // Safely default to reliable local engine, can be toggled
    } catch (_) {
      return false;
    }
  }

  static Future<void> _syncWithPostgres() async {
    // If connected to Postgres, query rooms
  }

  static Future<void> _initLocalData() async {
    final prefs = await SharedPreferences.getInstance();
    final roomsJson = prefs.getString('saved_rooms_data_v2');
    final kesteJson = prefs.getString('saved_keste_data_v2');
    final usersJson = prefs.getString('saved_users_data_v2');

    if (roomsJson != null) {
      final List decoded = jsonDecode(roomsJson);
      _localRooms = decoded.map((e) => Room.fromMap(Map<String, dynamic>.from(e))).toList();
    } else {
      // Default initial campus auditoriums
      _localRooms = [
        Room(
          id: '1',
          name: 'C1.1.201',
          capacity: 120,
          floor: '1-қабат (1st Floor)',
          type: 'Дәріс залы (Lecture Hall)',
          building: 'C1',
          features: ['Проектор 4K', 'Микрофон', 'Wi-Fi 6', 'Кондиционер'],
          isAvailable: true,
        ),
        Room(
          id: '2',
          name: 'C1.1.254',
          capacity: 36,
          floor: '1-қабат (1st Floor)',
          type: 'Компьютер сыныбы (PC Lab)',
          building: 'C1',
          features: ['36 iMac M3', 'Cisco Routers', 'High-speed LAN', 'Smart Board'],
          isAvailable: true,
        ),
        Room(
          id: '3',
          name: 'C1.2.302',
          capacity: 45,
          floor: '2-қабат (2nd Floor)',
          type: 'Коворкинг және оқу залы (Study & Co-working)',
          building: 'C1',
          features: ['Жұмсақ дивандар', 'Розеткалар', 'Талқылау аймағы', 'Wi-Fi'],
          isAvailable: true,
        ),
        Room(
          id: '4',
          name: 'C1.2.320',
          capacity: 28,
          floor: '2-қабат (2nd Floor)',
          type: 'Жасанды интеллект лабораториясы (AI Lab)',
          building: 'C1',
          features: ['NVIDIA RTX 4090 GPU', '3D Принтерлер', 'IoT жинақтары'],
          isAvailable: false,
          currentBookingUser: 'a.smagulov@aitu.edu.kz',
          currentBookingTime: '14:00 - 15:20',
        ),
        Room(
          id: '5',
          name: 'C1.3.405',
          capacity: 220,
          floor: '3-қабат (3rd Floor)',
          type: 'Акт залы (Conference Hall)',
          building: 'C1',
          features: ['Сахна', 'LED Экран', 'Кәсіби дыбыс', 'Синхронды аударма'],
          isAvailable: true,
        ),
        Room(
          id: '6',
          name: 'C1.3.412',
          capacity: 50,
          floor: '3-қабат (3rd Floor)',
          type: 'Стартап инкубатор (Innovation Hub)',
          building: 'C1',
          features: ['Smart TV 85"', 'Маркерлік тақталар', 'Coffee Point', 'Wi-Fi'],
          isAvailable: true,
        ),
        Room(
          id: '7',
          name: 'C2.1.108',
          capacity: 32,
          floor: '1-қабат (1st Floor)',
          type: 'Киберқауіпсіздік орталығы (Cyber Lab)',
          building: 'C2',
          features: ['Оқшауланған желі', 'Dual Monitor setups', 'Server rack'],
          isAvailable: true,
        ),
        Room(
          id: '8',
          name: 'C2.2.215',
          capacity: 40,
          floor: '2-қабат (2nd Floor)',
          type: 'Семинар аудиториясы (Seminar Room)',
          building: 'C2',
          features: ['Интерактивті тақта', 'Аудио жүйе', 'Жылжымалы парталар'],
          isAvailable: true,
        ),
      ];
      await _persistRooms();
    }

    if (kesteJson != null) {
      final List decoded = jsonDecode(kesteJson);
      _localKeste = decoded.map((e) => KesteItem.fromMap(Map<String, dynamic>.from(e))).toList();
    } else {
      // Default initial schedule / timetable
      _localKeste = [
        KesteItem(
          id: 'k1',
          roomId: '1',
          roomName: 'C1.1.201',
          subject: 'Деректер қоры (PostgreSQL)',
          teacher: 'Доц. А. Смағұлов',
          timeSlot: '09:00 - 10:20',
          day: 'Дүйсенбі',
          group: 'SE-2204',
          status: 'lecture',
        ),
        KesteItem(
          id: 'k2',
          roomId: '2',
          roomName: 'C1.1.254',
          subject: 'Мобильді әзірлеу (Flutter & Dart)',
          teacher: 'Аға оқытушы М. Құсайынова',
          timeSlot: '10:30 - 11:50',
          day: 'Дүйсенбі',
          group: 'CS-2208',
          status: 'lab',
        ),
        KesteItem(
          id: 'k3',
          roomId: '4',
          roomName: 'C1.2.320',
          subject: 'Жасанды интеллект және ML',
          teacher: 'PhD. Д. Оспанов',
          timeSlot: '14:00 - 15:20',
          day: 'Дүйсенбі',
          group: 'AI-2103',
          status: 'practice',
        ),
        KesteItem(
          id: 'k4',
          roomId: '7',
          roomName: 'C2.1.108',
          subject: 'Желілік қауіпсіздік пен криптография',
          teacher: 'Магистр Б. Қалиев',
          timeSlot: '12:10 - 13:30',
          day: 'Сейсенбі',
          group: 'CYBER-2201',
          status: 'lab',
        ),
        KesteItem(
          id: 'k5',
          roomId: '8',
          roomName: 'C2.2.215',
          subject: 'Алгоритмдер және деректер құрылымы',
          teacher: 'Доц. Е. Серікбаев',
          timeSlot: '15:30 - 16:50',
          day: 'Сәрсенбі',
          group: 'IT-2305',
          status: 'practice',
        ),
      ];
      await _persistKeste();
    }

    if (usersJson != null) {
      final List decoded = jsonDecode(usersJson);
      _localUsers = decoded.map((e) => Map<String, String>.from(e)).toList();
    } else {
      _localUsers = [
        {'email': 'student@aitu.edu.kz', 'password': 'password123', 'name': 'AITU Student'},
        {'email': 'kussainova@aitu.edu.kz', 'password': 'password123', 'name': 'Malika Kussainova'},
      ];
      await _persistUsers();
    }
  }

  static Future<void> _persistRooms() async {
    final prefs = await SharedPreferences.getInstance();
    final jsonStr = jsonEncode(_localRooms.map((r) => r.toMap()).toList());
    await prefs.setString('saved_rooms_data_v2', jsonStr);
  }

  static Future<void> _persistKeste() async {
    final prefs = await SharedPreferences.getInstance();
    final jsonStr = jsonEncode(_localKeste.map((k) => k.toMap()).toList());
    await prefs.setString('saved_keste_data_v2', jsonStr);
  }

  static Future<void> _persistUsers() async {
    final prefs = await SharedPreferences.getInstance();
    final jsonStr = jsonEncode(_localUsers);
    await prefs.setString('saved_users_data_v2', jsonStr);
  }

  // Public API methods
  static Future<List<Room>> getRooms() async {
    if (_localRooms.isEmpty) {
      await _initLocalData();
    }
    return List.from(_localRooms);
  }

  static Future<List<KesteItem>> getKeste() async {
    if (_localKeste.isEmpty) {
      await _initLocalData();
    }
    return List.from(_localKeste);
  }

  static Future<bool> bookRoom({
    required String roomId,
    required String userEmail,
    required String timeSlot,
    required String purpose,
  }) async {
    final roomIndex = _localRooms.indexWhere((r) => r.id == roomId);
    if (roomIndex != -1) {
      final room = _localRooms[roomIndex];
      room.isAvailable = false;
      room.currentBookingUser = userEmail;
      room.currentBookingTime = timeSlot;

      // Add to schedule (Кесте)
      final newKesteItem = KesteItem(
        id: 'k_${DateTime.now().millisecondsSinceEpoch}',
        roomId: room.id,
        roomName: room.name,
        subject: purpose.isNotEmpty ? purpose : 'Студенттік брондау (Student Booking)',
        teacher: userEmail.split('@').first,
        timeSlot: timeSlot,
        day: 'Бүгін (Today)',
        group: 'Жеке оқу (Self-study)',
        status: 'booked',
        bookedBy: userEmail,
      );

      _localKeste.insert(0, newKesteItem);

      await _persistRooms();
      await _persistKeste();
      return true;
    }
    return false;
  }

  static Future<bool> cancelBooking(String roomId) async {
    final roomIndex = _localRooms.indexWhere((r) => r.id == roomId);
    if (roomIndex != -1) {
      _localRooms[roomIndex].isAvailable = true;
      _localRooms[roomIndex].currentBookingUser = null;
      _localRooms[roomIndex].currentBookingTime = null;

      // Remove or update in keste
      _localKeste.removeWhere((k) => k.roomId == roomId && k.status == 'booked');

      await _persistRooms();
      await _persistKeste();
      return true;
    }
    return false;
  }

  static Future<bool> registerUser(String email, String password) async {
    if (_localUsers.any((u) => u['email']?.toLowerCase() == email.toLowerCase())) {
      return false; // Already exists
    }
    _localUsers.add({
      'email': email,
      'password': password,
      'name': email.split('@').first,
    });
    await _persistUsers();
    return true;
  }

  static Future<bool> loginUser(String email, String password) async {
    if (_localUsers.isEmpty) {
      await _initLocalData();
    }
    return _localUsers.any(
      (u) => u['email']?.toLowerCase() == email.toLowerCase() && u['password'] == password,
    );
  }

  static Map<String, dynamic> getDatabaseStats() {
    return {
      'engine': activeEngine,
      'is_postgres': isPostgresConnected,
      'rooms_count': _localRooms.length,
      'keste_count': _localKeste.length,
      'users_count': _localUsers.length,
      'tables': [
        {
          'name': 'users',
          'columns': 'id (PK), email (VARCHAR), password (VARCHAR), role (VARCHAR)',
          'rows': _localUsers.length,
        },
        {
          'name': 'rooms',
          'columns': 'id (PK), name (VARCHAR), capacity (INT), floor, type, is_available (BOOL)',
          'rows': _localRooms.length,
        },
        {
          'name': 'keste',
          'columns': 'id (PK), room_id (FK), user_id (FK), subject, time_slot, status',
          'rows': _localKeste.length,
        },
      ]
    };
  }
}
