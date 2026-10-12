import 'package:flutter/material.dart';
import '../models/room.dart';
import '../models/keste_item.dart';
import '../services/database_service.dart';

class RoomsProvider extends ChangeNotifier {
  List<Room> _rooms = [];
  List<KesteItem> _keste = [];
  bool _isLoading = false;

  List<Room> get rooms => _rooms;
  List<KesteItem> get keste => _keste;
  bool get isLoading => _isLoading;
  int get bookedCount => _rooms.where((r) => !r.isAvailable).length;
  int get totalRoomsCount => _rooms.length;
  int get availableRoomsCount => _rooms.where((r) => r.isAvailable).length;

  RoomsProvider() {
    refreshAll();
  }

  Future<void> refreshAll() async {
    _isLoading = true;
    notifyListeners();

    try {
      _rooms = await DatabaseService.getRooms();
      _keste = await DatabaseService.getKeste();
    } catch (e) {
      debugPrint('Error loading rooms and keste: $e');
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  List<KesteItem> getUserBookings(String? userEmail) {
    if (userEmail == null || userEmail.isEmpty) return [];
    return _keste.where((k) => k.bookedBy?.toLowerCase() == userEmail.toLowerCase()).toList();
  }

  List<KesteItem> getRoomSchedule(String roomId) {
    return _keste.where((k) => k.roomId == roomId).toList();
  }

  Future<bool> bookRoom({
    required String roomId,
    required String userEmail,
    required String timeSlot,
    String purpose = 'Өздік жұмыс / Self-study',
  }) async {
    final success = await DatabaseService.bookRoom(
      roomId: roomId,
      userEmail: userEmail,
      timeSlot: timeSlot,
      purpose: purpose,
    );

    if (success) {
      await refreshAll();
      return true;
    }
    return false;
  }

  Future<bool> cancelBooking(String roomId) async {
    final success = await DatabaseService.cancelBooking(roomId);
    if (success) {
      await refreshAll();
      return true;
    }
    return false;
  }

  Map<String, dynamic> getDbStats() {
    return DatabaseService.getDatabaseStats();
  }
}
