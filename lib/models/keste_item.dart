class KesteItem {
  final String id;
  final String roomId;
  final String roomName;
  final String subject;
  final String teacher;
  final String timeSlot;
  final String day;
  final String group;
  final String status; // 'lecture', 'practice', 'lab', 'booked', 'free'
  final String? bookedBy;

  KesteItem({
    required this.id,
    required this.roomId,
    required this.roomName,
    required this.subject,
    required this.teacher,
    required this.timeSlot,
    required this.day,
    required this.group,
    required this.status,
    this.bookedBy,
  });

  Map<String, dynamic> toMap() {
    return {
      'id': id,
      'room_id': roomId,
      'room_name': roomName,
      'subject': subject,
      'teacher': teacher,
      'time_slot': timeSlot,
      'day': day,
      'group': group,
      'status': status,
      'booked_by': bookedBy,
    };
  }

  factory KesteItem.fromMap(Map<String, dynamic> map) {
    return KesteItem(
      id: map['id']?.toString() ?? '',
      roomId: map['room_id']?.toString() ?? '',
      roomName: map['room_name'] ?? '',
      subject: map['subject'] ?? '',
      teacher: map['teacher'] ?? '',
      timeSlot: map['time_slot'] ?? '',
      day: map['day'] ?? '',
      group: map['group'] ?? '',
      status: map['status'] ?? 'lecture',
      bookedBy: map['booked_by'],
    );
  }
}
