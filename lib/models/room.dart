class Room {
  final String id;
  final String name;
  final int capacity;
  final String floor;
  final String type;
  final String building;
  final List<String> features;
  bool isAvailable;
  String? currentBookingUser;
  String? currentBookingTime;

  Room({
    required this.id,
    required this.name,
    required this.capacity,
    required this.floor,
    required this.type,
    this.building = 'C1',
    this.features = const ['Wi-Fi', 'Projector', 'Power Sockets'],
    this.isAvailable = true,
    this.currentBookingUser,
    this.currentBookingTime,
  });

  Map<String, dynamic> toMap() {
    return {
      'id': id,
      'name': name,
      'capacity': capacity,
      'floor': floor,
      'type': type,
      'building': building,
      'features': features.join(','),
      'is_available': isAvailable,
      'current_booking_user': currentBookingUser,
      'current_booking_time': currentBookingTime,
    };
  }

  factory Room.fromMap(Map<String, dynamic> map) {
    List<String> featList = ['Wi-Fi', 'Projector'];
    if (map['features'] != null) {
      if (map['features'] is List) {
        featList = List<String>.from(map['features']);
      } else if (map['features'] is String) {
        featList = (map['features'] as String).split(',').map((e) => e.trim()).toList();
      }
    }

    return Room(
      id: map['id']?.toString() ?? '',
      name: map['name'] as String? ?? 'Auditorium',
      capacity: (map['capacity'] as num?)?.toInt() ?? 30,
      floor: map['floor'] as String? ?? 'Floor 1',
      type: map['type'] as String? ?? 'General',
      building: map['building'] as String? ?? 'C1',
      features: featList,
      isAvailable: (map['is_available'] is bool)
          ? map['is_available'] as bool
          : (map['is_available'] == 1 || map['is_available'] == 'true'),
      currentBookingUser: map['current_booking_user'] as String?,
      currentBookingTime: map['current_booking_time'] as String?,
    );
  }
}
